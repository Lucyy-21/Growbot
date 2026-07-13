import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")


def get_farmer_info():
    name= input("What is your name?")
    location= input("Where is your farm located?").lower()
    return name, location


def check_temperature(temp):
    if temp > 35:
        return "Too hot to plant today.", "Avoid planting. Water your existing crops early morning or evening"
    elif 20 < temp <= 35:
        return "Good planting conditions.", "Consider planting maize, tomatoes or peppers in this weather."
    else:
        return "Too cold today.", "Cover sensitive crops. Good time for planting cabbage or lettuce."


def get_crop_advice(crop):
    if crop == "cassava":
        return "Plant at start of rainy season, doesn't need much water."
    elif crop == "rice":
        return "Needs a lot of water, plant in lowland areas."
    elif crop == "yam":
        return "Needs deep loose soil, plant before rainy season."
    elif crop == "beans":
        return "Needs moderate water, plant at start of rainy season."
    elif crop == "maize":
        return "Needs consistent water, plant at start of rainy season."
    else:
        return "We don't have specific advice for that crop yet"

name, location = get_farmer_info()
crop = input("What crop are you planning to plant? ").lower()


url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

response = requests.get(url)
data = response.json()
if data["cod"] == "404":
    print(f"Weather data for {location} not found. Please check the city name.")
    exit()
temp = data["main"]["temp"]
description = data["weather"][0]["description"]

print(f"Hi {name}, Here is your farming update for {location.title()}.")
print(f"Current weather: {description}, {temp}°C")
recommendation, tip = check_temperature(temp)
print(recommendation)
print(tip)
print(get_crop_advice(crop))