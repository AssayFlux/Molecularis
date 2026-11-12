from molecularis_api.trainer import _record_to_text

def test_text_record():
    assert _record_to_text({"text": "hello"}) == "hello"

def test_prompt_completion_record():
    assert _record_to_text({"prompt": "question", "completion": "answer"}) == "User: question\nAssistant: answer"

def test_chat_messages_record():
    assert _record_to_text({"messages": [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}]}) == "user: hi\nassistant: hello"
