"""Maxer config utilities"""


import json
import os
import re

from .common import print_warning


def load_config(config_file):
    """
    Load a config file

    :param config_file: The path to the config file
    :return: The config object
    """
    with open(config_file, 'r') as json_data:
        config = json.load(json_data)

        if 'extends' in config:
            super_config = load_config(
                os.path.join(os.path.dirname(config_file), config['extends']),
            )
            super_config.update(config)
            return super_config

        return config

# TODO: Provide detailled error description


def check_layer_config(layers):
    """
    Perform a fast validity check on the passed layer config

    :param layers: The layer config
    :return: The validity state
    """
    return (layers
            and not [
                layer for layer in layers
                if not (isinstance(layer, str)
                        or isinstance(layer, dict) and 'file' in layer
                        or isinstance(layer, list) and check_layer_config(layer))
            ])


# TODO: Provide detailled error description
def check_config(config):
    """
    Perform a fast validity check on the passed config

    :param config: The config object
    :return: The validity state
    """
    return (config and isinstance(config, dict)
            and 'input' in config and isinstance(config['input'], dict)
            and 'layers' in config['input'] and isinstance(config['input']['layers'], list)
            and check_layer_config(config['input']['layers'])
            and 'output' in config and 'file' in config['output']
            and (not 'combinations' in config or isinstance(config['combinations'], list))
            and (not 'palette' in config or isinstance(config['palette'], dict)))


def invert_layer_order(config):
    """
    Invert the order of layers in the given config

    :param config: The config object
    """
    config['input']['layers'].reverse()


def generate_combinations(config):
    """
    Generate all variable sets for the given config

    :param config: The config object
    :return: An array of variable sets
    """
    if 'combinations' in config:
        output = []

        # Process given combinations
        for input_layer in config['combinations']:
            result = []

            # Split dynamic/static attributes
            static_attributes = config['palette'].copy(
            ) if 'palette' in config else {}
            dynamic_attributes = {}

            for key, attribute in input_layer.items():
                if key == 'for':
                    continue

                if isinstance(attribute, list):
                    dynamic_attributes[key] = attribute
                else:
                    static_attributes[key] = attribute

            # Generate combinations from array attributes
            result.append(static_attributes)
            for key, attribute in dynamic_attributes.items():
                next_result = []
                for out in result:
                    for value in attribute:
                        next_result.append({**out, key: value})

                result = next_result

            # Generate combinations from 'for' attribute
            if 'for' in input_layer and isinstance(input_layer['for'], list):
                next_result = []
                for sub_combination in input_layer['for']:
                    for out in result:
                        next_result.append({**out, **sub_combination})
                result = next_result
            
            
            # Generate combinations from 'for' attribute
            if 'for2' in input_layer and isinstance(input_layer['for2'], list):
                for sub_combination_array in input_layer['for2']:
                    next_result = []
                    for sub_combination in sub_combination_array:
                        for out in result:
                            next_result.append({**out, **sub_combination})
                    result = next_result

            # Apply combinations to output
            output.extend(result)

        return output
    return [config['palette'] if 'palette' in config else {}]


VARIABLE_REGEX = re.compile(r'{{(.+?)}}')


class MaxerResolveError(ValueError):
    """The resolve error"""
    pass


def resolve_value(value, variable_set):
    """
    Resolve a config value

    :param value: The input value
    :return: The resolved value
    """

    # Resolve strings
    if isinstance(value, str):
        def replace_variable(match):
            """Replace a variable match by the according value"""
            variable_name = match.group(1)
            if variable_name in variable_set:
                return resolve_value(variable_set[variable_name], variable_set)
            print_warning('Variable \'{}\' is undefined'.format(variable_name))
            return ''

        match = re.fullmatch(VARIABLE_REGEX, value)
        return re.sub(VARIABLE_REGEX, replace_variable, value) if match is None else replace_variable(match)

    # Resolve complex expressions (e.g. logic)
    if isinstance(value, dict) and 'op' in value:
        operation = value['op']
        knownOperation = False

        if operation == 'parse':
            knownOperation = True
            if 'input' in value:
                try:
                    return json.loads(resolve_value(value['input'], variable_set))
                except json.decoder.JSONDecodeError:
                    raise MaxerResolveError(
                        'Invalid input value \'{}\' for parse operation'.format(
                            value['input'])
                    )
            raise MaxerResolveError('Invalid configuration for operation \'{}\''.format(
                operation))  # TODO: Provide detailled error description

        elif operation == 'oneOf':
            knownOperation = True
            if 'input' in value and 'values' in value and isinstance(value['values'], list):
                result = resolve_value(value['input'], variable_set) in [
                    resolve_value(compare_value, variable_set) for compare_value in value['values']
                ]
                return not result if 'negate' in value and value['negate'] else result
            raise MaxerResolveError('Invalid configuration for operation \'{}\''.format(
                operation))  # TODO: Provide detailled error description

        # TODO: Resolve keys
        elif operation == 'select':
            knownOperation = True
            if 'input' in value and 'values' in value and isinstance(value['values'], dict):
                input_value = resolve_value(value['input'], variable_set)
                return resolve_value(value['values'][input_value], variable_set) if input_value in value['values'] else input_value
            raise MaxerResolveError('Invalid configuration for operation \'{}\''.format(
                operation))  # TODO: Provide detailled error description

        elif operation == 'fileExists':
            knownOperation = True
            if 'input' in value:
                result = os.path.isfile(
                    resolve_value(value['input'], variable_set))
                return not result if 'negate' in value and value['negate'] else result

        if knownOperation:
            raise MaxerResolveError(
                'Invalid configuration for operation \'{}\''.format(operation))

        raise MaxerResolveError('Undefined operation \'{}\''.format(operation))

    return value
