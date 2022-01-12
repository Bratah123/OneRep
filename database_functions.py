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


def get_squat(client_id):
    return DATABASE[client_id]["squat"]


def get_squat_url(client_id):
    return DATABASE[client_id]["squat_url"]


def get_bench(client_id):
    return DATABASE[client_id]["bench"]


def get_bench_url(client_id):
    return DATABASE[client_id]["bench_url"]


def get_deadlift(client_id):
    return DATABASE[client_id]["deadlift"]


def get_deadlift_url(client_id):
    return DATABASE[client_id]["deadlift_url"]


def get_clean_and_jerk(client_id):
    return DATABASE[client_id]["clean_and_jerk"]


def get_clean_and_jerk_url(client_id):
    return DATABASE[client_id]["clean_and_jerk_url"]


def get_snatch(client_id):
    return DATABASE[client_id]["snatch"]


def get_snatch_url(client_id):
    return DATABASE[client_id]["snatch_url"]


def user_exists(client_id):
    return DATABASE.get(client_id) is not None


def save_db():
    with open('database.json', 'w') as db:
        json.dump(DATABASE, db, indent=4)
