"""Maxer image processing"""


import os
import pyvips

from .common import (
    ensure_dir,
    parse_color,
    print_error,
    print_failed,
    print_info,
    print_warning,
)
from .config import resolve_value

BLEND_MODES = [pyvips.GValue.from_enum(pyvips.GValue.blend_mode_type, i) for i in range(0, 25)]

def is_layer_hidden(layer, variable_set):
    """
    Check if the given layer is hidden

    :param layer: The layer configuration
    :param variable_set: The active variable set
    :return: True, if the layer is hidden
    """
    return (isinstance(layer, dict)
            and 'hidden' in layer and resolve_value(layer['hidden'], variable_set))

def create_layer(layer, base_dir, variable_set):
    """
    Create a new layer

    :param layer: The layer configuration
    :param base_dir: The base working directory
    :param variable_set: The active variable set
    :return: The layer (vips image)
    """
    is_dict = isinstance(layer, dict)

    # Get file path
    file = os.path.join(base_dir, resolve_value(layer['file'] if is_dict else layer, variable_set))

    # Load image
    try:
        image = pyvips.Image.new_from_file(file, access='sequential')
    except pyvips.error.Error:
        raise IOError('Unable to load file \'{}\''.format(file))

    if is_dict and 'blendMode' in layer and layer['blendMode'] == 'multiply':
        image = image.unpremultiply()

    # Recolor layer
    if is_dict and 'color' in layer:
        color = resolve_value(layer['color'], variable_set)
        if not color == 'retain':
            try:
                color = parse_color(color)
                image = image.colourspace(pyvips.enums.Interpretation.SRGB)
                if image.get('bands') == 4:
                    image *= [0, 0, 0, 1]
                    image += [color[0], color[1], color[2], 0]
                else:
                    image *= [0, 0, 0]
                    image += [color[0], color[1], color[2]]
            except ValueError:
                print_error('Invalid color \'{}\''.format(color))

    return image

def get_blend_mode(layer, variable_set):
    """
    Get the blend mode of a given layer

    :param layer: The layer configuration
    :param variable_set: The active variable set
    :return: The layer's blend mode
    """
    if isinstance(layer, dict) and 'blendMode' in layer:
        blend_mode = resolve_value(layer['blendMode'], variable_set)
        if blend_mode in BLEND_MODES:
            return blend_mode
        print_warning('Unrecognized blend mode \'{}\', using \'over\' instead'.format(blend_mode))
    return 'over'

def composite_image(config, base_dir, variable_set):
    """
    Build an image

    :param config: The maxer config
    :param base_dir: The base working directory
    :param variable_set: The active variable set
    """
    input_config = config['input']
    input_base_dir = os.path.join(
        base_dir,
        resolve_value(input_config['baseDir'], variable_set) if 'baseDir' in input_config else '',
    )

    output_config = config['output']
    output_file_identifier = os.path.join(
        resolve_value(output_config['baseDir'], variable_set) if 'baseDir' in output_config else '',
        resolve_value(output_config['file'], variable_set),
    )
    output_file = os.path.join(
        base_dir,
        output_file_identifier,
    )

    base_layer, *layers = input_config['layers']

    try:
        # Load background
        image = create_layer(base_layer, input_base_dir, variable_set)

        # Apply layers
        if layers:
            images = [
                create_layer(layer, input_base_dir, variable_set)
                for layer in layers
                if not is_layer_hidden(layer, variable_set)
            ]
            modes = [
                get_blend_mode(layer, variable_set)
                for layer in layers
                if not is_layer_hidden(layer, variable_set)
            ]
            image = image.composite(images, modes)
    except IOError as err:
        print_error(str(err))
        print_failed('Failed: \'{}\''.format(output_file_identifier))
        return

    # Set output options
    output_options = {}

    # Set JPEG quality
    file_extension = os.path.splitext(output_file)[1]
    if 'quality' in output_config and file_extension == 'jpg' or file_extension == 'jpeg':
        quality = output_config['quality']
        if isinstance(quality, int) and 0 <= quality <= 100:
            output_options['Q'] = quality
        else:
            print_warning('Invalid quality setting \'{}\''.format(str(quality)))

    # Set size
    if 'width' in output_config:
        width = output_config['width']
        if isinstance(width, int) and 0 < width:
            image = image.resize(width / image.get('width'))
        else:
            print_warning('Invalid width setting \'{}\''.format(str(width)))
    
    # TODO: Scale by height

    # Write image
    try:
        ensure_dir(os.path.dirname(output_file))
        image.write_to_file(output_file, **output_options)
        print_info('Done: \'{}\''.format(output_file_identifier))
    except pyvips.error.Error:
        print_error('Unable to write file {}'.format(output_file_identifier))
        print_failed('Failed: \'{}\''.format(output_file_identifier))
