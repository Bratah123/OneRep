import json

"""
File for editing the database.json file.
database structure:
{
    client_id: {

        # Powerlifting section
        "squat": int_value_here,
        "squat_url": "video of squat here",

        "bench": int_value_here,
        "bench_url": "video of bench press here",

        "deadlift": int_value_here,
        "deadlift_url": "video of deadlift here",

        # Weightlifting section
        "clean_and_jerk": int_value_here,
        "clean_and_jerk_url": "video of C&J here",

        "snatch": int_value_here,
        "snatch_url": "snatch url"
    }
}
"""

# a global variable that caches the database so that we don't have to keep rewriting the file
with open('database.json', 'r') as f:
    DATABASE = json.load(f)


def create_new_profile(client_id):
    DATABASE[client_id] = {
        # Powerlifting section
        "squat": 0,
        "squat_url": "video of squat here",

        "bench": 0,
        "bench_url": "",

        "deadlift": 0,
        "deadlift_url": "",

        # Weightlifting section
        "clean_and_jerk": 0,
        "clean_and_jerk_url": "",

        "snatch": 0,
        "snatch_url": ""
    }


def user_exists(client_id):
    return DATABASE.get(client_id) is not None


def save_db():
    with open('database.json', 'w') as f:
        json.dump(DATABASE, f, indent=4)
