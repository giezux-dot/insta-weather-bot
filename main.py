import os
import requests
from instagrapi import Client
from PIL import Image, ImageDraw

# Pobieranie danych z "Secretów" GitHub
USERNAME = os.environ.get("IG_USERNAME")
PASSWORD = os.environ.get("IG_PASSWORD")
API_KEY = os.environ.get("WEATHER_API")

# Lokalizacja
CITY_API = "Zwierzyniec,PL"
DISPLAY_NAME = "ROZTOCZE"

def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_API}&appid={API_KEY}&units=metric&lang=pl"
    try:
        res = requests.get(url).json()
        if res.get("cod") != 200:
            print(f"Błąd API pogody: {res.get('message')}")
            return None, None
        
        temp = int(round(res['main']['temp']))
        desc = res['weather'][0]['description']
        return temp, desc
    except:
        return None, None

def create_image(temp, desc):
    # Generowanie grafiki
    img = Image.new('RGB', (1080, 1080), color=(34, 139, 34)) # Leśna zieleń
    draw = ImageDraw.Draw(img)
    text = f"{DISPLAY_NAME}\n{temp}°C\n{desc.capitalize()}"
    draw.text((540, 540), text, fill="white", anchor="mm", align="center")
    img.save("upload.jpg")

def run_bot():
    print("Pobieranie danych...")
    temp, desc = get_weather()
    
    if temp is None:
        print("Nie udało się pobrać pogody. Kończę.")
        return

    create_image(temp, desc)
    
    cl = Client()
    try:
        print(f"Próba logowania na konto: {USERNAME}...")
        cl.login(USERNAME, PASSWORD)
        
        caption = (
            f"Pogoda na dziś: {temp}°C, {desc}. #roztocze #zwierzyniec #pogoda"
        )
        
        cl.photo_upload("upload.jpg", caption)
        print("Sukces! Post opublikowany.")
    except Exception as e:
        print(f"BŁĄD LOGOWANIA: {e}")
        print("Podpowiedź: Jeśli widzisz błąd hasła lub 'challenge', Instagram zablokował serwer.")

if __name__ == "__main__":
    run_bot()
