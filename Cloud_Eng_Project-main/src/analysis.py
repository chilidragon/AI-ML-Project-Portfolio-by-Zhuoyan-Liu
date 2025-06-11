import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger("heartattack")

def save_figures(data: pd.DataFrame, save_dir: Path) -> list[Path]:
    """
    Generates and saves statistical visualizations of the data to the specified directory.
    Currently supports histograms for all numeric columns.

    Args:
        data (pd.DataFrame): The dataset to visualize.
        save_dir (Path): The directory to save the generated figure files.

    Returns:
        list[Path]: A list of paths where the figures are saved.

    """
    saved_paths = []
    for column in data.select_dtypes(include=["number"]).columns:
        plt.figure()
        data[column].hist()
        plt.title(f"Histogram of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")

        # Define the path for saving the figure
        figure_path = save_dir / f"{column}_histogram.png"
        plt.savefig(figure_path)
        plt.close()

        # Log and collect the saved path
        logger.info("Figure saved to %s", figure_path)
        saved_paths.append(figure_path)

    return saved_paths
