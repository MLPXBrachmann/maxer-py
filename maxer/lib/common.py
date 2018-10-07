"""Shared utility functions"""

import os
import colorama
from colour import Color

# '\n' newline is directly appended to the message to ensure thread-safety

def print_done(message):
    """Print a done message."""
    print(colorama.Fore.BLUE + message + '\n', end='')

def print_error(message):
    """Print an error message."""
    print(colorama.Fore.RED + 'Error: ' + message + '\n', end='')

def print_failed(message):
    """Print a fail message."""
    print(colorama.Fore.RED + message + '\n', end='')

def print_info(message):
    """Print an info message."""
    print(colorama.Fore.WHITE + message + '\n', end='')

def print_start(message):
    """Print a start message."""
    print(colorama.Fore.BLUE + message + '\n', end='')

def print_warning(message):
    """Print an error message."""
    print(colorama.Fore.RED + 'Warning: ' + message + '\n', end='')

def ensure_dir(path):
    """
    Ensure the given directory exists

    :param path: The directory path
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

def parse_color(color_string):
    """
    Convert a color to an sRGB tuple

    :param color_string: The color
    :return: A tuple with sRGB values
    """
    rgb = Color(color_string).rgb
    return (rgb[0] * 255, rgb[1] * 255, rgb[2] * 255)

def flatten(nested_list):
    """
    Recursively flatten a nested list

    :param list: The list to flatten
    :return: A flat list
    """
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
