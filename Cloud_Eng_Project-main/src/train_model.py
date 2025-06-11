import logging
from pathlib import Path
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger('heartattack')

def train_model(df: pd.DataFrame, config: dict) -> tuple:
    """
    Trains the RandomForest model based on provided configurations and returns
    both the model and train/test datasets.

    Args:
        df (pd.DataFrame): The full dataset from which to extract features and target.
        config (dict): Configuration dict that includes settings for model training.

    Returns:
        tuple: Tuple containing the trained model, training set, and testing set.
    """
    logging.info('Starting model training process.')

    # Extract target and features based on config
    target_column = config['get_target']['target']
    feature_columns = config['choose_features']['features_to_use']
    test_size = config['split_data']['test_size']
    random_state = config['parameters'].get('random_state', None)  # Optional

    # Splitting the data
    logging.info('Splitting data into train and test datasets.')
    x_train, x_test, y_train, y_test = train_test_split(
        df[feature_columns], df[target_column], test_size=test_size, random_state=random_state
    )

    # Model training
    model_params = config.get('parameters', {})
    model = RandomForestClassifier(**model_params)
    model.fit(x_train, y_train)
    logging.info('Model training completed.')

    # Concatenate features with their respective targets for returning datasets
    train_set = pd.concat([x_train, y_train], axis=1)
    test_set = pd.concat([x_test, y_test], axis=1)

    return model, train_set, test_set

def save_data(train: pd.DataFrame, test: pd.DataFrame, artifacts_path: Path) -> tuple:
    """
    Saves the training and testing datasets to specified paths.

    Args:
        train (pd.DataFrame): Training dataset to save.
        test (pd.DataFrame): Testing dataset to save.
        artifacts_path (Path): Base path where the datasets should be saved.
    """
    logging.info('Saving training and testing datasets.')
    train_path = artifacts_path / 'train.csv'
    test_path = artifacts_path / 'test.csv'
    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)
    logging.info('Training data saved to %s', train_path)
    logging.info('Testing data saved to %s', test_path)
    return train_path, test_path

def save_model(model, path: Path):
    """
    Saves the trained model to disk.

    Args:
        model: Trained model to be saved.
        path (Path): Path where the model should be saved.
    """
    logging.info('Saving model to %s', path)
    path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    joblib.dump(model, path)
    logging.info('Model saved successfully at %s', path)
    return path
