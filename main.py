import os
import requests
from instagrapi import Client
from PIL import Image, ImageDraw

# --- KONFIGURACJA ---
USERNAME = os.environ.get("IG_USERNAME")
PASSWORD = os.environ.get("IG_PASSWORD")
API_KEY = os.environ.get("WEATHER_API")
SESSION_ID = os.environ.get("IG_SESSIONID")

CITY_API = "Zwierzyniec,PL"
DISPLAY_NAME = "ROZTOCZE"

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_API}&appid={API_KEY}&units=metric&lang=pl"
    try:
        response = requests.get(url)
        res = response.json()
        if res.get("cod") != 200:
            print(f"!!! PROBLEM Z API POGODY: {res.get('message')}")
            return None, None
        
        temp = int(round(float(res['main']['temp'])))
        desc = res['weather'][0]['description']
        return temp, desc
    except Exception as e:
        print(f"!!! BŁĄD POGODY: {e}")
        return None, None

def create_image(temp, desc):
    img = Image.new('RGB', (1080, 1080), color=(34, 139, 34))
    draw = ImageDraw.Draw(img)
    text = f"{DISPLAY_NAME}\n{temp}°C\n{desc.capitalize()}"
    draw.text((540, 540), text, fill="white", anchor="mm", align="center")
    img.save("upload.jpg")

def run_bot():
    print("--- START BOTA ---")
    
    # 1. POGODA
    temp, desc = get_weather()
    if temp is None:
        print("BŁĄD: Przerywam pracę, brak danych pogodowych (Klucz API może być jeszcze nieaktywny).")
        return
    
    create_image(temp, desc)
    
    # 2. LOGOWANIE
    cl = Client()
    cl.request_timeout = 30
    
    print("Próba logowania przez Session ID...")
    try:
        if not SESSION_ID:
            raise Exception("Brak zmiennej IG_SESSIONID w Secrets!")
            
        cl.login_by_sessionid(SESSION_ID)
        cl.get_timeline_feed() # Test połączenia
        print("ZALOGOWANO POMYŚLNIE PRZEZ SESJĘ!")
        
        # 3. PUBLIKACJA (Tylko jeśli logowanie się udało)
        print("Publikowanie na Instagramie...")
        caption = (
            f"Dzień dobry! 🌲 Aktualna pogoda na #Roztocze: {temp}°C. \n"
            f"Warunki: {desc.capitalize()}. \n\n"
            f"#roztocze #zwierzyniec #pogoda #lubelskie #natura"
        )
        cl.photo_upload("upload.jpg", caption)
        print("--- SUKCES! POST OPUBLIKOWANY ---")

    except Exception as e:
        print(f"!!! BŁĄD LOGOWANIA/SESJI: {e}")
        print("Próba logowania hasłem została pominięta, aby uniknąć blokady IP.")

if __name__ == "__main__":
    run_bot()
