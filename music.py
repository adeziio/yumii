import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from func import menu

class music(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.is_playing = False
    self.music_queue = []
    self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    self.vc = ""
    self.status = discord.Status.online
    self.activity = discord.Activity(type=discord.ActivityType.listening, name="Spotify")
  
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
    return {'source': info['formats'][0]['url'], 'title': info['title']}

  def play_next(self):
    if len(self.music_queue) > 0:
      self.is_playing = True

      m_url = self.music_queue[0][0]['source']
      m_title = self.music_queue[0][0]['title']
      self.status = discord.Status.online
      self.activity = discord.Activity(type=discord.ActivityType.listening, name=str(m_title))

      self.music_queue.pop(0)
      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
    if len(self.music_queue) == 0:
      self.is_playing = False
    
  async def play_music(self):
    global status_type
    global status_name
    if len(self.music_queue) > 0:
      self.is_playing = True

      m_url = self.music_queue[0][0]['source']
      m_title = self.music_queue[0][0]['title']
      self.status = discord.Status.online
      self.activity = discord.Activity(type=discord.ActivityType.listening, name=str(m_title))

      try:
        self.vc = await self.music_queue[0][1].connect()
      except Exception as e:
        print(e)
      
      self.music_queue.pop(0)
      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
    if len(self.music_queue) == 0:
      self.is_playing = False

  async def vc_disconnect(self):
    if self.vc != "":
      self.vc.stop()
      await self.vc.disconnect()
    
  @commands.command()
  async def yumii(self, ctx):
    await ctx.send(embed=menu())

  @commands.command()
  async def p(self, ctx, *args):
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
        await ctx.send("Added to queue ▶️:\n" + "*" + str(song['title']) + "*")
        self.music_queue.append([song, voice_channel])

        if self.is_playing == False:
          await self.play_music()
  
  @commands.command()
  async def q(self, ctx):
    if len(self.music_queue) > 0:
      retval = "Up next ⌛:\n"
      for i in range(0, len(self.music_queue)):
        retval += "*" + self.music_queue[i][0]['title'] + "*\n"
      if retval != "":
        await ctx.send(retval)
    else:
      await ctx.send("Music queue is empty.")

  @commands.command()
  async def s(self, ctx):
    if self.vc != "":
      if len(self.music_queue) == 0:
        self.is_playing = False
        await ctx.send("Music queue is empty.")
      self.vc.stop()
      self.play_next()
  

