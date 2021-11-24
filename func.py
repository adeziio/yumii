import discord

def displayMenu():
  description =  "To add a song ▶:\n-p *song name*\n\n"
  description += "To skip a song ⏩:\n-s\n\n"
  description += "To check queue list ⌛:\n-q\n\n"
  
  embed = discord.Embed(
          title = "Menu 🎶🎵",
          description = description,
          colour = discord.Colour.purple(),
          )
  embed.set_footer(text="\nMusic bot created by Aden Tran\n")
  return embed

def displaySongInfo(status, songInfo, color):
  colour = discord.Colour.light_gray()
  if color == "light_gray":
    colour = discord.Colour.light_gray()
  if color == "green":
    colour = discord.Colour.green()
  
  title = status + "\n\n" + songInfo['title']
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
  title = "Up next ⌛:\n\n"
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
