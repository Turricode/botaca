import discord
from discord.ext import commands

from googleapiclient.discovery import build
import pafy

from dotenv import dotenv_values

bot = commands.Bot(command_prefix='$')

CONFIG = dotenv_values('.env')
TOKEN = CONFIG['DISCORD_TOKEN']
YT_TOKEN = CONFIG['YOUTUBE_TOKEN']

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

if TOKEN == None:
    print('Invalid .env varibale')
    exit()


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, *args):

    if not ctx.author.voice:
        await ctx.send('Join a voice channel')
        return

    channel = ctx.author.voice.channel

    vc = await channel.connect()
    url = find_url(''.join(args))

    if(url == None):
        await ctx.send('Url for args not found')
        return 

    
    song = pafy.new(url)
    audio = song.getbestaudio()

    source = discord.FFmpegPCMAudio(executable=CONFIG['FFMPEG_PATH'], source=audio.url, **FFMPEG_OPTIONS)

    vc.play(source)


def find_url(name):
    yt = build('youtube', 'v3', developerKey=YT_TOKEN)
    req = yt.search().list(q=name, part='snippet', type='video')
    res = req.execute()

    if res['items'] == []:
        return

    return f'https://youtu.be/{res["items"][0]["id"]["videoId"]}'

if __name__ == '__main__':
    bot.run(TOKEN)
