import os
import requests
from instagrapi import Client
from PIL import Image, ImageDraw

# Pobieranie danych z "Secretów" GitHub
USERNAME = os.environ.get("IG_USERNAME")
PASSWORD = os.environ.get("IG_PASSWORD")
API_KEY = os.environ.get("WEATHER_API")

# Ustawienia lokalizacji dla Roztocza (Zwierzyniec jest jego sercem)
CITY_API = "Zwierzyniec,PL"
DISPLAY_NAME = "ROZTOCZE"

def get_weather():
    # Pobieranie danych dla Zwierzyńca
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_API}&appid={API_KEY}&units=metric&lang=pl"
    res = requests.get(url).json()
    temp = int(res['main']['temp'])
    desc = res['weather'][0]['description']
    return temp, desc

def create_image(temp, desc):
    # Tworzenie tła 1080x1080 - kolor zielony "leśny" pasujący do Roztocza
    # (34, 139, 34) to Forest Green
    img = Image.new('RGB', (1080, 1080), color=(34, 139, 34))
    draw = ImageDraw.Draw(img)
    
    # Napis z nazwą regionu i pogodą
    text = f"{DISPLAY_NAME}\n{temp}°C\n{desc.capitalize()}"
    
    # Używamy domyślnej czcionki systemowej (działa zawsze na GitHub Actions)
    draw.text((540, 540), text, fill="white", anchor="mm", align="center")
    
    img.save("upload.jpg")

def run_bot():
    try:
        temp, desc = get_weather()
        create_image(temp, desc)
        
        cl = Client()
        # Logowanie
        print("Logowanie do Instagrama...")
        cl.login(USERNAME, PASSWORD)
        
        # Profesjonalny opis z regionalnymi hashtagami
        caption = (
            f"Dzień dobry! 🌲 Aktualna pogoda na #Roztocze: {temp}°C. \n"
            f"Warunki: {desc.capitalize()}. \n\n"
            f"#roztocze #zwierzyniec #pogoda #lubelskie #natura #polskajestpiekna"
        )
        
        print("Wysyłanie zdjęcia...")
        cl.photo_upload("upload.jpg", caption)
        print("Sukces! Post o Roztoczu opublikowany.")
        
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    run_bot()
