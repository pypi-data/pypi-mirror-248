import numpy as np
import pandas as pd

from credit_scoring_model.predict import make_prediction
from sklearn.preprocessing import MinMaxScaler

def test_make_prediction(sample_input_data):
    # Given
    expected_shape = (800, 16)

    scaler = MinMaxScaler()

    scaler.fit(sample_input_data)

    sample_input_data = pd.DataFrame(
        scaler.transform(sample_input_data),
        columns=sample_input_data.columns
    )

    # When
    result = make_prediction(input_data=sample_input_data)
    # Then
    preds = result.get("preds")
    probs = result.get("probs")

    assert isinstance(preds, list)
    assert isinstance(preds[0], np.int32)
    assert isinstance(probs[0], np.float64)
    assert result.get("errors") is None
    assert len(preds) == len(probs) == expected_shape[0]
