import ast

import pandas as pd
from lightweight_charts.abstract import Line, AbstractChart
import re

re_rgba_extract = re.compile('rgb[a]?(.*?)$')


def hex_to_rgb(hex, alpha=1):
    hex = hex.strip().lower().replace(' ', '')
    if '#' in hex:
        hex = hex.replace('#', '')
        hex = [int(hex[i:i + 2], 16) for i in (0, 2, 4)]
        hex.append(alpha)

    elif 'rgb' in hex:
        hex = re_rgba_extract.findall(hex)[0]
        hex = list(ast.literal_eval(hex))
        if len(hex) == 3:
            hex.append(alpha)
        elif len(hex) == 4:
            hex[3] = alpha

    return f'rgba{tuple(hex)}'


def add_background_color(chart: AbstractChart | Line, data: pd.DataFrame() = None, start_time=None, end_time=None,
                         color='rgba(252, 219, 3, 0.8)', **kwargs):
    # background span can only be added to line overaly by using a different function on the line instead of the chart

    if isinstance(data, pd.DataFrame):
        assert {'start_time', 'end_time', 'color'}.issubset(set(
            data.columns)), "start_time, end_time, color needed to color background ranges"
        list_of_spans = []
        for t in data.itertuples():
            span = chart.vertical_span(start_time=t.start_time, end_time=t.end_time, color=t.color)
            list_of_spans.append(span)

        return list_of_spans
    else:
        assert all([start_time, end_time, color]), "missing required fields: start_time, end_time, color"

        if "#" in color:
            alpha = kwargs.get('alpha')
            assert alpha, 'alpha needs to be provide for hex color'
            color = hex_to_rgb(color.replace('#', '').strip())
            color = f'rgba({color[0]}, {color[1]}, {color[2]}, {alpha})'

        chart.vertical_span(start_time=start_time, end_time=end_time, color=color)