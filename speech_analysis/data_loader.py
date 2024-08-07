import os
import pandas as pd


def load_data(data_path: str) -> dict[str, dict[str, pd.DataFrame]]:
    """
    Load validated data for each language and split by gender.

    Args:
        data_path (str): The path to the main data directory.

    Returns:
        dict[str, dict[str, pd.DataFrame]]: A dictionary with language codes as keys and another dictionary
                                            containing DataFrames for male and female speakers as values.
    """
    languages = [
        d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))
    ]
    data = {}

    for language in languages:
        validated_path = os.path.join(data_path, language, "validated.tsv")
        if os.path.exists(validated_path):
            df = pd.read_csv(
                validated_path, sep="\t", usecols=["path", "gender", "locale"]
            )
            male_df = df[df["gender"] == "male_masculine"]
            female_df = df[df["gender"] == "female_feminine"]
            data[language] = {"male": male_df, "female": female_df}

    return data
