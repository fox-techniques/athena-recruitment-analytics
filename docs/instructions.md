# 📥 Instructions 

Follow these steps to clone the repository, set up the environment, and run the **ATHENA** dashboard.

**Prerequisites:**

- 🐍 Python 3.10+

Ensure you have **Python 3.10+** installed. If not, download and install it from the [official Python website](https://www.python.org/downloads/). Check your version:

```bash
python --version
```
For installation guides and troubleshooting, refer to the [RealPython](https://realpython.com/installing-python/) documentation.

!!! tip

    If you don't have prior experience with Python, we recommend reading
    [Using Python's pip to Manage Your Projects' Dependencies], which is a
    really good introduction on the mechanics of Python package management and
    helps you troubleshoot if you run into errors.

  [virtual environment]: https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment
  [Using Python's pip to Manage Your Projects' Dependencies]: https://realpython.com/what-is-pip/

## 🐙 Git


**Step 1.** Open your terminal or command prompt.

**Step 2.** Clone the **ATHENA** repository from GitHub:

```bash
git clone https://github.com/your-repo/athena-recruitment-analytics.git
```

**Step 3.** Navigate to the project directory:

```bash
cd athena-recruitment-analytics
```

## 📦 Package manager

=== "pip"

    **Step 4.** Create a virtual environment to isolate dependencies:

    ```bash
    python -m venv .venv
    ```

    **Step 5.** Activate the virtual environment:

    === "Windows"

        ```
        .venv\Scripts\activate
        ```

    === "macOS/Linux"

        ```bash
        source .venv/bin/activate
        ```


    **Step 6.** Upgrade pip to the latest version:

    ```bash
    pip install --upgrade pip
    ```

    ## Install Dependencies

    **Step 7.** Install the required Python packages using requirements.txt:

    ```bash
    pip install -r requirements.txt
    ```

=== "poetry"

    **Step 4.** Make sure Poetry is installed:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
    ```

    **Step 5.** Configure a virtual environment to isolate dependencies:

    ```bash
    poetry install
    ```

    **Step 6.** Activate the virtual environment:

    ```bash
    poetry shell
    ```

    ## Update Dependencies

    **Step 7.** Add, remove, or update packages:

    ```bash
    poetry add pandas
    poetry remove pandas
    poetry update
    ```

**Step 8.** Run the **ATHENA** Dashboard

Start the dashboard application:

```bash
python app.py
```

Open your web browser and navigate to:

```bash
http://127.0.0.1:8050/
```