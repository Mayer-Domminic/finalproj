import pandas as pd
import plotly.express as px

def fetch_workout_frequency(connection, user_id, timeframe='month'):
    with connection.cursor() as cursor:
        if timeframe == 'month':
            cursor.execute("""
                SELECT DATE_TRUNC('month', date) AS period, COUNT(*) AS workout_count
                FROM workout
                WHERE user_id = %s
                GROUP BY period
                ORDER BY period;
                """, (user_id,))
        else:  # week
            cursor.execute("""
                SELECT DATE_TRUNC('week', date) AS period, COUNT(*) AS workout_count
                FROM workout
                WHERE user_id = %s
                GROUP BY period
                ORDER BY period;
                """, (user_id,))

        results = cursor.fetchall()
        if results:
            return pd.DataFrame(results, columns=['period', 'workout_count'])
        else:
            return pd.DataFrame(columns=['period', 'workout_count'])

def plot_workout_frequency(data):
    fig = px.bar(data, x='period', y='workout_count', title='Workout Frequency Over Time',
                 labels={'period': 'Period', 'workout_count': 'Number of Workouts'})
    fig.show()

def fetch_routine_progress(connection, user_id, routine_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT workout_ids FROM routine
            WHERE routine_id = %s AND user_id = %s;
            """, (routine_id, user_id))
        workout_ids = cursor.fetchone()
        if not workout_ids or not workout_ids[0]:
            return pd.DataFrame(columns=['date', 'weight'])

        cursor.execute("""
            SELECT date, unnest(weights) as weight
            FROM workout
            WHERE workout_id = ANY(%s)
            ORDER BY date;
            """, (workout_ids[0],))

        results = cursor.fetchall()
        if results:
            return pd.DataFrame(results, columns=['date', 'weight'])
        else:
            return pd.DataFrame(columns=['date', 'weight'])

def plot_weight_progression(data, routine_desc):
    if not data.empty:
        average_weight_data = data.groupby('date')['weight'].mean().reset_index()
        average_weight_data.rename(columns={'weight': 'average_weight'}, inplace=True)
        fig = px.line(average_weight_data, x='date', y='average_weight', title=f'Weight Progression for {routine_desc}',
                      labels={'date': 'Date', 'average_weight': 'Average Weight (lbs)'})
        fig.show()
    else:
        print(f"No weight data available for {routine_desc}.")

def plot_max_weight(connection, user_id):
    data = fetch_max_weight_data(connection, user_id)
    if not data.empty:
        fig = px.line(data, x='date', y='max_weight', title='Max Weight Lifted Over Time',
                      labels={'date': 'Date', 'max_weight': 'Max Weight (lbs)'})
        fig.show()
    else:
        print("No data found for max weights.")

def fetch_max_weight_data(connection, user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT date, MAX(weight) AS max_weight
            FROM workout,
                 LATERAL unnest(weights) AS weight
            WHERE user_id = %s
            GROUP BY date
            ORDER BY date;
            """, (user_id,))
        results = cursor.fetchall()
        if results:
            return pd.DataFrame(results, columns=['date', 'max_weight'])
        else:
            return pd.DataFrame(columns=['date', 'max_weight'])