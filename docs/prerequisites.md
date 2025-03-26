# ⚡️ Prerequisites

To run **ATHENA** Recuitment Analytics dashboard, ensure you have the following dependencies installed:

- Python 3.10+
- Poetry or pip
- Git
- Docker 

---

## 🐍 Python 3.10+

Ensure you have **Python 3.10+** installed. If not, download and install it from the [official Python website](https://www.python.org/downloads/). Check your version:

```bash
python --version

```
For installation guides and troubleshooting, refer to the [RealPython](https://realpython.com/installing-python/) documentation.

## 📦 Package managers


=== "Poetry"

    !!! tip "Why We Recommend Poetry Over pip"

        While pip is the standard Python package manager, **we strongly recommend using Poetry for managing dependencies**.

        - **Simplified Dependency Management** – Poetry resolves, installs, and locks dependencies automatically, preventing version conflicts.
        - **Built-in Virtual Environments** – Unlike pip, Poetry creates and manages isolated environments for your projects.
        - **Reproducible Installs** – Poetry uses pyproject.toml and poetry.lock to ensure consistency across different environments.
        - **Better Publishing Workflow** – If you plan to contribute or package extensions, Poetry makes publishing to PyPI seamless.

        For long-term projects and production environments, Poetry provides a **more robust and scalable solution** than pip.

    Install Poetry as package manager and dependencies management:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

    Check if Poetry is installed correctly:

    ```bash
    poetry --version
    
    ```

=== "pip"

    !!! info "Knowledge"

        If you don't have prior experience with Python, we recommend reading
        [Using Python's pip to Manage Your Projects' Dependencies], which is a
        really good introduction on the mechanics of Python package management and
        helps you troubleshoot if you run into errors.

    [virtual environment]: https://realpython.com/what-is-pip/#using-pip-in-a-python-virtual-environment
    [semantic versioning]: https://semver.org/
    [Using Python's pip to Manage Your Projects' Dependencies]: https://realpython.com/what-is-pip/

    Upgrade pip to the latest version: 

    ``` sh
    python -m pip install --upgrade pip
    ```

## 🌱 Git

Ensure you have **Git** installed. If not, download and install it from the [official Git website](https://git-scm.com/downloads). Check your version:

```bash
git --version
```

## 🐳 Docker

To demonstrate **ATHENA** using Docker, ensure you have Docker and Docker Compose installed. Download and install Docker from the official website:

- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Desktop](https://docs.docker.com/desktop/)

Verify installation with: 

```bash
docker version

```

Now that prerequisites are set, continue with **configuration**. 🎯

  [GitHub]: https://github.com/fox-techniques/athena-recuitment-analytics
  [Poetry]: https://python-poetry.org/docs/#installation