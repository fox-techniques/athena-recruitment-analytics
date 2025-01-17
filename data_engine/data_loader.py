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

from data_engine.data_parser import parse_job_application_directory

from utils.performance import _log_execution_time

import logging

logger = logging.getLogger(__name__)

# Directories for data and mappings
MAPPING_DIR = os.getenv("MAPPING_DIR", "./data/mappings")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./data/output")


@_log_execution_time
def parse_and_load_data(applications_dir, output_dir):
    """
    Parse data from the application directory or load pre-parsed data from the output directory.

    This function checks if `applications_dir` exists and is non-empty. If so, it parses the data,
    overwrites the existing `parsed_data.csv` in `output_dir`, and returns the parsed data.
    Otherwise, it loads the data from `parsed_data.csv` in `output_dir` if it exists.

    Args:
        applications_dir (str): Path to the directory containing application files to parse.
        output_dir (str): Path to the directory where parsed data is stored.

    Returns:
        pandas.DataFrame: The parsed or loaded data as a DataFrame.

    Raises:
        FileNotFoundError: If neither `applications_dir` contains data nor `output_dir/parsed_data.csv` exists.
    """

    parsed_data_filepath = os.path.join(output_dir, "parsed_data.csv")

    if os.path.exists(applications_dir):
        if os.listdir(applications_dir):
            print(f"Parsing data from APPLICATION_DIR: {applications_dir}")
            parsed_df = parse_job_application_directory(applications_dir)
            print(f"Data has been parsed from: {parsed_data_filepath}")

    elif os.path.exists(parsed_data_filepath):
        print(f"Loading data from OUTPUT_DIR: {parsed_data_filepath}")
        parsed_df = pd.read_csv(parsed_data_filepath)

    else:
        raise FileNotFoundError(
            "No data available to load or parse. Ensure APPLICATION_DIR or OUTPUT_DIR is populated."
        )

    return parsed_df


@_log_execution_time
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


@_log_execution_time
def load_json_mappings():
    """
    Load mappings from JSON files for company-industry and position-field relationships.

    Returns:
        tuple: A tuple containing two dictionaries:
            - company_industry_mapping (dict): Mapping of companies to industries.
            - position_field_mapping (dict): Mapping of positions to fields.
    """
    try:
        with open(os.path.join(MAPPING_DIR, "company_industry.json"), "r") as file:
            company_industry_mapping = json.load(file)
        with open(os.path.join(MAPPING_DIR, "position_field.json"), "r") as file:
            position_field_mapping = json.load(file)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return {}, {}

    return company_industry_mapping, position_field_mapping


@_log_execution_time
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


@_log_execution_time
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


@_log_execution_time
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
