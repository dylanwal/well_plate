
import pandas as pd

import well_plate


def main():
    import os
    print(os.getcwd())
    df = pd.read_csv("example1_data.csv", index_col=0)
    print(df.head())

    wp = well_plate.WellPlate(384)

    wp.plot()
    wp.add_data(df["mw_n"])
    wp.plot(key="mw_n")
    wp.heatmap(key="mw_n")

    print(wp)


if __name__ == '__main__':
    main()
