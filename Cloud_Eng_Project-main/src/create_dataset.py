import logging
import sys
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

logger = logging.getLogger('heartattack')

def create_dataset(file_path: str, config: dict) -> pd.DataFrame:
    """
    Reads the raw data file and processes it according to the provided configurations.

    Args:
        file_path (str): The path to the raw data file.
        config (dict): Configuration details for data processing.

    Returns:
        pd.DataFrame: The processed dataset.
    """
    # Load data
    df = pd.read_csv(file_path)

    # Remove specified columns
    df.drop(columns=config['remove_columns'], inplace=True)

    # Encode categorical variables with custom mappings
    for col, mapping in config['encode_categorical'].items():
        df[col + '_encoded'] = df[col].map(mapping['mapping'])
        df.drop(col, axis=1, inplace=True)

    # Split and encode columns
    for col, details in config['encode_and_split'].items():
        new_cols = df[col].str.split(details['separator'], expand=True)
        df[details['new_columns']] = new_cols
        df[details['new_columns']] = df[details['new_columns']].astype(int)
        df.drop(col, axis=1, inplace=True)

    # One-hot encoding
    encoder = OneHotEncoder(sparse_output=False)
    encoded_cols = encoder.fit_transform(df[config['one_hot_encode']])
    encoded_df = pd.DataFrame(encoded_cols, columns=encoder.get_feature_names_out(config['one_hot_encode']))
    df = pd.concat([df, encoded_df], axis=1)
    df.drop(config['one_hot_encode'], axis=1, inplace=True)

    return df

def save_dataset(df: pd.DataFrame, save_path: str) -> None:
    """
    Saves the DataFrame to a CSV file. This method provides a way to store the processed
    data which can be later used for further processing or analysis.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        save_path (str): The path where the CSV file will be saved.
    """
    try:
        df.to_csv(save_path, index=False)
        logger.info('Dataset saved to %s', save_path)
    except IOError as e:
        logger.error('Failed to save data to %s: %s', save_path, e)
        sys.exit(1)
    except pd.errors.EmptyDataError as e:
        logger.error('No data to save to %s: %s', save_path, e)
        sys.exit(1)
