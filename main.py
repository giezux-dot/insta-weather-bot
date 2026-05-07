import os
import requests
from instagrapi import Client
from PIL import Image, ImageDraw

# Konfiguracja z Secrets
USERNAME = os.environ.get("IG_USERNAME")
PASSWORD = os.environ.get("IG_PASSWORD")
API_KEY = os.environ.get("WEATHER_API")

# Ustawienia lokalizacji
CITY_API = "Zwierzyniec,PL"
DISPLAY_NAME = "ROZTOCZE"

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_API}&appid={API_KEY}&units=metric&lang=pl"
    try:
        response = requests.get(url)
        res = response.json()
        
        # SPRAWDZANIE BŁĘDÓW API
        if res.get("cod") != 200:
            print(f"!!! PROBLEM Z API POGODY: {res.get('message')} (Kod: {res.get('cod')})")
            return None, None
            
        temp = int(res['main']['temp'])
        desc = res['weather'][0]['description']
        return temp, desc
    except Exception as e:
        print(f"!!! BŁĄD POŁĄCZENIA: {e}")
        return None, None

def create_image(temp, desc):
    img = Image.new('RGB', (1080, 1080), color=(34, 139, 34))
    draw = ImageDraw.Draw(img)
    text = f"{DISPLAY_NAME}\n{temp}°C\n{desc.capitalize()}"
    draw.text((540, 540), text, fill="white", anchor="mm", align="center")
    img.save("upload.jpg")

def run_bot():
    print("Pobieranie pogody...")
    temp, desc = get_weather()
    
    if temp is None:
        print("Bot zatrzymany z powodu błędu pobierania danych pogodowych.")
        return

    create_image(temp, desc)
    
    try:
        cl = Client()
        print("Logowanie do Instagrama...")
        cl.login(USERNAME, PASSWORD)
        
        caption = f"Dzień dobry! 🌲 Aktualna pogoda na #Roztocze: {temp}°C. \nWarunki: {desc.capitalize()}."
        
        print("Wysyłanie zdjęcia...")
        cl.photo_upload("upload.jpg", caption)
        print("Sukces! Post opublikowany.")
    except Exception as e:
        print(f"!!! BŁĄD INSTAGRAMA: {e}")

if __name__ == "__main__":
    run_bot()
