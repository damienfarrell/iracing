import logging
import pymysql
from database import connect_mysql

def import_race_data(data, race, group):
    conn = connect_mysql()
    query = """
    INSERT INTO wp_iracing_results_teams (
    fin_pos, car_id, Car, car_class_id, car_class, team_id, cust_id, Name, start_pos, car_number, out_id, `Out`, `Interval`, laps_led, qualify_time, average_lap_time, fastest_lap_time, fastest_lap_number, laps_comp, Inc, club_id, Club, max_pct_fuel_fill, weight_penalty_kg, session_name, AI, race, `group`
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    with conn.cursor() as cursor:
        for result in data["session_results"][0]["results"]:
            cursor.execute(query, (
                result["finish_position"],
                result["car_id"],
                result["car_name"],
                result["car_class_id"],
                result["car_class_name"],
                result["cust_id"],
                result["cust_id"],
                result["display_name"],
                result["starting_position"],
                result["livery"]["car_number"],
                result["reason_out_id"],
                result["reason_out"],
                result["interval"],
                result["laps_lead"],
                result["best_qual_lap_at"],
                result["average_lap"],
                result["best_lap_time"],
                result["best_lap_num"],
                result["laps_complete"],
                result["incidents"],
                result["club_id"],
                result["club_name"],
                result["max_pct_fuel_fill"],
                result["weight_penalty_kg"],
                data.get("session_name"),
                result["ai"],
                race,
                group
            ))
        conn.commit()
    logging.info("Data imported into the database successfully.")