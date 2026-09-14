from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os
from dotenv import load_dotenv
from crop_data import CROPS, get_crop_advice, get_crop_list

load_dotenv()

app = Flask(__name__)
api_key = os.getenv("OPENWEATHER_API_KEY")
sessions = {}
def match_crop(user_input):
    """
    Try to match user input to a crop in the CROPS dictionary.
    Returns the crop key (e.g. 'maize') or None if no good match.
    """
    # 1. Clean the input
    user_input = user_input.lower().strip()

    # 2. Exact match against known crops
    if user_input in CROPS:
        return user_input

    # 3. Curated typo map
    typo_map = {
        "maiz": "maize",
        "maze": "maize",
        "casava": "cassava",
        "cassavaa": "cassava",
        "tomatoe": "tomato",
        "potato": "yam",       # common mistake
        "g/nut": "groundnut",
        "ground nut": "groundnut",
        "coco yam": "cocoyam",
        "plantin": "plantain",
        "okro": "okra",
    }
    if user_input in typo_map:
        return typo_map[user_input]

    # 4. Partial match — only if exactly one crop contains the input
    matches = [crop for crop in CROPS if user_input in crop]
    if len(matches) == 1:
        return matches[0]

    # 5. No confident match
    return None
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip().lower()
    sender = request.values.get("From", "")
    resp = MessagingResponse()
    msg = resp.message()

    # Check if API key is missing
    if not api_key:
        msg.body("❌ GrowBot is currently unavailable. Please try again later.")
        return str(resp)

    if incoming_msg in ["hi", "hello", "hey"]:
        sessions[sender] = {"step": "waiting_for_location"}
        msg.body("🌱 Welcome to GrowBot! Your farming assistant for Nigerian farmers.\n\nPlease reply with your location. (e.g. Lagos, Abuja, Kano)")

    elif sessions.get(sender, {}).get("step") == "waiting_for_location":
        location = incoming_msg
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") == "404":
            msg.body("❌ Location not found. Please try again with a valid city name.")
        else:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            sessions[sender]["step"] = "waiting_for_crop"
            sessions[sender]["temp"] = temp
            sessions[sender]["location"] = location
            
            crop_list = get_crop_list()
            msg.body(f"📍 {location.title()} Weather Update:\n🌡 Temperature: {temp}°C\n🌤 Condition: {description}\n\nWhat crop are you planning to plant?\nAvailable crops: {crop_list}")

   elif sessions.get(sender, {}).get("step") == "waiting_for_crop":
    crop = match_crop(incoming_msg)

    if crop is None:
        # Stay in the same step so they can try again
        msg.body(
            "❌ I don't recognize that crop.\n\n"
            f"Available crops: {get_crop_list()}\n\n"
            "Please reply with one of those."
        )
        return str(resp)

    temp = sessions[sender]["temp"]
    location = sessions[sender]["location"]
    # ... rest stays the same

        if temp > 35:
            weather_tip = "⚠️ Too hot to plant today. Water your crops early morning or evening."
        elif 20 < temp <= 35:
            weather_tip = "✅ Good planting conditions today!"
        else:
            weather_tip = "🥶 Too cold today. Consider covering sensitive crops."

        # Use the imported function that returns the formatted advice
        advice = get_crop_advice(crop)
        sessions[sender]["step"] = "done"
        
        msg.body(f"🌱 GrowBot Recommendation for {location.title()}:\n\n{weather_tip}\n{advice}\n\nSend 'Hi' to start again!")
    elif incoming_msg in ["thanks", "thank you", "thank", "ok", "okay", "great"]:
        msg.body("🙏 You're welcome! Happy farming! 🌾")
        
    elif incoming_msg == "crops":
        crop_list = get_crop_list()
        msg.body(f"🌾 Available crops:\n{crop_list}\n\nReply with a crop name to get advice.")    
    else:
        msg.body("🌱 Hello! I'm GrowBot. Send 'Hi' to get started.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)