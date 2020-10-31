# bot.py
import os
from discord.ext import commands
import discord

import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)

from datetime import date, datetime
import holidays

import csv
import random
import json
import uuid
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
async def holiday(ctx):
    curr_day = date.today()
    year = curr_day.year

    closed = {
            holidays.calc_easter(year): 'Easter',
            holidays.get_irregular_date('Sunday', 2, 5, year): 'Mother\'s Day',
            holidays.get_irregular_date('Saturday', 4, 5, year): 'Memorial Day Weekend',
            holidays.get_irregular_date('Sunday', 4, 5, year): 'Memorial Day Weekend',
            holidays.get_irregular_date('Monday', 4, 5, year): 'Memorial Day',
            date(year, 7, 4): 'July 4th',
            holidays.get_irregular_date('Monday', 1, 9, year): 'Labor Day',
            holidays.get_irregular_date('Thursday', 4, 11, year): 'Thanksgiving'
    }

    if curr_day in closed:
        holiday_name = closed[curr_day]
        await ctx.send('The Edge is **closed** for {}'.format(holiday_name))
    else:
        await ctx.send('The Edge is **open** today!')

@bot.command()
async def plot(ctx):
    dates = []
    people = []
    with open('edge_data.csv', "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.reader(scraped, delimiter=",")
        for row in reader:
            if row:  # avoid blank lines
                people.append(row[0])
                time = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')
                dates.append(time)

    rule = rrulewrapper(YEARLY, interval=24)
    loc = RRuleLocator(rule)
    formatter = DateFormatter('%m/%d/%y')
    fig, ax = plt.subplots()
    plt.plot_date(dates, people)
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)

    imagename = 'graphs/{}.png'.format(uuid.uuid1())
    plt.savefig(imagename)
    await ctx.send(file=discord.File(imagename))


bot.run(os.getenv("TOKEN"))
