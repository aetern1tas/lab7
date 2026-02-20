import requests
import json

API_KEY = "e14f02a8d29b96ea81dd10b4297c831b"

def get_weather_kitakyushu(api_key):

    city = "Kitakyushu"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    
    response = requests.get(url)
    response.raise_for_status()       
    weather_data = response.json()
    temperature = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    weather_description = weather_data['weather'][0]['description']
    wind_speed = weather_data['wind']['speed']
        
    print(f"ПОГОДА В ЛУЧШЕМ ГОРОДЕ КИТАКЮСЮ")
    print(f"Температура: {temperature:.1f}°C (ощущается как {feels_like:.1f}°C), {weather_description.capitalize()}")
    print(f"Влажность: {humidity}%")
    print(f"Давление: {pressure} гПа")
    print(f"Скорость ветра: {wind_speed} м/с")


if __name__ == "__main__":
    get_weather_kitakyushu(API_KEY)