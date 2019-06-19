import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands.cooldowns import BucketType
import asyncio
import requests
import os
import platform
import colorsys
import random
import time
from discord.voice_client import VoiceClient
from discord import Game, Embed, Color, Status, ChannelType


Forbidden= discord.Embed(title="Permission Denied", description="1) Please check whether you have permission to perform this action or not. \n2) Please check whether my role has permission to perform this action in this channel or not. \n3) Please check my role position.", color=0x00ff00)
client = Bot(description="DarkBot Bot is best", command_prefix="d!", pm_help = True)
client.remove_command('help')


async def status_task():
    while True:
        await client.change_presence(game=discord.Game(name='for d!help'))
        await asyncio.sleep(5)
        await client.change_presence(game=discord.Game(name='with '+str(len(set(client.get_all_members())))+' users'))
        await asyncio.sleep(5)
        await client.change_presence(game=discord.Game(name='in '+str(len(client.servers))+' servers'))
        await asyncio.sleep(5)


@client.command(pass_context=True)
async def play (ctx, url):
    channel = ctx.message.author.voice_channel
    await client.join_voice_channel(channel)
    server = ctx.message.server
    voice = client.voice_client_in(server)
    player = await voice.create_ytdl_player(url)
    player_dict[server.id] = player
    await client.send_message(ctx.message.channel, "Playing `%s` now" % player.title)
    player.start()


@client.command(pass_context=True)
async def stop(ctx):
    server = ctx.message.server
    player = player_dict[server.id]
    player.stop()
    await client.send_message(ctx.message.channel, "Stopped `%s`" % player.title)
    del player_dict[server.id]


@client.command(pass_context=True)
async def pause(ctx):
    server = ctx.message.server
    player = player_dict[server.id]
    player.pause()
    await client.send_message(ctx.message.channel, "Paused `%s`" % player.title)


@client.command(pass_context=True)
async def resume(ctx):
    server = ctx.message.server
    player = player_dict[server.id]
    player.resume()
    await client.send_message(ctx.message.channel, "Resumed `%s`" % player.title)


client.run(str(os.environ.get('BOT_TOKEN')))
