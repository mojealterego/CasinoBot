"""Tests for typed state and reversible R3Mem archives."""
import unittest
from casinobot.omni_core import R3Mem, initial_state


class OmniCoreTests(unittest.TestCase):
    def test_state_defaults(self):
        state = initial_state("session-1")
        self.assertEqual(state["daemon_status"], "idle")
        self.assertEqual(state["sasos_episode_refs"], [])

    def test_unicode_round_trip(self):
        archive = R3Mem()
        episode = {"observation": "żółć", "values": [1, 2, {"x": True}]}
        token = archive.encode_to_virtual_token(episode)
        self.assertEqual(archive.decode_from_virtual_token(token), episode)

    def test_deterministic_content_address(self):
        archive = R3Mem()
        self.assertEqual(archive.encode_to_virtual_token({"a": 1, "b": 2}),
                         archive.encode_to_virtual_token({"b": 2, "a": 1}))

    def test_export_import(self):
        original = R3Mem()
        token = original.encode_to_virtual_token({"sample": [3, 5, 8]})
        restored = R3Mem()
        restored.import_archive(original.export_archive())
        self.assertEqual(restored.decode_from_virtual_token(token),
                         {"sample": [3, 5, 8]})

    def test_unknown_token(self):
        with self.assertRaises(KeyError):
            R3Mem().decode_from_virtual_token("r3mem:missing")

    def test_tamper_detection(self):
        archive = R3Mem()
        token = archive.encode_to_virtual_token({"ok": True})
        exported = archive.export_archive()
        fake = {"r3mem:" + "0" * 64: exported[token]}
        with self.assertRaises(ValueError):
            R3Mem().import_archive(fake)


if __name__ == "__main__":
    unittest.main()
