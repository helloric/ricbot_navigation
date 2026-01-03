from .png import save_png
from .sdf import save_sdf
from .yaml import save_yaml
from .svg import save_svg
from .rosmap import save_rosmap


SAVE = {
    'sdf': save_sdf,
    'yaml': save_yaml,
    'png': save_png,
    'svg': save_svg,
    'rosmap': save_rosmap
}
