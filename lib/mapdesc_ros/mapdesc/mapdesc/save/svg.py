import math
from ..util import image_dimensions


SVG_TPL = '''<svg width="{width:.0f}" height="{height:.0f}">
  <g transform="translate({offset_x:.0f} {offset_y:.0f})">
    {items}
  </g>
</svg>'''
WALL_STYLE = 'fill:black;'
SVG_LINE = '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" ' \
    'style="{style}" />'
SVG_CIRCLE = '<circle cx="{cx}" cy="{cy}" r="{r}" ' \
    'stroke-width="{stroke_width}" stroke="{stroke}" style="{style}" '\
    'fill="#00000000" />'
LANE_STYLE = 'stroke:red;stroke-width:1'


def save_svg(_map, output_file):
    width, height, offset_x, offset_y = image_dimensions(_map)
    res = _map.resolution

    svg_data = SVG_TPL.format(
        width=math.ceil(width / res), height=math.ceil(height / res),
        offset_x=0, offset_y=0,
        items='{items}')

    svg_items = []
    if _map.area:
        svg_items.append('<!-- areas -->')
        for area in _map.area:
            color = area.color if area.color else [100, 100, 255]
            style = 'fill:#{:02x}{:02x}{:02x};'.format(*color)
            svg_poly = '<polyline points="{points}" style="{style}" />'.format(
                style=style, points=''.join([
                    f'{round((p.x + offset_x) / res):.0f},'
                    f'{round((p.y + offset_y) / res):.0f} '
                    for p in area.local_points()]))
            svg_items.append(svg_poly)
    else:
        svg_items.append('<!-- (no areas) -->')

    if _map.wall:
        svg_items.append('<!-- walls -->')
        for wall in _map.wall:
            svg_poly = '<polyline points="{points}" style="{style}" />'.format(
                style=WALL_STYLE, points=''.join([
                    f'{round((p.x + offset_x) / res):.0f},'
                    f'{round((p.y + offset_y) / res):.0f} '
                    for p in wall.local_points()]))
            svg_items.append(svg_poly)
    else:
        svg_items.append('<!-- (no walls) -->')

    # TODO: path!

    if _map.lane_graph:
        svg_items.append('<!-- lanes -->')
        for edge in _map.lane_graph.edges:
            s = edge.source.position
            t = edge.target.position
            x1 = (s.x + offset_x) / res
            y1 = (s.y + offset_y) / res
            x2 = (t.x + offset_x) / res
            y2 = (t.y + offset_y) / res
            svg_items.append(SVG_LINE.format(
                x1=x1, x2=x2, y1=y1, y2=y2, style=LANE_STYLE))
    else:
        svg_items.append('<!-- (no lanes) -->')

    if _map.marker:
        svg_items.append('<!-- marker -->')
        for marker in _map.marker:
            pos = marker.pose.position
            x = int((pos.x + offset_x) / res)
            y = int((pos.y + offset_y) / res)
            color = marker.color if marker.color else [0, 0, 255]
            stroke = '#{:02x}{:02x}{:02x}'.format(*color)
            radius = (marker.radius if marker.radius else 1.0) / res
            _style = 'fill:none'
            svg_items.append(SVG_CIRCLE.format(
                style=_style, cx=x, cy=y, r=radius, stroke_width=1,
                stroke=stroke))
    else:
        svg_items.append('<!-- (no marker) -->')

    with open(output_file, 'w', encoding='utf-8') as fp:
        fp.write(svg_data.format(items='\n    '.join(svg_items)))
