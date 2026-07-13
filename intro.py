def get_farmer_info():
    name= input("What is your name?")
    location= input("Where is yout farm located?")
    return name, location


def check_temperature(temp):
    if temp > 35:
        return "Too hot to plant today."
    elif 20 < temp <= 35:
        return "Good planting conditions."
    else:
        return "Too cold today."
temp = int(input("Enter temperature: "))

name, location = get_farmer_info()
print(f"Hi {name}, Here is your farming update for {location}.")
print(check_temperature(temp))
