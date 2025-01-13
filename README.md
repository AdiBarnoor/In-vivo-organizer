# In Vivo Organizer

## Overview

The **In Vivo Organizer** is a web-based application designed to assist researchers in managing their animal experiments. The tool provides a dynamic dashboard, experiment planning, animal tracking, and schedule management. It allows researchers to set up new experiments, track animals, manage their health status, and visualize experiment timelines. It provides a dynamic dashboard to manage the life cycle of experiments, from planning to monitoring.


## Features

- **Dynamic Dashboard**: A live view of ongoing experiments, groups, and timelines with real-time updates.
- **Experiment Planning**: Set up new experiments with groups, treatments, and timelines. Includes metadata like species, animal ID, treatments, etc.
- **Animal Tracking**: Add animals individually or in bulk, assign them to experimental groups, and track their health status (e.g., "Sacrifice" for dead animals).
- **Schedule Management**: Create schedules for interventions, measurements, and observations with calendar integration.
- **Real-Time Updates**: Dynamic updates when changes are made to experiments or animals.

## Requirements

- `Python 3.6+` (Python 3.13 is currently not fully supported)
- `Flask`
- `Bootstrap` (for styling)

You can install the required dependencies using the following:

```bash
pip install -r requirements.txt
```
---

### Steps to Install
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/AdiBarnoor/in-vivo-organizer.git
   cd in-vivo-organizer

   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Run the application:
   ```bash
   python app.py
   ```
This will start a Flask development server on `http://127.0.0.1:5000/`.

4. Access the Web Application
   Open your browser and go to the following address:
   ```
   http://127.0.0.1:5000
   ```
---

## Usage

1. **Start the Program:**
   Run the script to start the application.

2. **Plan Your Experiment**
   - Define experimental groups and variables.
   - Set up timelines for interventions and observations.

3. **Track Animals and Treatments**
   - Log details of animal groups, including health and interventions.
   - Monitor treatments and environmental conditions.

4. **Collect and Analyze Data**
   - Record observations and measurements.
   - Generate graphs and reports for analysis and presentation.

---

## Technology Stack
- **Backend:** `Python`, `Flask`
- **FrontEnd:** `HTML`, `CSS`, `Bootstrap4`
- **Database:** `JSON`
