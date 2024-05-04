from db import get_connection, add_exercise
import csv

def login(connection, user):
    with connection.cursor() as cursor:
        cursor.execute("BEGIN;")

        cursor.execute("SELECT user_id FROM users WHERE name = %s;", (user,))
        uid = cursor.fetchone()

        if uid:
            # if user exits we chillin
            cursor.execute("COMMIT;")
            return uid[0] # to get the first one
        else:
            cursor.execute("INSERT INTO users (name) VALUES (%s) RETURNING user_id;", (user,))
            uid = cursor.fetchone()
            cursor.execute("COMMIT;")
            return uid


def user_inp(user):
    print('Choices [0, 1, 2, 3]:')
    print('[0] View Log')
    print('[1] View Workouts')
    print('[2] Find an exercise')
    print('[3] Quit')
    choice = input('Choice: ')
    return choice


# display items, then ask to perform crud
def view_log(connection, uid):
    # TODO
    with connection.cursor() as cur:
        # Execute the query to fetch all logs for the given user ID
        cur.execute("""
            SELECT log_id, routine_id, workout_id, date, rating
            FROM log
            WHERE user_id = %s;
        """, (uid,))
        logs = cur.fetchall()

        # Check if any logs were found
        if logs:
            return logs
        else:
            return "No logs found for this user."

def view_workout(connection, uid):
    # TODO
    with connection.cursor() as cur:
        # Execute the query to fetch all logs for the given user ID
        cur.execute("""
            SELECT workout_id, exercise_details, description
                FROM workout
            WHERE user_id = %s;
        """, (uid,))
        logs = cur.fetchall()

        # Check if any logs were found
        if logs:
            return logs
        else:
            return "No workouts found for this user."

def view_routine(connection, uid):
    # TODO
    with connection.cursor() as cur:
        # Execute the query to fetch all logs for the given user ID
        cur.execute("""
            SELECT routine_id, name, workout_ids, description
            FROM routine
            WHERE user_id = %s;
        """, (uid,))
        logs = cur.fetchall()

        # Check if any logs were found
        if logs:
            return logs
        else:
            return "No routines found for this user."

def add_exercises(connection, csv_file):
    with open(csv_file, newline='') as csvfile:
        exercise_reader = csv.reader(csvfile)
        next(exercise_reader)
        for row in exercise_reader:
            add_exercise(connection, row)
            # use add_exercise for singular additions
            print(row)

def new_exer():
    print("Please enter the details for the new exercise. Press ENTER without typing to skip.")

    fields = [
        "exercise_name", "difficulty_level", "target_muscle_group",
        "prime_mover_muscle", "secondary_muscle", "tertiary_muscle",
        "primary_equipment", "primary_items", "secondary_equipment",
        "secondary_items", "posture", "single_or_double_arm",
        "continuous_or_alternating_arms", "grip", "load_position_ending",
        "combination_exercises", "movement_pattern_1", "movement_pattern_2",
        "movement_pattern_3", "plane_of_motion_1", "plane_of_motion_2",
        "plane_of_motion_3", "body_region", "mechanics", "laterality",
        "exercise_classification"
    ]

    exercise = []
    for field in fields:
        value = input(f"Enter {field.replace('_', ' ').title()}: ").strip()
        exercise.append(value if value else None)
    return exercise

def find_exer(connection, search):
    search_pattern = f"%{search}%"

    with connection.cursor() as cursor:
        # Adjust the SQL query to only fetch the specific columns you're interested in
        cursor.execute("""
            SELECT exercise_id, exercise_name, target_muscle_group, body_region 
            FROM exercise
            WHERE exercise_name ILIKE %s
               OR target_muscle_group ILIKE %s
               OR prime_mover_muscle ILIKE %s
               OR secondary_muscle ILIKE %s
               OR body_region ILIKE %s
            LIMIT 10;
            """, (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern))
        results = cursor.fetchall()

    # Check if any results were found and print relevant information
    if results:
        print("Top results:")
        for result in results:
            # Print only the required fields
            print(f"ID: {result[0]}, Name: {result[1]}, Target Muscle Group: {result[2]}, Body Region: {result[3]}")
    else:
        print("No exercises found matching the search criteria.")

    return results


if __name__ == "__main__":
    print('Workout App')
    print('Please Log In')
    user = input('Name: ')
    connection = get_connection()
    # TODO
    # if exercises = 0, run this
    # add_exercises(connection, 'fixed_data.csv')

    uid = login(connection, user)
    choice = -1
    # sometype of if/else for choice
    search = input("Search for an exercise: ")

    find_exer(connection, search)

    connection.close()