import Data
import asyncio
import sympy
from discord.ext import commands

bot = commands.Bot(command_prefix=Data.COMMAND_PREFIX)

@bot.async_event
async def on_ready():
    print("Beep Boop\n---------------------")

@bot.command(pass_context=True, aliases=[])
async def join(context):
    for sv in Data.channels:
        if context.message.server.id in sv:
            await bot.say("Already connected to a channel in this server")
            return
    try:
        if context.message.author.voice.voice_channel:
            voiceClient = await bot.join_voice_channel(context.message.author.voice.voice_channel)
            Data.channels.append([context.message.server.id, voiceClient, [], False, None])
            await bot.say("Joined Voice Channel")
    except:
        print("Fuck you, you just hurt me!")

@bot.command(pass_context=True, aliases=["stop"])
async def leave(context):
    for i in range(0, len(Data.channels)):
        if context.message.server.id in Data.channels[i]:
            await Data.channels[i][1].disconnect()
            Data.channels.pop(i)
            await bot.say("Left Voice Channel")
            return

@bot.command(pass_context=True, aliases=[])
async def play(context, *, url):
    for sv in Data.channels:
        if context.message.server.id in sv:
            await bot.say("Song Added")
            if not sv[2]:
                sv[2].append(url)
                asyncio.get_event_loop().create_task(playSongs(context.message.server.id))
                return
            sv[2].append(url)
            return

# @bot.command(pass_context=True, aliases=[])
# async def math(context, *, expression):
#     try:
#         res = sympy.N(expression, 5)
#     except:
#         print("Error parsing math expression")
#         return
#     await bot.say("Result: " + str(res))

async def playSongs(server):
    for i in range(0, len(Data.channels)):
        if server in Data.channels[i]:
            voiceClient = Data.channels[i][1]
            try:
                while Data.channels[i][2]:
                    url = Data.channels[i][2][0]
                    try:
                        player = await voiceClient.create_ytdl_player(url, ytdl_options={"default_search":"ytsearch","noplaylist":True}, before_options="-err_detect ignore_err")
                    except:
                        print("The player hurt me daddy!")
                        Data.channels[i][2].pop(0)
                        Data.channels[i][4] = None
                        Data.channels[i][3] = False
                        continue
                    Data.channels[i][4] = player
                    player.volume = Data.STARTING_VOLUME
                    player.start()
                    # await bot.say("Now Playing " + player.title)
                    while not player.is_done() and not Data.channels[i][3]:
                        await asyncio.sleep(1)
                    player.stop()
                    del player
                    Data.channels[i][2].pop(0)
                    Data.channels[i][4] = None
                    Data.channels[i][3] = False
            except Exception as e:
                print("Your play song hurt me again for being out of index")
                print(e)
            return

@bot.command(pass_context=True, aliases=[])
async def queue(context):
    for sv in Data.channels:
        if context.message.server.id in sv:
            msg = "```\n----------Queue----------\n"
            for url in sv[2]:
                msg += url + "\n"
            await bot.say(msg[:1997] + "```")
            return

@bot.command(pass_context=True, aliases=[])
async def skip(context):
    for i in range(0, len(Data.channels)):
        if context.message.server.id in Data.channels[i]:
            Data.channels[i][3] = True
            await bot.say("Skipped Song")
            return

@bot.command(pass_context=True, aliases=[])
async def vol(context, vol):
    try:
        volume = int(vol)
    except:
        print("Non integer numbers hurt me senpai!")
        return
    for i in range(0, len(Data.channels)):
        if context.message.server.id in Data.channels[i]:
            if Data.channels[i][4]:
                try:
                    if volume > 200:
                        volume = 200
                    elif volume < 0:
                        volume = 0
                    volume /= 100
                    Data.STARTING_VOLUME = volume
                except:
                    print("Couldn't set the volume, maybe the number was too big to divide. Please don't punish me daddy")
                    return
                Data.channels[i][4].volume = volume
                await bot.say("Volume Set To: " + str(int(Data.channels[i][4].volume * 100)) + "%")
                return

@bot.command(pass_context=True, aliases=[])
async def pause(context):
    for i in range(0, len(Data.channels)):
        if context.message.server.id in Data.channels[i]:
            if Data.channels[i][4]:
                Data.channels[i][4].pause()
                await bot.say("Song Paused")
                return

@bot.command(pass_context=True, aliases=[])
async def resume(context):
    for i in range(0, len(Data.channels)):
        if context.message.server.id in Data.channels[i]:
            if Data.channels[i][4]:
                Data.channels[i][4].resume()
                await bot.say("Song Resumed")
                return

@bot.async_event
async def on_message(message):
    if message.content == "(╯°□°）╯︵ ┻━┻":
        await bot.send_message(message.channel, "┬─┬﻿ ノ( ゜-゜ノ)")
        return
    if message.author.id == Data.ID:
        if message.content == "┬─┬﻿ ノ( ゜-゜ノ)":
            return
        asyncio.get_event_loop().create_task(del_message(message, 8))
    else:
        if message.content[0] == Data.COMMAND_PREFIX:
            asyncio.get_event_loop().create_task(del_message(message, 2))

    await bot.process_commands(message)

async def del_message(msg, delay=0):
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(msg)
    except:
        print("Couldn't delete the message... I'm sad...")

bot.run(Data.TOKEN, bot=True, reconnect=True)