# bot.py
import os
from discord.ext import commands

from datetime import date
import calendar, dateutil

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

def get_irregular_date(weekday: str, num: int, month: int, year: int) -> date:
    '''
    generates date object for an irregular date (eg. the 4th Sunday of April)

    :param weekday: the day of the week (eg. "Sunday")
    :param num: the week number (eg. 4)
    :param month: the month number (eg. 4)
    :param year: the year (eg. 2020)
    :return: a datetime.date object representing the specified irregular date
    '''
    days = {
        'Sunday': 0,
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
        'Saturday': 6
    }
    day_index = days[weekday]

    cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
    month = cal.monthdatescalendar(year, month)
    irregular_date = month[num - 1, day_index]

    # calendar pads the start of month with days from the previous month
    # ensure we return a date from the proper month
    if irregular_date.month != month:
        irregular_date = month[num, day_index]

    return irregular_date

@bot.command()
async def holiday(ctx):
    curr_day = date.today()
    year = curr_day.year

    closed = {
            dateutil.easter.easter(year): 'Easter',
            get_irregular_date('Sunday', 2, 5, year): 'Mother\'s Day',
            get_irregular_date('Saturday', 4, 5, year): 'Memorial Day Weekend',
            get_irregular_date('Sunday', 4, 5, year): 'Memorial Day Weekend',
            get_irregular_date('Monday', 4, 5, year): 'Memorial Day',
            date(year, 7, 4): 'July 4th',
            get_irregular_date('Monday', 1, 9, year): 'Labor Day',
            get_irregular_date('Thursday', 4, 11, year): 'Thanksgiving'
    }

    if today in us_holidays:
        holiday_name = us_holidays[today]
        if holiday_name in closed:
            await ctx.send('The Edge is **closed** for {}'.format(holiday_name))
        else:
            await ctx.send('The Edge is **open** for {}'.format(holiday_name))
    else:
        await ctx.send('No it\'s not :upside_down:')

bot.run(os.getenv("TOKEN"))