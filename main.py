import os
import requests
from instagrapi import Client
from PIL import Image, ImageDraw, ImageFont

# Pobieranie danych z "Secretów" GitHub (ustawimy to w kroku 4)
USERNAME = os.environ.get("IG_USERNAME")
PASSWORD = os.environ.get("IG_PASSWORD")
API_KEY = os.environ.get("WEATHER_API")
CITY = "Warsaw"

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=pl"
    res = requests.get(url).json()
    temp = int(res['main']['temp'])
    desc = res['weather'][0]['description']
    return temp, desc

def create_image(temp, desc):
    # Tworzenie tła 1080x1080
    color = (30, 144, 255) if temp > 0 else (100, 149, 237)
    img = Image.new('RGB', (1080, 1080), color=color)
    draw = ImageDraw.Draw(img)
    
    # Prosty napis (bez zewnętrznych czcionek dla ułatwienia)
    text = f"{CITY}\n{temp}°C\n{desc.capitalize()}"
    draw.text((540, 540), text, fill="white", anchor="mm", align="center")
    
    img.save("upload.jpg")

def run_bot():
    temp, desc = get_weather()
    create_image(temp, desc)
    
    cl = Client()
    # Logowanie z obsługą sesji
    cl.login(USERNAME, PASSWORD)
    
    caption = f"Prognoza dla miasta {CITY}: {temp}°C, {desc}. #pogoda #weather #automatyzacja"
    cl.photo_upload("upload.jpg", caption)
    print("Opublikowano!")

if __name__ == "__main__":
    run_bot()