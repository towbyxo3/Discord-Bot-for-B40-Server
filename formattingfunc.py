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


def remove_hashtag(username):
	"""
	Removes the discriminatorof in a users name
	"""

	name_cut = username.partition('#')
	name = name_cut[0]

	return name


def human_format(num):
    """
    converts population numbers to readable formats using K, M. and returns them as string.

    code from https://stackoverflow.com/a/45846841
    """

    num = float('{:.3g}'.format(num))
    magnitude = 0

    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0

    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', ' K', ' M', ' B', ' T'][magnitude])


