import discord
from discord.ext import commands
import datetime
import os
import random
from urllib import parse, request
import re
import requests
import json
import flag
import math
import pycountry
from keep_alive import keep_alive 
from PIL import Image, ImageFont, ImageDraw
from tabulate import tabulate
from formattingfunc import *




def get_level(user):
	"""
	Fetches level, rank, xp, message count data from mee6s leaderboard
	"""

	try:
		URL = 'https://mee6.xyz/api/plugins/levels/leaderboard/739175633673781259'
		res = requests.get(URL)

		for count, item in enumerate(res.json()['players']):
		    name = item['username']
		    discriminator = item['discriminator']
		    level = item['level']
		    msg_count = item['message_count']
		    xp = item['xp']
		    if name == user:
		    	rank = count+1

		    	return level, rank, xp, msg_count
	except:
		return None


def get_quote():
	"""
	Fetches a random quote off https://zenquotes.io/api/random
	"""

	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']

	return (quote)



def GetStreet(Add):
	"""
	Based on the location given, it returns a googlestreet-view picture of the location.
	"""

	key = "&key=" + "AIzaSyDnmmANZ2R50QtRlioo2HzB8AabSVhjKzM" 
	base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
	street_view_url = base + parse.quote_plus(Add) + key #added url encoding
	fi = "test" + ".jpg"

	return street_view_url

def dictionary(q):
	"""
	Fetches information about a word from https://api.dictionaryapi.dev
	"""

	url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{q}"
	data = requests.get(url).json()

	main = data[0]

	word = main["word"]

	phonetic = main["phonetic"]
	word_type = main["meanings"][0]["partOfSpeech"]
	definition = main["meanings"][0]["definitions"][0]["definition"]

	try:
		example = main["meanings"][0]["definitions"][0]["example"]
	except:
		example = "None given"
	synonyms = main["meanings"][0]["definitions"][0]["synonyms"]
	list_of_synonyms = ""

	for synonym in synonyms:
		if len(list_of_synonyms)<35:
			list_of_synonyms+=synonym + ", "
		else:
			break
	if len(list_of_synonyms)==0:
		list_of_synonyms = "None given"

	return word, phonetic, word_type, definition, example, list_of_synonyms

def weather_api(q):
    """
    API function to gather weather information and returns them as tuple.
    API source: https://openweathermap.org/ 
    """

    WEATHER_API_KEY = "11a8994c28e7df09bfbd1124d1554bad"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    #assign the json data to variables
    main = data["main"]
    temperature = main["temp"]
    temp_fahrenheit = str(round((temperature * 9/5) + 32,1)) + "°F"
    temp_celsius = str(round(temperature, 1)) + "°C"
    wind = str(round(data["wind"]["speed"],1)) + "km/h"
    humidity = str(main["humidity"]) + "%"

    weather = data["weather"]
    weather_description = weather[0]["description"]
    weather_icon = weather[0]["icon"]
    weather_icon_url = f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"

    country = data["sys"]["country"]
    country_names = pycountry.countries.get(alpha_2=country)
    country_name = country_names.name
    country_icon = flag.flag(country)

    return weather_icon_url, country_name, country, country_icon, humidity, wind, temp_celsius, temp_fahrenheit, weather_description


def country_api(country):
    """
    API function that gathers information about a country and returns them as tuple.
    API source: https://restcountries.com/
    """

    url =f"https://restcountries.com/v3.1/name/{country}"
    data = requests.get(url).json()

    region = data[0]["subregion"] #subregion
    region_s = data[0]["region"] #subregion
    c_name_l = data[0]["name"]["common"] #long country name
    flag_icon = data[0]["flag"] #flag as icon
    c_name_s = data[0]["cca2"] #short country name
    capital = data[0]["capital"][0] #capital city

    currencydata = data[0]["currencies"]
    currency_short, value = list(currencydata.items())[0]
    curr_name = value["name"] #name of currency
    currr_symbol = value["symbol"] #currency symbol

    languages = data[0]["languages"]
    language_list = []

		#covert tuple to a readable string
    for slang, language in languages.items():
        language_list.append(language)

    language_list = ', '.join(language_list)

    flag_data = data[0]["flags"]["png"] #flag as pic
    
    populatation = data[0]["population"]
    popu_short = human_format(populatation) #population in human readable format
    area = data[0]["area"]/1000
    area_short = '{:,}'.format(area).replace(',','.')+" km²" #area human-readable

    return flag_icon, c_name_s, c_name_l, capital, curr_name, currr_symbol, language_list, flag_data, popu_short, area_short, region, region_s

def tenor(q):
    """
    API function that finds a random gif that it finds with the search query and returns a gif link.
    API source: https://tenor.com/gifapi

    q: any search query word or phrase
    """

    TENOR_API_KEY = "LIVDSRZULELA"
    lmt = 40
    random_pic = random.randint(1,25)

    r = requests.get(
        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (q, TENOR_API_KEY, lmt))

    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        tenorgifs = json.loads(r.content)
		
        return (tenorgifs["results"][random_pic]["media"][0]["mediumgif"]["url"])
    else:
        return None