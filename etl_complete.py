# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np


# %%
df_json = pd.read_json("../pokemon_first.json")
df_json.head()


# %%
df_csv = pd.read_csv("../pokemon_second.csv")
df_csv.head()


# %%
df_csv = df_csv[["Name", "Generation", "Legendary", "Tier"]]
df_csv.head()


# %%
pokemon_df = pd.merge(df_json, df_csv, on="Name", how="inner")
pokemon_df.head()


# %%
pokemon_df.drop(columns=["Category", "Height (ft)", "Height (m)", "Weight (lbs)", "Weight (kg)", "Capture Rate", "Egg Steps", "Exp Group"], inplace=True)


# %%
full_type = []
for row in range(0, len(pokemon_df)):
    if pokemon_df.iloc[row, 3] == "None":
        full_type.append(pokemon_df.iloc[row, 2])
    else:
        full_type.append(pokemon_df.iloc[row, 2] + "/" + pokemon_df.iloc[row, 3])


# %%
pokemon_df["Full Type"] = full_type


# %%
pokemon_df = pokemon_df.rename(columns={"Sp. Attack":"Sp_Attack","Sp. Defense":"Sp_Defense"})


# %%
temp_df = pokemon_df.groupby("Full Type")

avg_total = round(temp_df["Total"].mean(), 1)
avg_hp = round(temp_df["HP"].mean(), 1)
avg_atk = round(temp_df["Attack"].mean(), 1)
avg_def = round(temp_df["Defense"].mean(), 1)
avg_spa = round(temp_df["Sp_Attack"].mean(), 1)
avg_spd = round(temp_df["Sp_Defense"].mean(), 1)
avg_spe  = round(temp_df["Speed"].mean(), 1)

# ou_list = []
# for tier in temp_df["Tier"]:
#     if tier == "PU":
#         ou_list.append(tier)        
# ou_count = len(ou_list)

# ou_count = temp_df.loc[temp_df["Tier"] == "OU"].count()
# # ou_count = pokemon_df.groupby('Tier')['OU'].count()
# ou_count = pokemon_df.groupby(['OU', 'Tier']).size().unstack(fill_value=0)

type_df = pd.DataFrame({
    "Avg Total" : avg_total,
    "Avg HP" : avg_hp,
    "Avg Attack" : avg_atk,
    "Avg Defense" : avg_def,
    "Avg Sp Attack" : avg_spa,
    "Avg Sp Defense" : avg_spd,
    "Avg Speed" : avg_spe
})

type_df.head()


# %%
temp_df = pokemon_df.groupby("Tier")

avg_total = round(temp_df["Total"].mean(), 1)
avg_hp = round(temp_df["HP"].mean(), 1)
avg_atk = round(temp_df["Attack"].mean(), 1)
avg_def = round(temp_df["Defense"].mean(), 1)
avg_spa = round(temp_df["Sp_Attack"].mean(), 1)
avg_spd = round(temp_df["Sp_Defense"].mean(), 1)
avg_spe  = round(temp_df["Speed"].mean(), 1)

mode_type = temp_df["Full Type"].agg(lambda x:x.value_counts().index[0])
mode_gen = temp_df["Generation"].agg(lambda x:x.value_counts().index[0])

tier_df = pd.DataFrame({
    "Avg Total" : avg_total,
    "Avg HP" : avg_hp,
    "Avg Attack" : avg_atk,
    "Avg Defense" : avg_def,
    "Avg Sp Attack" : avg_spa,
    "Avg Sp Defense" : avg_spd,
    "Avg Speed" : avg_spe,
    "Most Common Type" : mode_type,
    "Most Common Gen" : mode_gen
})

tier_df


# %%
import pymongo


# %%
conn = 'mongodb://localhost:27017'


# %%
client = pymongo.MongoClient(conn)


# %%
db = client.pokemon_db


# %%
collection = db.pokemons


# %%
pokemon_df.columns


# %%
# Dictionary to be inserted into MongoDB
data = pokemon_df.to_dict(orient='records')  # Here's our added param..
collection.insert_many(data)


# %%
pokemon_col=db.pokemons.find()
for p in pokemon_col:
    print(p)


# %%
collection2 = db.type


# %%
# Dictionary to be inserted into MongoDB
data2 = type_df.to_dict(orient='records')  # Here's our added param..
collection2.insert_many(data2)


# %%
type_col=db.type.find()
for p in type_col:
    print(p)


# %%
collection3=db.tier


# %%
# Dictionary to be inserted into MongoDB
data3 = tier_df.to_dict(orient='records')  # Here's our added param..
collection3.insert_many(data3)


# %%
tier_col=db.tier.find()
for p in tier_col:
    print(p)


# %%



# %%



# %%



# %%



# %%



# %%


