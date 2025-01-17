import os
import random

from utils.performance import _log_execution_time

# Lists of positions, companies, countries, and statuses
positions = [
    "Analytics Engineer",
    "Artificial Intelligence",
    "Azure Data Engineer",
    "Azure Data Engineer",
    "Business Analyst",
    "Chapter Lead",
    "Climate Data",
    "Cloud Architect",
    "Cloud Engineer",
    "Cloud Software Engineer",
    "Data Analyst",
    "Data Architect",
    "Data Engineer",
    "Data Management Specialist",
    "Data Manager",
    "Data Platform Engineer Advanced",
    "Data Scientist ",
    "Data Scientist and Process Mining",
    "Data Warehouse Architect",
    "Data Warehouse Engineer",
]
companies = [
    "Roche",
    "Eneco",
    "Microsoft",
    "ING",
    "Heineken",
    "HelloFresh",
    "BasicFit",
    "MAN",
    "BMW",
    "ABN Amro",
    "TU Delft",
    "Netflix",
    "Deloitte",
]
countries = ["NL", "US", "UK", "CA", "DE", "FR", "ES", "AT", "CH"]
statuses = ["R", "IR", "IIR", "H", "G", "CITIO", "VR", "CR", "N", "IIIR", "VIITO"]

# Number of random folders to generate
num_folders = 42

# Root directory for job applications
root_dir = "./data/job_applications"

# Ensure the root directory exists
os.makedirs(root_dir, exist_ok=True)

# Generate random folders
for i in range(num_folders):
    # Randomly select position, company, country, and status
    position = random.choice(positions)
    company = random.choice(companies)
    country = random.choice(countries)
    status = random.choice(statuses)

    # Construct folder name
    folder_name = f"{position} - {company} [{country}] ({status})"

    # Create the folder path
    folder_path = os.path.join(root_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Create dummy job description file
    with open(os.path.join(folder_path, "job_description.txt"), "w") as f:
        f.write(f"This is a dummy job description for {position} at {company}.")

    # Create dummy CV file
    candidate_name = f"john_smith"  # Unique candidate name

    with open(os.path.join(folder_path, f"{candidate_name}_cv.txt"), "w") as f:
        f.write(
            "This is a John Smith's CV... it can be in other formats .docx, dpf, etc."
        )

    # Create dummy cover letter file
    with open(
        os.path.join(folder_path, f"{candidate_name}_cover_letter.txt"), "w"
    ) as f:
        f.write(
            "This is a John Smith's cover letter...it can be in other formats .docx, dpf, etc."
        )

print(f"{num_folders} folders with dummy files created under '{root_dir}'.")
