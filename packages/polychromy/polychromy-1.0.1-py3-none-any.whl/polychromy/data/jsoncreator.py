# This is used to easily modify the json file using a csv file source.

import csv
import json

# Specify the CSV and JSON file names
csv_file = "colors.csv"
json_file = "colors.json"

# Read data from CSV and convert it to a dictionary
data = {}
with open(csv_file, newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        color_name = row["Color Name"]
        hex_value = row["Hex Value"]
        rgb_value = row["RGB Value"]        
        xterm = row["Xterm Number"]
        ansi_fg = row["FG ANSI Code"]
        ansi_bg = row["BG ANSI Code"]
        alt_name = row["Alternative Name"]
        data[color_name] = {"hex": hex_value, "rgb": rgb_value, "xterm": xterm, "fg": ansi_fg, "bg": ansi_bg, "alt": alt_name}

# Write the data to a JSON file
with open(json_file, "w") as file:
    json.dump(data, file, indent=4)

print(f"Data from '{csv_file}' has been saved to '{json_file}' as JSON.")
