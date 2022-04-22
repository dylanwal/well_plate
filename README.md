# Well Plate (well_plate)

---
---
![PyPI](https://img.shields.io/pypi/v/well_plate)
![downloads](https://img.shields.io/pypi/dm/well_plate)
![license](https://img.shields.io/github/license/dylanwal/well_plate)

Makes nice visualizations of well plates!


---

## Installation

```
pip install well-plate
```

## Dependencies

[numpy](https://github.com/numpy/numpy)
[pandas](https://github.com/pandas-dev/pandas)
[plotly](https://github.com/plotly/plotly.py)

---
---

## Example

```python
    import well_plate

    wp = well_plate.WellPlate(24)
    wp.plot()
```
![well_plate](https://github.com/dylanwal/well_plate/tree/master/examples/well_plate_24.svg)

```python
    import well_plate

    wp = well_plate.WellPlate(96, "rect")
    wp.plot()
```
![well_plate](https://github.com/dylanwal/well_plate/tree/master/examples/well_plate_96r.svg)

```python
    import pandas as pd    
    import well_plate

    wp = well_plate.WellPlate(384, "rect")
    
    df = pd.read_csv("example1_data.csv", index_col=0)
    wp.add_data(df["mw_n"])
    
    wp.plot(key="mw_n")
    wp.heatmap(key="mw_n")
```
![well_plate](https://github.com/dylanwal/well_plate/tree/master/examples/well_plate_with_data.svg)
![well_plate](https://github.com/dylanwal/well_plate/tree/master/examples/heatmap.svg)
