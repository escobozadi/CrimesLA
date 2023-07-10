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


def format_mocodes(path):
    # Formatting MO_CODES_Numerical_20191119.csv
    motives = pd.DataFrame(pd.read_csv(path, header=0, names=["code", "modus operandi", "further description"]))

    # Separating T/C - 'Description' into two columns
    tmp = motives.loc[motives["modus operandi"].str.startswith("T/C"), "modus operandi"]    # locating rows with T/C
    # Keeping T/C on column 'modus operandi'
    motives.loc[motives["modus operandi"].str.startswith("T/C"), "modus operandi"] = "T/C"
    # Moving 'Description' into 'further description column
    motives.loc[motives["modus operandi"].str.startswith("T/C"), "further description"] = tmp.str[5:]

    # Separating SSI - 'Description' into two columns
    tmp = motives.loc[motives["modus operandi"].str.startswith("SSI"), "modus operandi"]
    motives.loc[motives["modus operandi"].str.startswith("SSI"), "modus operandi"] = "SSI"
    motives.loc[motives["modus operandi"].str.startswith("SSI"), "further description"] = tmp.str[5:]

    # Adding new column, True/False whether the description mentions there's a victim
    motives["victim"] = motives["modus operandi"].str.contains("Victim|victim|victims|Victims|vict|Vict")

    # victim = motives["modus operandi"].str.contains(["Victim|victim|victims|Victims|vict|Vict"])
    # suspect = motives["modus operandi"].str.contains(["Suspect|suspect|Susp|susp|susps"])
    # motives["vict/susp"] = list(map(lambda x: x.contains("Victim"), motives["modus operandi"]))
    motives.to_csv(path)

    return


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
    mo_codes = "~/Documents/BedTracks/git_test/MO_CODES_Numerical_20191119.csv"
    # dataframe = format_file(file_path)

    # MO CODES
    format_mocodes(mo_codes)
    # print(motives)

    # pd.set_option("display.max_columns", len(dataframe))
    # print(dataframe.head())
    # map_locations(dataframe)
    # pd.reset_option("display.max_columns")

