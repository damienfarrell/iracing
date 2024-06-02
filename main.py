import requests
import pandas as pd
import os
import json

CSV_FILE_PATH = "data.csv"

with open('data.json', 'r') as file:
    data = json.load(file)

results = []
for result in data["session_results"][0]["results"]:
    results.append({
        "Fin Pos": result["finish_position"],
        "Car ID": result["car_id"],
        "Car": result["car_name"],
        "Car Class ID": result["car_class_id"],
        "Car Class": result["car_class_name"],
        "Team ID": result["cust_id"],
        "Cust ID": result["cust_id"],
        "Name": result["display_name"],
        "Start Pos": result["starting_position"],
        "Car #": result["livery"]["car_number"],
        "Out ID": result["reason_out_id"],
        "Out": result["reason_out"],
        "Interval": result["interval"],
        "Laps Led": result["laps_lead"],
        "Qualify Time": result["best_qual_lap_at"],
        "Average Lap Time": result["average_lap"],
        "Fastest Lap Time": result["best_lap_time"],
        "Fast Lap#": result["best_lap_num"],
        "Laps Comp": result["laps_complete"],
        "Inc": result["incidents"],
        "Club ID": result["club_id"],
        "Club": result["club_name"],
        "Max Fuel Fill%": result["max_pct_fuel_fill"],
        "Weight Penalty (KG)": result["weight_penalty_kg"],
        "Session Name": data.get("session_name"),
        "AI": result["ai"],
        "race": 1,
        "group": 6  
    })

df = pd.DataFrame(results)

df.to_csv(CSV_FILE_PATH, index=False)

print(f"Data has been exported to {CSV_FILE_PATH}")

print(df)