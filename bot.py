# bot.py
import os
import re
import csv
import random
import discord
import requests
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()

def get_climbers():
    response = requests.get("https://portal.rockgympro.com/portal/public/5b68a6f4de953dcb1285dc466295eb59/occupancy")

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

@client.event
async def on_message(message):

    if "!ppl" in message.content.lower():
        data = get_climbers()
        prime_time_string = '**:rotating_light: PRIME CLIMB TIME :rotating_light:** \n'
        await message.channel.send(
            f"{prime_time_string if data[0] <= 15 else ''}{data[0]} climbers (last updated at {data[1]})"
        )

    if "!holidays" in message.content.lower():
        await message.channel.send(
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

    if "!beta" in message.content.lower():

        beta = [ "Be taller", "It's just not physically possible for someone of your height :(", 
        "Just stand up", "You have a foot to your left", "Technically that jug is part of the route", 
        "You bicycle?", "You go from the start to the end hold", "BETA", "beta", "beta!", "BETA!",
        "Just do a pull up", "Just dyno it", "Have you tried campusing?" ]

        await message.channel.send(
            random.choice(beta)
        )

client.run(os.getenv("TOKEN"))
