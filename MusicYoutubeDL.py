import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from MusicYoutubeDL_utils import displayMenu, displaySongInfo, displayQueueList, displayMessage
from datetime import datetime, timedelta

class MusicYoutubeDL(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.ctx = ""
    self.is_playing = False
    self.music_queue = []
    self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    self.vc = ""
    self.status = discord.Status.online
    self.activity = discord.Activity(type=discord.ActivityType.listening, name="Spotify")
    self.songInfo = {}
  
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

  def search_yt(self, item):
    with YoutubeDL(self.YDL_OPTIONS) as ydl:
      try:
        info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
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
      'upload_date': str(datetime.strptime(info['upload_date'],'%Y%m%d').strftime('%b %d, %Y')),
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
        self.activity = discord.Activity(type=discord.ActivityType.listening, name=str(self.music_queue[0][0]['title']))
        self.vc.play(discord.FFmpegPCMAudio(self.music_queue[0][0]['source'], **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        self.music_queue.pop(0)
      except Exception:
        self.is_playing = False
    else:
      self.is_playing = False  
      
  async def play_music(self):
    try:
      self.vc = await self.music_queue[0][1].connect()
    except Exception as e:
      print(e)
    self.play_next()

  async def vc_disconnect(self):
    if self.vc != "":
      self.vc.stop()
      await self.displayMessage("", "Music queue is empty, good bye...", "red")
      await self.vc.disconnect()
      self.vc = ""
    
  async def displaySongInfo(self, status, song, color):
    await self.ctx.send(embed=displaySongInfo(status, song, color))
  
  async def displayQueueList(self, queueList):
    await self.ctx.send(embed=displayQueueList(queueList))

  async def displayMessage(self, title, message, color):
    await self.ctx.send(embed=displayMessage(title, message, color))
    
  @commands.command()
  async def yumii(self, ctx):
    await ctx.send(embed=displayMenu())

  @commands.command()
  async def p(self, ctx, *args):
    self.ctx = ctx
    query = " ".join(args)
    voice_channel = ""
    try:
      voice_channel = ctx.author.voice.channel
    except Exception:
      await ctx.send("Connect to a voice channel!")
    if voice_channel != "":
      song = self.search_yt(query)
      if type(song) == type(True):
        await ctx.send("Could not download the song. Incorrect format.")
      else:
        await self.displaySongInfo("Added to queue ⌛", song, "light_gray")
        self.music_queue.append([song, voice_channel])
        
        if self.is_playing == False:
          await self.play_music()
  
  @commands.command()
  async def q(self, ctx):
    self.ctx = ctx
    await self.displayQueueList(self.music_queue)

  @commands.command()
  async def s(self, ctx):
    self.ctx = ctx
    if self.vc != "":
      self.vc.stop() 

  @commands.command()
  async def P(self, ctx, *args):
    await self.p(ctx, *args)

  @commands.command()
  async def Q(self, ctx, *args):
    await self.q(ctx, *args)

  @commands.command()
  async def S(self, ctx, *args):
    await self.s(ctx, *args)