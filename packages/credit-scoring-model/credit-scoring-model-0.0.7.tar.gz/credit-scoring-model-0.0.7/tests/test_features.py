import numpy as np

from credit_scoring_model.config.core import config


def test_temporal_variable_transformer(sample_input_data):
    assert sample_input_data["balance"].iat[0] == 49
    assert sample_input_data["housing"].iat[3] == 1.0

    subject = sample_input_data

    # Then
    # test 1
    test_subject_1 = subject["balance"].iat[0]
    assert isinstance(test_subject_1, np.int64)
    assert test_subject_1 == 49

    # test 2
    test_subject_2 = subject["housing"].iat[3]
    assert isinstance(test_subject_2, np.int64)
    assert test_subject_2 == 1.0
