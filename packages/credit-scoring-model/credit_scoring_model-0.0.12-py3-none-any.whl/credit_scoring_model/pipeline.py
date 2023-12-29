# pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

# feature scaling
from sklearn.preprocessing import MinMaxScaler

from credit_scoring_model.config.core import config

# set up the pipeline
credit_scoring_pipe = Pipeline(
    [
        # scale
        ("scaler", MinMaxScaler()),
        (
            "RandomForestClassifier",
            RandomForestClassifier(
                criterion=config.model_config.criterion,
                min_samples_leaf=config.model_config.min_samples_leaf,
                min_samples_split=config.model_config.min_samples_split,
                n_estimators=config.model_config.n_estimators,
            ),
        ),
    ]
)
