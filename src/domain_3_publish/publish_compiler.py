import json
import yaml
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional

class SupersetProfile(Enum):
    BOILERPLATE = "boilerplate"
    SOCIAL_POST = "social_post"
    MICRO_POST = "micro_post"

class AttachmentTier(Enum):
    ATOMIC_TEXT = "atomic_text"
    ILLUSTRATED = "illustrated"
    FANCY = "fancy"

# STATIC MIANVI REGISTRY (STUB FOR MARK 0)
STATIC_MIANZI_REGISTRY = {
    "P0": [
        {"id": "comfyui", "name": "ComfyUI Node Engine", "weight": 95, "logo_slot": "P0_DS0P_Core"},
        {"id": "fairlight", "name": "Fairlight NLE", "weight": 90, "logo_slot": "P0_Fairlight_Audio"},
    ],
    "P1": [
        {"id": "nvidia_cuda", "name": "NVIDIA CUDA Acceleration", "weight": 85, "logo_slot": "P1_NVIDIA_Omniverse"},
        {"id": "linux_runtime", "name": "Enterprise Linux", "weight": 80, "logo_slot": "P1_Linux_Kernel"},
    ],
    "P2": [
        {"id": "mcp_harness", "name": "Model Context Protocol (MCP)", "weight": 60, "logo_slot": "P2_MCP_Daemon"},
    ],
    "P3": [
        {"id": "dsop_branding_notebook", "name": "DS0P Branding Master Notebook", "weight": 40, "logo_slot": "P3_Local_Notebook"},
    ],
}

@dataclass
class AgentGatekeeperApproval:
    approval_id: str
    tone_audit_status: str
    tri_tone_scores: Dict[str, float]
    prohibited_conventions_check: Dict[str, bool]
    fsr_star_rank_cleared: str
    target_platform_fsr_ceiling: str

@dataclass
class PublishCandidate:
    candidate_id: str
    title: str
    body_text: str
    domain_category: str
    attachment_tier: AttachmentTier = AttachmentTier.ATOMIC_TEXT
    media_url: Optional[str] = None
    alt_text: Optional[str] = None
    gatekeeper_approval: Optional[AgentGatekeeperApproval] = None
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

class PublishCompiler:
    def __init__(self, platform_config: PlatformConfig):
        self.config = platform_config

    def resolve_mianzi_stub(self, tool_ids: List[str]) -> Dict:
        attributed_tools = []
        outro_slots = []
        for tier, tools in STATIC_MIANZI_REGISTRY.items():
            for t in tools:
                if not tool_ids or t["id"] in tool_ids:
                    attributed_tools.append(t)
                    if t.get("logo_slot"):
                        outro_slots.append(t["logo_slot"])
        
        attributed_tools.sort(key=lambda x: x["weight"], reverse=True)
        return {
            "attributed_tools": attributed_tools,
            "outro_logo_slots": outro_slots
        }

    def compile(self, candidate: PublishCandidate) -> Dict:
        gatekeeper_log = None
        if candidate.gatekeeper_approval:
            app = candidate.gatekeeper_approval
            gatekeeper_log = {
                "approval_id": app.approval_id,
                "status": app.tone_audit_status,
                "tri_tone_scores": app.tri_tone_scores,
                "fsr_cleared": app.fsr_star_rank_cleared <= app.target_platform_fsr_ceiling
            }

        body = candidate.body_text.strip()
        if self.config.include_domain_link and self.config.profile != SupersetProfile.MICRO_POST:
            body_with_domain = f"{body}\n\n{self.config.domain_url}"
        else:
            body_with_domain = body

        footer_elements: List[str] = []
        if candidate.partner_tags:
            partner_str = " ".join([f'#{t.lstrip("#")}' for t in candidate.partner_tags])
            footer_elements.append(f"In collaboration with: {partner_str}")

        all_tags = []
        all_tags.extend([f'#{t.lstrip("#")}' for t in candidate.primary_hashtags])
        all_tags.extend([f'#{t.lstrip("#")}' for t in candidate.secondary_hashtags])
        all_tags.extend([f'#{t.lstrip("#")}' for t in candidate.boilerplate_hashtags])
        
        content_len = len(body_with_domain)
        headroom = self.config.max_chars - content_len
        
        audit_logs = []
        retained_tags = []
        nl = "\n"
        retained_footer_text = nl.join(footer_elements) if footer_elements else ""
        
        needed_for_footer = len(retained_footer_text) + (2 if retained_footer_text else 0)
        current_headroom = headroom - needed_for_footer

        if current_headroom < 0:
            audit_logs.append({
                "code": "BODY_EXCEEDS_CAP",
                "level": "warn",
                "message": f"Content length ({content_len}) exceeds allocation ({self.config.max_chars}).",
                "action": "Footer and hashtags omitted."
            })
            retained_footer_text = ""
            quota_status = "body_only"
        else:
            accumulated_tags_len = 0
            for tag in all_tags:
                tag_cost = len(tag) + 1
                if accumulated_tags_len + tag_cost <= current_headroom:
                    retained_tags.append(tag)
                    accumulated_tags_len += tag_cost
                else:
                    audit_logs.append({
                        "code": "HEADROOM_CONSTRAINED",
                        "level": "info",
                        "message": "Platform headroom limit reached.",
                        "action": f"Pruned hashtag {tag}"
                    })
                    break
            quota_status = "optimal" if len(retained_tags) == len(all_tags) else "pruned"

        tag_block = " ".join(retained_tags)
        payload_parts = [body_with_domain]
        if retained_footer_text:
            payload_parts.append(retained_footer_text)
        if tag_block:
            payload_parts.append(tag_block)

        dnl = "\n\n"
        final_payload_text = dnl.join(payload_parts)

        mianzi_data = self.resolve_mianzi_stub(candidate.tool_ids)

        media_payload = None
        if candidate.attachment_tier == AttachmentTier.ILLUSTRATED:
            media_payload = {
                "type": "image",
                "image_url": candidate.media_url or "mock_visual_asset",
                "alt_text": candidate.alt_text or candidate.title,
                "color_palette_token": "monochrome_abyssal"
            }
        elif candidate.attachment_tier == AttachmentTier.FANCY:
            media_payload = {
                "type": "video",
                "video_url": candidate.media_url or "mock_video_asset",
                "alt_text": candidate.alt_text or candidate.title,
                "video_outro_logo_slots": mianzi_data["outro_logo_slots"],
                "fps": 60,
                "resolution": "4K_2160p"
            }

        sidecar_manifest = {
            "run_metadata": {
                "candidate_id": candidate.candidate_id,
                "target_platform": self.config.platform_name,
                "profile_applied": self.config.profile.value,
                "attachment_tier": candidate.attachment_tier.value
            },
            "gatekeeper_audit": gatekeeper_log,
            "budget_interface": {
                "platform_max_chars": self.config.max_chars,
                "content_body_chars": content_len,
                "headroom_remaining": headroom,
                "allocated_footer_chars": len(final_payload_text) - content_len,
                "total_payload_chars": len(final_payload_text)
            },
            "execution_status": {
                "superset_profile_applied": self.config.profile.value,
                "quota_status": quota_status,
                "tags_retained": len(retained_tags),
                "tags_pruned": len(all_tags) - len(retained_tags)
            },
            "attachment_status": {
                "tier": candidate.attachment_tier.value,
                "attached": candidate.attachment_tier != AttachmentTier.ATOMIC_TEXT
            },
            "mianzi_attribution_stub": {
                "top_attributed_tool": mianzi_data["outro_logo_slots"][0] if mianzi_data["outro_logo_slots"] else None,
                "total_tools_credited": len(mianzi_data["attributed_tools"])
            },
            "errata_audit_log": audit_logs
        }

        return {
            "atomic_text_base": final_payload_text,
            "media_payload": media_payload,
            "sidecar_yaml": yaml.dump(sidecar_manifest, sort_keys=False)
        }

