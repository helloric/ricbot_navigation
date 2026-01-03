# load data description
from ..model import Map
import yaml
import logging

logger = logging.getLogger(__name__)


def load_yaml(input_file=None):
    """Load from custom yaml format.
    """
    with open(input_file, encoding='utf-8') as fd:
        yaml_data = yaml.safe_load(fd)
    return Map(**yaml_data)
