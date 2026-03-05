import requests
import json
import os

API_KEY = os.getenv('MY_API_KEY')

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
        
    print(f"ПОГОДА В ЛУЧШЕМ ГОРОДЕ КИТАКЮСЮ / 最高の都市・北九州の天気")
    print(f"Температура / 気温: {temperature:.1f}°C (ощущается как / 体感温度 {feels_like:.1f}°C)")
    print(f"Влажность / 湿度: {humidity}%")
    print(f"Давление / 気圧: {pressure} hPa")
    print(f"Скорость ветра / 風速: {wind_speed} m/s")


if __name__ == "__main__":
    get_weather_kitakyushu(API_KEY)