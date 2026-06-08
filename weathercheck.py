from flask import Flask, render_template, request
import requests
app = Flask(__name__)
API_KEY = 'e8478303f059fc3d5cbfe524c761a774' 

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        weather_info = get_weather_info(city)
        forecast_info = get_weather_forecast(city)
        return render_template('indexweather.html', city = city, weather_info = weather_info, forecast_info = forecast_info)
    else:
        return render_template('indexweather.html')
    
def get_weather_info(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        if response.status_code == 200:
            temperature_kelvin = data['main']['temp']
            temperature_celsius = temperature_kelvin - 273.15
            weather_description = data['weather'][0]['description']
            return f'Temperature: {temperature_celsius:.2f}°C, Weather: {weather_description}'
        else:
            return 'Error fetching weather data.'

def get_weather_forecast(city):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        forecast_info = []
        for item in data['list']:
            temperature_kelvin = item['main']['temp']
            temperature_celsius = temperature_kelvin - 273.15
            weather_desc = item['weather'][0]['description']
            forecast_info.append({
                'date': item['dt_txt'],
                'temperature': f'{temperature_celsius:.2f}°C',
                'weather_desc': weather_desc
            })              
        return forecast_info
    else:
        return 'Error fetching forecast data.'
    
if __name__ == '__main__':
    app.run(debug=True)