import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class music(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.is_playing = False
    self.music_queue = []
    self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    self.vc = ""

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
      # self.set_status(discord.ActivityType.listening, m_title)

      print("play_next", len(self.music_queue))
      self.music_queue.pop(0)
      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=self.play_next())
    

  async def play_music(self):
    if len(self.music_queue) > 0:
      self.is_playing = True

      m_url = self.music_queue[0][0]['source']
      m_title = self.music_queue[0][0]['title']
      # await self.set_status(discord.ActivityType.listening, m_title)

      if self.vc == "":
        try:
          self.vc = await self.music_queue[0][1].connect()
        except Exception as e:
          print(e)
      
      print("play_music", len(self.music_queue))
      self.music_queue.pop(0)
      self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=self.play_next())


  async def set_status(self, type, name):
    await self.bot.change_presence(activity=discord.Activity(type=type, name=name))

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
        await ctx.send("Added to queue ▶️: " + "*" + str(song['title']) + "*")
        self.music_queue.append([song, voice_channel])

        if self.is_playing == False:
          # await self.set_status(discord.ActivityType.listening, str(song['title']))
          await self.play_music()

  @commands.command()
  async def q(self, ctx):
    if len(self.music_queue) > 0:
      retval = "Up next ⏯:\n"
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
      self.vc.stop()
      self.play_next()

  @commands.command()
  async def m(self, ctx):
    await ctx.send("-p *song name* (play)\n-s (skip)\n-q (queue list)\n-m (menu)")