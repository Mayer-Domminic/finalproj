import csv
import psycopg
from analytics import *

# SQL TABLE STRINGS
exercise = """
CREATE TABLE exercise (
    exercise_id SERIAL PRIMARY KEY,
    exercise_name VARCHAR(255),
    difficulty_level VARCHAR(255),
    target_muscle_group VARCHAR(255),
    prime_mover_muscle VARCHAR(255),
    secondary_muscle VARCHAR(255),
    tertiary_muscle VARCHAR(255),
    primary_equipment VARCHAR(255),
    primary_items VARCHAR(255),
    secondary_equipment VARCHAR(255),
    secondary_items VARCHAR(255),
    posture VARCHAR(255),
    single_or_double_arm VARCHAR(255),
    continuous_or_alternating_arms VARCHAR(255),
    grip VARCHAR(255),
    load_position_ending VARCHAR(255),
    combination_exercises VARCHAR(255),
    movement_pattern_1 VARCHAR(255),
    movement_pattern_2 VARCHAR(255),
    movement_pattern_3 VARCHAR(255),
    plane_of_motion_1 VARCHAR(255),
    plane_of_motion_2 VARCHAR(255),
    plane_of_motion_3 VARCHAR(255),
    body_region VARCHAR(255),
    mechanics VARCHAR(255),
    laterality VARCHAR(255),
    exercise_classification VARCHAR(255)
);
"""
user = """
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);
"""
workout = """
CREATE TABLE workout (
    workout_id SERIAL PRIMARY KEY,
    user_id INT,
    exercise_id INT,
    sets INT,
    reps INT[],
    weights INT[],
    date DATE,
    description TEXT
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (exercise_id) REFERENCES exercise(exercise_id)
);
"""
routine = """
CREATE TABLE routine (
    routine_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    user_id INT REFERENCES users(user_id),
    workout_ids INT[],
    description TEXT
);
"""
log = """
CREATE TABLE log (
    log_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    routine_id INT REFERENCES routine(routine_id),
    date DATE,
    rating TEXT,
    CHECK (routine_id IS NOT NULL)
);
"""


# postgres main commands (for random purposes)
def get_connection():
    return psycopg.connect(
        dbname="workout",
        user="postgres",
        password="abc123",
        host="localhost",
        port="5432"
    )
def create_tables(connection):
    with connection.cursor() as cursor:
        cursor.execute(user)
        cursor.execute(routine)
        cursor.execute(exercise)
        cursor.execute(workout)
        cursor.execute(log)
    connection.commit()
    print("created tables")
def drop_tables(connection):
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS exercise;")
        cursor.execute("DROP TABLE IF EXISTS log;")
        cursor.execute("DROP TABLE IF EXISTS routine;")
        cursor.execute("DROP TABLE IF EXISTS workout;")
        cursor.execute("DROP TABLE IF EXISTS users;")
    connection.commit()
    print("dropped tables")
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


# ADD FUNCTIONS (SQL)
def add_workout(connection, user_id, exercise_id, sets, reps, weights, date, description):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO workout (user_id, exercise_id, sets, reps, weights, date, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING workout_id;
                """, (user_id, exercise_id, sets, reps, weights, date, description))
            connection.commit()
            workout_id = cursor.fetchone()[0]
            return workout_id
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        return None
def add_log(connection, user_id, routine_id, date, rating):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO log (user_id, routine_id, date, rating)
                VALUES (%s, %s, %s, %s)
                RETURNING log_id;
                """, (user_id, routine_id, date, rating))
            connection.commit()
            log_id = cursor.fetchone()[0]
            return log_id
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
        return None
