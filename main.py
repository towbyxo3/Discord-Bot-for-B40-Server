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
from apifunc import *
from chatstatsfunc import *
from formattingfunc import *

#set up the global prefix for bot commands
intents = discord.Intents.default()
intents.members = True

global_prefix = '^'
bot = commands.Bot(command_prefix=global_prefix, description=f"With the prefix {global_prefix} you are able to use following commands \n *optional",intents = intents)


#BOT COMMANDS
#the following bot commands are triggered if message sent by a user consists of the prefix followed by the command function name.
# For example, to trigger the serverinfo function, it would be   "   ^serverinfo    "
#some commands can 
@bot.command()
async def lb(ctx):
	"""
	Returns server leaderboard: lb
	"""

	#get data from mee6s leaderboard
	URL = 'https://mee6.xyz/api/plugins/levels/leaderboard/739175633673781259'

	res = requests.get(URL)
	for count, item in enumerate(res.json()['players']):
		name = item['username']
		id_user = item['id']
		discriminator = item['discriminator']
		level = item['level']
		msg_count = item['message_count']
		xp = item['xp']

	#Structuring the embed message using the data obtained from mee6s website
	embed = discord.Embed(description = "[Leaderboard](https://mee6.xyz/leaderboard/739175633673781259)",timestamp=ctx.message.created_at, color=discord.Color.red())

	embed.set_thumbnail(url="https://i.imgur.com/7dyGz0S.jpg")

	#create fields for the top 10 
	for count, item in enumerate(res.json()['players']):
		nickname = item['username']
		discriminator = item['discriminator']
		level = item ['level']
		xp = item['xp']
		if count<10: #how many ppl the leaderboard shows
			rank = count+1
			embed.add_field(name=f"#{rank}   {nickname}#{discriminator}", value=f"LEVEL {level}       |        {xp} XP",inline=False)

	await ctx.send(embed=embed)






@bot.command()
async def userinfo(ctx,member:discord.Member=None):
	"""
	Returns information about a user: userinfo *@user
	"""

	if member==None:
		member=ctx.author

	rlist = [] #list of all the roles the user has
	for role in member.roles:
		if role.name != "@everyone":
			rlist.append(role.mention)

	b = " ".join(rlist) #format the list 

	embed = discord.Embed(colour=member.color,timestamp=ctx.message.created_at)

	embed.set_author(icon_url=member.avatar_url, name=f"{member}   •   {member.id}"),
	embed.set_thumbnail(url=member.avatar_url),
	embed.add_field(name='Name',value=member.mention,inline=True)
	#embed.add_field(name='Booster', value=f'{("Yes" if member.premium_since else "No")}',inline=True)

	try:
		name = remove_hashtag(str(member))
		level, rank, xp, msg_count =get_level(name)

		embed.add_field(name='Level', value=level,inline=True)
		embed.add_field(name='Rank', value=f"#{rank}",inline=True)
		#embed.add_field(name='XP',value=xp,inline=True)
		#embed.add_field(name='Msg Count', value=msg_count,inline=True)
	except Exception as e:
		print(str(e))

	embed.add_field(name=f'Roles ({len(rlist)})',value=''.join([b]),inline=False)
	#embed.add_field(name='Top Role:',value=member.top_role.mention,inline=False)
	embed.add_field(name='Joined', value=f'{str(member.joined_at)[:16]}', inline=True)
	embed.add_field(name='Registered', value=f'{str(member.created_at)[:16]}', inline=True)
		
	#embed.set_footer(text=f'Requested by - {ctx.author}',
	#icon_url=ctx.author.avatar_url)

	await ctx.send(embed=embed)


@bot.command()
async def moveall(ctx: commands.Context):
	if ctx.author.guild_permissions.kick_members:
		for voice_channel in ctx.guild.voice_channels:
			if voice_channel is ctx.author.voice.channel:
				print(voice_channel)
				continue
			for x in voice_channel.members:
				print(x.name)
				await x.move_to(ctx.author.voice.channel) 





