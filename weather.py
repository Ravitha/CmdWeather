# Create command line tool for providing weather information for a city

import argparse
import pkgutil
import requests
import json
from sys import exit
#include libraries which can offer fancy output in the console
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


def get_weather(city):
    # Get weather information for a city
    # Create url for api call
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city)
    # Make api call
    response = requests.get(url)
    #include test condition if response is not 200
    if response.status_code != 200:
        print('Error: Invalid city name')
        return
    # Convert response to json
    data = response.json()
    # Return data
    return data

def parse_weather_data(data):
    #create a empty dict
    weather_data = {}
    # add city name to dict
    weather_data['city'] = data['name']
    # add weather description to dict
    weather_data['weather'] = data['weather'][0]['description']
    # add temp, temp_min, temp_max to dict
    weather_data['temp'] = data['main']['temp']
    weather_data['temp_min'] = data['main']['temp_min']
    weather_data['temp_max'] = data['main']['temp_max']
    # add wind speed, clouds, pressure to dict
    weather_data['wind'] = data['wind']['speed']
    weather_data['clouds'] = data['clouds']['all']
    weather_data['pressure'] = data['main']['pressure']
    #add country_name, lat and lon to dict
    weather_data['country'] = data['sys']['country']
    weather_data['lat'] = data['coord']['lat']
    weather_data['lon'] = data['coord']['lon']
    print_details(weather_data)  

def print_details(dict):
    
    print('-' * 80)

    # use coloroma to print "Weather in " as black "city,country_name" as light blue ":" as black and weather as light blue
    print('Weather in ', Fore.LIGHTBLUE_EX + '{},{}'.format(dict['city'], dict['country']), ':', Fore.LIGHTBLUE_EX + '{}'.format(dict['weather']))
    # print information in "temp °С from temp_min to temp_max °С, wind speed m/s. clouds %, pressure hpa"
    # print the temperature, pressure in separate lines inside a table with each column separated by 2 spaces
    #enclose the statement inside a border of '-' with length equal to the length of the statement   
    
    print('Temperature' , Fore.LIGHTYELLOW_EX  + '{}°С'.format(dict['temp']) \
    , 'Wind speed' , Fore.LIGHTYELLOW_EX  + '{} m/s'.format(dict['wind']) \
    , 'Clouds' , Fore.LIGHTYELLOW_EX  + '{}%'.format(dict['clouds']) \
    , 'Pressure' , Fore.LIGHTYELLOW_EX  + '{} hpa'.format(dict['pressure']))
    print('-' * 80)

    #print the "*source from openweathermap.org" in font style italic 
    print(Fore.LIGHTGREEN_EX + Style.DIM + '*source from openweathermap.org')


# include following lines in a block with __name as main to run as a script and not as a module
if __name__ == '__main__':
    # Create parser object
    parser = argparse.ArgumentParser(description='Get weather information for a city')  
    # Add arguments
    # modify the help message to include if city name has more than one word enclose it in quotes
    parser.add_argument('-c','--city', help='city for which to get weather information. If city name has more than one word enclose it in quotes')
    # Parse arguments
    args = parser.parse_args()
    if args.city is None:
        print('Check its usage with -h or --help')
        exit(1)
    data = get_weather(args.city)
    #check if data is not None
    if data is not None:
        parse_weather_data(data)
    