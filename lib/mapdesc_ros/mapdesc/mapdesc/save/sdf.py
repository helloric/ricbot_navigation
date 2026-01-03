import os
import jinja2
from pathlib import Path


BASE_DIR = Path(os.path.dirname(__file__)).absolute()
TEMPLATE_DIR = BASE_DIR.parent / 'data' / 'templates'
templateLoader = jinja2.FileSystemLoader(searchpath=TEMPLATE_DIR)
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_SDF = "model.sdf.j2"
TEMPLATE_CFG = "model.config.j2"
template_sdf = templateEnv.get_template(TEMPLATE_SDF)
template_cfg = templateEnv.get_template(TEMPLATE_CFG)


def save_sdf(_map, output_path):
    output_path = Path(output_path)
    if not output_path.exists():
        os.mkdir(output_path)
    with open(output_path / 'model.sdf', 'w', encoding='UTF-8') as model:
        model.write(template_sdf.render(map=_map))
    with open(output_path / 'model.config', 'w', encoding='UTF-8') as model:
        author = {'name': 'MapDesc Generator', 'email': 'noone@example.com'}
        model.write(template_cfg.render(map=_map, author=author))
