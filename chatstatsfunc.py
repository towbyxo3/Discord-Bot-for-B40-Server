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





def get_user_chat_date_information(chat_date,id):
	with open('databases/chat_user_stats.json','r') as file:
		chat_data = json.load(file) 
		data = chat_data[chat_date]
		total_messages = data[str(id)]['total_messages']
		total_messages_length = data[str(id)]['total_messages_length']
		return total_messages, total_messages_length


def get_date_user_chat_information(chat_date):
	with open('databases/chat_user_stats.json', 'r') as file:
		chat_data = json.load(file)
		data = chat_data[chat_date]
		top_10_date = sorted(data, key=lambda x: (data[x]['total_messages']),reverse=True)
		top_10_messages = []
		top_10_messages_length = []
		for i in top_10_date:
			top_10_messages.append(chat_data[chat_date][i]["total_messages"])
			top_10_messages_length.append(chat_data[chat_date][i]["total_messages_length"])
		return top_10_date,top_10_messages, top_10_messages_length


def get_unique_chat_participants(date):
	"""
	Counts unique chat participants at a particular date.
	"""

	with open('databases/chat_user_stats.json','r') as file:
		chat_data = json.load(file)

		return len(chat_data[date])
		