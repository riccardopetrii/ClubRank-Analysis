import numpy as np
import pandas as pd

df = pd.read_json('top_clubs_2018_2024.json')

# df.drop(['link', 'website'], axis=1, inplace=True)

df_italy = df.query("country == 'Italy'")
print(df_italy) # club in italy

# print partial dataframe
# print(df)

# print entire dataframe
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#   print(df)

# print(df.dtypes)
# print(df.describe())

# ------------------------------

# test gen map
# import folium

# m = folium.Map(location=[df['lat'].mean(), df['lng'].mean()], zoom_start=2)

# for index, row in df.iterrows():
#     folium.Marker(location=[row['lat'], row['lng']]).add_to(m)

# m.save('test.html') # for notebook simply calling m
