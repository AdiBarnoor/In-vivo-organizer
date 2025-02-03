import json
from flask import Flask, render_template, request, redirect, url_for, flash
import calendar
import datetime
import sqlite3
import secrets

app = Flask(__name__)

# Set the secret key for session management and flash messages
app.secret_key = secrets.token_hex(16)

# File-based storage
DATA_FILE = 'data.json'

def read_data():
    """Reads data from the JSON file."""
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"experiments": []}


def write_data(data):
    """Writes data to the JSON file."""
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


@app.route('/')
def index():
    """Main page showing experiments with filtering options and calendar."""
    data = read_data()
    experiments = data["experiments"] 

    # Get filter values from the request (these are from the query string)
    species_filter = request.args.get('species', '')
    status_filter = request.args.get('status', '')
    age_filter = request.args.get('age', '')
    weight_filter = request.args.get('weight', '')
    genotype_filter = request.args.get('genotype', '')

    # Initialize sets to collect unique values
    unique_species = set()
    unique_ages = set()
    unique_weights = set()
    unique_genotypes = set()

    # Get current month and year
    today = datetime.date.today()
    year = int(request.args.get('year', today.year))
    month = int(request.args.get('month', today.month))

    # Get the active experiment (default to first one)
    active_tab = request.args.get('active_tab', experiments[0]["name"] if experiments else '')

    # Fetch events from the database
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("SELECT experiment, date, note FROM events WHERE strftime('%Y-%m', date) = ?", (f"{year}-{month:02d}",))
        event_data = c.fetchall()
    
    # Organize events into a dictionary {experiment: {date: note}}
    events = {}
    for exp, date, note in event_data:
        if exp not in events:
            events[exp] = {}
        events[exp][date] = note

    # Generate calendars and filter experiments
    cal = calendar.Calendar()
    filtered_experiments = []
    for experiment in experiments:
        filtered_animals = []
        for animal in experiment["animals"]:
            # Apply filters to the animals
            if (not species_filter or animal["species"] == species_filter) and \
               (not status_filter or animal["status"] == status_filter) and \
               (not age_filter or str(animal["age"]) == age_filter) and \
               (not weight_filter or str(animal["weight"]) == weight_filter) and \
               (not genotype_filter or animal["genotype"] == genotype_filter):
                filtered_animals.append(animal)

                # Collect unique values for the filters
                unique_species.add(animal["species"])
                unique_ages.add(animal["age"])
                unique_weights.add(animal["weight"])
                unique_genotypes.add(animal["genotype"])

        # Generate calendar for the experiment
        month_days = cal.monthdayscalendar(year, month)

        filtered_experiments.append({
            "name": experiment["name"],
            "description": experiment["description"],
            "animals": filtered_animals,  # Could be empty, still included
            "calendar": month_days,  # Store the calendar
            "events": events.get(experiment["name"], {})  # Get events for this experiment
        })

    return render_template(
        'index.html',
        experiments=filtered_experiments,
        species=sorted(unique_species),
        ages=sorted(unique_ages),
        weights=sorted(unique_weights),
        genotypes=sorted(unique_genotypes),
        year=year,
        month=month,
        calendar=calendar,
        active_tab=active_tab
    )

@app.route('/add_event', methods=['POST'])
def add_event():
    """Adds an event to the calendar."""
    experiment = request.form['experiment']
    date = request.form['date']
    note = request.form['note']

    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO events (experiment, date, note) VALUES (?, ?, ?)", 
                  (experiment, date, note))
        conn.commit()

    year, month = map(int, date.split("-")[:2])
    return redirect(url_for('index', year=year, month=month))

@app.route('/add_experiment', methods=['GET', 'POST'])
def add_experiment():
    """Page for adding a new experiment."""
    if request.method == 'POST':
        experiment_name = request.form['name']
        experiment_description = request.form['description']
        # Add the experiment data to the JSON file
        data = read_data()
        data["experiments"].append({
            "name": experiment_name,
            "description": experiment_description,
            "animals": []
        })
        write_data(data)
        return redirect(url_for('index'))
    return render_template('add_experiment.html')


@app.route('/add_animal/<experiment_name>', methods=['GET', 'POST'])
def add_animal(experiment_name):
    if request.method == 'POST':
        try:
            animal_id = int(request.form['id'])
        except ValueError:
            flash('Animal ID must be an integer.', 'danger')
            return redirect(url_for('add_animal', experiment_name=experiment_name))

        species = request.form['species']
        dob = request.form['dob']
        age = request.form['age']
        weight = request.form['weight']
        genotype = request.form['genotype']
        comments = request.form['comments']
        
        # Initialize treatments as an empty list
        treatments = []

        data = read_data()
        for experiment in data["experiments"]:
            if experiment["name"] == experiment_name:
                experiment["animals"].append({
                    "id": animal_id,
                    "species": species,
                    "dob": dob,
                    "age": age,
                    "weight": weight,
                    "genotype": genotype,
                    "comments": comments,
                    "status": "Alive",
                    "treatments": treatments
                })
        write_data(data)
        return redirect(url_for('index'))
    return render_template('add_animal.html', experiment_name=experiment_name)


