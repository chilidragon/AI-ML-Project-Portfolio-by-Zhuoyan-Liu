import logging
import pandas as pd
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger('heartattack')

def generate_features(df: pd.DataFrame, config: dict[str, any]) -> pd.DataFrame:
    """
    Transforms a DataFrame according to specified operations in the config dictionary.
    This function performs log transformations, multiplications, and normalization of ranges
    based on the configuration provided.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be transformed.
        config (dict): A dictionary containing configuration details for various transformations.

    Returns:
        pd.DataFrame: The DataFrame with the applied transformations.

    Raises:
        KeyError: If the specified column keys are not found in the DataFrame or the config dictionary.
        ValueError: If any numerical operations result in undefined or infinite values.
    """
    try:
        # Check if the specified features are present in the DataFrame
        if not set(config['features']).issubset(df.columns):
            raise KeyError('One or more specified features are not present in the DataFrame.')

        # Check if the data types of the features are numeric
        numeric_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        non_numeric_features = [feature for feature in config['features'] if df[feature].dtype not in numeric_types]

        if non_numeric_features:
            logger.error('Non-numeric features found: %s. StandardScaler requires numeric types.', non_numeric_features)
            raise ValueError('All features must be numeric to apply StandardScaler.')

        # Apply StandardScaler to the specified features
        scaler = StandardScaler()
        df[config['features']] = scaler.fit_transform(df[config['features']])
        logging.info('StandardScaler applied successfully to the features.')
    except Exception as e:
        logger.error('An error occurred: %s', e)
        raise e

    return df
