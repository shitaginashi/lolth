"""Mark 1 draft payload compiler. It compiles; it does not govern or publish."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import yaml

from workflow import ControlTower, Review


class SupersetProfile(str, Enum):
    BOILERPLATE = "boilerplate"
    SOCIAL_POST = "social_post"
    MICRO_POST = "micro_post"


class AttachmentTier(str, Enum):
    ATOMIC_TEXT = "atomic_text"
    ILLUSTRATED = "illustrated"
    FANCY = "fancy"


@dataclass
class PublishCandidate:
    candidate_id: str
    title: str
    body_text: str
    domain_category: str
    attachment_tier: AttachmentTier = AttachmentTier.ATOMIC_TEXT
    media_url: Optional[str] = None
    alt_text: Optional[str] = None
    partner_tags: List[str] = field(default_factory=list)
    primary_hashtags: List[str] = field(default_factory=list)
    secondary_hashtags: List[str] = field(default_factory=list)
    boilerplate_hashtags: List[str] = field(default_factory=list)
    tool_ids: List[str] = field(default_factory=list)


@dataclass
class PlatformConfig:
    platform_name: str
    profile: SupersetProfile
    max_chars: int
    include_domain_link: bool = True
    domain_url: str = "ledante.com"


# Illustrative display metadata only. Mianzi policy/registry is not implemented.
STATIC_MIANZI_REGISTRY = {
    "comfyui": {"name": "ComfyUI Node Engine", "weight": 95, "logo_slot": "P0_DS0P_Core"},
    "fairlight": {"name": "Fairlight NLE", "weight": 90, "logo_slot": "P0_Fairlight_Audio"},
    "nvidia_cuda": {"name": "NVIDIA CUDA Acceleration", "weight": 85, "logo_slot": "P1_NVIDIA_Omniverse"},
    "linux_runtime": {"name": "Enterprise Linux", "weight": 80, "logo_slot": "P1_Linux_Kernel"},
    "mcp_harness": {"name": "Model Context Protocol (MCP)", "weight": 60, "logo_slot": "P2_MCP_Daemon"},
    "dsop_branding_notebook": {"name": "DS0P Branding Master Notebook", "weight": 40, "logo_slot": "P3_Local_Notebook"},
}


def load_contract(path: Path) -> tuple[dict, dict]:
    """Load and minimally validate the canonical YAML fixture/contract."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"could not load gatekeeper contract: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError("contract root must be a mapping")
    review = raw.get("gatekeeper_review")
    candidate = raw.get("candidate_payload")
    if not isinstance(review, dict) or not isinstance(candidate, dict):
        raise ValueError("contract requires gatekeeper_review and candidate_payload mappings")
    required_candidate = ("candidate_id", "title", "body_text", "domain_category", "attachment_tier")
    missing = [key for key in required_candidate if key not in candidate]
    if missing:
        raise ValueError(f"candidate_payload missing required keys: {', '.join(missing)}")
    if not isinstance(review.get("prohibited_conventions_check"), dict):
        raise ValueError("gatekeeper_review.prohibited_conventions_check must be a mapping")
    fsr = review.get("fsr")
    if not isinstance(fsr, dict) or fsr.get("status") not in {"not_evaluated", "cleared", "rejected"}:
        raise ValueError("gatekeeper_review.fsr.status must be not_evaluated, cleared, or rejected")
    return review, candidate


