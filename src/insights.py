def get_overall_insights(df):
    """
    Calculate key insights from applicants' DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing applicants' data with columns such as "Country", "Industry", "Field", etc.

    Returns:
        tuple: A tuple containing the following insights:
            - num_of_applications (int): Total number of applications.
            - num_of_countries (int): Number of unique countries.
            - num_of_industries (int): Number of unique industries.
            - num_of_fields (int): Number of unique fields.
            - num_of_active (int): Number of active applications (where "Status" is NaN).
            - num_of_interviews (int): Number of applications with interview status ("I" in "Status").
    """

    # Define inactive status codes
    inactive_status = {"N", "H", "G", "R"}

    # Check if the status contains any inactive codes
    def is_active(status):
        return not any(char in inactive_status for char in status)

    # Apply the function to check for active statuses
    df["isActive"] = df["Status"].apply(is_active)

    # Define interview-related status codes
    interview_status = {"I", "A", "T"}

    # Function to check if a status includes any interview-related code
    def has_interview(status):
        return any(char in interview_status for char in status)

    # Apply the function to check for interview-related statuses
    df["hasInterview"] = df["Status"].apply(has_interview)

    num_of_applications = df.shape[0]
    num_of_countries = len(df["Country"].unique())
    num_of_industries = len(df["Industry"].unique())
    num_of_fields = len(df["Field"].unique())
    num_of_active = df["isActive"].sum()
    num_of_interviews = df["hasInterview"].sum()

    return (
        num_of_applications,
        num_of_countries,
        num_of_industries,
        num_of_fields,
        num_of_active,
        num_of_interviews,
    )
