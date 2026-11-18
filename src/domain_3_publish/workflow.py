from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set


class ItemStatus(str, Enum):
    STAGED = "staged"
    BANKED = "banked"
    REVIEW_PENDING = "review_pending"
    HELD = "held"
    COMPILE_ELIGIBLE = "compile_eligible"
    COMPILED = "compiled"
    RELEASE_ELIGIBLE = "release_eligible"


@dataclass
class ContentItem:
    item_id: str
    payload: Dict
    provenance: str
    status: ItemStatus = ItemStatus.STAGED
    decision_reasons: List[str] = field(default_factory=list)


class StagingArea:
    """Transient intake for harvested or submitted content; no publishing side effects."""

    def __init__(self) -> None:
        self._items: Dict[str, ContentItem] = {}

    def stage(self, item: ContentItem) -> None:
        if not item.item_id.strip():
            raise ValueError("item_id must not be empty")
        if item.item_id in self._items:
            raise ValueError(f"item already staged: {item.item_id}")
        item.status = ItemStatus.STAGED
        self._items[item.item_id] = item

    def get(self, item_id: str) -> ContentItem:
        return self._items[item_id]

    def items(self) -> List[ContentItem]:
        return list(self._items.values())


class ContentBank:
    """Separate store for deliberately preloaded/curated reusable content."""

    def __init__(self) -> None:
        self._items: Dict[str, ContentItem] = {}

    def preload(self, item: ContentItem) -> None:
        if not item.item_id.strip():
            raise ValueError("item_id must not be empty")
        if item.item_id in self._items:
            raise ValueError(f"item already in content bank: {item.item_id}")
        item.status = ItemStatus.BANKED
        self._items[item.item_id] = item

    def get(self, item_id: str) -> ContentItem:
        return self._items[item_id]

    def items(self) -> List[ContentItem]:
        return list(self._items.values())


@dataclass(frozen=True)
class Review:
    approval_id: Optional[str]
    status: str
    prohibited_conventions_check: Dict[str, Optional[bool]]
    fsr_status: str = "not_evaluated"


@dataclass(frozen=True)
class TowerDecision:
    compile_allowed: bool
    publish_allowed: bool
    status: str
    reasons: List[str]


class ControlTower:
    """Governance boundary. Compilation can be allowed while publishing remains blocked."""

    REQUIRED_FLAGS = ("sensationalism_detected", "lighthearted_humor_detected")

    def review(self, review: Review) -> TowerDecision:
        reasons: List[str] = []
        if review.status != "approved":
            reasons.append("gatekeeper_review_not_approved")
        for flag in self.REQUIRED_FLAGS:
            value = review.prohibited_conventions_check.get(flag)
            if value is not False:
                reasons.append(f"prohibited_convention_check_not_clear:{flag}")

        compile_allowed = not reasons
        if review.fsr_status != "cleared":
            reasons.append("fsr_not_evaluated_or_not_cleared")
        publish_allowed = compile_allowed and review.fsr_status == "cleared"
        status = "release_eligible" if publish_allowed else (
            "compile_eligible" if compile_allowed else "held"
        )
        return TowerDecision(compile_allowed, publish_allowed, status, reasons)

    def apply(self, item: ContentItem, review: Review) -> TowerDecision:
        decision = self.review(review)
        item.decision_reasons = list(decision.reasons)
        item.status = ItemStatus(decision.status)
        return decision


def transfer_to_staging(bank: ContentBank, staging: StagingArea, item_id: str) -> ContentItem:
    """Explicitly copy a banked item into staging; bank contents are never auto-published."""
    source = bank.get(item_id)
    staged = ContentItem(
        item_id=source.item_id,
        payload=dict(source.payload),
        provenance=f"content_bank:{source.item_id}; {source.provenance}",
    )
    staging.stage(staged)
    return staged
