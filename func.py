import discord

def menu():
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