"""
Module for Loading Applicants Data and Mappings

This module provides utility functions to load various datasets and mappings required
for the Application tracking  analytics. The functions handle JSON mappings, CSV files,
and raw jobhunt data to facilitate easy data loading and processing.

Directories:
    - MAPPING_DIR: Directory containing JSON and CSV mapping files.
    - OUTPUT_DIR: Directory containing processed and raw jobhunt data.

Functions:
    - load_json_mappings: Load mappings between companies and industries, and positions and fields.
    - load_status_mapping: Load the mapping of job application statuses.
    - load_countries_ISO: Load and map country codes between different ISO formats.
    - load_raw_data: Load the raw applicants' data from a CSV file.
"""

import pandas as pd
import os
import json

# Define directories for mappings and output data
MAPPING_DIR = "./data/mappings"
OUTPUT_DIR = "./data/output"


def load_map_projections():
    """
    Load map projections from JSON file.

    Returns:
        map_projections (list)
    """
    map_projections_filepath = os.path.join(MAPPING_DIR, "map_projections.json")

    # Load the list from the JSON file
    with open(map_projections_filepath, "r") as file:
        map_projections = json.load(file)

    return map_projections


def load_json_mappings():
    """
    Load mappings from JSON files for company-industry and position-field relationships.

    Returns:
        tuple: A tuple containing two dictionaries:
            - company_industry_mapping (dict): Mapping of companies to industries.
            - position_field_mapping (dict): Mapping of positions to fields.
    """
    company_industry_mapping_filepath = os.path.join(
        MAPPING_DIR, "company_industry.json"
    )

    with open(company_industry_mapping_filepath, "r") as file:
        company_industry_mapping = json.load(file)

    position_field_mapping_filepath = os.path.join(MAPPING_DIR, "position_field.json")

    with open(position_field_mapping_filepath, "r") as file:
        position_field_mapping = json.load(file)

    return company_industry_mapping, position_field_mapping


def load_status_mapping():
    """
    Load the mapping of job application statuses from a JSON file.

    Returns:
        dict: A dictionary mapping application statuses to their descriptions or codes.
    """
    status_mapping_filepath = os.path.join(MAPPING_DIR, "status.json")

    with open(status_mapping_filepath, "r") as file:
        status_mapping = json.load(file)

    return status_mapping


def load_countries_ISO(abbr_from: str = "alpha-2", abbr_to: str = "alpha-3"):
    """
    Load and map country codes between different ISO formats using a CSV file.

    Args:
        abbr_from (str): The column name of the source ISO code format (default: "alpha-2").
        abbr_to (str): The column name of the target ISO code format (default: "alpha-3").

    Returns:
        dict: A dictionary mapping country codes from the `abbr_from` format to the `abbr_to` format.
    """
    # Path to the countries_ISO.csv file
    countries_ISO_filepath = os.path.join(MAPPING_DIR, "countries_ISO.csv")

    # Load the CSV file into a pandas DataFrame
    countries_ISO_df = pd.read_csv(countries_ISO_filepath)

    # Create a dictionary that maps abbr_from to abbr_to (e.g., alpha-2 to alpha-3)
    country_mapping = dict(zip(countries_ISO_df[abbr_from], countries_ISO_df[abbr_to]))

    return country_mapping


def load_raw_data():
    """
    Load the raw applicants' data from a CSV file.

    Returns:
        pandas.DataFrame: A DataFrame containing the raw applicants' data.
    """
    raw_data_filepath = os.path.join(OUTPUT_DIR, "raw_data.csv")

    # Load the CSV file into a DataFrame
    raw_df = pd.read_csv(raw_data_filepath)

    return raw_df
