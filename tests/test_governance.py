from __future__ import annotations

import pytest

from molecularis.governance import (
    DataClassification, EgressDenied, EgressGrant, EgressPolicy,
)


def test_unknown_or_malformed_classification_defaults_to_restricted():
    assert DataClassification.from_metadata(None) is DataClassification.RESTRICTED
    assert DataClassification.from_metadata("typo") is DataClassification.RESTRICTED
    assert DataClassification.from_metadata("PUBLIC") is DataClassification.PUBLIC


def test_egress_is_denied_by_default():
    with pytest.raises(EgressDenied):
        EgressPolicy().authorize(
            url="https://models.example/api", purpose="inference",
            classification="public", payload_bytes=12,
        )


def test_egress_requires_exact_recipient_purpose_class_and_byte_ceiling():
    policy = EgressPolicy((EgressGrant(
        recipient="models.example", purpose="inference",
        classification=DataClassification.PUBLIC, max_bytes=1024,
    ),))
    decision = policy.authorize(
        url="https://models.example/v1/generate", purpose="inference",
        classification="public", payload_bytes=1024,
    )
    assert decision.allowed is True
    assert decision.grant_index == 0
    for kwargs in (
        {"url": "https://other.example/api", "purpose": "inference",
         "classification": "public", "payload_bytes": 12},
        {"url": "https://models.example/api", "purpose": "training",
         "classification": "public", "payload_bytes": 12},
        {"url": "https://models.example/api", "purpose": "inference",
         "classification": "confidential", "payload_bytes": 12},
        {"url": "https://models.example/api", "purpose": "inference",
         "classification": "public", "payload_bytes": 1025},
    ):
        with pytest.raises(EgressDenied):
            policy.authorize(**kwargs)


@pytest.mark.parametrize("url", [
    "http://models.example/api",
    "https://user:secret@models.example/api",
    "https://127.0.0.1/api",
    "https://10.0.0.2/api",
    "https://[::1]/api",
    "https://models.example:8443/api",
])
def test_egress_rejects_unsafe_destinations(url):
    policy = EgressPolicy((EgressGrant(
        "models.example", "inference", DataClassification.PUBLIC, 100,
    ),))
    with pytest.raises(EgressDenied):
        policy.authorize(
            url=url, purpose="inference", classification="public", payload_bytes=1,
        )


def test_egress_grant_validation():
    with pytest.raises(ValueError):
        EgressGrant("Models.Example", "inference", DataClassification.PUBLIC, 100)
    with pytest.raises(ValueError):
        EgressGrant("models.example", "inference", DataClassification.PUBLIC, 0)
