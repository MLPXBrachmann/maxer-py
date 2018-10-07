"""Tests for Maxer's image processing utilities"""


from unittest import TestCase

from maxer.lib.image import BLEND_MODES, get_blend_mode, is_layer_hidden

class TestImage(TestCase):
    def test_holds_blend_modes(self):
        self.assertTrue('over' in BLEND_MODES)

    def test_identifies_hidden_layer(self):
        self.assertFalse(is_layer_hidden('file', {}))
        self.assertFalse(is_layer_hidden({'file': 'file'}, {}))
        self.assertTrue(is_layer_hidden({'file': 'file', 'hidden': True}, {}))
        self.assertFalse(is_layer_hidden({'file': 'file', 'hidden': False}, {}))

    def test_gets_blend_mode(self):
        self.assertEqual(get_blend_mode('file', {}), 'over')
        self.assertEqual(get_blend_mode({'file': 'file'}, {}), 'over')
        self.assertEqual(
            get_blend_mode({'file': 'file', 'blendMode': '{{blend}}'}, {'blend': 'multiply'}),
            'multiply',
        )
