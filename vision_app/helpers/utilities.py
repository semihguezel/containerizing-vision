import yaml
import random


def generate_random_rgb_color_list(n):
    """
    Generate a list of random RGB colors.

    Args:
    - n (int): Number of colors to generate.

    Returns:
    - list: A list of randomly generated RGB colors.
    """
    color_list = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(n)]
    return color_list


def read_yaml_file(file_path):
    """
    Read YAML file and return its content.

    Args:
    - file_path (str): Path to the YAML file.

    Returns:
    - dict: Dictionary containing the data from the YAML file.
    """
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error reading YAML file {file_path}: {e}")
            return None
