import os
import time
from selenium import webdriver
import pandas as pd
import folium
from folium.plugins import HeatMap
import shutil

def create_maps(df, maps_folder):
    for year in range(2018, 2025):
        df_year = df[df['year'] == year].dropna(subset=['lat', 'lng'])

        m = folium.Map(location=[df_year['lat'].mean(), df_year['lng'].mean()], tiles="Cartodb dark_matter", zoom_start=2)
        HeatMap(df_year[['lat', 'lng']].values.tolist()).add_to(m)

        m.save(os.path.join(maps_folder, f'map_{year}.html'))

def modify_html(maps_folder):
    for year in range(2018, 2025):
        fn = os.path.join(maps_folder, f'map_{year}.html')

        with open(fn, 'r+', encoding='utf-8') as file:
            content = file.read().replace('zoomControl: true', 'zoomControl: false')
            file.seek(0)
            file.write(content)
            file.truncate()

def capture_screenshots(maps_folder, imgs_folder):
    if not os.path.exists(imgs_folder):
        os.makedirs(imgs_folder)
    
    for i in range(2018, 2025):
        fn = f'file://{os.getcwd()}/{os.path.join(maps_folder, f"map_{i}.html")}'
        browser = webdriver.Chrome()
        browser.set_window_position(100, 50)
        browser.get(fn)
        time.sleep(5)
        browser.save_screenshot(os.path.join(imgs_folder, f'img_{i}.png'))
        browser.quit()

maps_folder = 'maps'
imgs_folder = 'imgs'

df = pd.read_json('datasets/top_clubs_2018_2024_fixed.json')

if not os.path.exists(maps_folder):
    os.makedirs(maps_folder)

df['lat'] = df['lat'].replace('Unknown', pd.NA)
df['lng'] = df['lng'].replace('Unknown', pd.NA)

create_maps(df, maps_folder)
modify_html(maps_folder)
capture_screenshots(maps_folder, imgs_folder)

shutil.rmtree('maps')
