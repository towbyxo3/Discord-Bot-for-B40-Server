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


#set up the global prefix for bot commands
bot = commands.Bot(command_prefix='^', description="description")




def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return (quote)



def GetStreet(Add):
	"""
	Base on the location given, it returns a pic of the location.
	"""
	key = "&key=" + "AIzaSyDnmmANZ2R50QtRlioo2HzB8AabSVhjKzM" 
	base = "https://maps.googleapis.com/maps/api/streetview?size=1200x800&location="
	MyUrl = base + parse.quote_plus(Add) + key #added url encoding
	fi = "test" + ".jpg"

	return MyUrl



def dictionary(q):
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

    q: a place (could be a city or a country) of which weather data should be displayed 
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

def human_format(num):
    """
    converts population numbers to readable formats using K, M. and returns them as string.

    num: population number

    code from https://stackoverflow.com/a/45846841
    """

    num = float('{:.3g}'.format(num))
    magnitude = 0

    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', ' K', ' M', ' B', ' T'][magnitude])

def country_api(country):
    """
    API function that gathers information about a country and returns them as tuple.
    API source: https://restcountries.com/
    
    country: any country name
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

#BOT COMMANDS
#the following bot commands are triggered if message sent by a user consists of the prefix followed by the command function name.
# For example, to trigger the serverinfo function, it would be   "   ^serverinfo    "
#some commands can 

@bot.command()
async def userinfo(ctx,member:discord.Member=None):
	"""
	Display information about a user. 
	"""

	if member==None:
		member=ctx.author

	rlist = []
	for role in member.roles:
		if role.name != "@everyone":
			rlist.append(role.mention)

	b = ", ".join(rlist)


	embed = discord.Embed(colour=member.color,timestamp=ctx.message.created_at)

	embed.set_author(name=f"{member}   •   {member.id}"),
	embed.set_thumbnail(url=member.avatar_url),


	embed.add_field(name='Name:',value=member.mention,inline=True)
	embed.add_field(name='Booster', value=f'{("Yes" if member.premium_since else "No")}',inline=True)



	

	embed.add_field(name=f'Roles:({len(rlist)})',value=''.join([b]),inline=False)
	embed.add_field(name='Top Role:',value=member.top_role.mention,inline=False)

	embed.add_field(name='Joined ', value=f'```{str(member.joined_at)[:16]}```', inline=True)
	embed.add_field(name='Registered', value=f'```{str(member.created_at)[:16]}```', inline=True)
		
	embed.set_footer(text=f'Requested by - {ctx.author}',
	icon_url=ctx.author.avatar_url)


	await ctx.send(embed=embed)



@bot.command()
async def serverinfo(ctx):
    """
    This command shows an overview of the server and displays information like creation date or member count.
    """

    guild = ctx.guild
    embed = discord.Embed(title='B40', description="Community for autistic, depressed people", timestamp=ctx.message.created_at, color=discord.Color.red())
    embed.set_thumbnail(url="https://i.imgur.com/7dyGz0S.jpg")
    embed.add_field(name="Owner:", value="blacky#5204")
    embed.add_field(name="Server ID", value=guild.id)
    embed.add_field(name="Members:", value=guild.member_count)
    embed.add_field(name="Channels:", value=len(guild.channels))
    embed.add_field(name="Roles:", value=len(guild.roles))
    embed.add_field(name="Booster Status:", value=guild.premium_subscription_count)
    
    embed.add_field(name="Created at:", value=str(guild.created_at)[:16])
    embed.set_footer(text=f"Used by {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

@bot.command()
async def map(ctx, *, args):
	picture = GetStreet(args)
	embed = discord.Embed(title=args)
	embed.set_image(url=picture)
	await ctx.send(embed=embed)
	
@bot.command()
async def quote(ctx):
	"""
	sends a random quote
	"""
	
	r_quote = get_quote()
	await ctx.send(r_quote)

@bot.command()
async def country(ctx, *, args):
    """
    Shows extensive stats about a country requested by the user.
    """

    flag_icon, c_name_s, c_name_l, capital, curr_name, currr_symbol, language_list, flag_data, popu_short, area_short, region, region_s = country_api(args)
    shord_field = c_name_s + " " + flag_icon
    embed = discord.Embed(title=c_name_l, description=f"Country in {region}", timestamp=ctx.message.created_at, color=discord.Color.red())
    embed.set_thumbnail(url=flag_data)
    embed.add_field(name="Name:", value=c_name_l)
    embed.add_field(name="Capital:", value=capital)
    embed.add_field(name="Short:", value=shord_field)
    embed.add_field(name="Area:", value=area_short)
    embed.add_field(name="Continent:", value=region_s)
    embed.add_field(name="Population:", value=popu_short)
    embed.add_field(name="Currency:", value=curr_name)
    embed.add_field(name="Symbol:", value=currr_symbol)
    embed.add_field(name="Language(s):", value=language_list)

    embed.set_footer(text=f"Used by {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

@bot.command()
async def weather(ctx, *, args):
    """
    Shows extensive weather stats about a place requested by the user.
    """
    
    try:
        weather_icon_url, country_name, country, country_icon, humidity, wind, temp_celsius, temp_fahrenheit, weather_description= weather_api(args)
        
        country_field = country + " " + country_icon
        embed = discord.Embed(title=args.capitalize(), description=f"A place in {country_name}", timestamp=ctx.message.created_at, color=discord.Color.red())
        embed.set_thumbnail(url=weather_icon_url)
        embed.add_field(name="Country:", value=country_field)
        embed.add_field(name="Humidity:", value=humidity)
        embed.add_field(name="Wind:", value=wind)
        embed.add_field(name="Temp.:", value=temp_celsius)
        embed.add_field(name="Temp.:", value=temp_fahrenheit)
        embed.add_field(name="Weather:", value=weather_description)
        embed.set_footer(text=f"Used by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
    except:pass

@bot.command()
async def word(ctx, *, args):
    """
    dictionary ish display of a word.
    """

    word, phonetic, word_type, definition, example, list_of_synonyms = dictionary(args)
    embed = discord.Embed(title=word, description=definition, timestamp=ctx.message.created_at, color=discord.Color.red())
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Flag_of_the_United_Kingdom.svg/640px-Flag_of_the_United_Kingdom.svg.png")
    embed.add_field(name="Type:", value=word_type)
    embed.add_field(name="Phonetic:", value=phonetic)
    embed.add_field(name="Synonyms:", value=list_of_synonyms)
    embed.add_field(name="Example:", value=example)

    embed.set_footer(text=f"Used by {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

from datalists import tj_dog_pictures
@bot.command()
async def tj(ctx):
	"""
	Returns a random picture of TJs dogs.
	"""

	pic = tj_dog_pictures[random.randint(0,len(tj_dog_pictures)-1)]
	await ctx.send(pic)




@bot.command()
async def omri(ctx):
    await ctx.send("Omri is the 3x Consecutive Holder of the "'Funniest Person In B40'" Title.")

@bot.command()
async def hug(ctx, *, user : discord.Member=None):
	"""
	sends an embed Discord message including who wants to hug who. A random hug-related gif will be attached.
	"""

	embed = discord.Embed(title=f"{ctx.author.name} sends hugs to {user.name}")
	embed.set_image(url=tenor("anime-hugs"))
	await ctx.send(embed=embed)

@bot.command()
async def kiss(ctx, *, user : discord.Member=None):
	"""
	sends an embed Discord message including who wants to kiss who. A random kiss related gif will be attached.
	"""

	embed = discord.Embed(title=f"{ctx.author.name} sends kisses to {user.name}")
	embed.set_image(url=tenor("anime-kiss"))
	await ctx.send(embed=embed)

@bot.command()
async def slap(ctx, *, user : discord.Member=None):
	embed = discord.Embed(title=f"{ctx.author.name} slaps {user.name}")
	embed.set_image(url=tenor("anime-slap"))
	await ctx.send(embed=embed)

@bot.command()
async def cringe(ctx, *, user : discord.Member=None):
	embed = discord.Embed(title=f"{ctx.author.name} cringes at {user.name}")
	embed.set_image(url=tenor("cringe"))
	await ctx.send(embed=embed)

@bot.command()
async def meme(ctx, *, user : discord.Member=None):
	embed = discord.Embed(title=f"{ctx.author.name} requested a meme")
	embed.set_image(url=tenor("meme"))
	await ctx.send(embed=embed)

@bot.command()
async def penis(ctx, *, user : discord.Member=None):
	"""
	Shows stats about the requested persons penis.
	"""

	penis = "8" + "="*random.randint(0, 18) + "D"

	if len(penis)>15:
		penis_info = "DAMN UR PACKING"

	elif len(penis)>9:
		penis_info = "average boi"

	elif len(penis)>2:
		penis_info = "lol bozo + ratio + small pp"

	else:
		penis_info = "LOL U ONLY HAVE BALLS AND A TIP"

	embed = discord.Embed(title='B40 PENIS MEASUREMENT', description=penis_info, timestamp=ctx.message.created_at, color=discord.Color.red())
	embed.set_thumbnail(url="https://i.imgur.com/7dyGz0S.jpg")
	embed.add_field(name="DICK OF:", value=user.mention)
	embed.add_field(name="LENGTH:", value=len(penis))
	embed.add_field(name="UNIT:", value="cm")
	embed.add_field(name="PENIS DISPLAY:", value= penis)
	embed.set_footer(text=f"Used by {ctx.author}", icon_url=ctx.author.avatar_url)

	await ctx.send(embed=embed)


# dont delete this, need this for future reference
@bot.command()
async def test(ctx):
    SENDER_OF_THE_MESSAGE = message.author.mention
    await ctx.send(SENDER_OF_THE_MESSAGE)

#dont delete this either
@bot.command()
async def test2(ctx, *,  user : discord.Member=None):
    usermention = user.mention

    await ctx.send(usermention)

@bot.command()
async def avatar(ctx, *, user : discord.Member=None):
	try:
		embed = discord.Embed(title=f"{user.name}")
		embed.set_image(url=user.avatar_url)
		await ctx.send(embed=embed)
	except:        
		embed = discord.Embed(title=f"{ctx.author.name}")
		embed.set_image(url=ctx.message.author.avatar_url)
		await ctx.send(embed=embed)


# Events
@bot.event
async def on_ready():
    print('My Ready is Body')

@bot.listen()
async def on_message(message):
  if "who asked?" in message.content.lower():
      with open('pictures/SOVAWHOASKED.png', 'rb') as f:
        picture = discord.File(f)
        await message.channel.send(file=picture)

@bot.listen()
async def on_message(message):
    if "blacky?" in message.content.lower():
        with open('pictures/blacky.png','rb') as f:
          picture = discord.File(f)
          await message.channel.send('The Prince of Dubai',file=picture)

@bot.listen()
async def on_message(message):
    if "nigga" in message.content.lower():
        with open('pictures/nword.png','rb') as f:
          picture = discord.File(f)
          await message.channel.send(file=picture)

@bot.listen()
async def on_message(message):
    if "fadil?" in message.content.lower():
        await message.channel.send('The worst valorant player in B40')


@bot.listen()
async def on_message(message):
    if "threat?" in message.content.lower():
        await message.channel.send('The Sexiest Nugget')

@bot.listen()
async def on_message(message):
    if "3bood?" in message.content.lower():
        await message.channel.send('glory hole beta tester')

my_secret = os.environ['TOKEN']
keep_alive()
bot.run(my_secret)

