import pandas as pd
import numpy as np

from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt


def colour(row):
    """
    Returns row colors for primary physio vs other physios
    """
    if row["Physio"] == "Primary Physio":
        return "r"
    else:
        return "b"


if __name__ == "__main__":
    filename = "data/processed/physio_fees_clean.csv"
    df = pd.read_csv(filename)

    session_type = CategoricalDtype(
        categories=[
            "initial (45 mins)",
            "standard follow up (30 mins)",
            "long follow up (45 mins)",
            "extended consultation (60 mins)",
            "clinical exercise class (50 mins)",
        ],
        ordered=True,
    )
    df["Category"] = df["Category"].astype(session_type)
    df = df.sort_values("Category")

    # no. of entries for each category, in sorted order
    category_n = [10, 11, 4, 7, 4]

    # Generate x scatter values for each point
    xs = list()

    for i, n in enumerate(category_n):
        xs.extend(list(np.random.normal(i + 1, 0.04, n)))

    # Append x scatter values to table
    df["xs"] = xs
    # Add color column
    df["colour"] = df.apply(lambda row: colour(row), axis=1)

    # Generate boxplot
    bxplt = df.boxplot(
        column=["Standardised Fee ($)"],
        by=["Category"],
        figsize=(11.75, 8.25),
        grid=True,
        rot=25,
        showmeans=True,
        showfliers=False,
    )
    bxplt.set(title="", xlabel="Session Type", ylabel="Adjusted Cost ($)")

    plt.suptitle("")
    plt.yticks(np.arange(0, 250, 25))
    plt.scatter(df["xs"], df["Standardised Fee ($)"], alpha=0.4, c=df["colour"])

    plt.savefig(
        'figures/physio_fees_boxplot_grid.png',
        dpi=300,
        format='png',
        facecolor='White',
        transparent=False,
    )