import logging
from pathlib import Path

import numpy as np
import pandas as pd
from config.core import LOG_DIR, DATASET_DIR, config
from imblearn.over_sampling import RandomOverSampler
from pipeline import credit_scoring_pipe
from processing.data_manager import load_train_dataset, save_pipeline
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from credit_scoring_model import __version__ as _version


def run_training() -> None:
    """Train the model."""
    # Update logs
    log_path = Path(f"{LOG_DIR}/log_{_version}.log")
    if Path.exists(log_path):
        log_path.unlink()
    logging.basicConfig(filename=log_path, level=logging.DEBUG)

    # read training data
    data = load_train_dataset(file_name=config.app_config.data_file_train)

    print(data)
    data["age"] = data["age"].astype("int")
    data["job"] = data["job"].astype("object")
    data["marital"] = data["marital"].astype("object")
    data["education"] = data["education"].astype("object")
    data["default"] = data["default"].astype("object")
    data["balance"] = data["balance"].astype("int")
    data["housing"] = data["housing"].astype("object")
    data["loan"] = data["loan"].astype("object")
    data["contact"] = data["contact"].astype("object")
    data["day"] = data["day"].astype("int")
    data["month"] = data["month"].astype("object")
    data["duration"] = data["duration"].astype("int")
    data["campaign"] = data["campaign"].astype("int")
    data["pdays"] = data["pdays"].astype("int")
    data["previous"] = data["previous"].astype("int")
    data["poutcome"] = data["poutcome"].astype("object")

    lst = ["job", "marital", "education", "default", "housing", "housing", "loan", "contact", "month", "poutcome", "y"]

    le = LabelEncoder()

    for i in lst:
        data[i] = le.fit_transform(data[i])

    x = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    sm = RandomOverSampler()
    x, y = sm.fit_resample(x, y)

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        x,  # predictors
        y,
        test_size=config.model_config.test_size,
        random_state=config.model_config.random_state,
    )

    # fit model
    credit_scoring_pipe.fit(X_train, y_train)

    # make predictions for train set
    pred = credit_scoring_pipe.predict(X_train)

    mse_train = mean_squared_error(y_train, pred)
    rmse_train = np.sqrt(mse_train)

    print(f"train RMSE: {rmse_train}")
    print()

    logging.info(f"train RMSE: {rmse_train}")

    # make predictions for test set
    pred = credit_scoring_pipe.predict(X_test)

    # determine test accuracy and roc-auc
    mse_test = mean_squared_error(y_test, pred)
    rmse_test = np.sqrt(mse_test)

    print(f"test RMSE: {rmse_test}")
    print()

    logging.info(f"test RMSE: {rmse_test}")

    # persist trained model
    save_pipeline(pipeline_to_persist=credit_scoring_pipe)

    X_train.to_csv(f'{DATASET_DIR}/xtrain.csv', index=False)
    X_test.to_csv(f'{DATASET_DIR}/xtest.csv', index=False)

    y_train.to_csv(f'{DATASET_DIR}/ytrain.csv', index=False)
    y_test.to_csv(f'{DATASET_DIR}/ytest.csv', index=False)


if __name__ == "__main__":
    run_training()
