# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 22:01:17 2025

@author: User
"""

import pandas as pd
import random 
import csv
import copy
import sys

# Load old pairs from CSV
old_pairs = set()
try:
    with open("old_pairs.csv", "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            old_pairs.add(tuple(row))
except FileNotFoundError:
    print("No previous pairs found. Creating new groups.")

# Import responses
form = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS6qlLaBzBmalJO89WuAXfnY3RmS7JBGP5hSMWWTs6tVwQ-z_Wfz_Lw3GqB9QxBxPps6xp0KB2yVZ7b/pub?gid=1234636299&single=true&output=csv"
df = pd.read_csv(form)

# Import conversation starters
convo = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSAah_CXFgmp4n_C06ttemHHpMvOPbNv4yIk3o0rWVBTR3MhzuEBMSDG0kb5geOZQ0um1O3oI6W98pE/pub?output=csv"
convo_df = pd.read_csv(convo)

# Load used conversation starters
used_starters = set()
try:
    with open("used_starters.csv", "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            used_starters.add(tuple(row))
except FileNotFoundError:
    pass  # No used starters yet

# Determine group size
group_size = int(input("What size do you want the groups to be? (2-5)"))

# Get participant list
all_participants = df["Email address"].tolist()
num_participants = len(all_participants)

# Attempt to find unique pairs
new_pairs_found = False
tries = 0
new_pairs = set()

while not new_pairs_found and tries < 10:
    tries += 1

    participants = copy.deepcopy(all_participants)
    all_pairs = set()
    pair = []

    while len(participants) > 0:
        # Adjust logic for different group sizes
        person = random.choice(participants)
        participants.remove(person)
        pair.append(person)
        
        if len(pair) >= group_size:  # When group size is reached
            pair.sort()  # Sort to avoid duplicate pairs
            all_pairs.add(tuple(pair))
            pair = []  # Reset the pair for the next group

    # If there are any remaining people in the pair, add them as a final group
    if len(pair) > 0:
        pair.sort()
        all_pairs.add(tuple(pair))

    # Ensure there are no duplicate pairs
    if old_pairs.isdisjoint(all_pairs):
        new_pairs_found = True
        new_pairs = all_pairs  # Save the first successful round

# If no unique pairs found after 10 tries, print message & exit
if not new_pairs_found:
    print("No more unique pairs found after 10 attempts.")
    exit()

# Save new pairs to the old_pairs.csv file
with open("old_pairs.csv", "a+", newline="") as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerows(new_pairs)

# Get conversation starters lists
fun_starters = convo_df['Fun conversation starters'].dropna().tolist()
below_surface_starters = convo_df['Below the surface conversation starters'].dropna().tolist()

# Remove used conversation starters
available_fun_starters = [s for s in fun_starters if s not in used_starters]
available_below_surface_starters = [s for s in below_surface_starters if s not in used_starters]

# Reset used starters if all are used
if not available_fun_starters:
    available_fun_starters = fun_starters
if not available_below_surface_starters:
    available_below_surface_starters = below_surface_starters

# Select conversation starters
fun_starter = random.choice(available_fun_starters)
below_surface_starter = random.choice(available_below_surface_starters)

# Save used starters
used_starters.add(fun_starter)
used_starters.add(below_surface_starter)
with open("used_starters.csv", "w", newline="") as file:
    writer = csv.writer(file)
    for starter in used_starters:
        writer.writerow([starter])

# Save new pairs to a text file
output_file_path = r"C:\Users\User\Documents\Coffee_Partner_Lottery_new_pairs.txt"

with open(output_file_path, "w", encoding="utf-8") as file:
    file.write("------------------------\n")
    file.write("⋆˚✿˖°  Espresso Express Groups ⋆˚✿˖°  :\n")
    file.write("------------------------\n")
    for group in new_pairs:
        file.write("⋆ " + "," .join(group) + "\n")
    file.write(f"\nFun Conversation Starter: {fun_starter}\n")
    file.write(f"Below the Surface Conversation Starter: {below_surface_starter}\n")

# Print output to console
output_string = "\n------------------------\n"
output_string += "⋆ Espresso Express Groups ⋆ :\n"
output_string += "------------------------\n"

for group in all_pairs:
    output_string += "ᯓ⋆˚✿˖° "
    for i in range(len(group)):
        # Correct column references
        name_email_pair = f"{df[df['Email address'] == group[i]].iloc[0]['Name']} ({group[i]})"
        if i < len(group) - 1:
            output_string += name_email_pair + ", "
        else:
            output_string += name_email_pair + "\n" + "\n"

output_string += f"\n \033[1mFun Conversation Starter\033[0m : {fun_starter}\n"
output_string += f" \033[1mBelow the Surface Conversation Starter\033[0m : {below_surface_starter}\n"

print(output_string)
print(f"Groups saved to {output_file_path}")
