import logging
from .database import connect_mysql

def fetch_session_data(session, url):
    """Fetch data from the given URL."""
    response = session.get(url)
    response.raise_for_status()
    response_link = response.json().get("link")
    if not response_link:
        raise ValueError("Failed to retrieve the data link.")
    response_data = session.get(response_link)
    response_data.raise_for_status()
    response_data = response_data.json()
    return response_data

def parse_data(response_data):

    parsed_data = []
    race = 1
    group = 50

    # Check if any of the keys are present in the response data
    key_found = False
    for session_result in response_data.get("session_results", []):
        if session_result.get("simsession_type_name") in ["Race"]:
            key_found = True
            break
    
    if not key_found:
        raise ValueError("None of the specified keys: 'Race' were found in the response data")

    for session_result in response_data["session_results"]:
        if session_result.get("simsession_type_name") in ["Race"]:
            for result in session_result["results"]:
                processed_result = {
                    "finish_position": result["finish_position"],
                    "car_id": result["car_id"],
                    "car_name": result["car_name"],
                    "car_class_id": result["car_class_id"],
                    "car_class_name": result["car_class_name"],
                    "cust_id": result["cust_id"],
                    "display_name": result["display_name"],
                    "starting_position": result["starting_position"],
                    "car_number": result["livery"]["car_number"],
                    "reason_out_id": result["reason_out_id"],
                    "reason_out": result["reason_out"],
                    "interval": result["interval"],
                    "laps_lead": result["laps_lead"],
                    "best_qual_lap_at": result["best_qual_lap_at"],
                    "average_lap": result["average_lap"],
                    "best_lap_time": result["best_lap_time"],
                    "best_lap_num": result["best_lap_num"],
                    "laps_complete": result["laps_complete"],
                    "incidents": result["incidents"],
                    "club_id": result["club_id"],
                    "club_name": result["club_name"],
                    "max_pct_fuel_fill": result["max_pct_fuel_fill"],
                    "weight_penalty_kg": result["weight_penalty_kg"],
                    "session_name": response_data.get("session_name"),
                    "ai": result["ai"],
                    "race":race,
                    "group":group,
                    "test":session_result.get("simsession_type_name"),
                    "test2":session_result.get("simsession_name")
                }
                parsed_data.append(processed_result)
            race += 1
            group += 50
    
    return parsed_data

def import_race_data(parsed_data):
    conn = connect_mysql()
    query = """
    INSERT INTO wp_iracing_results_teams (
    fin_pos, car_id, Car, car_class_id, car_class, team_id, cust_id, Name, start_pos, car_number, out_id, `Out`, `Interval`, laps_led, qualify_time, average_lap_time, fastest_lap_time, fastest_lap_number, laps_comp, Inc, club_id, Club, max_pct_fuel_fill, weight_penalty_kg, session_name, AI, race, `group`
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    with conn.cursor() as cursor:
        for result in parsed_data:
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
                result["car_number"],
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
                result["session_name"],
                result["ai"],
                result["race"],
                result["group"]
            ))
        conn.commit()
    logging.info("Data imported into the database successfully.")