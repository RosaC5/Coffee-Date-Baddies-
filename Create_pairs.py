import pandas as pd
import random 

    # Import responses
form = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS6qlLaBzBmalJO89WuAXfnY3RmS7JBGP5hSMWWTs6tVwQ-z_Wfz_Lw3GqB9QxBxPps6xp0KB2yVZ7b/pub?gid=1234636299&single=true&output=csv"
df = pd.read_csv(form)
print(df)

    # Import conversation starters
convo = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgt1kS7uILz7a2TWev7kTu8xmxRc_go8nIUYpAKDAVI3mXaJMDhvokC8Vs1BDcg9GVp88e4mbhHHLa/pub?gid=0&single=true&output=csv"
convo_df = pd.read_csv(convo)
print(convo_df)


    # Determine group sizes
group_size = int(input("What size do you want the groups to be? (2-5)")) 


    # Number of participants
num_participants = df.shape[0]

    # Create list of participants
participants = df["Email address"].tolist()

    # Check if any
single = num_participants % group_size

    # Create an empty pair
pair = []

    # Create a list of all groups
all_pairs = []

    # Create pairs
while len(participants) > 0:
    if single == 1 and len(participants) == 2:
        all_pairs.append(pair)
        pair = []
        pair.append(participants.pop())
        pair.append(participants.pop())
    else:
        person = random.choice(participants)
        participants.remove(person)
        pair.append(person)
        if len(pair) >= group_size:
            all_pairs.append(pair)
            pair = []
if len(pair) > 0:
    all_pairs.append(pair)

