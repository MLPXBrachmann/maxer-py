"""Tests for Maxer's config utilities"""


from unittest import TestCase

from maxer.lib.config import check_config, invert_layer_order, generate_combinations, resolve_value

class TestConfig(TestCase):
    def test_checks_config(self):
        self.assertTrue(check_config({
            'input': {'layers': ['input']},
            'output': {'file': 'output'},
        }))

        self.assertFalse(check_config({
            'input': {'layers': []},
            'output': {'file': 'output'},
        }))

        self.assertFalse(check_config({
            'input': {'layers': ['input']}
        }))

        self.assertFalse(check_config({
            'input': {'layers': ['input']},
            'output': {'file': 'output'},
            'combinations': {},
        }))

        self.assertTrue(check_config({
            'input': {'layers': ['input']},
            'output': {'file': 'output'},
            'palette': {},
            'combinations': [],
        }))

    def test_inverts_layer_order(self):
        config = {'input': {'layers': ['1', '2', '3']}}
        invert_layer_order(config)

        self.assertEqual(config, {'input': {'layers': ['3', '2', '1']}})

    def test_generates_combinations(self):
        self.assertEqual(generate_combinations({}), [{}])

        self.assertEqual(generate_combinations({
            'palette': {'var1': 'test'},
        }), [{'var1': 'test'}])

        self.assertEqual(generate_combinations({
            'combinations': [],
            'palette': {'var1': 'test'},
        }), [])

        self.assertEqual(generate_combinations({
            'combinations': [{'var1': 'test'}],
        }), [{'var1': 'test'}])

        self.assertEqual(generate_combinations({
            'combinations': [
                {'var1': 'test', 'var2': 'test2'},
                {'var1': 'test3'},
                {'var1': 'test3', 'for': [{'var2': 'test4'}, {'var2': 'test5'}]},
            ],
            'palette': {'var3': 'test0'},
        }), [
            {'var1': 'test', 'var2': 'test2', 'var3': 'test0'},
            {'var1': 'test3', 'var3': 'test0'},
            {'var1': 'test3', 'var2': 'test4', 'var3': 'test0'},
            {'var1': 'test3', 'var2': 'test5', 'var3': 'test0'},
        ])

        self.assertEqual(generate_combinations({
            'combinations': [{'var1': ['test', 'test2']}],
        }), [
            {'var1': 'test'},
            {'var1': 'test2'},
        ])

    def test_resolves_value(self):
        self.assertEqual(resolve_value('', {}), '')
        self.assertEqual(resolve_value(True, {}), True)
        self.assertEqual(resolve_value('test', {'test': 'value'}), 'test')

        self.assertEqual(resolve_value(
            '{{test}} and {{test2}}',
            {'test': 'value', 'test2': 'value2'},
        ), 'value and value2')
        self.assertEqual(resolve_value(
            '{{test}} and {{test2}}',
            {'test': 'value', 'test2': '{{test}}'},
        ), 'value and value')

        self.assertTrue(resolve_value({'op': 'parse', 'input': 'true'}, {}))
        self.assertFalse(resolve_value({'op': 'parse', 'input': 'false'}, {}))
        self.assertEqual(resolve_value({'op': 'parse', 'input': '{{num}}'}, {'num': '5'}), 5)

        self.assertTrue(resolve_value(
            {'op': 'oneOf', 'input': '{{test}}', 'values': ['value1', 'value2', '{{test2}}']},
            {'test': 'value', 'test2': '{{test}}'},
        ))
        self.assertFalse(resolve_value(
            {
                'op': 'oneOf',
                'negate': True,
                'input': '{{test}}',
                'values': ['value1', 'value2', '{{test2}}'],
            },
            {'test': 'value', 'test2': '{{test}}'},
        ))
        self.assertFalse(resolve_value(
            {'op': 'oneOf', 'input': '{{test}}', 'values': ['value1', 'value2', '{{test2}}']},
            {'test': 'value', 'test2': 'value3'},
        ))

        self.assertEqual(resolve_value(
            {'op': 'select', 'input': '{{test}}', 'values': {}},
            {'test': 'value'},
        ), 'value')
        self.assertEqual(resolve_value(
            {
                'op': 'select',
                'input': '{{test}}',
                'values': {'value': 'value2', 'value3': 'value4'}
            },
            {'test': 'value'},
        ), 'value2')
