import string

import numpy as np
import pandas as pd
import plotly.graph_objs as go

from well_plate.config import WELL_PLATE_DATA
from well_plate.grid import GridPattern
from well_plate.color_map import PlotlyColorMap
from well_plate.utils import flatten_list


class WellPlate:

    def __init__(self, number_wells: int = 24, shape: str = "circle"):
        """

        Parameters
        ----------
        number_wells: int
            range: 6, 12, 24, 96, 384
            number of wells
        shape: str
            range: "circle", "rect"
            shape of wells

        """
        if number_wells not in WELL_PLATE_DATA:
            raise ValueError("Invalid 'number_wells'. ")

        self.number_wells = number_wells
        self.specs = WELL_PLATE_DATA[number_wells]
        self.shape = shape

        self.row_labels = self._get_row_labels()
        self.col_labels = self._get_col_labels()
        self.well_positions = self._get_well_positions()
        self.data_dict = self._create_data_dict()

    def __repr__(self):
        return f"wells: {self.number_wells}"

    def _get_row_labels(self):
        return list(string.ascii_uppercase[:self.specs["rows"]])

    def _get_col_labels(self):
        return list(range(1, self.specs["columns"] + 1))

    def _get_well_positions(self) -> np.ndarray:
        grid = GridPattern(
            corner=np.array([self.specs["x_off"], self.specs["y_off"]]),
            x_length=self.specs["x_space"] * (self.specs["columns"] - 1),
            y_length=self.specs["y_space"] * (self.specs["rows"] - 1),
            x_count=self.specs["columns"],
            y_count=self.specs["rows"]
        )
        return grid.xy_points

    def _create_data_dict(self) -> dict:
        out = {}
        i = 0
        for col in self.col_labels:
            for row in reversed(self.row_labels):
                out[f"{row}{col}"] = {"xy": self.well_positions[i, :]}
                i += 1

        return out

    def add_data(self, ser: pd.Series):
        for index, row in ser.items():
            if index not in self.data_dict:
                raise ValueError(f"'{index}' is not a valid well position. "
                                 f"Ranges are: {self.row_labels}, {self.col_labels}")

            self.data_dict[index][ser.name] = row

    def plot(self, key: str = None, auto_open: bool = True) -> go.Figure:
        layout_figure = {
            "autosize": False,
            "width": int(self.specs["length"] * 10),
            "height": int(self.specs["width"] * 10),
            "plot_bgcolor": "white",
            "showlegend": False
        }

        layout_xaxis = {
            "tickprefix": "<b>",
            "ticksuffix": "</b>",
            "showline": False,
            "ticks": "outside",
            "tickwidth": 0,
            "showgrid": False,
            'zeroline': False,
            'visible': False,
            "range": [-5, 132]
        }

        layout_yaxis = {
            "tickprefix": "<b>",
            "ticksuffix": "</b>",
            "showline": False,
            "ticks": "outside",
            "tickwidth": 0,
            "showgrid": False,
            'zeroline': False,
            'visible': False,
            "range": [-5, 90]
        }

        fig = go.Figure()

        self._draw_outline(fig)
        self._draw_labels(fig)

        if key is not None:
            self._draw_values(fig, key)
        else:
            self._draw_wells(fig)

        fig.update_layout(layout_figure)
        fig.update_xaxes(layout_xaxis)
        fig.update_yaxes(layout_yaxis)

        if auto_open:
            fig.write_html("temp.html", auto_open=True)

        return fig

    def _draw_outline(self, fig: go.Figure):
        """ Adds outline to well plate. """
        x = [0, self.specs["length"], self.specs["length"], 0, 0]
        y = [0, 0, self.specs["width"], self.specs["width"], 0]
        fig.add_trace(
            go.Scatter(x=x, y=y, mode="lines", line={"width": 10, "color": "black"})
        )

    def _draw_wells(self, fig: go.Figure):
        r = self.specs["diameter"] / 2
        kwargs = {'type': self.shape, 'xref': 'x', 'yref': 'y', 'fillcolor': "white",
                  "line": {"color": "black", "width": 4}}
        points = [go.layout.Shape(x0=x - r, y0=y - r, x1=x + r, y1=y + r, **kwargs) for x, y in self.well_positions]
        fig.update_layout(shapes=points)

    def _draw_labels(self, fig: go.Figure):
        self._draw_letters(fig)
        self._draw_numbers(fig)

    def _draw_letters(self, fig: go.Figure):
        if self.number_wells < 100:
            y = self.specs["width"] - (self.specs["width"] - (
                    self.specs["y_off"] + (self.specs["y_space"] * (self.specs["rows"] - 0.5)))) + 0.5
        else:
            y = self.specs["y_off"] + (self.specs["y_space"] * (self.specs["rows"]))

        for i, label in enumerate(self.col_labels):
            x = self.specs["x_off"] + self.specs["x_space"] * i
            fig.add_annotation(x=x, y=y, text=f"<b>{label}</b>", showarrow=False,
                               font={"size": self.specs["font_size"], "family": "Arial", "color": "black"})

    def _draw_numbers(self, fig: go.Figure):
        if self.number_wells < 100:
            x = (self.specs["x_off"] - self.specs["x_space"] / 2) - 1
        else:
            x = self.specs["x_off"] - self.specs["x_space"]
        for i, label in enumerate(reversed(self.row_labels)):
            y = self.specs["y_off"] + self.specs["y_space"] * i
            fig.add_annotation(x=x, y=y, text=f"<b>{label}</b>", showarrow=False,
                               font={"size": self.specs["font_size"], "family": "Arial", "color": "black"})

    def _draw_values(self, fig: go.Figure, key: str):
        heat_map_values = flatten_list(self._get_heatmap_values(key))
        min_value = min([v for v in heat_map_values if v is not None])
        max_value = max([v for v in heat_map_values if v is not None])
        color_map = PlotlyColorMap(min_value, max_value)
        r = self.specs["diameter"] / 2
        kwargs = {'type': self.shape, 'xref': 'x', 'yref': 'y', "line": {"color": "black", "width": 4}}

        points = []
        for (x, y), v in zip(self.well_positions, heat_map_values):
            points.append(go.layout.Shape(x0=x - r, y0=y - r, x1=x + r, y1=y + r, fillcolor=color_map.get(v), **kwargs))

        fig.update_layout(shapes=points)

        # add colorbar
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers",
                                 marker={"colorscale": color_map.colorscale_label, "showscale": True,
                                         "cmin": min_value, "cmax": max_value,
                                         "colorbar": {"title": f"<b>{key}</b>",
                                                      "tickprefix": "<b>", "ticksuffix": "</b>"}}))

    def heatmap(self, key: str, auto_open: bool = True) -> go.Figure:
        z = self._get_heatmap_values(key)

        fig = go.Figure(go.Heatmap(
            x=self.col_labels, y=self.row_labels, z=z, hoverongaps=False
        ))

        layout_figure = {
            "autosize": False,
            "width": int(self.specs["length"] * 10),
            "height": int(self.specs["width"] * 10),
            "font": dict(family="Arial", size=18, color="black"),
            "plot_bgcolor": "white",
            "showlegend": False
        }

        layout_xaxis = {
            "tickprefix": "<b>",
            "ticksuffix": "</b>",
            "showline": True,
            "linecolor": 'black',
            "linewidth": 5,
            "ticks": "outside",
            "tickwidth": 0,
            "showgrid": True,
            "gridwidth": 1,
            "gridcolor": 'lightgray',
            'zeroline': True,
            'side': "top",
            "dtick": 1,

        }

        layout_yaxis = {
            "tickprefix": "<b>",
            "ticksuffix": "</b>",
            "showline": True,
            "linecolor": 'black',
            "linewidth": 5,
            "ticks": "outside",
            "tickwidth": 0,
            "showgrid": True,
            "gridwidth": 1,
            "gridcolor": 'lightgray',
            'zeroline': True,
            "mirror": True,
        }

        fig.update_layout(layout_figure)
        fig.update_xaxes(layout_xaxis)
        fig.update_yaxes(layout_yaxis)

        if auto_open:
            fig.write_html("temp_heatmap.html", auto_open=True)

        return fig

    def _get_heatmap_values(self, key) -> list[list]:
        out = []
        for row in reversed(self.row_labels):
            out_ = []
            for col in self.col_labels:
                well_label = f"{row}{col}"
                well = self.data_dict[well_label]
                if key in well:
                    out_.append(well[key])
                else:
                    out_.append(None)

            out.append(out_)

        return out