def add_routine(connection, user_id, name, workouts, description):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO routine (name, user_id, workout_ids, description)
            VALUES (%s, %s, %s, %s) RETURNING routine_id;
            """, (name, user_id, workouts, description))
            connection.commit()
            return True
        return False
    except Exception as e:
        print(f"An error occursorred: {e}")
        connection.rollback()
        return None
def add_exercise(connection, exercise):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO exercise (
                    exercise_name, difficulty_level, target_muscle_group,
                    prime_mover_muscle, secondary_muscle, tertiary_muscle,
                    primary_equipment, primary_items, secondary_equipment,
                    secondary_items, posture, single_or_double_arm,
                    continuous_or_alternating_arms, grip, load_position_ending,
                    combination_exercises, movement_pattern_1, movement_pattern_2,
                    movement_pattern_3, plane_of_motion_1, plane_of_motion_2,
                    plane_of_motion_3, body_region, mechanics, laterality,
                    exercise_classification
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING exercise_id;
                """, exercise)
            connection.commit()
            return cursor.fetchone()[0]
    except Exception as e:
        print(f"An error occursorred: {e}")
        connection.rollback()
        return None


# MANAGE
def manage_logs(connection, user_id):
    while True:
        print("\nLog Management:")
        print("1. View Last 5 Logs")
        print("2. Create New Log")
        print("3. Delete a Log")
        print("4. Return to Main Menu")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            view_last_logs(connection, user_id)
        elif choice == '2':
            create_new_log(connection, user_id)
        elif choice == '3':
            delete_log(connection, user_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice, please choose again.")
def manage_routines(connection, user_id):
    while True:
        print("\nRoutine Management:")
        print("1. View Last 5 Routines")
        print("2. Create New Routine")
        print("3. Edit an Existing Routine")
        print("4. Delete a Routine")
        print("5. Return to Main Menu")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            view_last_routines(connection, user_id)
        elif choice == '2':
            create_new_routine(connection, user_id)
        elif choice == '3':
            edit_routine(connection, user_id)
        elif choice == '4':
            delete_routine(connection, user_id)
        elif choice == '5':
            break
        else:
            print("Invalid choice, please choose again.")
def manage_workouts(connection, user_id):
    while True:
        print("\nWorkout Management:")
        print("1. View Last 5 Workouts")
        print("2. Create New Workout")
        print("3. Delete a Workout")
        print("4. Return to Main Menu")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            view_last_workouts(connection, user_id)
        elif choice == '2':
            create_new_workout(connection, user_id)
        elif choice == '3':
            delete_workout(connection, user_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice, please choose again.")
def manage_exercises(connection):
    while True:
        print("\nExercise Management:")
        print("1. Search for an Exercise")
        print("2. Create a New Exercise")
        print("3. Return to Main Menu")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            exercise_id = search_exercise(connection)
            if exercise_id:
                exercise_decision(connection, exercise_id)
        elif choice == '2':
            create_new_exercise(connection)
        elif choice == '3':
            break
        else:
            print("Invalid choice, please choose again.")
def exercise_decision(connection, exercise_id):
    print("\nSelected Exercise ID:", exercise_id)
    print("1. Edit this Exercise")
    print("2. Delete this Exercise")

    decision = input("What would you like to do? (edit/delete): ")
    if decision.lower() == 'edit':
        edit_exercise(connection, exercise_id)
    elif decision.lower() == 'delete':
        delete_exercise(connection, exercise_id)


# VIEW
def view_last_logs(connection, user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT log_id, date, rating, routine_id FROM log
                WHERE user_id = %s
                ORDER BY date DESC
                LIMIT 5;
                """, (user_id,))
        logs = cursor.fetchall()

        if not logs:
            print("No recent logs found.")
            return

        print("\nLast 5 Logs:")
        for log in logs:
            cursor.execute("SELECT name FROM routine WHERE routine_id = %s", (log[3],))
            routine = cursor.fetchone()
            routine_name = routine[0] if routine else "Unknown Routine"

            print(f"Log ID: {log[0]}, Date: {log[1]}, Rating: {log[2]}, Routine: {routine_name}")
def view_last_routines(connection, user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT routine_id, name, description FROM routine
            WHERE user_id = %s
            ORDER BY routine_id DESC
            LIMIT 5;
            """, (user_id,))
        routines = cursor.fetchall()
        if routines:
            for routine in routines:
                print(f"Routine ID: {routine[0]}, Name: {routine[1]}, Description: {routine[2]}")
        else:
            print("No recent routines found.")
def view_last_workouts(connection, user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT workout_id, exercise_id, sets, reps, weights, date, description FROM workout
            WHERE user_id = %s
            ORDER BY date DESC
            LIMIT 5;
            """, (user_id,))
        workouts = cursor.fetchall()
        if workouts:
            for workout in workouts:
                print(f"Workout ID: {workout[0]}, Description: {workout[6]}, Date: {workout[5]}, Exercise ID: {workout[1]}, Sets: {workout[2]}, Reps: {workout[3]}, Weight: {workout[4]}")
        else:
            print("No recent workouts found.")
def view_analytics(connection, user_id):
    while True:
        print("\nAnalytics Menu:")
        print("1. Workout Frequency")
        print("2. Routine Weight Progression")
        print("3. Max Weight Lifted Over Time")
        print("4. Return to Main Menu")

        choice = input("Select an analytics option (1-4): ")

        if choice == '1':
            timeframe = input("Enter timeframe (week/month): ")
            data = fetch_workout_frequency(connection, user_id, timeframe)
            if not data.empty:
                plot_workout_frequency(data)
            else:
                print("No workout data available for this period.")
        elif choice == '2':
            routines = fetch_routines(connection, user_id)
            if routines:
                routine_choice = int(input("Select the number of the routine to analyze: "))
                print(routine_choice)
                if routine_choice < len(routines)+1:
                    print(routines)
                    routine_id = routines[routine_choice-1][0]
                    routine_name = routines[routine_choice-1][1]
                    print(routine_name, routine_id, len(routines))
                    data = fetch_routine_progress(connection, user_id, routine_id)
                    if not data.empty:
                        plot_weight_progression(data, f"Routine: {routine_name}")
                    else:
                        print("No weight data found for the specified routine.")
                else:
                    print("Invalid routine selection. Please select a number from the list.")
            else:
                print("No routines available to analyze.")
        elif choice == '3':
            data = fetch_max_weight_data(connection, user_id)
            if not data.empty:
                plot_max_weight(connection, user_id)
            else:
                print("No max weight data available.")
        elif choice == '4':
            break
        else:
            print("Invalid choice, please choose again.")


# CREATE
def create_new_log(connection, user_id):
    print("\nCreating a New Log:")
    routines = fetch_routines(connection, user_id)
    if not routines:
        print("No routines available to log.")
        return

    try:
        routine_choice = int(input("Select the number of the routine you want to log: "))
        if routine_choice < 0 or routine_choice >= len(routines):
            print("Invalid selection. Please try again.")
            return
        routine_id = routines[routine_choice][0]
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return

    date = input("Enter date (YYYY-MM-DD): ")
    rating = input("Enter your rating or feedback: ")

    # Add the log with the selected routine
    if add_log(connection, user_id, routine_id, date, rating):
        print("Log created successfully!")
    else:
        print("Log failed to create.")
def create_new_routine(connection, user_id):
    print("\nCreating a New Routine:")
    routine_name = input("Enter the routine name: ")
    description = input("Enter a description for the routine: ")

    workouts = []
    while True:
        workout_name = input("Enter workout name to search and add (or enter 'done' to finish): ")
        if workout_name.lower() == 'done':
            break
        workout_id = select_workout(connection, workout_name)
        if workout_id:
            workouts.append(workout_id)
        else:
            print("No workout found. Try again.")
    add_routine(connection, user_id, routine_name, workouts, description)
def create_new_workout(connection, user_id):
    print("\nCreating a New Workout:")
    description = input("Enter a description for the workout: ")
    while True:
        exercise_name = input("Enter an *Exercise* name to search or type 'new': ")

        if exercise_name.lower() == 'new':
            exercise_id = create_new_exercise(connection)
            if exercise_id:
                print(f"New exercise created with ID: {exercise_id}")
                break
            else:
                print("Failed to create a new exercise. Please try again.")
                continue

        exercise_id = select_exercise(connection, exercise_name)
        if not exercise_id:
            print("No exercise found matching your query.")
            continue_option = input("Would you like to continue searching or create a new exercise? (continue/create): ")
            if continue_option.lower() == 'create':
                exercise_id = create_new_exercise(connection)
                if exercise_id:
                    print(f"New exercise created with ID: {exercise_id}")
                    break
                else:
                    print("Failed to create a new exercise. Please try again.")
            else:
                continue
        else:
            use_existing = input(f"Found exercise with ID {exercise_id}. Use this exercise? (yes/no): ")
            if use_existing.lower() == 'yes':
                break
            else:
                continue

    sets = int(input("Enter number of sets: "))
    reps = list(map(int, input("Enter reps for each set separated by space: ").split()))
    include_weights = input("Do you want to include weights for each set? (yes/no): ")
    weights = []
    if include_weights.lower() == 'yes':
        weights = list(map(int, input("Enter weights for each set separated by space: ").split()))
        if len(weights) != sets:
            print("Number of weights does not match number of sets. Using default weights.")
            weights = []
    date = input("Enter date (YYYY-MM-DD): ")

    add_workout(connection, user_id, exercise_id, sets, reps, weights, date, description)
def create_new_exercise(connection):
    print("\nEnter new exercise details (type 'quit' at any point to stop entering and set all following to None):")

    fields = [
        "Exercise name", "Difficulty level", "Target muscle group",
        "Prime mover muscle", "Secondary muscle", "Tertiary muscle",
        "Primary equipment", "Primary items", "Secondary equipment",
        "Secondary items", "Posture", "Single or double arm",
        "Continuous or alternating arms", "Grip", "Load position ending",
        "Combination exercises", "Movement pattern 1", "Movement pattern 2",
        "Movement pattern 3", "Plane of motion 1", "Plane of motion 2",
        "Plane of motion 3", "Body region", "Mechanics", "Laterality",
        "Exercise classification"
    ]

    exercise_details = []
    quit_entered = False

    for field in fields:
        if quit_entered:
            exercise_details.append(None)
        else:
            input_value = input(f"Enter {field}: ").strip()
            if input_value.lower() == 'quit':
                exercise_details.extend([None] * (len(fields) - len(exercise_details)))
                break
            else:
                exercise_details.append(input_value if input_value else None)

    exercise_id = add_exercise(connection, tuple(exercise_details))


# SELECT
def select_exercise(connection, exercise_name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT exercise_id, exercise_name FROM exercise
            WHERE exercise_name ILIKE %s LIMIT 8;
            """, ('%' + exercise_name + '%',))
        exercises = cursor.fetchall()
        if not exercises:
            return None
        for i, (id, name) in enumerate(exercises, 1):
            print(f"{i}. {name} (ID: {id})")
        choice = int(input("Select an exercise number: "))
        return exercises[choice - 1][0]
def select_workout(connection, workout_name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT workout_id, description FROM workout
            WHERE description ILIKE %s LIMIT 8;
            """, ('%' + workout_name + '%',))
        workouts = cursor.fetchall()
        if not workouts:
            return None
        for i, (id, description) in enumerate(workouts, 1):
            print(f"{i}. {description} (ID: {id})")
        choice = int(input("Select a workout number: "))
        return workouts[choice - 1][0]
def search_exercise(connection):
    search_term = input("Enter exercise name to search: ")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT exercise_id, exercise_name FROM exercise
            WHERE exercise_name ILIKE %s ORDER BY exercise_name;
            """, ('%' + search_term + '%',))
        exercises = cursor.fetchall()

        if not exercises:
            print("No exercises found.")
            return None

        print("Search Results:")
        for i, (id, name) in enumerate(exercises, 1):
            print(f"{i}. {name} (ID: {id})")

        choice = int(input("Select an exercise number: "))
        if 1 <= choice <= len(exercises):
            selected_id = exercises[choice - 1][0]
            print(f"Selected Exercise ID: {selected_id}")
            return selected_id
        else:
            print("Invalid choice.")
            return None


# FETCH
def fetch_routines(connection, user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT routine_id, name FROM routine
            WHERE user_id = %s ORDER BY routine_id DESC;
            """, (user_id,))
        routines = cursor.fetchall()
        if not routines:
            print("No routines found.")
            return None
        print("Available Routines:")
        for i, routine in enumerate(routines, 1):
            print(f"{i}. {routine[1]} (ID: {routine[0]})")
        return routines
def fetch_workouts(connection, user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT workout_id, date, description FROM workout
            WHERE user_id = %s ORDER BY date DESC;
            """, (user_id))
        workouts = cursor.fetchall()
        if not workouts:
            return None
        for workout in workouts:
            print(f"Workout ID: {workout[0]}, Date: {workout[1]}, Description: {workout[2]}")
        return workouts
def fetch_logs(connection, user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT log_id, date FROM log
            WHERE user_id = %s ORDER BY date DESC;
            """, (user_id,))
        logs = cursor.fetchall()
        if not logs:
            return None
        for log in logs:
            print(f"Log ID: {log[0]}, Date: {log[1]}")
        return logs


# EDIT
def edit_routine(connection, user_id):
    print("Available Routines:")
    routines = fetch_routines(connection, user_id)

    routine_id = input("Enter the ID of the routine you want to edit: ")

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT name, description, workouts FROM routine
            WHERE routine_id = %s;
            """, (routine_id,))
        routine = cursor.fetchone()
        if not routine:
            print("Routine not found.")
            return


    new_name = input(f"Enter new name or press enter to keep ({routine[0]}): ")
    new_description = input(f"Enter new description or press enter to keep ({routine[1]}): ")
    new_workouts = input("Enter new list of workout IDs separated by commas or press enter to keep: ")

    # use old values if no input
    new_name = new_name.strip() or routine[0]
    new_description = new_description.strip() or routine[1]
    new_workouts = new_workouts.strip() or routine[2]

    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE routine SET name = %s, description = %s, workouts = %s
            WHERE routine_id = %s;
            """, (new_name, new_description, new_workouts, routine_id))
        connection.commit()
        print("Routine updated successfully.")
def edit_exercise(connection, exercise_id):
    print("\nEdit Exercise Details:")

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM exercise WHERE exercise_id = %s", (exercise_id,))
        exercise = cursor.fetchone()

        columns = [desc[0] for desc in cursor.description]
        for index, (col, value) in enumerate(zip(columns, exercise), 1):
            print(f"{index}. {col}: {value}")

        try:
            field_index = int(input("Enter the number of the field you want to edit: ")) - 1
            if field_index < 1 or field_index >= len(columns):
                print("Invalid field number. Operation cancelled.")
                return

            new_value = input(f"Enter new value for {columns[field_index]}: ")
            sql_update = f"UPDATE exercise SET {columns[field_index]} = %s WHERE exercise_id = %s"

            cursor.execute(sql_update, (new_value, exercise_id))
            connection.commit()
            print(f"{columns[field_index]} updated successfully.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"Failed to update exercise: {e}")
            connection.rollback()


# DELETE
def delete_log(connection, user_id):
    print("Available Logs:")
    logs = fetch_logs(connection, user_id)
    if not logs:
        print("No logs available to delete.")
        return

    log_id = input("Enter the ID of the log to delete: ")
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM log WHERE user_id = %s AND log_id = %s;
            """, (user_id, log_id))
        connection.commit()
        if cursor.rowcount:
            print("Log deleted successfully.")
        else:
            print("Log not found or could not be deleted.")
def delete_routine(connection, user_id):
    print("Available Routines:")
    routines = fetch_routines(connection, user_id)

    routine_id = input("Enter the ID of the routine to delete: ")
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM routine WHERE user_id = %s AND routine_id = %s;
            """, (user_id, routine_id))
        connection.commit()
        if cursor.rowcount:
            print("Routine deleted successfully.")
        else:
            print("Routine not found or could not be deleted.")
def delete_workout(connection, user_id):
    print("Available Workouts:")
    workouts = fetch_workouts(connection, user_id)
    if not workouts:
        print("No workouts available to delete.")
        return

    workout_id = input("Enter the ID of the workout to delete: ")
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM workout WHERE user_id = %s AND workout_id = %s;
            """, (user_id, workout_id))
        connection.commit()
        if cursor.rowcount:
            print("Workout deleted successfully.")
        else:
            print("Workout not found or could not be deleted.")
