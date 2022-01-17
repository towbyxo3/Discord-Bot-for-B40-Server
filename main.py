import discord
from discord.ext import commands
import datetime
import os
import random
from urllib import parse, request
import re
import requests
import json



#DONT DELETE ANYTHING YET. PLS INFORM ME BEFORE HAND, I HAVENT FINISHED THE FUNCTIONS IM WORKING ON

#PREFIX
bot = commands.Bot(command_prefix='^', description="description")


#changes big numbers to appropriate units
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', ' K', ' M', ' B', ' T'][magnitude])

def country_api(country):
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
      language_list = "" #list of languages

      for slang, language in languages.items():
            language_list+=language + " "


      flag = data[0]["flags"]["png"] #flag as pic
      
      populatation = data[0]["population"]
      popu_short = human_format(populatation) #population in human readable format
      area = data[0]["area"]/1000
      area_short = '{:,}'.format(area).replace(',','.')+" km²" #area human-readable

      return flag_icon, c_name_s, c_name_l, capital, curr_name, currr_symbol, language_list, flag, popu_short, area_short, region, region_s





def tenor(q):
	tenor_api_key = "LIVDSRZULELA" 
	lmt = 40
	random_pic = random.randint(1,25)

	r = requests.get(
	    "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (q, tenor_api_key, lmt))

	if r.status_code == 200:
	    # load the GIFs using the urls for the smaller GIF sizes
	    tenorgifs = json.loads(r.content)
	    return (tenorgifs["results"][random_pic]["media"][0]["mediumgif"]["url"])
	else:
	    return None

@bot.command()
async def serverinfo(ctx):
      guild = ctx.guild
      embed = discord.Embed(title='B40', description="Community for autistic, depressed people", timestamp=ctx.message.created_at, color=discord.Color.red())
      embed.set_thumbnail(url="https://i.imgur.com/7dyGz0S.jpg")
      embed.add_field(name="Owner:", value="blacky#5204")
      embed.add_field(name="Server ID", value=guild.id)
      embed.add_field(name="Members:", value=guild.member_count)
      embed.add_field(name="Channels:", value=len(guild.channels))
      embed.add_field(name="Roles:", value=len(guild.roles))
      embed.add_field(name="Booster Staus:", value=guild.premium_subscription_count)
      
      embed.add_field(name="Created at:", value=str(guild.created_at)[:16])
      embed.set_footer(text=f"Used by {ctx.author}", icon_url=ctx.author.avatar_url)

      await ctx.send(embed=embed)



@bot.command()
async def country(ctx, *, args):
      flag_icon, c_name_s, c_name_l, capital, curr_name, currr_symbol, language_list, flag, popu_short, area_short, region, region_s = country_api(args)
      shord_field = c_name_s + " " + flag_icon
      embed = discord.Embed(title=c_name_l, description=f"Country in {region}", timestamp=ctx.message.created_at, color=discord.Color.red())
      embed.set_thumbnail(url=flag)
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
async def tj(ctx):
    dog_pics = ["https://cdn.discordapp.com/attachments/930547006521364500/932343519576727653/224B8621-A849-4509-854D-32717BED961A.jpg",
    "https://cdn.discordapp.com/attachments/930547006521364500/931273190481723522/551A6C05-7F32-4789-92D6-B431D882D0BD.jpg",
    "https://cdn.discordapp.com/attachments/930547006521364500/930547380116389988/691FA563-229A-4300-916D-902E4E107FD0.jpg",
    "https://cdn.discordapp.com/attachments/739175633673781262/930462292594786334/6599EB5E-CEEC-4A88-BBD5-2456C201453F.jpg",
    "https://cdn.discordapp.com/attachments/739175633673781262/929373440765485066/IMG_4681.jpg",
    "https://cdn.discordapp.com/attachments/739175633673781262/924434608639049728/IMG_4405.jpg",
    "https://cdn.discordapp.com/attachments/739175633673781262/920632198212763648/A01BD834-C37C-4A4B-8F79-361EFCA15B22.jpg",
    "https://cdn.discordapp.com/attachments/739175633673781262/920633169332547584/IMG_3828.JPG",
    "https://cdn.discordapp.com/attachments/739175633673781262/920631410862207006/7D5EE211-6E60-4EB6-AFB6-0EF7CAD780E1.jpg",
    "https://cdn.discordapp.com/attachments/739175633673781262/932425725347250186/C4C92C61-18C8-44EE-9D00-B813C2AC91F3.jpg"
    ]
    pic = dog_pics[random.randint(0,len(dog_pics)-1)]
    await ctx.send(pic)


@bot.command()
async def omri(ctx):
    await ctx.send("Omri is the 3x Consecutive Holder of the "'Funniest Person In B40'" Title.")

@bot.command()
async def hug(ctx, *, user : discord.Member=None):
      embed = discord.Embed(title=f"{ctx.author.name} sends hugs to {user.name}")
      embed.set_image(url=tenor("anime-hugs"))
      await ctx.send(embed=embed)

@bot.command()
async def kiss(ctx, *, user : discord.Member=None):
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
async def pp(ctx, *, user : discord.Member=None):
      penis = "8" + "="*random.randint(0, 18) + "D"
      
      pptell = ""

      if len(penis)>15:
        pptell = "DAMN UR PACKING"

      elif len(penis)>9:
        pptell = "average boi"

      elif len(penis)>2:
        pptell = "lol bozo + ratio + small pp"

      else:
        pptell = "LOL U ONLY HAVE BALLS AND A TIP"


      embed = discord.Embed(title='B40 PENIS MEASUREMENT', description=pptell, timestamp=ctx.message.created_at, color=discord.Color.red())
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
      with open('SOVAWHOASKED.png', 'rb') as f:
        picture = discord.File(f)
        await message.channel.send(file=picture)

@bot.listen()
async def on_message(message):
    if "blacky?" in message.content.lower():
        with open('blacky.png','rb') as f:
          picture = discord.File(f)
          await message.channel.send('The Prince of Dubai',file=picture)

@bot.listen()
async def on_message(message):
    if "nigga" in message.content.lower():
        with open('penis.png','rb') as f:
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
bot.run(my_secret)