@app.route('/sacrifice_animal/<experiment_name>/<int:animal_id>', methods=['POST'])
def sacrifice_animal(experiment_name, animal_id):
    """Mark an animal as 'sacrificed'."""
    data = read_data()

    # Find the experiment
    for experiment in data["experiments"]:
        if experiment["name"] == experiment_name:
            for animal in experiment["animals"]:
                if animal["id"] == animal_id:  # Ensure integer comparison
                    animal["status"] = "Sacrificed"
                    write_data(data)  # Save changes
                    flash(f'Animal {animal_id} has been sacrificed.', 'success')
                    return redirect(url_for('index'))
    
    flash('Animal not found.', 'danger')
    return redirect(url_for('index'))

@app.route('/delete_animal/<experiment_name>/<int:animal_id>', methods=['POST'])
def delete_animal(experiment_name, animal_id):
    """Delete an animal from an experiment."""
    data = read_data()
    for experiment in data["experiments"]:
        if experiment["name"] == experiment_name:
            experiment["animals"] = [
                animal for animal in experiment["animals"] if animal["id"] != animal_id
            ]
    write_data(data)
    flash('Animal deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete_exp/<experiment_name>', methods=['POST'])
def delete_exp(experiment_name):
    """Delete an experiment from the list"""
    data = read_data()
    
    # Find the experiment by name
    experiment_to_delete = next((exp for exp in data["experiments"] if exp["name"] == experiment_name), None)

    if experiment_to_delete:
        data["experiments"].remove(experiment_to_delete)
        write_data(data)
        flash('Experiment deleted successfully!', 'success')
    else:
        flash('Experiment not found.', 'danger')

    return redirect(url_for('index'))


@app.route('/modify_animal/<experiment_name>/<int:animal_id>', methods=['GET', 'POST'])
def modify_animal(experiment_name, animal_id):
    """Modify an animal's details."""
    data = read_data()
    # Find the experiment
    experiment = next((exp for exp in data["experiments"] if exp["name"] == experiment_name), None)
    
    if not experiment:
        flash('Experiment not found!', 'danger')
        return redirect(url_for('index'))  # Redirect to the index page if experiment is not found

    # Find the animal
    animal = next((animal for animal in experiment["animals"] if animal["id"] == animal_id), None)
    
    if not animal:
        flash('Animal not found!', 'danger')
        return redirect(url_for('index'))  # Redirect to the index page if animal is not found

    if request.method == 'POST':
        # Update animal details from form
        animal["species"] = request.form['species']
        animal["dob"] = request.form['dob']
        animal["age"] = request.form['age']
        animal["weight"] = request.form['weight']
        animal["comments"] = request.form['comments']
        write_data(data)
        flash('Animal details updated successfully!', 'success')
        return redirect(url_for('index'))  # Redirect to the index page after updating

    # For GET request, render the template with current animal data
    return render_template('modify_animal.html', experiment_name=experiment_name, animal=animal)

@app.route('/add_treatment/<experiment_name>/<int:animal_id>', methods=['GET', 'POST'])
def add_treatment(experiment_name, animal_id):
    if request.method == 'POST':
        treatment_date = request.form['date']
        treatment_description = request.form['description']

        data = read_data()
        for experiment in data["experiments"]:
            if experiment["name"] == experiment_name:
                # Find the animal by id
                for animal in experiment["animals"]:
                    if animal["id"] == animal_id:
                        # Add the treatment to the animal's treatments list
                        animal["treatments"].append({
                            "date": treatment_date,
                            "description": treatment_description
                        })
                        break
        
        write_data(data)

        flash('Treatment added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_treatment.html', experiment_name=experiment_name, animal_id=animal_id)


@app.route('/animal_treatments/<experiment_name>/<int:animal_id>')
def animal_treatments(experiment_name, animal_id):
    """Page to show treatments for a specific animal in an experiment."""
    data = read_data()

    # Find the experiment and the animal
    experiment = next((exp for exp in data["experiments"] if exp["name"] == experiment_name), None)
    if not experiment:
        flash('Experiment not found!', 'danger')
        return redirect(url_for('index'))

    animal = next((animal for animal in experiment["animals"] if animal["id"] == animal_id), None)
    if not animal:
        flash('Animal not found!', 'danger')
        return redirect(url_for('index'))

    return render_template('animal_treatments.html', experiment_name=experiment_name, animal=animal)


if __name__ == '__main__':
    app.run(debug=False)
