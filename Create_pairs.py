import pandas as pd
import random 
import csv
import copy

# open file
old_pairs = set()
try:
    with open("old_pairs.csv", "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            old_pairs.add(tuple(row))
except FileNotFoundError:
    print("old_pairs.csv not found, running without old pairs.")

    # Import responses
form = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS6qlLaBzBmalJO89WuAXfnY3RmS7JBGP5hSMWWTs6tVwQ-z_Wfz_Lw3GqB9QxBxPps6xp0KB2yVZ7b/pub?gid=1234636299&single=true&output=csv"
df = pd.read_csv(form)

    # Import conversation starters
convo = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgt1kS7uILz7a2TWev7kTu8xmxRc_go8nIUYpAKDAVI3mXaJMDhvokC8Vs1BDcg9GVp88e4mbhHHLa/pub?gid=0&single=true&output=csv"
convo_df = pd.read_csv(convo)


    # Determine group sizes
group_size = int(input("What size do you want the groups to be? (2-5)")) 


    # Number of participants
num_participants = df.shape[0] # 0- rows & 1-columns

    # Create list of participants
all_participants = df["Email address"].tolist()

    # Check if any
single = num_participants % group_size

# Boolean flag to check if new pairing has been found
new_pairs_found = False

# Number of tries to create unique pairs
tries = 0

    # Create pairs
while not new_pairs_found and tries < 10:
    tries += 1
    print(f"Making pairs...{tries}")

    participants = copy.deepcopy(all_participants)

    # Create an empty pair
    pair = []

    # Create a list of all groups
    all_pairs = set()

    while len(participants) > 0:
        if single == 1 and len(participants) == 2:
            if group_size > 2:
                pair.sort()
                all_pairs.add(tuple(pair))
                pair = []
            pair.append(participants.pop())
            pair.append(participants.pop())
        else:
            person = random.choice(participants)
            participants.remove(person)
            pair.append(person)
            if len(pair) >= group_size:
                pair.sort()
                all_pairs.add(tuple(pair))
                pair = []
    if len(pair) > 0:
        pair.sort()
        all_pairs.add(tuple(pair))

    # check if all new pairs are indeed new, else reset
    if old_pairs.isdisjoint(all_pairs):
        new_pairs_found = True

if tries >= 10:
    print ("No more unique pairs found.")
else:
# open file
    with open("old_pairs.csv", "a+", newline="") as file:
        writer = csv.writer(file, delimiter=',')
        # write all pairs to csv
        writer.writerows(all_pairs)
