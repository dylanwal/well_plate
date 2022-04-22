
import pandas as pd

import well_plate


def main():
    # Image 1
    wp = well_plate.WellPlate(24)
    fig = wp.plot(auto_open=False)
    fig.write_image("well_plate_24.svg")

    # Image 2
    wp = well_plate.WellPlate(96, "rect")
    fig = wp.plot(auto_open=False)
    fig.write_image("well_plate_96r.svg")

    # Image 3
    wp = well_plate.WellPlate(384)

    df = pd.read_csv("example1_data.csv", index_col=0)
    wp.add_data(df["mw_n"])

    fig = wp.plot(key="mw_n", auto_open=False)
    fig.write_image("well_plate_with_data.svg")
    fig = wp.heatmap(key="mw_n", auto_open=False)
    fig.write_image("heatmap.svg")


if __name__ == '__main__':
    main()