if __name__ == "__main__":
    yaml_contract_str = """
agent_gatekeeper_approval:
  approval_id: "auth_token_dsop_9921"
  tone_audit_status: "PASSED"
  tri_tone_scores:
    authoritative: 0.94
    philosophical: 0.91
    evocative: 0.88
  prohibited_conventions_check:
    sensationalism_detected: false
    lighthearted_humor_detected: false
  fsr_star_rank_cleared: "*"
  target_platform_fsr_ceiling: "*"

candidate_payload:
  candidate_id: "pluto_yuggoth_01"
  title: "Latent Navigation Spec"
  agent_polished_body: "Thermal surveys confirm dark gravitational perturbers beyond Pluto at 120 AU. Remote outposts observe our sun from the frozen rim of the solar system."
  domain_category: "ai_mechanics"
  attachment_tier: "fancy"
  media_url: "mock_video_asset"
  alt_text: "Deep space thermal scan showing Yuggoth outpost"
  partner_tags: ["JWST", "ComfyUI"]
  primary_hashtags: ["CosmicHorror", "Yuggoth"]
  secondary_hashtags: ["PlanetX", "Astronomy"]
  boilerplate_hashtags: ["DS0P", "GenerativeSciFi"]
  tool_ids: ["comfyui", "nvidia_cuda", "mcp_harness", "dsop_branding_notebook"]
"""
    raw_data = yaml.safe_load(yaml_contract_str)
    gk_raw = raw_data["agent_gatekeeper_approval"]
    cd_raw = raw_data["candidate_payload"]

    gatekeeper = AgentGatekeeperApproval(
        approval_id=gk_raw ["approval_id"],
        tone_audit_status=gk_raw["tone_audit_status"],
        tri_tone_scores=gk_raw["tri_tone_scores"],
        prohibited_conventions_check=gk_raw["prohibited_conventions_check"],
        fsr_star_rank_cleared=gk_raw ["fsr_star_rank_cleared"],
        target_platform_fsr_ceiling=gk_raw["target_platform_fsr_ceiling"]
    )

    candidate = PublishCandidate(
        candidate_id=cd_raw["candidate_id"],
        title=cd_raw["title"],
        body_text=cd_raw ["agent_polished_body"],
        domain_category=cd_raw["domain_category"],
        attachment_tier=AttachmentTier(cd_raw["attachment_tier"]),
        media_url=cd_raw["media_url"],
        alt_text=cd_raw["alt_text"],
        gatekeeper_approval=gatekeeper,
        partner_tags=cd_raw["partner_tags"],
        primary_hashtags=cd_raw ["primary_hashtags"],
        secondary_hashtags=cd_raw["secondary_hashtags"],
        boilerplate_hashtags=cd_raw["boilerplate_hashtags"],
        tool_ids=cd_raw["tool_ids"]
    )

    x_micro_config = PlatformConfig(
        platform_name="x_micro",
        profile=SupersetProfile.MICRO_POST,
        max_chars=280
    )

    compiler = PublishCompiler(x_micro_config)
    res = compiler.compile(candidate)

    print("candidate compiled successfully")
    print(res["sidecar_yaml"])
