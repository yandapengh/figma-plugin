import unittest

from memory_os.decision_gate import build_decision_payload, prepare_wiki_write
from memory_os.wiki_router import WikiRouter, WikiRouterError, validate_route_decision


class WikiRouterTests(unittest.TestCase):
    def setUp(self):
        with open("figma-wiki/_index.md", "r", encoding="utf-8") as f:
            self.index_markdown = f.read()

    def test_existing_route_requires_confirm(self):
        router = WikiRouter(
            category_tree_markdown=self.index_markdown,
            content_summary="按钮组件状态整理",
            recommendations=["components/button"],
        )

        q1 = router.next_question()
        self.assertEqual("S1.select_position", q1.question_id)
        self.assertIn("components/button", q1.candidates)

        r1 = router.submit_answer("S1.select_position", {"selected_path": "components/button", "rationale": "最相关"})
        self.assertFalse(r1.done)
        self.assertEqual("S4.confirm", r1.question.question_id)

        r2 = router.submit_answer("S4.confirm", {"user_confirmed": True, "rationale": "确认放置"})
        self.assertTrue(r2.done)
        self.assertEqual("existing", r2.route["route_mode"])
        self.assertTrue(r2.route["user_confirmed"])
        self.assertGreaterEqual(len(router.audit_log), 2)

    def test_create_subcategory_after_not_match(self):
        router = WikiRouter(
            category_tree_markdown=self.index_markdown,
            content_summary="Badge 组件规范",
            recommendations=["components/card"],
        )

        router.submit_answer("S1.select_position", {"selected_path": "not_matched", "rationale": "暂无匹配"})
        router.submit_answer("S2.create_new_category", {"create_new": True, "under_existing": True})
        router.submit_answer(
            "S3a.select_parent",
            {
                "parent_path": "components",
                "new_category_name": "badge",
                "new_category_description": "状态徽标组件",
            },
        )
        end = router.submit_answer("S4.confirm", {"user_confirmed": True})

        self.assertTrue(end.done)
        self.assertEqual("new_under_existing", end.route["route_mode"])
        self.assertEqual("components", end.route["parent_path"])
        self.assertEqual("badge", end.route["new_category_name"])

    def test_invalid_duplicate_category_name(self):
        with self.assertRaises(WikiRouterError):
            validate_route_decision(
                {
                    "route_mode": "new_under_existing",
                    "parent_path": "components",
                    "new_category_name": "button",
                    "user_confirmed": True,
                },
                existing_paths=["components/button"],
            )

    def test_prepare_wiki_write_pending(self):
        payload = build_decision_payload("new_page", {"component": {}}, {"wiki_index": ["components"]})
        routed = prepare_wiki_write(payload, None)
        self.assertEqual("pending_confirmation", routed["write_status"])
        self.assertFalse(routed["write_allowed"])

        confirmed = prepare_wiki_write(
            payload,
            {
                "route_mode": "existing",
                "selected_path": "components/button",
                "user_confirmed": True,
                "rationale": "已有分类",
            },
        )
        self.assertEqual("ready", confirmed["write_status"])
        self.assertTrue(confirmed["write_allowed"])
        self.assertEqual("components/button", confirmed["wiki_target_selected"])


if __name__ == "__main__":
    unittest.main()
