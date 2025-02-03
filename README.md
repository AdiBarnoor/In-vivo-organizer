# In Vivo Organizer

## Overview

The **In Vivo Organizer** is a web-based application designed to assist researchers in managing their animal experiments. The tool provides a dynamic dashboard, experiment planning, animal tracking, and schedule management. It allows researchers to set up new experiments, track animals, manage their health status, and visualize experiment timelines. It provides a dynamic dashboard to manage the life cycle of experiments, from planning to monitoring.


## Features

- **Experiment Management**: Add, delete, and view experiments.
- **Animal Management**: Add, modify, and delete animals associated with experiments.
- **Animal Treatments**: Add treatments and view details of treatments for each animal.
- **Event Scheduling**: Add and view events on the calendar for each experiment.
- **Filtering**: Filter animals by species, age, weight, genotype, and status.

## Project Structure

Here’s how the project is organized:
```bash
your_project/
│
├── app.py # Main Flask application
│
├── templates/ # HTML templates for the app
│ ├── index.html
│ ├── add_experiment.html
│ └── ...
│ └── database.db # SQLite database (auto-created if not exists)
```

## Requirements

- `Python 3.6+` (Python 3.13 is currently not fully supported)
- `Flask`
- `Bootstrap` (for styling)
- SQLite (no need to install)

You can install the required dependencies using the following:

```bash
pip install -r requirements.txt
```
---

### Steps to Install
1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/your-project.git
    cd your-project
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the app**:
    ```bash
    python app.py
    ```
Visit `http://127.0.0.1:5000/` in your browser to see the app in action!

---

## Technology Stack
- **Backend:** `Python`, `Flask`
- **FrontEnd:** `HTML`, `CSS`, `Bootstrap4`
- **Database:** `JSON`
