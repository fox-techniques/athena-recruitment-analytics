"""
Module for Processing and Mapping Applicants' Data

This module provides functions to handle missing data, predict mappings using 
zero-shot classification, and enhance recruitment and applicants datasets by adding relevant fields 
(e.g., industry, field, status levels). It also includes utilities for introducing 
missing values for testing purposes.

Directories:
    - MAPPING_DIR: Directory containing mapping files in JSON format.

Functions:
    - find_missing_companies: Identify companies missing from the company-industry mapping.
    - find_missing_positions: Identify positions missing from the position-field mapping.
    - predict_missing_company_industry: Predict missing company-industry mappings.
    - predict_missing_position_field: Predict missing position-field mappings.
    - add_industry_and_field: Add "Industry" and "Field" columns to the dataset.
    - add_suffix_to_cross_column_duplicates: Add suffixes to duplicate values across columns.
    - add_missing_values: Introduce missing values (NaNs) into specific columns.
    - extend_status_levels: Expand application statuses into multiple levels.
"""

import os
import re
import json
import pandas as pd
import numpy as np
from transformers import pipeline
from src.data_loader import load_status_mapping

# Directory for mapping files
MAPPING_DIR = "./data/mappings"


def find_missing_companies(raw_data_df, company_industry_mapping):
    """
    Identify companies that are missing from the company-industry mapping.

    Args:
        raw_data_df (pd.DataFrame): DataFrame containing jobhunt data.
        company_industry_mapping (dict): Existing mapping of companies to industries.

    Returns:
        list: List of companies that are missing from the mapping.
    """
    unique_companies = raw_data_df["Company"].unique()
    available_companies = set(company_industry_mapping.keys())
    missing_companies = [
        company for company in unique_companies if company not in available_companies
    ]
    return missing_companies


def find_missing_positions(raw_data_df, position_field_mapping):
    """
    Identify positions that are missing from the position-field mapping.

    Args:
        raw_data_df (pd.DataFrame): DataFrame containing jobhunt data.
        position_field_mapping (dict): Existing mapping of positions to fields.

    Returns:
        list: List of positions that are missing from the mapping.
    """
    unique_positions = raw_data_df["Position"].unique()
    available_positions = set(position_field_mapping.keys())
    missing_positions = [
        position for position in unique_positions if position not in available_positions
    ]
    return missing_positions


def predict_missing_company_industry(company_names, company_industry_mapping):
    """
    Predict industries for companies missing in the company-industry mapping.

    Args:
        company_names (list): List of company names to predict industries for.
        company_industry_mapping (dict): Existing mapping of companies to industries.

    Returns:
        dict: Updated company-industry mapping with predictions.
    """
    industries = list(set(company_industry_mapping.values()))
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    updated_mapping = company_industry_mapping.copy()

    for company in company_names:
        clean_company_name = re.sub(r"\sx\d+$", "", company)
        if clean_company_name not in updated_mapping:
            result = classifier(clean_company_name, industries)
            predicted_industry = result["labels"][0]
            print(f"Predicted industry for {clean_company_name}: {predicted_industry}")
            updated_mapping[clean_company_name] = predicted_industry

    updated_filepath = os.path.join(MAPPING_DIR, "company_industry.json")
    with open(updated_filepath, "w") as file:
        json.dump(updated_mapping, file, indent=4, sort_keys=True)
    return updated_mapping


def predict_missing_position_field(job_positions, position_field_mapping):
    """
    Predict fields for positions missing in the position-field mapping.

    Args:
        job_positions (list): List of job positions to predict fields for.
        position_field_mapping (dict): Existing mapping of positions to fields.

    Returns:
        dict: Updated position-field mapping with predictions.
    """
    fields = list(set(position_field_mapping.values()))
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    updated_mapping = position_field_mapping.copy()

    for position in job_positions:
        if position not in updated_mapping:
            result = classifier(position, fields)
            predicted_field = result["labels"][0]
            print(f"Predicted field for {position}: {predicted_field}")
            updated_mapping[position] = predicted_field

    updated_filepath = os.path.join(MAPPING_DIR, "position_field.json")
    with open(updated_filepath, "w") as file:
        json.dump(updated_mapping, file, indent=4, sort_keys=True)
    return updated_mapping


def add_industry_and_field(
    raw_data_df, company_industry_mapping, position_field_mapping
):
    """
    Add "Industry" and "Field" columns to the applicants dataset.

    Args:
        raw_data_df (pd.DataFrame): Raw data.
        company_industry_mapping (dict): Mapping of companies to industries.
        position_field_mapping (dict): Mapping of positions to fields.

    Returns:
        pd.DataFrame: Updated DataFrame with "Industry" and "Field" columns.
    """
    raw_data_df["Industry"] = (
        raw_data_df["Company"].map(company_industry_mapping).fillna("Unknown")
    )
    raw_data_df["Field"] = (
        raw_data_df["Position"].map(position_field_mapping).fillna("Unknown")
    )
    processed_data_df = add_suffix_to_cross_column_duplicates(
        raw_data_df, ["Industry", "Field"], suffix="-x"
    )
    return processed_data_df


def add_suffix_to_cross_column_duplicates(df, columns, suffix="-x"):
    """
    Add suffixes to duplicate values across specified columns in the same row.

    Args:
        df (pd.DataFrame): Input DataFrame.
        columns (list): List of column names to check for duplicates.
        suffix (str): Suffix to append to duplicates.

    Returns:
        pd.DataFrame: DataFrame with updated values.
    """
    for idx, row in df.iterrows():
        seen = {}
        for col in columns:
            value = row[col]
            if value not in seen:
                seen[value] = 1
            else:
                seen[value] += 1
                df.at[idx, col] = f"{value}{suffix}{seen[value]-1}"
    return df


def add_missing_values(df, columns, missing_fraction=0.1):
    """
    Randomly introduce missing values to specified columns in a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame to modify.
        columns (list): List of columns to introduce missing values into.
        missing_fraction (float or int): Fraction or number of missing values.

    Returns:
        pd.DataFrame: DataFrame with missing values added.
    """
    df_copy = df.copy()
    for col in columns:
        if col in df_copy.columns:
            n_missing = (
                int(len(df_copy) * missing_fraction)
                if isinstance(missing_fraction, float)
                else min(missing_fraction, len(df_copy))
            )
            missing_indices = np.random.choice(df_copy.index, n_missing, replace=False)
            df_copy.loc[missing_indices, col] = np.nan
    return df_copy


def extend_status_levels(df, include_suffix_for=["Interview"]):
    """
    Expand application statuses into multiple levels as separate columns.

    Args:
        df (pd.DataFrame): DataFrame containing a "Status" column.
        include_suffix_for (list): List of statuses to append suffixes.

    Returns:
        pd.DataFrame: DataFrame with expanded status levels.
    """
    mapping = load_status_mapping()
    max_levels = df["Status"].dropna().apply(len).max() + 1

    for i in range(max_levels):
        df[f"StatusLevel{i}"] = None

    for idx, row in df.iterrows():
        status_string = row["Status"] if isinstance(row["Status"], str) else ""
        levels = (
            ["Submitted"] + [mapping.get(char, "NA") for char in status_string]
            if status_string
            else ["Submitted", "No Reply"]
        )
        for i, level in enumerate(levels):
            df.at[idx, f"StatusLevel{i}"] = (
                f"{level}-R{i}" if level in include_suffix_for else level
            )
    return df
