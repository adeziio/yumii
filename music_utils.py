import discord
import time

def displayMenuDismusic():
  title = "Menu 🎶🎵"
  description = ""
  description += "▶ `-p *song name*` <Play/add a song to music queue>" + "\n"
  description += "❓ `-np` <Check now playing>" + "\n"
  description += "⌛ `-q` <Check music queue>" + "\n"
  description += "⏩ `-skip` <Skip to next song>" + "\n"
  description += "🔁 `-loop` <Set loop to NONE, CURRENT or PLAYLIST>" + "\n"
  description += "⏸ `-pause` <Pause the track>" + "\n"
  description += "⏯ `-resume` <Resume the track>" + "\n"
  description += "🚩 `-connect` <Connect to voice channel>" + "\n"
  description += "⛔ `-disconnect` <Disconnect from voice channel>" + "\n"
  colour = discord.Colour.blue()
  embed = discord.Embed(
          title = title,
          description = description,
          colour = colour,
          )
  embed.set_footer(text="\nMusic bot created by Aden Tran\n")
  return embed

def displayMenuYoutubeDL():
  title = "Menu 🎶🎵"
  description = ""
  description += "▶ `-p *song name*` <Play/add a song to music queue>" + "\n"
  description += "⌛ `-q` <Check music queue>" + "\n"
  description += "⏩ `-s` <Skip to next song>" + "\n"
  colour = discord.Colour.blue()
  embed = discord.Embed(
          title = title,
          description = description,
          colour = colour,
          )
  embed.set_footer(text="\nMusic bot created by Aden Tran\n")
  return embed

def displaySongInfo(status, songInfo, color, timestamp, musicQueue):
  colour = discord.Colour.light_gray()
  if color == "light_gray":
    colour = discord.Colour.light_gray()
  if color == "green":
    colour = discord.Colour.green()

  queueList = "Up next ⌛\n\n"
  if (musicQueue):
    if len(musicQueue) > 0:
      for i in range(0, len(musicQueue)):
        queueList += "\t" + str(i+1) + ". *" + musicQueue[i][0]['title'] + "*\n"
    else:
      queueList = "Music queue is empty."
  else:
    queueList = "Music queue is empty."
  

  title = f"{songInfo['title']}"
  description = songInfo['artist'] + "\n\n" + songInfo['album'] + "\n\n" if songInfo['album'] else ""
  description += songInfo['view_count'] + " views * " + songInfo['upload_date']
  url=f"{songInfo['webpage_url']}"
  embed = discord.Embed(
          title = title,
          url = url,
          description = description,
          colour = colour,
          width = 150,
          height = 150
          )
  currentTime = time.strftime('%H:%M:%S', time.gmtime(timestamp))
  maxDuration = timeStrToNum(songInfo['duration'])
  leadingZero = '0' if len(songInfo['duration'])==7 else ''

  redProgress = '🟥' * int(1+(timestamp/maxDuration)*23)
  whiteProgress = '⬜' * int(23-(timestamp/maxDuration)*23)
  footer = f"{status}\t\t\t\t\t\t\t\t\t\t{currentTime} / {leadingZero}{songInfo['duration']}\n\n{redProgress}{whiteProgress}\n\n{queueList}"
  
  embed.set_image(url=songInfo['thumbnail'])
  embed.set_footer(text=footer)
  return embed

def displayQueueList(queueList):
  title = "Up next ⌛\n\n"
  description = ""
  if len(queueList) > 0:
    for i in range(0, len(queueList)):
      description += str(i+1) + ". *" + queueList[i][0]['title'] + "*\n"
  else:
    description = "Music queue is empty."
  embed = discord.Embed(
          title = title,
          description = description,
          colour = discord.Colour.blue()
          )
  embed.set_footer(text="")
  return embed

def displayMessage(title, message, color):
  colour = discord.Colour.red()
  if color == "red":
    colour = discord.Colour.red()
  title = title
  description = message
  embed = discord.Embed(
          title = title,
          description = description,
          colour = colour,
          )
  embed.set_footer(text="")
  return embed

def timeStrToNum(timeStr):
  h, m, s = timeStr.split(':')
  timeNum = int(h) * 3600 + int(m) * 60 + int(s)
  return timeNum

#  ▶ ⌛ ⏩