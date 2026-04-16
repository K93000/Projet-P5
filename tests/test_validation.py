import sys 
import os 
import pandas as pd
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from migration import validate_data


def test_columns_cleaning():
    df = pd.DataFrame({
        "Name": ["john doe"],
        "Age": [30],
        "Gender": ["male"],
        "Blood Type": ["a+"],
        "Medical Condition": ["cancer"],
        "Date of Admission": ["2024-01-01"],
        "Doctor": ["dr smith"],
        "Hospital": ["city hospital"],
        "Insurance Provider": ["axa"],
        "Billing Amount": [1000]
    })

    df_clean = validate_data(df)

    assert "Blood_Type" in df_clean.columns
    assert "Date_of_Admission" in df_clean.columns


def test_missing_column():
    df = pd.DataFrame({
        "Name": ["john doe"]
        # volontairement incomplet
    })

    with pytest.raises(ValueError):
        validate_data(df)


def test_date_conversion():
    df = pd.DataFrame({
        "Name": ["john doe"],
        "Age": [30],
        "Gender": ["male"],
        "Blood Type": ["a+"],
        "Medical Condition": ["cancer"],
        "Date of Admission": ["invalid_date"],
        "Doctor": ["dr smith"],
        "Hospital": ["city hospital"],
        "Insurance Provider": ["axa"],
        "Billing Amount": [1000]
    })

    df_clean = validate_data(df)

    # La ligne doit être supprimée car date invalide
    assert df_clean.empty