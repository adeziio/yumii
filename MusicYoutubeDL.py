import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from music_utils import displayMenuYoutubeDL, displaySongInfo
from datetime import datetime, timedelta


class MusicYoutubeDL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx = ""
        self.is_playing = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.vc = ""
        self.status = discord.Status.online
        self.activity = discord.Activity(
            type=discord.ActivityType.listening, name="Spotify")
        self.songInfo = {}
        self.currentDisplay = None

    def getSongInfo(self):
        return self.songInfo

    def getStatus(self):
        return self.status

    def getActivity(self):
        return self.activity

    def getIsPlaying(self):
        return self.is_playing

    def setIsPlaying(self, status):
        self.is_playing = status

    def setVC(self, vc):
        self.vc = vc

    def setCurrentDisplay(self, newCurrentDisplay):
        self.currentDisplay = newCurrentDisplay

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" %
                                        item, download=False)['entries'][0]
            except Exception:
                return False

        try:
            artist = info['artist']
        except Exception:
            artist = ""

        try:
            album = info['album']
        except Exception:
            album = ""

        infoJson = {
            'source': info['formats'][0]['url'],
            'title': info['title'],
            'artist': artist,
            'album': album,
            'thumbnail': info['thumbnail'],
            'webpage_url': info['webpage_url'],
            'channel_url': info['channel_url'],
            'description': info['description'],
            'duration': str(timedelta(seconds=info['duration'])),
            'view_count': "{:,}".format(info['view_count']),
            'upload_date': str(datetime.strptime(info['upload_date'], '%Y%m%d').strftime('%b %d, %Y')),
        }
        return infoJson

    def checkIsPlaying(self):
        if self.is_playing:
            if len(self.music_queue) == 0:
                self.is_playing = False
        else:
            if len(self.music_queue) > 0:
                self.is_playing = True

    def play_next(self):
        if len(self.music_queue) > 0:
            try:
                self.is_playing = True
                self.songInfo = self.music_queue[0][0]
                self.status = discord.Status.online
                self.activity = discord.Activity(
                    type=discord.ActivityType.listening, name=str(self.music_queue[0][0]['title']))
                self.vc.play(discord.FFmpegPCMAudio(
                    self.music_queue[0][0]['source'], **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
                self.music_queue.pop(0)
            except Exception:
                self.is_playing = False
        else:
            self.is_playing = False

    async def play_music(self):
        try:
            self.vc = await self.music_queue[0][1].connect()
            self.play_next()
        except Exception as e:
            print(e)

    async def vc_disconnect(self):
        if self.vc != "":
            self.vc.stop()
            await self.vc.disconnect()

    async def displaySongInfo(self, song, color, timestamp, musicQueue, customMsg):
        return await self.ctx.send(embed=displaySongInfo(song, color, timestamp, musicQueue, customMsg))

    @commands.command()
    async def yumii(self, ctx):
        await ctx.send(embed=displayMenuYoutubeDL())

    @commands.command()
    async def p(self, ctx, *args):
        self.ctx = ctx
        await ctx.message.delete()
        query = " ".join(args)
        voice_channel = ""
        try:
            voice_channel = ctx.author.voice.channel
        except Exception:
            await self.displaySongInfo(None, "red", 0, [], "Connect to a voice channel!")
        if voice_channel != "":
            song = self.search_yt(query)
            if type(song) == type(True):
                await self.displaySongInfo(None, "red", 0, [], "Could not download the song. Incorrect format.")
            else:
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music()

    @commands.command()
    async def skip(self, ctx):
        await ctx.message.delete()
        if self.vc != "":
            self.vc.stop()
        if len(self.music_queue) == 0:
            await self.vc.disconnect()
        await self.currentDisplay.delete()

    @commands.command()
    async def stop(self, ctx):
        await ctx.message.delete()
        if self.vc != "":
            self.vc.stop()
        self.music_queue = []
        await self.vc.disconnect()
        await self.currentDisplay.delete()
