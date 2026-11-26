"""Fail-closed data classification and external-egress authorization primitives.

These checks are policy decisions, not a network firewall. Deployments must call
them at every adapter boundary and enforce the returned decision at the network
boundary; an unintegrated policy object does not prevent data exfiltration.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from urllib.parse import urlsplit
import ipaddress
import re

from .platform.contracts import PlatformError, ValidationError


class EgressDenied(PlatformError):
    """An outbound transfer is not covered by an explicit policy grant."""

    code = "EGRESS_DENIED"


class DataClassification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

    @classmethod
    def from_metadata(cls, value: object) -> "DataClassification":
        """Unknown, absent or malformed labels fail closed to RESTRICTED."""
        if not isinstance(value, str):
            return cls.RESTRICTED
        try:
            return cls(value.strip().lower())
        except ValueError:
            return cls.RESTRICTED


@dataclass(frozen=True, slots=True)
class EgressGrant:
    """One narrowly scoped grant; host, purpose, class and byte ceiling all match."""

    recipient: str
    purpose: str
    classification: DataClassification
    max_bytes: int

    def __post_init__(self) -> None:
        if not self.recipient or self.recipient != self.recipient.lower():
            raise ValueError("recipient must be a lowercase DNS hostname")
        if not re.fullmatch(r"(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)(?:\.(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?))*", self.recipient):
            raise ValueError("recipient must be a valid lowercase DNS hostname")
        if not self.purpose or len(self.purpose) > 256:
            raise ValueError("purpose must be non-empty bounded text")
        if not isinstance(self.classification, DataClassification):
            raise ValueError("classification must be a DataClassification value")
        if isinstance(self.max_bytes, bool) or not isinstance(self.max_bytes, int) or self.max_bytes <= 0:
            raise ValueError("max_bytes must be positive")


@dataclass(frozen=True, slots=True)
class EgressDecision:
    allowed: bool
    recipient: str
    purpose: str
    classification: DataClassification
    payload_bytes: int
    grant_index: int | None


class EgressPolicy:
    """Deny-by-default policy; a grant must exactly match all declared dimensions."""

    def __init__(self, grants: tuple[EgressGrant, ...] = ()) -> None:
        if not isinstance(grants, tuple) or any(not isinstance(g, EgressGrant) for g in grants):
            raise TypeError("grants must be a tuple of EgressGrant records")
        self._grants = grants

    @staticmethod
    def _recipient(url: str) -> str:
        if not isinstance(url, str) or len(url) > 2048:
            raise ValidationError("egress URL must be bounded text")
        try:
            parsed = urlsplit(url)
            hostname = parsed.hostname
            port = parsed.port
        except ValueError as exc:
            raise EgressDenied("egress URL is malformed") from exc
        if parsed.scheme != "https" or not hostname or parsed.username or parsed.password:
            raise EgressDenied("egress requires an HTTPS URL without embedded credentials")
        host = hostname.lower().rstrip(".")
        try:
            address = ipaddress.ip_address(host)
        except ValueError:
            address = None
        if address is not None:
            if not address.is_global:
                raise EgressDenied("private, loopback and reserved IP destinations are forbidden")
            raise EgressDenied("egress grants must name an explicit DNS host, not an IP address")
        if port not in (None, 443):
            raise EgressDenied("non-standard HTTPS ports are not permitted")
        return host

    def authorize(
        self,
        *,
        url: str,
        purpose: str,
        classification: object,
        payload_bytes: int,
    ) -> EgressDecision:
        if not isinstance(purpose, str) or not purpose or len(purpose) > 256:
            raise ValidationError("egress purpose must be non-empty bounded text")
        if isinstance(payload_bytes, bool) or not isinstance(payload_bytes, int) or payload_bytes < 0:
            raise ValidationError("payload_bytes must be a non-negative integer")
        recipient = self._recipient(url)
        label = DataClassification.from_metadata(classification)
        for index, grant in enumerate(self._grants):
            if (
                grant.recipient == recipient
                and grant.purpose == purpose
                and grant.classification is label
                and payload_bytes <= grant.max_bytes
            ):
                return EgressDecision(True, recipient, purpose, label, payload_bytes, index)
        raise EgressDenied(
            "outbound transfer is not covered by an explicit classification/recipient/purpose/size grant",
            details={
                "recipient": recipient,
                "purpose": purpose,
                "classification": label.value,
                "payload_bytes": payload_bytes,
            },
        )