def delete_exercise(connection, exercise_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM exercise WHERE exercise_id = %s", (exercise_id,))
        connection.commit()
        print(f"Exercise with ID {exercise_id} deleted successfully.")


# IMPORT BIG DATA!!!
def check_exercises_exist(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM exercise LIMIT 1);")
        exists = cursor.fetchone()[0]
        return exists
def add_exercises(connection, csv_file):
    i = 0
    with connection.cursor() as cursor:
        with open(csv_file, newline='') as csvfile:
            exercise_reader = csv.reader(csvfile)
            next(exercise_reader)
            for row in exercise_reader:
                cursor.execute(
                    """
                    INSERT INTO exercise (
                        exercise_name, difficulty_level, target_muscle_group,
                        prime_mover_muscle, secondary_muscle, tertiary_muscle,
                        primary_equipment, primary_items, secondary_equipment,
                        secondary_items, posture, single_or_double_arm,
                        continuous_or_alternating_arms, grip, load_position_ending,
                        combination_exercises, movement_pattern_1, movement_pattern_2,
                        movement_pattern_3, plane_of_motion_1, plane_of_motion_2,
                        plane_of_motion_3, body_region, mechanics, laterality,
                        exercise_classification
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, row)
                i = i + 1
        connection.commit()
    print(i)


# MAIN
def main_menu(connection, user_id):
    while True:
        print("\nMain Menu:")
        print("1. Manage Logs")
        print("   - Logs: Track and rate your experiences with routines.")
        print("2. Manage Routines")
        print("   - Routines: Create, edit, or delete collections of workouts.")
        print("3. Manage Workouts")
        print("   - Workouts: Log specific exercises, including sets and reps, on a given date.")
        print("4. Manage Exercises")
        print("   - Exercises: Add new exercises, search for existing ones, or modify exercise details.")
        print("5. View Analytics")
        print("   - Analytics: View workout frequencies, weight progression, and other performance insights.")
        print("6. Exit")
        print("   - Exit the application.")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            manage_logs(connection, user_id)
        elif choice == '2':
            manage_routines(connection, user_id)
        elif choice == '3':
            manage_workouts(connection, user_id)
        elif choice == '4':
            manage_exercises(connection, user_id)
        elif choice == '5':
            view_analytics(connection, user_id)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please choose again.")


if __name__ == "__main__":
    print('Workout App')
    print('Please Log In')
    user = input('Name: ')
    connection = get_connection()

    if not check_exercises_exist(connection):
        print("No exercises found, loading from CSV...")
        add_exercises(connection, 'fixed_data.csv')
    else:
        print("Exercises are already loaded in the database.")

    uid = login(connection, user)
    main_menu(connection, uid)

    connection.close()