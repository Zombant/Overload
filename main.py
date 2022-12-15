import json
from datetime import date

def load_json(file):
    with open(file, 'r') as f:
        return json.loads(f.read())

# Write data to a json file
def export_json(file, data):
    json_string = json.dumps(data, indent=2)
    with open(file, 'w') as f:
        f.write(json_string)

def new_log(file):
    overload = {"overload": {}}
    export_json(file, overload)

def print_muscle_groups(data):
    data = load_json('my_progress.json')
    for muscle_group, _ in data['overload'].items():
        print(muscle_group + ": " + str(len(muscle_group)))

def print_exercises(data, muscle_group):
    data = load_json('my_progress.json')
    for exercise, _ in data['overload'][muscle_group].items():
        print(exercise)

def print_current_status(data, exercise_to_find):
    data = load_json('my_progress.json')
    for muscle_group, _ in data['overload'].items():
        for exercise, _ in data['overload'][muscle_group].items():
            if exercise == exercise_to_find:
                exercise_data = data['overload'][muscle_group][exercise]['current']
                print("Reps: " + str(exercise_data['reps']))
                print("Sets: " + str(exercise_data['sets']))
                print("Weight: " + str(exercise_data['weight']))
                print("Times Completed: " + str(exercise_data['times']))
                break

def print_current_reps(data, exercise_to_find):
    data = load_json('my_progress.json')
    for muscle_group, _ in data['overload'].items():
        for exercise, _ in data['overload'][muscle_group].items():
            if exercise == exercise_to_find:
                exercise_data = data['overload'][muscle_group][exercise]['current']
                print("Reps: " + str(exercise_data['reps']))
                print("Sets: " + str(exercise_data['sets']))
                print("Weight: " + str(exercise_data['weight']))
                print("Times Completed: " + str(exercise_data['times']))
                break

def upgrade_exercise(file, exercise_to_find, reps=-1, sets=-1, weight=-1):
    data = load_json('my_progress.json')
    for muscle_group, _ in data['overload'].items():
        for exercise, _ in data['overload'][muscle_group].items():
            if exercise == exercise_to_find:
                exercise_data = data['overload'][muscle_group][exercise]['current']
                (data['overload'][muscle_group][exercise]['history']).append({'date': date.today().strftime("%m/%d/%Y"), 'reps': exercise_data['reps'], 'sets': exercise_data['sets'], 'weight': exercise_data['weight'], 'times': exercise_data['times']})
                if reps != -1:
                    data['overload'][muscle_group][exercise]['current']['reps'] = reps
                if sets != -1:
                    data['overload'][muscle_group][exercise]['current']['sets'] = sets
                if weight != -1:
                    data['overload'][muscle_group][exercise]['current']['weight'] = weight
                if reps != -1 or sets != -1 or weight != -1:
                    data['overload'][muscle_group][exercise]['current']['times'] = 0
                export_json(file, data)
                return

def increment_times(file, exercise_to_find):
    data = load_json('my_progress.json')
    for muscle_group, _ in data['overload'].items():
        for exercise, _ in data['overload'][muscle_group].items():
            if exercise == exercise_to_find:
                data['overload'][muscle_group][exercise]['current']['times'] = data['overload'][muscle_group][exercise]['current']['times'] + 1
                export_json(file, data)

def create_exercise(file, exercise_name, muscle_group_name, reps, sets, weight):
    data = load_json('my_progress.json')
    for muscle_group, _ in data['overload'].items():
        if muscle_group == muscle_group_name:
            if exercise_name not in data['overload'][muscle_group]:
                data['overload'][muscle_group][exercise_name] = {"current": {"reps": reps, "sets": sets, "weight": weight, "times": 0}, "history": []}
                export_json(file, data)
                return
            else:
                print("Exercise already exists")
                return
    print("Muscle group not found")

def remove_exercise(file, exercise_name, muscle_group_name):
    data = load_json('my_progress.json')
    for muscle_group, _ in data['overload'].items():
        if muscle_group == muscle_group_name:
            for exercise, _ in data['overload'][muscle_group].items():
                if exercise == exercise_name:
                    del data['overload'][muscle_group][exercise]
                    export_json(file, data)
                    return
            print("Exercise not found")
    print("Muscle group not found")

def create_muscle_group(file, muscle_group_name):
    data = load_json('my_progress.json')
    if muscle_group_name not in data['overload']:
        data['overload'][muscle_group_name] = {}
        export_json('my_progress.json', data)
    else:
        print("Muscle group already exists")

def remove_muscle_group(file, muscle_group_name):
    data = load_json('my_progress.json')
    try:
        del data['overload'][muscle_group_name]
        export_json(file, data)
    except:
        print("Muscle group not found")


if __name__ == "__main__":
    #print(data)
    #increment_times(data, "Test exercise")
    #upgrade_exercise(data, "Test exercise", sets=5, weight=50)
    #create_exercise(data, "Test exercise", "Biceps", 5, 10, 15)
    #remove_exercise(data, "Test exercise", "Biceps")
    #create_muscle_group(data, "Hands")
    #create_exercise(data, "Hand rotations", "Hands", 1, 2, 3)
    #remove_muscle_group(data, "Hands")
