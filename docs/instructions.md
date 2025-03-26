# 📥 Instructions 

Follow these steps to clone the repository, set up the environment, and run the **ATHENA** dashboard.


## 💻 ATHENA Dashboard (Local)

**Step 1.** Open your terminal or command prompt.

**Step 2.** Clone the **ATHENA** repository from GitHub:

```bash
git clone https://github.com/your-repo/athena-recruitment-analytics.git
```

**Step 3.** Navigate to the project directory:

```bash
cd athena-recruitment-analytics
```

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

    Install Dependencies

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

    Update Dependencies

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

---

## 🐳 Docker

You can also run the dashboard using the pre-built Docker image.

### Using Docker CLI

```sh
docker run -p 8050:8050 \
  -e DASH_HOST=0.0.0.0 \
  -e DASH_PORT=8050 \
  ghcr.io/fox-techniques/athena-dash-app:latest

```

Then open your browser and go to:

```sh
http://localhost:8050/

```

### Using Docker Compose

Add this to your `docker-compose.yml`:

```yml
services:
  athena:
    image: ghcr.io/fox-techniques/athena-dash-app:latest
    environment:
      - DASH_HOST=0.0.0.0
      - DASH_PORT=8050
    ports:
      - "8050:8050"
```

Then start the service:

```sh
docker-compose up -d
```

Navigate to:

```sh
http://localhost:8050/

```

---

🤩 CONGRAGULATIONS! Continue to the demo. Let's keep going...🚀