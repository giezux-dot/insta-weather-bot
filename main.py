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
    # Tworzenie leśnej grafiki
    img = Image.new('RGB', (1080, 1080), color=(34, 139, 34))
    draw = ImageDraw.Draw(img)
    text = f"{DISPLAY_NAME}\n{temp}°C\n{desc.capitalize()}"
    draw.text((540, 540), text, fill="white", anchor="mm", align="center")
    img.save("upload.jpg")
    print("Grafika wygenerowana pomyślnie.")

def run_bot():
    print("--- START BOTA ---")
    
    # 1. POGODA
    temp, desc = get_weather()
    if temp is None:
        print("BŁĄD: Przerywam pracę z powodu braku danych pogodowych.")
        return
    
    create_image(temp, desc)
    
    # 2. LOGOWANIE
    cl = Client()
    cl.request_timeout = 30
    login_success = False
    
    if SESSION_ID:
        print("Próba logowania przez Session ID...")
        try:
            cl.login_by_sessionid(SESSION_ID)
            cl.get_timeline_feed() 
            print("Zalogowano pomyślnie przez sesję!")
            login_success = True
        except Exception as e:
            print(f"Sesja nie zadziałała: {e}")
    
    if not login_success:
        print("Próba logowania hasłem (ryzykowne na GitHub)...")
        try:
            cl.login(USERNAME, PASSWORD)
            login_success = True
        except Exception as e:
            print(f"!!! BŁĄD INSTAGRAMA: {e}")

    # 3. PUBLIKACJA
    if login_success:
        try:
            print("Publikowanie na Instagramie...")
            caption = (
                f"Dzień dobry! 🌲 Aktualna pogoda na #Roztocze: {temp}°C. \n"
                f"Warunki: {desc.capitalize()}. \n\n"
                f"#roztocze #zwierzyniec #pogoda #lubelskie #natura"
            )
            cl.photo_upload("upload.jpg", caption)
            print("--- SUKCES! POST OPUBLIKOWANY ---")
        except Exception as e:
            print(f"!!! BŁĄD PUBLIKACJI: {e}")
    else:
        print("Nie udało się zalogować. Sprawdź IG_SESSIONID.")

if __name__ == "__main__":
    run_bot()
