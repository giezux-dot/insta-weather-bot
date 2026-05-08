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
    try:
        print("Pobieranie pogody...")
        temp, desc = get_weather()
        create_image(temp, desc)
        
        cl = Client()
        # Zwiększamy timeout, żeby serwer nie zrywał połączenia
        cl.request_timeout = 30 
        
        session_id = os.environ.get("IG_SESSIONID")
        
        if session_id:
            print("Logowanie za pomocą Session ID...")
            try:
                cl.login_by_sessionid(session_id)
                # Sprawdzenie czy sesja jest poprawna
                cl.get_timeline_feed() 
                print("Zalogowano pomyślnie przez sesję!")
            except Exception as e:
                print(f"Sesja wygasła lub jest błędna: {e}")
                print("Próba logowania tradycyjnego...")
                cl.login(USERNAME, PASSWORD)
        else:
            print("Brak Session ID. Logowanie hasłem...")
            cl.login(USERNAME, PASSWORD)

        print("Publikowanie posta na Roztocze...")
        caption = (
            f"Dzień dobry! 🌲 Aktualna pogoda na #Roztocze: {temp}°C. \n"
            f"Warunki: {desc.capitalize()}. \n\n"
            f"#roztocze #zwierzyniec #pogoda #lubelskie #natura"
        )
        
        cl.photo_upload("upload.jpg", caption)
        print("SUKCES! Post jest już na Twoim profilu.")
        
    except Exception as e:
        print(f"!!! BŁĄD INSTAGRAMA: {str(e)}")
    
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
