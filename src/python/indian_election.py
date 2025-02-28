import pandas as pd
import numpy as np

# Load the dirty dataset
file_path = "indian_election_dataset.csv"
df = pd.read_csv(file_path)

# 1. Handling NULL Values
print("Missing values before:")
print(df.isnull().sum())
df.fillna({'pc_type': 'Unknown', 'cand_sex': 'Unknown'}, inplace=True)
df.dropna(inplace=True)  # Dropping remaining rows with NULLs
print("Missing values after:")
print(df.isnull().sum())

# 2. Removing Duplicates
print("Duplicates before:", df.duplicated().sum())
df.drop_duplicates(inplace=True)
print("Duplicates after:", df.duplicated().sum())

# 3. Standardizing Data Formats
df['partyname'] = df['partyname'].str.replace("_", " ").str.title()
df['pc_name'] = df['pc_name'].str.title()
df['st_name'] = df['st_name'].str.title()

# 4. Correcting Inconsistent Data
df['cand_sex'] = df['cand_sex'].replace({
    'M': 'Male', 'MALE': 'Male', 'F': 'Female', 'FEMALE': 'Female'
})

# 5. Data Type Conversion
df['totvotpoll'] = pd.to_numeric(df['totvotpoll'], errors='coerce')
df['electors'] = pd.to_numeric(df['electors'], errors='coerce')

# Final Check
print("Final Data Types:")
print(df.dtypes)
print("Cleaned Dataset Preview:")
print(df.head())

# Save the cleaned dataset
cleaned_file_path = "indian_election_cleaned.csv"
df.to_csv(cleaned_file_path, index=False)

#///////////////////GRAPHS//////////////////////////

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned dataset
file_path = "/mnt/data/indian-election-cleaned.csv"
df = pd.read_csv(file_path)

# 1. Voter Turnout Percentage
df['voter_turnout'] = (df['totvotpoll'] / df['electors']) * 100
plt.figure(figsize=(10, 6))
sns.histplot(df['voter_turnout'], bins=20, kde=True, color='blue')
plt.title('Voter Turnout Distribution')
plt.xlabel('Voter Turnout (%)')
plt.ylabel('Frequency')
plt.savefig("voter_turnout_distribution.png")
plt.show()

# 2. Winning Party Trend
plt.figure(figsize=(12, 6))
winning_party_counts = df['partyname'].value_counts().head(10)  # Top 10 parties
sns.barplot(x=winning_party_counts.index, y=winning_party_counts.values, palette='coolwarm')
plt.xticks(rotation=45)
plt.title('Top 10 Winning Parties')
plt.xlabel('Party')
plt.ylabel('Number of Wins')
plt.savefig("winning_parties.png")
plt.show()

# 3. Top 5 States by Voter Turnout
state_turnout = df.groupby('st_name')['voter_turnout'].mean().sort_values(ascending=False).head(5)
plt.figure(figsize=(10, 6))
sns.barplot(x=state_turnout.index, y=state_turnout.values, palette='viridis')
plt.title('Top 5 States by Voter Turnout')
plt.xlabel('State')
plt.ylabel('Average Voter Turnout (%)')
plt.savefig("top_states_voter_turnout.png")
plt.show()

# 4. Gender Representation
plt.figure(figsize=(6, 6))
gender_counts = df['cand_sex'].value_counts()
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=['lightblue', 'pink'], startangle=90)
plt.title('Gender Representation of Candidates')
plt.savefig("gender_representation.png")
plt.show()

# 5. Winning Margin Distribution
df['winning_margin'] = df.groupby('pc_name')['totvotpoll'].diff().fillna(0).abs()
plt.figure(figsize=(10, 6))
sns.histplot(df['winning_margin'], bins=20, kde=True, color='green')
plt.title('Winning Margin Distribution')
plt.xlabel('Winning Margin (Votes)')
plt.ylabel('Frequency')
plt.savefig("winning_margin_distribution.png")
plt.show()