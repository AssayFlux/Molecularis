"""Molecularis Terminal: inspect and exercise the live A–N capability runtime.

This is an engineering workbench. A successful software run is not scientific
validation, and optional engines may still require local tools or datasets.
"""
from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path
from typing import Any, Sequence

from .bootstrap import create_full_platform
from .platform import Budget, ExecutionContext, Operation, Rulebook
from .platform.contracts import PlatformError
from .testlab import run_testlab


BANNER = r"""
 __  __       _ ____       _       _ _     
|  \/  | ___ | |  _ \ ___ | | __ _| (_)___ 
| |\/| |/ _ \| | |_) / _ \| |/ _` | | / __|
| |  | | (_) | |  _ < (_) | | (_| | | \__ \
|_|  |_|\___/|_|_| \_\___/|_|\__,_|_|_|___/
                 MOLECULARIS TERMINAL
"""


def _json_value(value: str, *, label: str) -> Any:
    source = value[1:] if value.startswith("@") else value
    try:
        if value.startswith("@"):
            source = Path(source).read_text(encoding="utf-8")
        return json.loads(source)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} must be valid JSON or @path-to-json: {exc}") from exc


def _capability_dict(capability: Any, platform: Any) -> dict[str, Any]:
    return {
        "id": capability.id,
        "service": capability.service,
        "operation": capability.operation,
        "version": capability.version,
        "description": capability.description,
        "input_schema": capability.input_schema,
        "output_schema": capability.output_schema,
        "deterministic": capability.deterministic,
        "handler_bound": platform.has_handler(capability.id),
    }


def _print_capabilities(platform: Any, service: str | None = None) -> None:
    capabilities = platform.registry.list(service=service)
    if not capabilities:
        print("No capabilities match.")
        return
    print(f"{'CAPABILITY':42} {'SERVICE':18} {'OPERATION':22} {'HANDLER':8}")
    print("-" * 94)
    for cap in capabilities:
        bound = "READY" if platform.has_handler(cap.id) else "MISSING"
        print(f"{cap.id[:41]:42} {cap.service[:17]:18} {cap.operation[:21]:22} {bound:8}")
    print(f"\n{len(capabilities)} capability registration(s) shown.")


def _show_capability(platform: Any, capability_id: str) -> None:
    cap = platform.registry.get(capability_id)
    print(json.dumps(_capability_dict(cap, platform), indent=2, sort_keys=True))


def _doctor(platform: Any) -> int:
    capabilities = platform.registry.list()
    ready = sum(platform.has_handler(cap.id) for cap in capabilities)
    services = sorted({cap.service for cap in capabilities})
    print("MOLECULARIS RUNTIME DIAGNOSTICS")
    print("=" * 34)
    print(f"Services registered : {len(services)} / 14 expected")
    print(f"Capabilities        : {len(capabilities)}")
    print(f"Handlers bound      : {ready}")
    print(f"Handlers missing    : {len(capabilities) - ready}")
    print(f"Workspace           : {platform.root}")
    print("Optional engines    : availability is capability-specific; run the operation to verify")
    print("Scientific status   : not assessed by this diagnostic")
    if len(services) != 14 or ready != len(capabilities):
        return 1
    print("\nRuntime registration check: PASS")
    return 0


def _run_capability(platform: Any, capability_id: str, inputs: dict[str, Any],
                    parameters: dict[str, Any], max_seconds: float) -> int:
    cap = platform.registry.get(capability_id)
    if not platform.has_handler(capability_id):
        print(f"ERROR: no handler is bound for {capability_id}", file=sys.stderr)
        return 2
    if not isinstance(inputs, dict) or not inputs:
        print("ERROR: --input must be a non-empty JSON object keyed by Rulebook input name.", file=sys.stderr)
        return 2
    if not isinstance(parameters, dict):
        print("ERROR: --params must be a JSON object.", file=sys.stderr)
        return 2
    operation = Operation(
        id="terminal-" + cap.operation,
        capability_id=capability_id,
        inputs=tuple(inputs.keys()),
        output="terminal_result",
        parameters=parameters,
    )
    rulebook = Rulebook(
        id="molecularis-terminal-single-capability",
        version="1.0.0",
        operations=(operation,),
        max_steps=1,
    )
    context = ExecutionContext(
        service_id="molecularis-terminal",
        rulebook_version=rulebook.version,
        parameters={"source": "molecularis-terminal"},
        budget=Budget(max_wall_seconds=max_seconds),
    )
    try:
        result = platform.execute(rulebook, inputs, context=context)
    except Exception as exc:
        code = getattr(exc, "code", type(exc).__name__)
        print(f"\nEXECUTION FAILED [{code}] {exc}", file=sys.stderr)
        details = getattr(exc, "details", None)
        if details:
            print(json.dumps(details, indent=2, default=str), file=sys.stderr)
        return 1
    print("\nEXECUTION SUCCEEDED")
    print(f"Capability : {cap.id}")
    print(f"Run ID     : {context.run_id}")
    print("\nRESULT")
    print(json.dumps(result.get("terminal_result"), indent=2, ensure_ascii=False, default=str))
    print("\nNote: this records software execution, not independent scientific validation.")
    return 0


