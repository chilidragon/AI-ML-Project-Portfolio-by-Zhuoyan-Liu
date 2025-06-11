import logging
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger('heartattack')

def score_model(test: pd.DataFrame, model: RandomForestClassifier,
                config: dict[str, dict[str, list[str]]]) -> dict[str, pd.Series]:
    """
    Generates scores for a trained model on the test dataset. The function produces both
    probability predictions for a positive class and binary class predictions.

    Args:
        test (pd.DataFrame): Test dataset that includes both features and the target.
        model (RandomForestClassifier): Trained machine learning model.
        config (dict): Configuration dict that specifies which features to use.

    Returns:
        dict: A dictionary containing the model's probability and binary predictions.
    """
    # Extract features based on the config
    try:
        feature_columns = config['choose_features']['features_to_use']

        # Generate predictions
        y_pred_proba_test = model.predict_proba(test[feature_columns])[:, 1]  # Probability of class 1
        y_pred_bin_test = model.predict(test[feature_columns])

        # Package results
        scores = {
            'probabilities': y_pred_proba_test,
            'binary_predictions': y_pred_bin_test,
            'actual_values': test['Heart Attack Risk']
        }

        return scores

    except Exception as e:
        logger.error('Failed to score model: %s', str(e))
        raise


def save_scores(scores: dict[str, pd.Series], save_path: str) -> None:
    """
    Saves the model scores to a CSV file.

    Args:
        scores (dict): A dictionary containing scoring arrays such as probabilities
                       and binary predictions.
        save_path (Path): The path where the scores CSV will be saved.
    """
    # Convert the scores dictionary to a DataFrame
    try:
        scores_df = pd.DataFrame(scores)

        # Ensure the directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Save the DataFrame to a CSV file
        scores_df.to_csv(save_path, index=False)

    except Exception as e:
        logger.error('Failed to save scores to %s: %s', save_path, str(e))
        raise
