# bot.py
import os
import discord
from discord.ext import commands
import csv
import random
import json
import re
import requests
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix='!')

def get_climbers():
    response = requests.get("https://portal.rockgympro.com/portal/public/5b68a6f4de953dcb1285dc466295eb59/occupancy")

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    people = int((re.search(r"'count' : (\d+)", response.text).group(1)))
    last_update = str((re.search(r"\d+:\d+ [AP]M", response.text).group()))

    return (people, last_update)
  
def fetch_most_recent(file_name):
    data = ""
    with open(file_name, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.reader(scraped, delimiter=",")
        for row in reader:
            if row:  # avoid blank lines
                data = row
    print(data)
    return data

@client.event
async def on_ready():
    data = get_climbers()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{data[0]} climbers"))
    print(f"{client.user} has connected to Discord!")


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
async def stretch(ctx):
    stretches = [ "Russian twists", " https://www.youtube.com/watch?v=6A2V9Bu80J4", "Side planks", ":penguin:s", "Plank", "Hollow body", "Superman", "Pull up ", "Wall sit", "Cobra", "Weird hand thing", "Bicycles", "Sit up ", "Crunches", "Plank (1 min)", "Plank (1 min)", "Plank (1 min)", "Plank"  ]

    await ctx.send(
        f"{random.choice(stretches)} {random.randint(0, 200)} reps"
    )

@bot.command()
async def holidays(ctx):
    await ctx.send(
            """
            ```
            The Edge is open:
                New Years Eve and Day
                MLK Day
                President's Day
                Columbus Day
                Veteran's Day

            The Edge is closed:
                Easter Sunday
                Mother's Day
                Memorial Day Weekend (Sat-Mon)
                July 4th
                Labor Day
                Thanksgiving
            ```
            """
        )

bot.run(os.getenv("TOKEN"))
