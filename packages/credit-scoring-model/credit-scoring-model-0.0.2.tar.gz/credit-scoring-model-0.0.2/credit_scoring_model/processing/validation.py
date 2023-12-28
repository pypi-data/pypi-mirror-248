import re
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, ValidationError

from credit_scoring_model.config.core import config


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    input_data["age"] = input_data["age"].astype("int")
    input_data["job"] = input_data["job"].astype("str")
    input_data["marital"] = input_data["marital"].astype("str")
    input_data["education"] = input_data["education"].astype("str")
    input_data["default"] = input_data["default"].astype("str")
    input_data["balance"] = input_data["balance"].astype("int")
    input_data["housing"] = input_data["housing"].astype("str")
    input_data["loan"] = input_data["loan"].astype("str")
    input_data["contact"] = input_data["contact"].astype("str")
    input_data["day"] = input_data["day"].astype("int")
    input_data["month"] = input_data["month"].astype("str")
    input_data["duration"] = input_data["duration"].astype("int")
    input_data["campaign"] = input_data["campaign"].astype("int")
    input_data["pdays"] = input_data["pdays"].astype("int")
    input_data["previous"] = input_data["previous"].astype("int")
    input_data["poutcome"] = input_data["poutcome"].astype("str")
    relevant_data = input_data[config.model_config.features].copy()

    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleCreditScoringInputs(inputs=relevant_data.replace({np.nan: None}).to_dict(orient="records"))
    except ValidationError as error:
        errors = error.json()

    return relevant_data, errors


class CreditScoringInputSchema(BaseModel):
    age: Optional[np.float64] = Field(None, alias="age")
    job: Optional[np.float64] = Field(None, alias="job")
    marital: Optional[np.float64] = Field(None, alias="marital")
    education: Optional[np.float64] = Field(None, alias="education")
    default: Optional[np.float64] = Field(None, alias="default")
    balance: Optional[np.float64] = Field(None, alias="balance")
    housing: Optional[np.float64] = Field(None, alias="housing")
    loan: Optional[np.float64] = Field(None, alias="loan")
    contact: Optional[np.float64] = Field(None, alias="contact")
    day: Optional[np.float64] = Field(None, alias="day")
    month: Optional[np.float64] = Field(None, alias="month")
    duration: Optional[np.float64] = Field(None, alias="duration")
    campaign: Optional[np.float64] = Field(None, alias="campaign")
    pdays: Optional[np.float64] = Field(None, alias="pdays")
    previous: Optional[np.float64] = Field(None, alias="previous")
    poutcome: Optional[np.float64] = Field(None, alias="poutcome")


class MultipleCreditScoringInputs(BaseModel):
    inputs: List[CreditScoringInputSchema]
