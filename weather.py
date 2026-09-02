
import requests
import os
from dotenv import load_dotenv
from crop_data import CROPS, get_crop_advice, get_crop_list

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")


def get_farmer_info():
    name = input("What is your name? ")
    location = input("Where is your farm located? ").lower()
    return name, location


def check_temperature(temp):
    if temp > 35:
        return "Too hot to plant today.", "Avoid planting. Water your existing crops early morning or evening"
    elif 20 < temp <= 35:
        return "Good planting conditions.", "Consider planting maize, tomatoes or peppers in this weather."
    else:
        return "Too cold today.", "Cover sensitive crops. Good time for planting cabbage or lettuce."




    # Check if the crop exists in our dictionary and format the output
    if crop in crop_data:
        info = crop_data[crop]
        return (f"\nAdvice for {crop.title()}:\n"
                f"- Tip: {info['tip']}\n"
                f"- Soil: {info['soil']}\n"
                f"- Spacing: {info['spacing']}")
    else:
        return "\nWe don't have specific advice for that crop yet."


name, location = get_farmer_info()
crop = input("What crop are you planning to plant? ").lower()


url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

response = requests.get(url)
data = response.json()

if data.get("cod") == "404" or data.get("cod") == 404:
    print(f"Weather data for '{location}' not found. Please check the city name.")
    exit()

temp = data["main"]["temp"]
description = data["weather"][0]["description"]

print(f"\nHi {name}, Here is your farming update for {location.title()}.")
print(f"Current weather: {description}, {temp}°C")

recommendation, tip = check_temperature(temp)
print(recommendation)
print(tip)

# Prints the formatted dictionary data
print(get_crop_advice(crop))