@bot.command()
async def serverinfo(ctx):
    """
    Returns information about the server: serverinfo
    """

    guild = ctx.guild
    embed = discord.Embed(title='B40', description="Community for autistic, depressed people", timestamp=ctx.message.created_at, color=discord.Color.red())
    embed.set_thumbnail(url="https://i.imgur.com/7dyGz0S.jpg")
    embed.add_field(name="Owner", value="blacky#5204")
    embed.add_field(name="Server ID", value=guild.id)
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Channels", value=len(guild.channels))
    embed.add_field(name="Roles", value=len(guild.roles))
    embed.add_field(name="Boosters", value=guild.premium_subscription_count)
    embed.add_field(name="Created on", value=str(guild.created_at.strftime("%b %d, %Y"))[:16])
    embed.set_footer(text=f"Used by {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

@bot.command()
async def map(ctx, *, args):
	"""
	Returns picture of an address/place: map [place/address/sight]
	"""

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
    Returns extensive stats of a country: country [country name]
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
    Returns weather stats of a location: weather [location]
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
    Returns dictionary-entry of a word: word [word]
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

@bot.command()
async def omri(ctx):
	"""
	Returns an important piece of information about Omri
	"""

	await ctx.send("Omri is the 4x Consecutive Holder of the "'Funniest Person In B40'" Title.")

@bot.command()
async def hug(ctx, *, user : discord.Member=None):
	"""
	Returns hug gif: hug @user
	"""

	embed = discord.Embed(title=f"{ctx.author.name} sends hugs to {user.name}")
	embed.set_image(url=tenor("anime-hugs"))

	await ctx.send(embed=embed)

@bot.command()
async def kiss(ctx, *, user : discord.Member=None):
	"""
	Returns kiss gif: kiss @user
	"""

	embed = discord.Embed(title=f"{ctx.author.name} sends kisses to {user.name}")
	embed.set_image(url=tenor("anime-kiss"))

	await ctx.send(embed=embed)

@bot.command()
async def kill(ctx, *, user : discord.Member=None):
	"""
	Returns kill gif: kill @user
	"""

	embed = discord.Embed(title=f"{ctx.author.name} kills {user.name}")
	embed.set_image(url=tenor("among-us-kill"))

	await ctx.send(embed=embed)

@bot.command()
async def slap(ctx, *, user : discord.Member=None):
	"""
	Returns slap gif: slap @user
	"""

	embed = discord.Embed(title=f"{ctx.author.name} slaps {user.name}")
	embed.set_image(url=tenor("anime-slap"))

	await ctx.send(embed=embed)

@bot.command()
async def cringe(ctx, *, user : discord.Member=None):
	"""
	Returns cringe gif: cringe @user
	"""

	embed = discord.Embed(title=f"{ctx.author.name} cringes at {user.name}")
	embed.set_image(url=tenor("cringe"))

	await ctx.send(embed=embed)

@bot.command()
async def punch(ctx, *, user : discord.Member=None):
	"""
	Returns punch gif: punch @user
	"""

	embed = discord.Embed(title=f"{ctx.author.name} punches {user.name}")
	embed.set_image(url=tenor("anime-punch"))

	await ctx.send(embed=embed)

@bot.command()
async def kick(ctx, *, user : discord.Member=None):
	"""
	Returns kick gif: kick @user
	"""

	embed = discord.Embed(title=f"{ctx.author.name} kicks {user.name}")
	embed.set_image(url=tenor("anime-kick"))

	await ctx.send(embed=embed)

@bot.command()
async def penis(ctx, *, user : discord.Member=None):
	"""
	Returns penis stats of user: penis @user
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
#@bot.command()
#async def test(ctx):
#    SENDER_OF_THE_MESSAGE = message.author.mention
#    await ctx.send(SENDER_OF_THE_MESSAGE)

#dont delete this either
#@bot.command()
#async def test2(ctx, *,  user : discord.Member=None):
#    usermention = user.mention

#    await ctx.send(usermention)

@bot.command()
async def avatar(ctx,member:discord.Member=None):
	"""
	Returns Avatar of user: avatar *@user
	"""

	if member==None:
		member=ctx.author

	
	embed = discord.Embed(colour=member.color,timestamp=ctx.message.created_at)
	embed.set_author(icon_url=member.avatar_url, name=f"{member}   •   {member.id}"),
	embed.set_image(url=member.avatar_url)

	await ctx.send(embed=embed)



# Events
@bot.event
async def on_ready():
    print('My Ready is Body')


@bot.listen()
async def on_message(message):
  if "ninja" in message.content.lower():
      with open('pictures/ninja.jpg', 'rb') as f:
        picture = discord.File(f)

        await message.channel.send(file=picture)

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
"""
@bot.listen()
async def on_message(message):
    if "nigga" in message.content.lower():
        with open('pictures/nword.png','rb') as f:
          picture = discord.File(f)

          await message.channel.send(file=picture)"""

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

@bot.listen()
async def on_message(message):	
	bad_words = ["nigga","nigger","niggger","niger","ni55er","ni33er","nibber","nibba"]
	for word in bad_words:
		if word in message.content.lower():

			
			with open('databases/ncounter.json', 'r') as file:
				chat_data = json.load(file)
				new_user = str(message.author.id)
			if new_user in chat_data:
				chat_data[new_user] += 1
				with open('databases/ncounter.json', 'w') as update_user_data:
					json.dump(chat_data, update_user_data, indent=4)
			else:
				chat_data[new_user] = 1
				with open('databases/ncounter.json', 'w') as new_user_data:
					json.dump(chat_data, new_user_data, indent=4)
			await message.delete()




@bot.listen()
async def on_message(message):
	if not message.author.bot:
		if not message.content.startswith('!'):
			with open('databases/chat_leaderboard.json', 'r') as file:
				chat_data = json.load(file)
				new_user = str(message.author.id)

			# Update existing user
			if new_user in chat_data:
				chat_data[new_user] += 1
				with open('databases/chat_leaderboard.json', 'w') as update_user_data:
					json.dump(chat_data, update_user_data, indent=4)

			# Add new user
			else:
				chat_data[new_user] = 1
				with open('databases/chat_leaderboard.json', 'w') as new_user_data:
					json.dump(chat_data, new_user_data, indent=4)

@bot.command()
async def chat(ctx):
	"""
	Returns the leaderboard graphically.
	"""
	with open('databases/chat_leaderboard.json', 'r') as file:
		chat_data = json.load(file)

	user_ids = list(chat_data.keys())
	user_message_counts = list(chat_data.values())

	new_leaderboard = []

	for index, user_id in enumerate(user_ids, 1):
		new_leaderboard.append([user_id, user_message_counts[index - 1]])

	# Sort leaderboard order by user message count
	new_leaderboard.sort(key=lambda items: items[1], reverse=True)

	user_rank_column = []
	user_name_column = []
	user_message_count_column = []

	# User ranks
	for rank_index, rank_value in enumerate(new_leaderboard[:10]):
		user_rank_column.append([rank_index + 1])

	# User names
	for name_index, name_value in enumerate(new_leaderboard[:10]):
		user_name_column.append([await bot.fetch_user(int(name_value[0]))])

	# User message counts
	for message_count_index, message_count_value in enumerate(new_leaderboard[:10]):
		user_message_count_column.append([message_count_value[1]])

	# Add column to table
	user_rank_table = tabulate(user_rank_column, tablefmt='plain', headers=['#\n'], numalign='right')
	user_name_table = tabulate(user_name_column, tablefmt='plain', headers=['Name\n'], numalign='right')
	user_message_count_table = tabulate(user_message_count_column, tablefmt='plain', headers=['Messages\n'],
										numalign='right')

	# Image
	image_template = Image.open('assets/chat_leaderboard_template.png')

	# Font
	font = ImageFont.truetype('theboldfont.ttf', 24)

	# Positions
	rank_text_position = 100, 50
	name_text_position = 270, 50
	message_count_text_position = 520, 50

	# Draws
	draw_on_image = ImageDraw.Draw(image_template)
	draw_on_image.text(rank_text_position, user_rank_table, 'white', font=font)
	draw_on_image.text(name_text_position, user_name_table, 'white', font=font)
	draw_on_image.text(message_count_text_position, user_message_count_table, 'white', font=font)

	# Save image
	image_template.convert('RGB').save('chat_leaderboard.jpg', 'JPEG')

	await ctx.send(file=discord.File('chat_leaderboard.jpg'))




@bot.listen()
async def on_message(message):
	if not message.author.bot:
		if not message.content.startswith('^'):
			#open json file
			with open('databases/chat_user_stats.json', 'r') as file:
				chat_data = json.load(file)
				new_user = str(message.author.id)
				today_date = str(datetime.date.today())

			#if new date, create new json dic
			if today_date in chat_data:
				pass
			else:
				chat_data[today_date]={}

			#update existing user at date
			if new_user in chat_data[today_date]:
				chat_data[today_date][new_user]["total_messages"]+=1
				if len(message.clean_content)>600 or "http" in message.content.lower():
					chat_data[today_date][new_user]['total_messages_length']+=5
				else:
					chat_data[today_date][new_user]['total_messages_length']+=len(message.clean_content)
				with open('databases/chat_user_stats.json', 'w') as update_user_data:
					json.dump(chat_data, update_user_data, indent=4)

			else:
				chat_data[today_date][new_user] = {"total_messages":1,"total_messages_length": len(message.clean_content)}
				with open('databases/chat_user_stats.json', 'w') as new_user_data:
					json.dump(chat_data, new_user_data, indent=4)
			
			#SERVERCHAT 
			with open('databases/server_stats.json', 'r') as file:
				chat_data = json.load(file)
				if today_date in chat_data:
					pass
				else:
					chat_data[today_date]={"total_server_messages":0,"total_server_messages_length":len(message.clean_content),"links":0,"members":message.guild.member_count,"files":0}
					with open('databases/server_stats.json', 'w') as new_user_data:
						json.dump(chat_data, new_user_data, indent=4)
				
				with open('databases/server_stats.json', 'r') as file:
					chat_data = json.load(file)
					if len(message.clean_content)>600 or "http" in message.content.lower():
						chat_data[today_date]['total_server_messages_length']+=5
					else:
						chat_data[today_date]['total_server_messages_length']+=len(message.clean_content)
					if "http" in message.content.lower():
						chat_data[today_date]['links']+=1
					chat_data[today_date]["total_server_messages"]+=1
					if len(message.attachments) >0:
						chat_data[today_date]["files"]+=1					
					with open('databases/server_stats.json', 'w') as new_user_data:
						json.dump(chat_data, new_user_data, indent=4)

@bot.command()
async def userchat(ctx,chat_date = str(datetime.date.today())):
	
	top_10_date,top_10_messages, top_10_messages_length = get_date_user_chat_information(chat_date)

	embed = discord.Embed(title=f"Chat Leaderboard [{chat_date}]", timestamp=ctx.message.created_at, color=discord.Color.red())
	embed.set_thumbnail(url="https://i.imgur.com/7dyGz0S.jpg")
	for i in range(10):
		rank = i+1
		userid = top_10_date[i]
		try:
			userid = await ctx.author.guild.fetch_member(userid)
		except:
			pass

		total_msg = top_10_messages[i]
		total_msg_len = top_10_messages_length[i]
		avg = round(total_msg_len/total_msg,1)

		embed.add_field(name=f"{rank}. {userid}", value=f" {total_msg} :envelope:  | {total_msg_len} :abc:  |  {avg} Chars/Msg",inline=False)
	await ctx.send(embed=embed)





@bot.command()
async def serverchat(ctx,chat_date = str(datetime.date.today())):
	"""
	Returns chat stats of a particular date: serverchat YYYY-DD-MM
	"""

	try:
		with open('databases/server_stats.json','r') as file:
			server_chat_data = json.load(file)
			total_messages = server_chat_data[chat_date]["total_server_messages"]
			total_characters = server_chat_data[chat_date]["total_server_messages_length"]
			avg_msg_len = total_characters/total_messages

			guild = ctx.guild
			embed = discord.Embed(title=f'B40 Chat Stats [{chat_date}]', timestamp=ctx.message.created_at, color=discord.Color.red())
			embed.set_thumbnail(url="https://i.imgur.com/7dyGz0S.jpg")
			embed.add_field(name="Messages", value = total_messages)
			embed.add_field(name="Characters", value = total_characters)
			embed.add_field(name="Average", value = f"~{round(avg_msg_len,1)} chars/msg")
			embed.add_field(name="Files", value = server_chat_data[chat_date]["files"])
			embed.add_field(name="Links", value = server_chat_data[chat_date]["links"])
			embed.add_field(name="Participants", value = get_unique_chat_participants(chat_date))
			embed.set_footer(text=f"Used by {ctx.author}", icon_url=ctx.author.avatar_url)

			await ctx.send(embed=embed)
	except:
		await ctx.send("Check formatting: ^serverinfo YYYY-MM-DD")


@bot.command()
async def userchatdate(ctx,chat_date,member: discord.Member = None):
	try:	
		if member==None:
			member=ctx.author

		total_messages, total_messages_length = get_user_chat_date_information(chat_date,member.id)
		avg = round(total_messages_length/total_messages,1)

		
		embed = discord.Embed(colour=member.color,timestamp=ctx.message.created_at)

		embed.set_author(icon_url=member.avatar_url, name=f"{member}   •   {chat_date}"),
		embed.set_thumbnail(url=member.avatar_url)
		embed.add_field(name='Messages',value=total_messages,inline=True)
		embed.add_field(name='Characters',value=total_messages_length,inline=True)
		embed.add_field(name='Chars/Msg',value=avg,inline=True)
		

		await ctx.send(embed=embed)
	except:
		await ctx.send("No messages found")




my_secret = os.environ['TOKEN']
keep_alive()
bot.run(my_secret)

