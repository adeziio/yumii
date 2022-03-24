import discord

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

def displaySongInfo(status, songInfo, color):
  colour = discord.Colour.light_gray()
  if color == "light_gray":
    colour = discord.Colour.light_gray()
  if color == "green":
    colour = discord.Colour.green()
  
  title = status + " " + songInfo['duration'] + "\n\n" + songInfo['title']
  description = songInfo['artist'] + "\n\n" + songInfo['album'] + "\n\n"
  description += songInfo['view_count'] + " views * " + songInfo['upload_date']
  embed = discord.Embed(
          title = title,
          description = description,
          colour = colour,
          width = 150,
          height = 150
          )
  embed.set_image(url=songInfo['thumbnail'])
  embed.set_footer(text="")
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

#  ▶ ⌛ ⏩