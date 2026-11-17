from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional
import json

class SupersetProfile(Enum):
    BOILERPLATE = "boilerplate"
    SOCIAL_POST = "social_post"
    MICRO_POST = "micro_post"

class AttachmentTier(Enum):
    ATOMIC_TEXT = "atomic_text"
    ILLUSTRATED = "illustrated"
    FANCY = "fancy"

@dataclass
class IllustratedAttachment:
    image_url: str
    aspect_ratio: str = "16:9"
    alt_text: str = ""
    color_palette_token: Optional[str] = "cosmic_darkness"
    thumbnail_manifest: Dict[str, str] = field(default_factory=lambda: {
        "thumb_sm": "1080x1080",
        "thumb_lg": "1920x1080"
    })

@dataclass
class FancyAttachment:
    video_url: str
    audio_stem_id: Optional[str] = "yuggoth_ambient_drone_v1"
    video_outro_logo_slots: List[str] = field(default_factory=lambda: ["P0_Primary", "P1_Partner_NVIDIA"])
    aspect_ratio: str = "16:9"
    fps: int = 60
    resolution: str = "4K_2160p"

@dataclass
class PublishCandidate:
    candidate_id: str
    title: str
    body_text: str
    domain_category: str
    credit_uri: Optional[str] = None
    partner_tags: List[str] = field(default_factory=list)
    primary_hashtags: List[str] = field(default_factory=list)
    secondary_hashtags: List[str] = field(default_factory=list)
    boilerplate_hashtags: List[str] = field(default_factory=list)
    attachment_tier: AttachmentTier = AttachmentTier.ATOMIC_TEXT
    illustrated_attachment: Optional[IllustratedAttachment] = None
    fancy_attachment: Optional[FancyAttachment] = None

@dataclass
class PlatformConfig:
    platform_name: str
    profile: SupersetProfile
    max_chars: int
    include_domain_link: bool = True
    domain_url: str = "ledante_site"

@dataclass
class SidecarAuditLog:
    code: str
    level: str
    message: str
    action: str

class PublishCompiler:
    def __init__(self, platform_config: PlatformConfig):
        self.config = platform_config

    def compile(self, candidate: PublishCandidate) -> Dict:
        body = candidate.body_text.strip()
        if self.config.include_domain_link and self.config.profile != SupersetProfile.MICRO_POST:
            body_with_domain = f"{body}\n\n{self.config.domain_url}"
        else:
            body_with_domain = body

        footer_elements: List[str] = []
        if candidate.partner_tags:
            partner_str = " ".join([f"#{t.lstrip('#')}" for t in candidate.partner_tags])
            footer_elements.append(f"In collaboration with: {partner_str}")

        all_tags = []
        all_tags.extend([f"#{t.lstrip('#')}" for t in candidate.primary_hashtags])
        all_tags.extend([f"#{t.lstrip('#')}" for t in candidate.secondary_hashtags])
        all_tags.extend([f"#{t.lstrip('#')}" for t in candidate.boilerplate_hashtags])
        content_len = len(body_with_domain)
        headroom = self.config.max_chars - content_len
        
        audit_logs: List[SidecarAuditLog] = []
        retained_tags: List[str] = []
        nl = "\n"
        retained_footer_text = nl.join(footer_elements) if footer_elements else ""
        
        needed_for_footer = len(retained_footer_text) + (2 if retained_footer_text else 0)
        current_headroom = headroom - needed_for_footer

        if current_headroom < 0:
            audit_logs.append(SidecarAuditLog(
                code="BODY_EXCEEDS_CAP",
                level="warn",
                message=f"Content length ({content_len}) exceeds allocation ({self.config.max_chars}).",
                action="Footer and hashtags omitted."
            ))
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
                    audit_logs.append(SidecarAuditLog(
                        code="HEADROOM_CONSTRAINED",
                        level="info",
                        message="Platform headroom limit reached.",
                        action=f"Pruned hashtag {tag}"
                    ))
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

        attachment_manifest = {
            "tier": candidate.attachment_tier.value,
            "media_payload": None
        }

        if candidate.attachment_tier == AttachmentTier.ILLUSTRATED and candidate.illustrated_attachment:
            attachment_manifest["media_payload"] = {
                "type": "image",
                "image_url": candidate.illustrated_attachment.image_url,
                "aspect_ratio": candidate.illustrated_attachment.aspect_ratio,
                "alt_text": candidate.illustrated_attachment.alt_text,
                "color_palette_token": candidate.illustrated_attachment.color_palette_token,
                "thumbnail_manifest": candidate.illustrated_attachment.thumbnail_manifest
            }
        elif candidate.attachment_tier == AttachmentTier.FANCY and candidate.fancy_attachment:
            attachment_manifest["media_payload"] = {
                "type": "video",
                "video_url": candidate.fancy_attachment.video_url,
                "audio_stem_id": candidate.fancy_attachment.audio_stem_id,
                "video_outro_logo_slots": candidate.fancy_attachment.video_outro_logo_slots,
                "aspect_ratio": candidate.fancy_attachment.aspect_ratio,
                "fps": candidate.fancy_attachment.fps,
                "resolution": candidate.fancy_attachment.resolution
            }

        sidecar_manifest = {
            "run_metadata": {
                "candidate_id": candidate.candidate_id,
                "target_platform": self.config.platform_name,
                "profile_applied": self.config.profile.value,
                "attachment_tier": candidate.attachment_tier.value,
            },
            "budget_interface": {
                "platform_max_chars": self.config.max_chars,
                "content_body_chars": content_len,
                "headroom_remaining": headroom,
                "allocated_footer_chars": len(final_payload_text) - content_len,
                "total_payload_chars": len(final_payload_text),
            },
            "execution_status": {
                "superset_profile_applied": self.config.profile.value,
                "quota_status": quota_status,
                "tags_retained": len(retained_tags),
                "tags_pruned": len(all_tags) - len(retained_tags),
            },
            "attachment_status": {
                "tier": candidate.attachment_tier.value,
                "attached": attachment_manifest["media_payload"] is not None
            },
            "errata_audit_log": [
                {
                    "errata_code": log.code,
                    "severity": log.level,
                    "message": log.message,
                    "action_taken": log.action,
                }
                for log in audit_logs
            ],
        }

        return {
            "atomic_text_base": final_payload_text,
            "attachment_manifest": attachment_manifest,
            "sidecar_manifest": sidecar_manifest,
        }