def _shell(platform: Any, max_seconds: float) -> int:
    print(BANNER)
    print("Type 'help' for commands. This session uses the live local A–N runtime.")
    while True:
        try:
            line = input("molecularis> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession closed.")
            return 0
        if not line:
            continue
        try:
            parts = shlex.split(line)
        except ValueError as exc:
            print(f"Parse error: {exc}")
            continue
        command, *args = parts
        if command in {"exit", "quit"}:
            return 0
        if command in {"help", "?"}:
            print("help | doctor | services | list [service] | show <capability-id> | testlab [service]")
            print("run <capability-id> --input '{\"key\": \"value\"}' [--params '{}']")
            print("JSON inputs may use @file.json. Type exit to leave.")
        elif command == "testlab":
            report = run_testlab(platform, service=args[0] if args else None)
            print(json.dumps(report, indent=2, ensure_ascii=False))
        elif command == "doctor":
            _doctor(platform)
        elif command == "services":
            for name in sorted({cap.service for cap in platform.registry.list()}):
                count = len(platform.registry.list(service=name))
                print(f"{name:24} {count:3} capabilities")
        elif command == "list":
            _print_capabilities(platform, args[0] if args else None)
        elif command == "show" and len(args) == 1:
            try:
                _show_capability(platform, args[0])
            except PlatformError as exc:
                print(f"ERROR: {exc}")
        elif command == "run" and len(args) >= 1:
            parser = argparse.ArgumentParser(prog="run", add_help=False)
            parser.add_argument("--input", required=True)
            parser.add_argument("--params", default="{}")
            try:
                parsed = parser.parse_args(args[1:])
                input_data = _json_value(parsed.input, label="--input")
                params = _json_value(parsed.params, label="--params")
                _run_capability(platform, args[0], input_data, params, max_seconds)
            except (SystemExit, ValueError) as exc:
                if isinstance(exc, ValueError):
                    print(f"ERROR: {exc}")
        else:
            print("Unknown command or arguments. Type 'help'.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="molecularis",
        description="Terminal workbench for the live Molecularis A–N capability runtime.",
    )
    parser.add_argument("--workspace", default=".molecularis-workspace",
                        help="artifact workspace directory (default: .molecularis-workspace)")
    parser.add_argument("--max-seconds", type=float, default=30.0,
                        help="per-operation wall-time budget (default: 30)")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("doctor", help="check service and handler registration")
    sub.add_parser("services", help="list registered scientific services")\n    testlab_parser = sub.add_parser("testlab", help="run deterministic fixture-backed capability smoke tests")\n    testlab_parser.add_argument("--service", help="limit tests to one service")
    list_parser = sub.add_parser("list", help="list registered capabilities")
    list_parser.add_argument("--service", help="filter by service name")
    show_parser = sub.add_parser("show", help="inspect one capability contract")
    show_parser.add_argument("capability_id")
    run_parser = sub.add_parser("run", help="execute one registered capability")
    run_parser.add_argument("capability_id")
    run_parser.add_argument("--input", required=True, help="JSON object or @input.json")
    run_parser.add_argument("--params", default="{}", help="JSON object of operation parameters")
    sub.add_parser("shell", help="open interactive terminal session")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.max_seconds <= 0:
        parser.error("--max-seconds must be positive")
    try:
        input_data = _json_value(args.input, label="--input") if args.command == "run" else None
        parameters = _json_value(args.params, label="--params") if args.command == "run" else {}
        if args.command == "run" and (not isinstance(input_data, dict) or not isinstance(parameters, dict)):
            parser.error("--input and --params must decode to JSON objects")
        with_workspace = Path(args.workspace).expanduser()
        platform = create_full_platform(str(with_workspace))
        try:
            if args.command in {None, "shell"}:
                return _shell(platform, args.max_seconds)
            if args.command == "doctor":
                return _doctor(platform)
            if args.command == "services":
                for name in sorted({cap.service for cap in platform.registry.list()}):
                    print(f"{name}: {len(platform.registry.list(service=name))} capabilities")
                return 0
            if args.command == "list":
                _print_capabilities(platform, args.service)
                return 0
            if args.command == "show":
                _show_capability(platform, args.capability_id)
                return 0
            if args.command == "run":
                return _run_capability(platform, args.capability_id, input_data, parameters,
                                       args.max_seconds)
            parser.print_help()
            return 0
        finally:
            platform.close()
    except (PlatformError, RuntimeError, ValueError, OSError) as exc:
        print(f"MOLECULARIS STARTUP ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
