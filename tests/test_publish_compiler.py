import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src" / "domain_3_publish"))

from publish_compiler import (  # noqa: E402
    AttachmentTier,
    PlatformConfig,
    PublishCandidate,
    PublishCompiler,
    SupersetProfile,
)


class PublishCompilerTests(unittest.TestCase):
    def compile(self, max_chars: int, **candidate_fields):
        config = PlatformConfig(
            platform_name="test",
            profile=SupersetProfile.MICRO_POST,
            max_chars=max_chars,
            include_domain_link=False,
        )
        candidate = PublishCandidate(
            candidate_id="test-1",
            title="Test",
            body_text="Body",
            domain_category="mythos",
            **candidate_fields,
        )
        return PublishCompiler(config).compile(candidate)

    def test_exact_cap_includes_footer_and_tag_separators(self):
        result = self.compile(
            52,
            partner_tags=["partner"],
            primary_hashtags=["one", "two"],
        )
        payload = result["atomic_text_base"]
        self.assertLessEqual(len(payload), 52)
        self.assertEqual(
            result["sidecar_manifest"]["budget_interface"]["total_payload_chars"],
            len(payload),
        )

    def test_omits_partner_footer_when_footer_alone_wont_fit(self):
        result = self.compile(10, partner_tags=["a-very-long-partner-tag"])
        self.assertEqual(result["atomic_text_base"], "Body")
        self.assertEqual(
            result["sidecar_manifest"]["execution_status"]["quota_status"],
            "body_only",
        )

    def test_reports_body_over_cap_without_truncating_it(self):
        result = self.compile(2)
        self.assertEqual(result["atomic_text_base"], "Body")
        self.assertEqual(
            result["sidecar_manifest"]["execution_status"]["quota_status"],
            "body_exceeds_cap",
        )

    def test_missing_attachment_is_not_reported_as_attached(self):
        result = self.compile(100, attachment_tier=AttachmentTier.FANCY)
        self.assertFalse(result["sidecar_manifest"]["attachment_status"]["attached"])


if __name__ == "__main__":
    unittest.main()
