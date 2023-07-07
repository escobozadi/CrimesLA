"""
    Data Analysis Course Project
Analysing DataFrame: Crimes in LA from 2020 to July 2023
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def format_file(path):
    df = pd.DataFrame(pd.read_csv(path))

    df["Date Rptd"] = pd.to_datetime(df["Date Rptd"], format='%m/%d/%Y %H:%M:%S %p')
    df["DATE OCC"] = pd.to_datetime(df["Date Rptd"])
    return df


def map_locations(df):
    # Mapping crime locations in LA map image
    box = (df.LON.min(), df.LON[df.LON != 0].max(),
           df.LAT[df.LAT != 0].min(), df.LAT.max())
    print(box)

    map_img = plt.imread("/Users/dianaescoboza/Documents/BedTracks/git_test/map.png")
    fig, ax = plt.subplots(figsize=(8, 7))

    ax.scatter(df.LON[df.LON != 0], df.LAT[df.LAT != 0],
               zorder=1, alpha=0.1, c='b', s=0.8)
    ax.set_title("Location of Crimes in LA from 2020 to July 2023")
    ax.set_xlim(box[0], box[1])
    ax.set_ylim(box[2], box[3])

    ax.imshow(map_img, zorder=0, extent=box, aspect='equal')
    plt.show()

    return


if __name__ == '__main__':
    # DataFrame: Crimes in LA from 2020 to July 2023
    # 752910 entries
    file_path = "~/Documents/BedTracks/git_test/Crime_Data_from_2020_to_Present.csv"
    dataframe = format_file(file_path)

    pd.set_option("display.max_columns", len(dataframe))
    print(dataframe.head())
    map_locations(dataframe)
    pd.reset_option("display.max_columns")

