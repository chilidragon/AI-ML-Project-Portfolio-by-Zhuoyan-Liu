import logging
from sklearn.metrics import roc_auc_score, accuracy_score, confusion_matrix, classification_report
import yaml

logger = logging.getLogger('heartattack')

def evaluate_performance(scores: dict[str, any], config: dict[str, any]) -> dict[str, any]:
    """
    Evaluate model performance based on various metrics.

    Args:
        scores (Dict[str, Any]): Dictionary containing actual values, probabilities, and binary predictions.
        config (Dict[str, Any]): Configuration dictionary that may specify which metrics to calculate.

    Returns:
        Dict[str, Any]: A dictionary containing computed performance metrics.
    """
    try:
        y_test = scores['actual_values']
        y_pred_proba = scores['probabilities']
        y_pred_bin = scores['binary_predictions']
        metrics_config = config.get('metrics', [])

        metrics = {}
        if 'auc' in metrics_config:
            metrics['auc'] = roc_auc_score(y_test, y_pred_proba)
        if 'accuracy' in metrics_config:
            metrics['accuracy'] = accuracy_score(y_test, y_pred_bin)
        if 'confusion' in metrics_config:
            metrics['confusion_matrix'] = confusion_matrix(y_test, y_pred_bin)
        if 'classification_report' in metrics_config:
            metrics['classification_report'] = classification_report(y_test, y_pred_bin, output_dict=True)

        return metrics

    except Exception as e:
        logger.error('Failed to evaluate performance metrics: %s', str(e))
        raise


def save_metrics(metrics: dict[str, any], save_path: str) -> None:
    """
    Save the computed metrics to a YAML file.

    Args:
        metrics (dict): A dictionary containing performance metrics.
        save_path (Path): The path where the metrics file will be saved.
    """
    try:
        # Ensure the directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)
        # Write metrics to a YAML file
        with open(save_path, 'w') as file:
            yaml.dump(metrics, file, default_flow_style=False)

    except Exception as e:
        logger.error('Failed to save metrics to %s: %s', save_path, str(e))
        raise
