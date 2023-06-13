import json
import csv
import os
import datetime


def json_to_csv(json_data_directory, csv_output_directory, status_csv_path):
    # Get the list of JSON files in the input directory
    json_files = [file for file in os.listdir(json_data_directory) if file.endswith('.json')]

    # Check if the status.csv file already exists
    is_status_csv_exists = os.path.isfile(status_csv_path)

    # Load the existing status file, if it exists
    if is_status_csv_exists:
        with open(status_csv_path, 'r') as status_file:
            status_csv_reader = csv.reader(status_file)
            processed_files = [row[0] for row in status_csv_reader]
    else:
        processed_files = []

    # Open the status.csv file in append mode
    with open(status_csv_path, 'a', newline='') as status_file:
        # Create a CSV writer
        status_csv_writer = csv.writer(status_file)

        # If the status.csv file doesn't exist, write the header row
        if not is_status_csv_exists:
            status_csv_writer.writerow(['File Name', 'Time'])

        for json_file in json_files:
            # Skip processing if the file has already been processed
            if json_file in processed_files:
                print(f"Skipping '{json_file}' as it has already been processed.")
                continue

            # Get the full path of the JSON file
            json_file_path = os.path.join(json_data_directory, json_file)

            # Create the output CSV file path by replacing the file extension
            csv_file = os.path.splitext(json_file)[0] + '.csv'
            csv_file_path = os.path.join(csv_output_directory, csv_file)

            # Process the JSON file and convert it to CSV
            with open(json_file_path, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    print(f"Error: Invalid JSON format in file '{json_file}'. Skipping...")
                    continue

                if not data:
                    print(f"Error: JSON data is empty in file '{json_file}'. Skipping...")
                    continue

                desired_columns = [
                    "match_number",
                    "date",
                    "gender",
                    "match_type", 
                    "teams",
                    "team1",
                    "team2",
                    "team_batting",
                    "team_bowling",
                    "venue",
                    "toss_winner",
                    "toss_decision",
                    "umpires",
                    "batter",
                    "bowler",
                    "non_striker",
                    "over",
                    "runs_batter",
                    "runs_extras",
                    "runs_total",
                    "legbyes",
                    "byes",
                    "no of balls",
                    "noballs",
                    "wides",
                    "player_out",
                    "kind",
                    "fielders",
                    "winner",
                    "player_of_match",
                    "iswicket_delivery",
                    "won_by"
                ]
                
                with open(csv_file_path, 'w', newline='') as file:
                    csv_writer = csv.DictWriter(file, fieldnames=desired_columns)
                    csv_writer.writeheader()

                    match_number = data.get("info", {}).get("event", {}).get("match_number")
                    gender = data.get("info", {}).get("gender")
                    match_type = data.get("info", {}).get("match_type")
                    venue = data.get("info", {}).get("venue")
                    teams = data.get("info", {}).get("teams", [])
                    team1 = teams[0] if len(teams) > 0 else ""
                    team2 = teams[1] if len(teams) > 1 else ""
                    player_of_match = ", ".join(data.get("info", {}).get("player_of_match", []))
                    toss_winner = data.get("info", {}).get("toss", {}).get("winner")
                    toss_decision = data.get("info", {}).get("toss", {}).get("decision")

                    umpires = ", ".join(data.get("info", {}).get("officials", {}).get("umpires", []))

                    for innings in data.get("innings", []):
                        batting_team = innings.get("team")
                        bowling_team = [team for team in teams if team != batting_team][0]

                        for over_data in innings.get("overs", []):
                            over_number = over_data.get("over")
                            deliveries = over_data.get("deliveries", [])

                            for ball_number, delivery in enumerate(deliveries, start=1):
                                batter = delivery.get("batter")
                                bowler = delivery.get("bowler")
                                non_striker = delivery.get("non_striker")
                                runs_batter = delivery.get("runs", {}).get("batter")
                                runs_extras = delivery.get("runs", {}).get("extras")
                                runs_total = delivery.get("runs", {}).get("total")

                                noballs = delivery.get("extras", {}).get("noballs", 0)
                                wides = delivery.get("extras", {}).get("wides", 0)
                                legbyes = delivery.get("extras", {}).get("legbyes", 0)
                                byes = delivery.get("extras", {}).get("byes", 0)

                                wickets = delivery.get("wickets")
                                player_out = ""
                                kind = ""
                                fielders = ""
                                is_wicket_delivery = 0

                                if wickets:
                                    wicket_list = []
                                    for wicket in wickets:
                                        player_out = wicket.get("player_out")
                                        kind = wicket.get("kind")
                                        fielders = ", ".join([fielder.get("name") for fielder in wicket.get("fielders", [])])
                                        wicket_info = f"{player_out} {kind} {fielders}"
                                        wicket_list.append(wicket_info)
                                    wickets = "; ".join(wicket_list)
                                    is_wicket_delivery = 1

                                winner = data.get("info", {}).get("outcome", {}).get("winner")
                                won_by = ""

                                if winner:
                                    result = data.get("info", {}).get("outcome", {}).get("by", {}).keys()
                                    if "wickets" in result:
                                        won_by = "Wickets"
                                    elif "runs" in result:
                                        won_by = "Runs"
                                    elif "super over" in result:
                                        won_by = "Super Over"
                                    else:
                                        won_by = "Other"

                                csv_writer.writerow({
                                    "match_number": match_number,
                                    "date": data.get("info", {}).get("dates", [])[0],
                                    "gender": gender,
                                    "match_type": match_type,
                                    "teams": ", ".join(teams),
                                    "team1": team1,
                                    "team2": team2,
                                    "team_batting": batting_team,
                                    "team_bowling": bowling_team,
                                    "venue": venue,
                                    "toss_winner": toss_winner,
                                    "toss_decision": toss_decision,
                                    "umpires": umpires,
                                    "batter": batter,
                                    "bowler": bowler,
                                    "non_striker": non_striker,
                                    "over": over_number,
                                    "runs_batter": runs_batter,
                                    "runs_extras": runs_extras,
                                    "runs_total": runs_total,
                                    "legbyes": legbyes,
                                    "byes": byes,
                                    "no of balls": ball_number,
                                    "noballs": noballs,
                                    "wides": wides,
                                    "player_out": player_out,
                                    "kind": kind,
                                    "fielders": fielders,
                                    "winner": winner,
                                    "player_of_match": player_of_match,
                                    "iswicket_delivery": is_wicket_delivery,
                                    "won_by": won_by
                                })

                # Get the current time
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Write the file name and time to the status.csv file
                status_csv_writer.writerow([json_file, current_time])

                print(f"Conversion successful. CSV file '{csv_file}' created.")

    print("All new JSON files converted to CSV.")
    print(f"Status file 'status.csv' updated.")


# Directory containing the JSON files
json_data_directory = "C:/Users/JAY/OneDrive/Desktop/internship/repo/ETL_ipl/JSON_files"

# Directory to save the processed CSV files
csv_output_directory = "C:/Users/JAY/OneDrive/Desktop/internship/repo/ETL_ipl/processed_files"

# Path to the status.csv file
status_csv_path = "C:/Users/JAY/OneDrive/Desktop/internship/repo/ETL_ipl/status.csv"

# Convert JSON files to CSV and update the status.csv file
json_to_csv(json_data_directory, csv_output_directory, status_csv_path)
