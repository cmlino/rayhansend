# bot.py
import os
from discord.ext import commands

from datetime import date
import holidays

import csv
import random
import json
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


def fetch_most_recent(file_name):
    data = ""
    with open(file_name, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.reader(scraped, delimiter=",")
        for row in reader:
            if row:  # avoid blank lines
                data = row
    print(data)
    return data


@bot.command()
async def ppl(ctx):
    total_people, recent_time, updated_time = fetch_most_recent("edge_data.csv")
    total_people = int(total_people)
    print(total_people)
    print(updated_time)
    prime_time_string = '**:rotating_light: PRIME CLIMB TIME :rotating_light:** \n '
    await ctx.send(
        f"{prime_time_string if total_people <= 15 else ''}{total_people} climbers (last updated at {updated_time})"
    )


@bot.command()
async def beta(ctx):
    f = open('beta.json')
    phrases = json.load(f)

    await ctx.send(
        random.choice(phrases['beta'])
    )


@bot.command()
async def holidays(ctx):
    closed = ['Easter', 'Mother\'s Day', 'Memorial Day Weekend', 'July 4th', 'Labor Day', 'Thanksgiving']
    today = date.today()
    us_holidays = holidays.US(years=today.year).items()
    if today in us_holidays:
        holiday_name = us_holidays[today]
        if holiday_name in closed:
            await ctx.send('The Edge is **closed** for {}'.format(holiday_name))
        else:
            await ctx.send('The Edge is **open** for {}'.format(holiday_name))
    else:
        await ctx.send('No it\'s not :sad:')

bot.run(os.getenv("TOKEN"))