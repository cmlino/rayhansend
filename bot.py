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

def import_csv(file_name):
    data = []
    row_index = 0
    with open(file_name, "r", encoding="utf-8", errors="ignore") as scraped:
        reader = csv.reader(scraped, delimiter=',')
        for row in reader:
            if row:  # avoid blank lines
                row_index += 1
                columns = [str(row_index), row[0], row[1] ]
                data.append(columns)
    return data

data = import_csv("edge_data.csv")
last_row = data[-1]

@client.event
async def on_message(message):
    if '!ppl' in message.content.lower():
        await message.channel.send(
            last_row
        )

client.run(TOKEN)
