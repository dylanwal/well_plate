import plotly.colors


class PlotlyColorMap:
    """
    Plotly doesn't make the colorscales directly accessible in a common format.
    Some are ready to use:

        colorscale = plotly.colors.PLOTLY_SCALES["Greens"]

    Others are just swatches that need to be constructed into a colorscale:

        viridis_colors, scale = plotly.colors.convert_colors_to_same_type(plotly.colors.sequential.Viridis)
        colorscale = plotly.colors.make_colorscale(viridis_colors, scale=scale)

        https://plotly.com/python/builtin-colorscales/
    """
    def __init__(self, min_value: float = 0, max_value: int = 1, colorscale_label: str = "viridis",
                 default_color: str = 'rgb(255,255,255)'):

        self.min_value = min_value
        self.max_value = max_value
        self.colorscale_label = colorscale_label
        self.default_color = default_color
        self.colorscale = self._get_colorscale()

    @staticmethod
    def _get_colorscale():
        viridis_colors, _ = plotly.colors.convert_colors_to_same_type(plotly.colors.sequential.Viridis)
        return plotly.colors.make_colorscale(viridis_colors)

    def _map_value(self, value: float) -> float:
        """ Maps values to [0,1] """
        if value > self.max_value:
            return 1
        if value < self.min_value:
            return 0
        return (value - self.min_value) / (self.max_value - self.min_value)

    def get(self, value):
        if value is None:
            return self.default_color

        value = self._map_value(value)

        if value == 0:
            return self.colorscale[0][1]
        if value == 1:
            return self.colorscale[-1][1]

        for cutoff, color in self.colorscale:
            if value > cutoff:
                low_cutoff, low_color = cutoff, color
            else:
                high_cutoff, high_color = cutoff, color
                break

        # noinspection PyUnboundLocalVariable
        return plotly.colors.find_intermediate_color(
            lowcolor=low_color, highcolor=high_color,
            intermed=value,
            colortype="rgb")
