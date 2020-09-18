# bot.py
import os
import discord
import csv
TOKEN = 'NzU0ODQ1NzI0MDU4ODQ1Mjk0.X16q3A.zN9RjxnkkPKpSNU0UjMFVvofr9U'
GUILD = 'CRIMB'


client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

def fetch_most_recent(file_name):
    data = ''
    with open(file_name, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.reader(scraped, delimiter=',')
        for row in reader:
            if row:  # avoid blank lines
                data = row
    return data

@client.event
async def on_message(message):
    if '!ppl' in message.content.lower():
        data = fetch_most_recent("edge_data.csv")
        await message.channel.send(
            data
        )

client.run(TOKEN)
