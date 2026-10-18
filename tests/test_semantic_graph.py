import unittest
from casinobot.semantic_graph import ConceptGraph

class SemanticGraphTests(unittest.TestCase):
    def setUp(self):
        self.graph = ConceptGraph()
        self.graph.put("rtp", {"value": 0.96})
        self.graph.put("analysis", {"kind": "audit"})
        self.graph.link("analysis", "rtp")

    def test_canonical_reference(self):
        self.assertEqual(self.graph.dependencies("analysis")["rtp"]["value"], {"value": 0.96})

    def test_version_change(self):
        before = self.graph.snapshot_versions("analysis")
        self.graph.put("rtp", {"value": 0.95}, expected_version=1)
        self.assertEqual(self.graph.stale("analysis", before), ["rtp"])

    def test_no_stale(self):
        self.assertEqual(self.graph.stale("analysis", self.graph.snapshot_versions("analysis")), [])

    def test_conflict(self):
        with self.assertRaises(ValueError):
            self.graph.put("rtp", {"value": 0.95}, expected_version=0)

    def test_copy_isolation(self):
        data = self.graph.get("rtp")
        data["value"]["value"] = 0.01
        self.assertEqual(self.graph.get("rtp")["value"]["value"], 0.96)

    def test_missing_node(self):
        with self.assertRaises(KeyError):
            self.graph.link("analysis", "unknown")

if __name__ == "__main__":
    unittest.main()
