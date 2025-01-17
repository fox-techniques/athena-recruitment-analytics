"""
Module for Processing and Mapping Applicants' Data

This module provides functions to handle missing data, predict mappings using 
zero-shot classification, and enhance recruitment and applicants datasets by adding relevant fields 
(e.g., industry, field, status levels). It also includes utilities for introducing 
missing values for testing purposes.

Directories:
    - MAPPING_DIR: Directory containing mapping files in JSON format.

Functions:
    - update_missing_company_industry: Identify companies missing industry in the company-industry mapping.
    - update_missing_position_field: Identify positions missing field in  the position-field mapping.
    - add_industry_and_field: Add "Industry" and "Field" columns to the dataset.
    - add_suffix_to_cross_column_duplicates: Add suffixes to duplicate values across columns.
    - add_missing_values: Introduce missing values (NaNs) into specific columns.
    - extend_status_levels: Expand application statuses into multiple levels.
"""

import os
import json
import re
import numpy as np

from utils.performance import _log_execution_time

import logging

logger = logging.getLogger(__name__)

# Directory for mapping files
MAPPING_DIR = "./data/mappings"

MISSING_ENTRIES_FILE = os.path.join(MAPPING_DIR, "missing_entries.log")
PLACEHOLDER = "MISSING!!!"


@_log_execution_time
def log_missing_entry(entry_type, name):
    """
    Log missing entries to a file for later review.

    Args:
        entry_type (str): The type of missing entry (e.g., "Company", "Position").
        name (str): The name of the missing entry.
    """
    with open(MISSING_ENTRIES_FILE, "a") as file:
        file.write(f"{entry_type}: {name}\n")
    print(f"Logged missing {entry_type.lower()}: '{name}' to {MISSING_ENTRIES_FILE}")


@_log_execution_time
def update_missing_company_industry(df, company_industry_mapping):
    """
    Update industries for companies missing in the company-industry mapping.

    Args:
        df (DataFrame): Enriched job application data.
        company_industry_mapping (dict): Existing mapping of companies to industries.

    Returns:
        dict: Updated company-industry mapping.
    """
    updated_mapping = company_industry_mapping.copy()
    company_names = df["Company"].unique()

    for company in company_names:
        clean_company_name = re.sub(r"\sx\d+$", "", company)
        if clean_company_name not in updated_mapping:
            print(f"Industry for company '{clean_company_name}' is missing.")
            log_missing_entry(
                "ALERT - Missing industry for company", clean_company_name
            )
            updated_mapping[clean_company_name] = (
                PLACEHOLDER  # Add placeholder for missing entry
            )

    updated_filepath = os.path.join(MAPPING_DIR, "company_industry.json")
    with open(updated_filepath, "w") as file:
        json.dump(updated_mapping, file, indent=4, sort_keys=True)
    return updated_mapping


@_log_execution_time
def update_missing_position_field(df, position_field_mapping):
    """
    Update fields for positions missing in the position-field mapping.

    Args:
        df (DataFrame): Enriched job application data.
        position_field_mapping (dict): Existing mapping of positions to fields.

    Returns:
        dict: Updated position-field mapping.
    """
    updated_mapping = position_field_mapping.copy()
    job_positions = df["Position"].unique()

    for position in job_positions:
        if position not in updated_mapping:
            print(f"Field for position '{position}' is missing.")
            log_missing_entry("ALERT - Missing field for position", position)
            updated_mapping[position] = PLACEHOLDER  # Add placeholder for missing entry

    updated_filepath = os.path.join(MAPPING_DIR, "position_field.json")
    with open(updated_filepath, "w") as file:
        json.dump(updated_mapping, file, indent=4, sort_keys=True)
    return updated_mapping


@_log_execution_time
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


@_log_execution_time
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


@_log_execution_time
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
