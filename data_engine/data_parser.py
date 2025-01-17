"""
Module for Parsing Jobhunt Directory and Extracting Job Details

This module provides utilities to parse a directory of job applications and extract
relevant details about the applications. The functions handle directories and files
to derive job titles, companies, countries, application statuses, timestamps, and
other metadata.

Directories:
    - APPLICATIONS_DIR: Directory containing job application folders.
    - OUTPUT_DIR: Directory to store processed output files.

Functions:
    - extract_job_details: Extract job title, company, country, and status from folder names.
    - format_timestamp: Convert timestamps into a readable date-time format.
    - parse_jobhunt_directory: Parse the jobhunt directory and create a DataFrame of job details.
"""

import re
import os
import pandas as pd
from datetime import datetime

from utils.performance import _log_execution_time

import logging

logger = logging.getLogger(__name__)

# Define directories
APPLICATIONS_DIR = "./data/job_applications"
OUTPUT_DIR = "./data/output"


@_log_execution_time
def extract_job_details(dirname):
    """
    Extract job details (title, company, country, status) from a directory name.

    Args:
        dirname (str): Name of the directory containing job application details.

    Returns:
        tuple: A tuple containing:
            - job_title (str): Title of the job.
            - company (str): Name of the company.
            - country_code (str): Country code (e.g., "NL" or "USA").
            - status (str): Application status.
        None: If the directory name does not conform to the expected format.

    Notes:
        - The directory name should follow a specific format such as:
            "JobTitle - CompanyName [CountryCode] (Status)".
        - If the format is invalid, the function returns None.
    """
    # Remove the file extension if any (e.g., .txt, .pdf)
    dirname = dirname.rsplit(".", 1)[0]

    try:
        dirname = dirname.rsplit(".", 1)[0]
        country_code = re.search(r"\[(.*?)\]", dirname)
        status = re.search(r"\((.*?)\)", dirname)
        job_and_company = re.split(
            r" - ", re.sub(r"\[.*?\]|\(.*?\)", "", dirname).strip()
        )

        if len(job_and_company) != 2:
            raise ValueError(f"Invalid format for: {dirname}")

        job_title, company = map(str.strip, job_and_company)
        return (
            job_title,
            company,
            country_code.group(1) if country_code else "NL",
            status.group(1) if status else "",
        )
    except Exception as e:
        print(f"Error extracting details from '{dirname}': {e}")
        return None


@_log_execution_time
def format_timestamp(timestamp):
    """
    Convert a Unix timestamp into a human-readable date-time format.

    Args:
        timestamp (float): Unix timestamp.

    Returns:
        str: Formatted date-time string in the format "YYYY-MM-DD HH:MM:SS".
    """
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


@_log_execution_time
def parse_job_application_directory(directory):
    """
    Parse a directory of job application folders to extract relevant details.

    Args:
        directory (str): Path to the directory containing job application folders.

    Returns:
        pandas.DataFrame: A DataFrame containing job details with the following columns:
            - Position (str): Title of the job.
            - Company (str): Name of the company.
            - Country (str): Country code (e.g., "NL" or "USA").
            - NumApplications (int): Number of applications submitted.
            - HasCover (bool): Whether a cover letter exists in the folder.
            - Status (str): Application status.
            - SubmissionTimestamp (str): Timestamp of submission.
            - LastUpdateTimestamp (str): Timestamp of the last update.

    Notes:
        - The function checks for specific file and folder structures:
            - Directory names should include "PositionTitle - CompanyName [CountryCode] (Status)".
            - A `job_description.txt` file in the directory is used for SubmissionTimestamp.
        - The parsed data is saved as a CSV file in the OUTPUT_DIR.
    """
    job_data = []

    for dirname in os.listdir(directory):
        dirpath = os.path.join(directory, dirname)
        if os.path.isdir(dirpath):
            details = extract_job_details(dirname)
            if details:
                job_title, company, country, status = details

                # Extract number of applications
                num_applications_match = re.search(r"x(\d+)", company)
                num_applications = (
                    int(num_applications_match.group(1))
                    if num_applications_match
                    else 1
                )
                company = re.sub(
                    r"\sx\d+$", "", company
                )  # Remove "xN" suffix from company name

                # Check for cover letter
                has_cover = any(
                    "cover" in filename.lower() or "motivation" in filename.lower()
                    for filename in os.listdir(dirpath)
                )

                # Extract timestamps
                job_description_file = os.path.join(dirpath, "job_description.txt")
                if os.path.exists(job_description_file):
                    submission_timestamp = format_timestamp(
                        os.stat(job_description_file).st_ctime
                    )
                else:
                    submission_timestamp = None

                last_update_timestamp = format_timestamp(os.stat(dirpath).st_mtime)
                if not status or status.lower() == "s":
                    last_update_timestamp = None

                # Append parsed data
                job_data.append(
                    (
                        job_title,
                        company,
                        country,
                        num_applications,
                        has_cover,
                        status,
                        submission_timestamp,
                        last_update_timestamp,
                    )
                )
            else:
                print(f"Skipping directory: {dirname}")

    # Create DataFrame
    parsed_data_df = pd.DataFrame(
        job_data,
        columns=[
            "Position",
            "Company",
            "Country",
            "NumApplications",
            "HasCover",
            "Status",
            "SubmissionTimestamp",
            "LastUpdateTimestamp",
        ],
    )

    jobhunt_parsed_data_filepath = os.path.join(OUTPUT_DIR, "parsed_data.csv")

    if parsed_data_df.empty:
        print("No data found. Please check filenames or folder structure.")
    else:
        parsed_data_df.to_csv(jobhunt_parsed_data_filepath, index=False)
        print(f"Data saved to {jobhunt_parsed_data_filepath}")

    return parsed_data_df
