from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


def _record_to_text(row: dict[str, Any]) -> str:
    if isinstance(row.get("text"), str):
        return row["text"]
    if isinstance(row.get("messages"), list):
        parts = []
        for message in row["messages"]:
            if isinstance(message, dict):
                role = str(message.get("role", "user"))
                content = str(message.get("content", ""))
                parts.append(f"{role}: {content}")
        return "\n".join(parts)
    if "prompt" in row:
        return f"User: {row.get('prompt', '')}\nAssistant: {row.get('completion', '')}"
    raise ValueError("Each JSONL record must contain text, messages, or prompt")


def train_lora(
    dataset_path: str,
    base_model: str,
    config: dict[str, Any],
    output_dir: str,
    progress_callback: Callable[[float, str], None] | None = None,
) -> dict[str, Any]:
    # Heavy ML dependencies are imported only inside the GPU worker process.
    import torch
    from datasets import Dataset
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        DataCollatorForLanguageModeling,
        Trainer,
        TrainerCallback,
        TrainingArguments,
    )

    method = config["method"]
    if method == "qlora" and not torch.cuda.is_available():
        raise RuntimeError("QLoRA requires a CUDA-capable GPU worker")
    if not torch.cuda.is_available():
        raise RuntimeError("This training worker requires a CUDA GPU; CPU training is intentionally disabled")

    model_path = Path(base_model).resolve(strict=True)
    if not model_path.is_dir():
        raise ValueError("Base model must be a local model directory")
    records = []
    with Path(dataset_path).open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append({"text": _record_to_text(json.loads(line))})
    if not records:
        raise ValueError("Dataset contains no training records")

    tokenizer = AutoTokenizer.from_pretrained(str(model_path), use_fast=True, local_files_only=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    load_kwargs: dict[str, Any] = {"device_map": "auto", "torch_dtype": torch.float16, "local_files_only": True}
    if method == "qlora":
        load_kwargs["quantization_config"] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )
    model = AutoModelForCausalLM.from_pretrained(str(model_path), **load_kwargs)
    if method == "qlora":
        model = prepare_model_for_kbit_training(model)
    model.config.use_cache = False
    adapter = LoraConfig(
        r=int(config["rank"]),
        lora_alpha=int(config["rank"]) * 2,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "v_proj"],
    )
    model = get_peft_model(model, adapter)

    dataset = Dataset.from_list(records)
    def tokenize(batch: dict[str, list[str]]) -> dict[str, Any]:
        return tokenizer(batch["text"], truncation=True, max_length=2048)
    tokenized = dataset.map(tokenize, batched=True, remove_columns=["text"])
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    class ApiProgressCallback(TrainerCallback):
        def on_step_end(self, args, state, control, **kwargs):
            if progress_callback:
                total = max(int(state.max_steps), 1)
                progress = min(95.0, state.global_step / total * 95.0)
                progress_callback(progress, f"Training step {state.global_step}/{total}")
            return control

        def on_log(self, args, state, control, logs=None, **kwargs):
            if progress_callback and logs and "loss" in logs:
                total = max(int(state.max_steps), 1)
                progress = min(95.0, state.global_step / total * 95.0)
                progress_callback(progress, f"Step {state.global_step}/{total} · loss {float(logs['loss']):.4f}")
            return control

    args = TrainingArguments(
        output_dir=str(output / "checkpoints"),
        num_train_epochs=int(config["epochs"]),
        learning_rate=float(config["learning_rate"]),
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        logging_steps=1,
        save_strategy="epoch",
        save_total_limit=2,
        report_to="none",
        fp16=True,
        gradient_checkpointing=True,
        optim="adamw_torch",
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
        callbacks=[ApiProgressCallback()],
    )
    trainer.train()
    model.save_pretrained(output / "adapter")
    tokenizer.save_pretrained(output / "adapter")
    digest = hashlib.sha256(Path(dataset_path).read_bytes()).hexdigest()
    manifest = {
        "base_model": str(model_path),
        "method": method,
        "rank": int(config["rank"]),
        "output_name": config.get("output_name", "astronaut-adapter"),
        "dataset_sha256": digest,
        "record_count": len(records),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "format": "peft-adapter",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    if progress_callback:
        progress_callback(100.0, "Adapter and manifest saved")
    return {"artifact_dir": str(output / "adapter"), "manifest": str(output / "manifest.json"), "record_count": len(records)}
