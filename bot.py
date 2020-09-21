# bot.py
import os
import discord
import csv

TOKEN = "NzU0ODQ1NzI0MDU4ODQ1Mjk0.X16q3A.zN9RjxnkkPKpSNU0UjMFVvofr9U"
GUILD = "CRIMB"


client = discord.Client()


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})\n"
    )

    members = "\n - ".join([member.name for member in guild.members])
    print(f"Guild Members:\n - {members}")


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
        if total_people <= 15:
            await message.channel.send(
                "**:rotating_light: PRIME CLIMB TIME :rotating_light:** \n {} climbers (last updated at {})".format(
                    total_people, updated_time
                )
            )
        else:
            await message.channel.send(
                "{} climbers (last updated at {})".format(total_people, updated_time)
            )


client.run(TOKEN)
