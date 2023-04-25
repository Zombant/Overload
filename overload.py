#!/usr/bin/env python3

import json
from datetime import date
import sys
import argparse
import os

def load_json(file):
    with open(file, 'r') as f:
        return json.loads(f.read())

def export_json(file, data):
    json_string = json.dumps(data, indent=2)
    with open(file, 'w') as f:
        f.write(json_string)

def new_log(file):
    overload = {"overload": {}}
    export_json(file, overload)

def print_muscle_groups(file):
    data = load_json(file)
    for muscle_group, _ in data['overload'].items():
        print(muscle_group + ": " + str(len(data['overload'][muscle_group].items())))

def print_exercises(file, muscle_group):
    data = load_json(file)
    for exercise, _ in data['overload'][muscle_group].items():
        print(exercise)

def print_current_status(file, exercise_to_find):
    data = load_json(file)
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
    data = load_json(file)
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
    data = load_json(file)
    for muscle_group, _ in data['overload'].items():
        for exercise, _ in data['overload'][muscle_group].items():
            if exercise == exercise_to_find:
                data['overload'][muscle_group][exercise]['current']['times'] = data['overload'][muscle_group][exercise]['current']['times'] + 1
                export_json(file, data)

def create_exercise(file, exercise_name, muscle_group_name, reps, sets, weight, times):
    data = load_json(file)
    for muscle_group, _ in data['overload'].items():
        if muscle_group == muscle_group_name:
            if exercise_name not in data['overload'][muscle_group]:
                data['overload'][muscle_group][exercise_name] = {"current": {"reps": reps, "sets": sets, "weight": weight, "times": times}, "history": []}
                export_json(file, data)
                return
            else:
                print("Exercise already exists")
                return
    print("Muscle group not found")

def remove_exercise(file, exercise_name):
    data = load_json(file)
    for muscle_group, _ in data['overload'].items():
        for exercise, _ in data['overload'][muscle_group].items():
            if exercise == exercise_name:
                del data['overload'][muscle_group][exercise]
                export_json(file, data)
                return
    print("Exercise not found")

def create_muscle_group(file, muscle_group_name):
    data = load_json(file)
    if muscle_group_name not in data['overload']:
        data['overload'][muscle_group_name] = {}
        export_json(file, data)
    else:
        print("Muscle group already exists")

def remove_muscle_group(file, muscle_group_name):
    data = load_json(file)
    try:
        del data['overload'][muscle_group_name]
        export_json(file, data)
    except:
        print("Muscle group not found")


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--file", action='store', required=False, default=os.path.expanduser('~') + "/.local/share/overloadprogress.json", help="specifies the file. (default: ~/.local/share/overloadprogress.json")
    argParser.add_argument("-p", "--print", action='store_true', required=False, help="print (prints list of muscle groups by default)")
    argParser.add_argument("-n", "--new", action='store_true', required=False, help="create a new log")
    argParser.add_argument("-u", "--upgrade", action='store_true', required=False, help="upgrades an exercise")
    argParser.add_argument("-i", "--increment", action='store_true', required=False, help="increments an exercise")
    argParser.add_argument("-d", "--delete", action='store_true', required=False, help="deletes an exercise or group")
    argParser.add_argument("-c", "--create", action='store_true', required=False, help="creates an exercise or group")
    argParser.add_argument("-g", "--group", action='store', required=False, help="specifies the muscle group")
    argParser.add_argument("-e", "--exercise", action='store', required=False, help="specifies the exercise")
    argParser.add_argument("-r", "--reps", action='store', type=int, required=False, help="specifies the number of reps")
    argParser.add_argument("-s", "--sets", action='store', type=int, required=False, help="specifies the number of sets")
    argParser.add_argument("-w", "--weight", action='store', type=int, required=False, help="specifies the number of weights")
    argParser.add_argument("-t", "--times", action='store', type=int, required=False, default=0, help="specifies the number of times completed")
    
    args = argParser.parse_args()

    if args.print:
        if args.group != None:
            print_exercises(args.file, args.group)
        elif args.exercise != None:
            print_current_status(args.file, args.exercise)
        else:
            print_muscle_groups(args.file)
    elif args.new:
        new_log(args.file)
    elif args.upgrade:
        upgrade_exercise(args.file, args.exercise, reps=args.reps, sets=args.sets, weight=args.weight)
    elif args.increment:
        increment_times(args.file, args.exercise)
    elif args.delete:
        if args.group != None:
            remove_muscle_group(args.file, args.group)
        elif args.exercise != None:
            remove_exercise(args.file, args.exercise)
    elif args.create:
        if args.exercise != None:
            create_exercise(args.file, args.exercise, args.group, reps=args.reps, sets=args.sets, weight=args.weight, times=args.times)
        elif args.group != None:
            create_muscle_group(args.file, args.group)
