import discord
from discord.ext import commands
from discord.ext.tasks import loop
from jotform import JotformAPIClient
import json

client = commands.Bot(command_prefix='key ')

def load_data():
    with open('keys.json', 'r') as f:
        return json.load(f)

@client.command()
async def enter(ctx, code):
    success_role = ctx.guild.get_role(690400019282526229)
    data = load_data()
    if data.get(ctx.author.name, None) == code or data.get(str(ctx.author), None) == code or data.get(str(ctx.author.nick), None) == code:
        await ctx.send('https://66.media.tumblr.com/6924ed150fd01ad56327c46d29d05285/tumblr_nxv9vnr00V1s3uawvo1_400.gif')
        await ctx.send('Access granted, you may enter the castle.')
        await ctx.author.add_roles(success_role)
    else:
        await ctx.send('https://thumbs.gfycat.com/IdenticalBackJaguarundi-size_restricted.gif')
        await ctx.send('Access denied, you\'re not getting in. Try again in 5 minutes.')

client.run('')
