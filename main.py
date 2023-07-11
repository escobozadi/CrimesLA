"""
    Data Analysis Course Project
Analysing DataFrame: Crimes in LA from 2020 to July 2023
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def data_tables(path, mo_code=None):
    df = pd.DataFrame(pd.read_csv(path))
    if mo_code:
        df2 = pd.DataFrame(pd.read_csv(mo_code, index_col=0))
    else:
        df2 = None

    df["Date Rptd"] = pd.to_datetime(df["Date Rptd"], format='%m/%d/%Y %H:%M:%S %p')
    df["DATE OCC"] = pd.to_datetime(df["Date Rptd"])

    # Victims Descent/Race Codes and Values
    df3 = pd.DataFrame({"Descent Code": ["A", "B", "C", "D", "F", "G", "H",
                                         "I", "J", "K", "L", "O", "P", "S",
                                         "U", "V", "W", "X", "Z"],
                        "Description": ["Other Asian", "Black", "Chinese",
                                        "Cambodian", "Filipino", "Guamanian",
                                        "Hispanic/Latin/Mexican", "American Indian/Alaskan Native",
                                        "Japanese", "Korean", "Laotian", "Other", "Pacific Islander",
                                        "Samoan", "Hawaiian", "Vietnamese", "White", "Unknown",
                                        "Asian Indian"]})

    return df, df2, df3


def format_mocodes(path):
    # Formatting MO_CODES_Numerical_20191119.csv
    motives = pd.DataFrame(pd.read_csv(path, header=0, names=["code", "modus operandi",
                                                              "further description", "victim"]))

    # Separating T/C - 'Description' into two columns
    tmp = motives.loc[motives["modus operandi"].str.startswith("T/C"), "modus operandi"]    # locating rows with T/C
    # Keeping T/C on column 'modus operandi'
    motives.loc[motives["modus operandi"].str.startswith("T/C"), "modus operandi"] = "T/C"
    # Moving 'Description' into 'further description column
    if list(tmp) != list(motives.loc[motives["modus operandi"].str.startswith("T/C"), "modus operandi"]):
        motives.loc[motives["modus operandi"].str.startswith("T/C"), "further description"] = tmp.str[5:]

    # Separating SSI - 'Description' into two columns
    tmp = motives.loc[motives["modus operandi"].str.startswith("SSI"), "modus operandi"]
    motives.loc[motives["modus operandi"].str.startswith("SSI"), "modus operandi"] = "SSI"
    if list(tmp) != list(motives.loc[motives["modus operandi"].str.startswith("SSI"), "modus operandi"]):
        motives.loc[motives["modus operandi"].str.startswith("SSI"), "further description"] = tmp.str[5:]

    # Adding new column, True/False whether the description mentions there's a victim
    motives["victim"] = motives["modus operandi"].str.contains("Victim|victim|victims|Victims|vict|Vict")

    # victim = motives["modus operandi"].str.contains(["Victim|victim|victims|Victims|vict|Vict"])
    # suspect = motives["modus operandi"].str.contains(["Suspect|suspect|Susp|susp|susps"])
    # motives["vict/susp"] = list(map(lambda x: x.contains("Victim"), motives["modus operandi"]))
    motives.to_csv(path)

    return


class Visualizations(object):

    def __init__(self, crime_df, mo_codes_df, descent_df):
        self.crime_df = crime_df
        self.mo_codes = mo_codes_df
        self.descent_df = descent_df

    def gender_race(self):
        victims_sex = self.crime_df["Vict Sex"].value_counts()

        victim_descent = pd.merge(self.crime_df, self.descent_df, how="left",
                                  left_on="Vict Descent", right_on="Descent Code")[["Descent Code", "Description"]]
        victims_descent = victim_descent["Description"].value_counts()

        fig, (ax, ax2) = plt.subplots(1, 2, subplot_kw=dict(aspect="equal"))
        # ax.pie(victims_sex.values[:-2],
        #        labels=["Male", "Female", "Unknown"],
        #        autopct=lambda pct: viz.chart_percentage(pct, victims_sex.values[:-2]))
        wedges, _, autotexts = ax.pie(victims_sex.values[:-2],
                                      autopct=lambda p: "{:.1f}% \n ({:d})".format(p, int(p * np.sum(
                                          victims_sex.values[:-2]) / 100)),
                                      explode=[0.01, 0.01, 0.01])

        wedges2, _, autotexts2 = ax2.pie(victims_descent.values,
                                         autopct=lambda p: "{:.1f}% \n ({:d})".format(p, int(p * np.sum(
                                             victims_descent.values) / 100)) if p > 5 else None)

        ax.legend(wedges, ["Male", "Female", "Unknown"], title="Victim Gender",
                  loc="upper right", bbox_to_anchor=(0, 1))
        ax2.legend(wedges2, labels=victims_descent.keys(), title="Victim Descent/Race",
                   loc="upper left", bbox_to_anchor=(0.9, 1),
                   fontsize="5")

        ax.set_title("Gender of Victim")
        ax2.set_title("Descent/Race of Victim")

        plt.setp(autotexts, size=8, weight="bold")
        plt.setp(autotexts2, size=6, weight="bold")
        plt.show()

        return

    def map_locations(self):
        # Mapping crime locations in LA map image
        df = self.crime_df
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

    @staticmethod
    def chart_percentage(pct, values):
        # function to add the percentages & total to charts
        val = int(np.round(pct/100.*np.sum(values)))
        return f"{pct:.1f}% \n ({val:d})"


if __name__ == '__main__':
    # DataFrame: Crimes in LA from 2020 to July 2023.     752910 entries
    file_path = "~/Documents/BedTracks/git_test/Crime_Data_from_2020_to_Present.csv"
    mo_codes = "~/Documents/BedTracks/git_test/MO_CODES_Numerical_20191119.csv"
    # Format csv of MO CODES
    # format_mocodes(mo_codes)

    # Read CSVs
    dataframe, modus_operandi, descent = data_tables(file_path, mo_codes)
    viz = Visualizations(dataframe, modus_operandi, descent)

    pd.set_option("display.max_columns", len(dataframe))
    print(dataframe.head())
    # print(modus_operandi.head())
    # print(descent)

    print(dataframe["Weapon Desc"].value_counts())
    print(dataframe["Weapon Desc"].value_counts().keys()[:10])
    print(list(dataframe["Weapon Desc"].value_counts())[:10])
    print(sum(list(dataframe["Weapon Desc"].value_counts())[11:]))

    # pd.set_option("display.max_columns", len(dataframe))
    # print(dataframe.head())
    # map_locations(dataframe)
    # pd.reset_option("display.max_columns")

