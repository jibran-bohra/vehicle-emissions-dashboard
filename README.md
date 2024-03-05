# Toyota Emissions Insights Platform

## Overview

Welcome to the Toyota Emissions Insights Platform! This Django-based project is designed to provide users with detailed insights into the carbon emissions associated with Toyota vehicles. Our aim is to empower users to make informed decisions by offering accurate and accessible emissions data for specific models and years of Toyota vehicles. By promoting environmental awareness and sustainability, we hope to contribute to a greener and more conscious automotive industry.

## Getting Started

Follow these steps to set up the project locally:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/toyota-emissions-insights.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd toyota-emissions-insights
    ```

3. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. **Make and Apply migrations:**

    ```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

5. **Get an API key:**

   Visit [Carbon Interface](https://www.carboninterface.com/users/sign_up) to get an API key. Paste the obtained API key into `testsite/settings.py` under the variable `MY_API_KEY`.

6. **Start the development server:**

    ```bash
    python3 manage.py runserver
    ```

7. **Open your browser and go to [http://localhost:8000/admin](http://localhost:8000/admin) to log in with your account and start managing emissions data.**

