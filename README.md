# In Vivo Organizer

## Overview

The **In Vivo Organizer** is a web-based application designed to assist researchers in managing their animal experiments. The tool provides a dynamic dashboard, experiment planning, animal tracking, and schedule management. It allows researchers to set up new experiments, track animals, manage their health status, and visualize experiment timelines. 

The application is built using **Flask**, **SQLAlchemy**, and **Bootstrap**, providing a simple yet effective interface for managing animal experiments.

## Features

- **Dynamic Dashboard**: A live view of ongoing experiments, groups, and timelines with real-time updates.
- **Experiment Planning**: Set up new experiments with groups, treatments, and timelines. Includes metadata like species, animal ID, treatments, etc.
- **Animal Tracking**: Add animals individually or in bulk, assign them to experimental groups, and track their health status (e.g., "Sacrifice" for dead animals).
- **Schedule Management**: Create schedules for interventions, measurements, and observations with calendar integration.
- **Real-Time Updates**: Dynamic updates when changes are made to experiments or animals.
- **Collaboration**: Add team members to the project and assign different roles (e.g., Admin, Observer).

## Requirements

- Python 3.6+ (Python 3.13 is currently not fully supported)
- Flask
- Flask-SQLAlchemy
- Bootstrap (for styling)

You can install the required dependencies using the following:

```bash
pip install -r requirements.txt
```
---

### Steps to Install
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/in-vivo-organizer.git
   cd in-vivo-organizer

   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Set Up the Database:
   The project uses SQLAlchemy to manage the database. You'll need to initialize the database before running the app.
   In your terminal, run:
   ```
   from app import db
   db.create_all()  # This will create the necessary tables in the database
   ```
   
4. Run the application:
   ```bash
   python organizer.py
   ```

5. Access the Web Application
   Open your browser and go to the following address:
   ```
   http://127.0.0.1:5000
   ```
---

## Usage

1. **Start the Program**
   Run the script to open the GUI application.

2. **Plan Your Experiment**
   - Define experimental groups and variables.
   - Set up timelines for interventions and observations.

3. **Track Animals and Treatments**
   - Log details of animal groups, including health and interventions.
   - Monitor treatments and environmental conditions.

4. **Collect and Analyze Data**
   - Record observations and measurements.
   - Generate graphs and reports for analysis and presentation.

