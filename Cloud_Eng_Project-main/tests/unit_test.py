import pytest
import pandas as pd

import src.generate_features as gf

def test_generate_features_happy():
    # Create a sample DataFrame
    data = {
        'feature1': [10, 20, 30],
        'feature2': [20, 30, 40]
    }
    df = pd.DataFrame(data)

    # Configuration for features to scale
    config = {'features': ['feature1', 'feature2']}

    # Expected DataFrame after applying StandardScaler
    expected_data = {
        'feature1': [-1.22474487, 0., 1.22474487],
        'feature2': [-1.22474487, 0., 1.22474487]
    }
    expected_df = pd.DataFrame(expected_data)

    # Apply the function
    result_df = gf.generate_features(df, config)

    # Assert that the result is as expected
    pd.testing.assert_frame_equal(result_df, expected_df)

def test_generate_features_unhappy():
    # Create a sample DataFrame with non-numeric type
    data = {
        'feature1': ['a', 'b', 'c'],  # Non-numeric values
        'feature2': [20, 30, 40]
    }
    df = pd.DataFrame(data)

    # Configuration for features to scale
    config = {'features': ['feature1', 'feature2']}

    # Expect ValueError due to non-numeric type in 'feature1'
    with pytest.raises(ValueError):
        gf.generate_features(df, config)