class PublishCompiler:
    """Pure draft compiler. Only the Control Tower owns review/release decisions."""

    def __init__(self, platform_config: PlatformConfig):
        if platform_config.max_chars < 0:
            raise ValueError("max_chars must be non-negative")
        self.config = platform_config

    @staticmethod
    def resolve_mianzi_stub(tool_ids: Sequence[str]) -> Dict:
        selected = set(tool_ids)
        tools = [
            {"id": tool_id, **STATIC_MIANZI_REGISTRY[tool_id]}
            for tool_id in selected
            if tool_id in STATIC_MIANZI_REGISTRY
        ]
        tools.sort(key=lambda tool: tool["weight"], reverse=True)
        return {
            "status": "stub",
            "selected_tools": tools,
            "unresolved_tool_ids": sorted(selected - STATIC_MIANZI_REGISTRY.keys()),
            "outro_logo_slots": [tool["logo_slot"] for tool in tools if tool.get("logo_slot")],
        }

    def compile(self, candidate: PublishCandidate, review: Review) -> Dict:
        # Compile is allowed only after the Tower's non-FSR review gate. It never authorizes publish.
        decision = ControlTower().review(review)
        if not decision.compile_allowed:
            raise ValueError("Control Tower holds candidate: " + ", ".join(decision.reasons))

        body = candidate.body_text.strip()
        body_with_domain = body
        if self.config.include_domain_link and self.config.profile != SupersetProfile.MICRO_POST:
            body_with_domain = f"{body}\n\n{self.config.domain_url}"

        footer = ""
        if candidate.partner_tags:
            footer = "In collaboration with: " + " ".join(
                f"#{tag.lstrip('#')}" for tag in candidate.partner_tags
            )
        tags = [
            f"#{tag.lstrip('#')}"
            for group in (
                candidate.primary_hashtags,
                candidate.secondary_hashtags,
                candidate.boilerplate_hashtags,
            )
            for tag in group
        ]

        def assemble(selected_tags: Sequence[str], include_footer: bool) -> str:
            parts = [body_with_domain]
            if footer and include_footer:
                parts.append(footer)
            if selected_tags:
                parts.append(" ".join(selected_tags))
            return "\n\n".join(parts)

        include_footer = bool(footer)
        retained: List[str] = []
        audit: List[dict] = []
        quota_status = "optimal"
        if len(assemble([], include_footer)) > self.config.max_chars:
            include_footer = False
            quota_status = "body_only"
            audit.append({"code": "FOOTER_OMITTED", "reason": "body_and_footer_exceed_cap"})
        if len(assemble([], include_footer)) > self.config.max_chars:
            quota_status = "body_exceeds_cap"
            audit.append({"code": "BODY_EXCEEDS_CAP", "reason": "body_retained_without_truncation"})
        else:
            for tag in tags:
                proposed = retained + [tag]
                if len(assemble(proposed, include_footer)) <= self.config.max_chars:
                    retained = proposed
                else:
                    quota_status = "pruned"
                    audit.append({"code": "HEADROOM_CONSTRAINED", "pruned_from": tag})
                    break

        text = assemble(retained, include_footer)
        mianzi = self.resolve_mianzi_stub(candidate.tool_ids)
        media_payload = None
        if candidate.attachment_tier != AttachmentTier.ATOMIC_TEXT and candidate.media_url:
            media_payload = {
                "type": "image" if candidate.attachment_tier == AttachmentTier.ILLUSTRATED else "video",
                "url": candidate.media_url,
                "alt_text": candidate.alt_text,
                "validation_status": "not_evaluated",
            }
        attachment_status = {
            "tier": candidate.attachment_tier.value,
            "requested": candidate.attachment_tier != AttachmentTier.ATOMIC_TEXT,
            "provided": bool(candidate.media_url) if candidate.attachment_tier != AttachmentTier.ATOMIC_TEXT else False,
            "validation_status": "not_implemented" if candidate.attachment_tier != AttachmentTier.ATOMIC_TEXT else "not_applicable",
        }
        manifest = {
            "run_metadata": {
                "candidate_id": candidate.candidate_id,
                "target_platform": self.config.platform_name,
                "profile_applied": self.config.profile.value,
                "attachment_tier": candidate.attachment_tier.value,
                "artifact_status": "draft_compiled",
            },
            "governance": {
                "compile_allowed": decision.compile_allowed,
                "publish_allowed": decision.publish_allowed,
                "status": decision.status,
                "reasons": decision.reasons,
                "fsr_status": review.fsr_status,
            },
            "budget_interface": {
                "platform_max_chars": self.config.max_chars,
                "content_body_chars": len(body_with_domain),
                "headroom_remaining": self.config.max_chars - len(body_with_domain),
                "total_payload_chars": len(text),
                "within_configured_limit": len(text) <= self.config.max_chars,
            },
            "execution_status": {
                "quota_status": quota_status,
                "tags_retained": len(retained),
                "tags_pruned": len(tags) - len(retained),
            },
            "attachment_status": attachment_status,
            "mianzi_attribution_stub": {
                "status": mianzi["status"],
                "selected_tool_ids": [tool["id"] for tool in mianzi["selected_tools"]],
                "unresolved_tool_ids": mianzi["unresolved_tool_ids"],
                "outro_logo_slots": mianzi["outro_logo_slots"],
            },
            "errata_audit_log": audit,
        }
        return {
            "atomic_text_base": text,
            "media_payload": media_payload,
            "sidecar_manifest": manifest,
        }


def main() -> None:
    contract_path = Path(__file__).with_name("agent_gatekeeper.yml")
    raw_review, raw_candidate = load_contract(contract_path)
    review = Review(
        approval_id=raw_review.get("approval_id"),
        status=str(raw_review.get("status", "pending")),
        prohibited_conventions_check=raw_review["prohibited_conventions_check"],
        fsr_status=raw_review["fsr"]["status"],
    )
    candidate = PublishCandidate(
        candidate_id=raw_candidate["candidate_id"],
        title=raw_candidate["title"],
        body_text=raw_candidate["body_text"],
        domain_category=raw_candidate["domain_category"],
        attachment_tier=AttachmentTier(raw_candidate["attachment_tier"]),
        media_url=raw_candidate.get("media_url"),
        alt_text=raw_candidate.get("alt_text"),
        partner_tags=raw_candidate.get("partner_tags", []),
        primary_hashtags=raw_candidate.get("primary_hashtags", []),
        secondary_hashtags=raw_candidate.get("secondary_hashtags", []),
        boilerplate_hashtags=raw_candidate.get("boilerplate_hashtags", []),
        tool_ids=raw_candidate.get("tool_ids", []),
    )
    compiler = PublishCompiler(PlatformConfig("x_micro", SupersetProfile.MICRO_POST, 280))
    decision = ControlTower().review(review)
    if not decision.compile_allowed:
        print(f"candidate held by Control Tower: {', '.join(decision.reasons)}")
        return
    result = compiler.compile(candidate, review)
    print(yaml.safe_dump(result["sidecar_manifest"], sort_keys=False))


if __name__ == "__main__":
    main()
