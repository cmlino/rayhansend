# bot.py
import os
import discord
import csv
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

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
async def on_message(message):
    if "!ppl" in message.content.lower():
        total_people, recent_time, updated_time = fetch_most_recent("edge_data.csv")
        total_people = int(total_people)
        print(total_people)
        print(updated_time)
        prime_time_string = '**:rotating_light: PRIME CLIMB TIME :rotating_light:** \n '
        await message.channel.send(
            f"{prime_time_string if total_people <= 15 else ''}{total_people} climbers (last updated at {updated_time})"
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


client.run(os.getenv("TOKEN"))
