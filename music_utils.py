import discord
import time


def displayMenuDismusic():
    title = "Menu 🎶🎵"
    description = ""
    description += "▶️ `-p *song name*` <Play/add a song to music queue>" + "\n"
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
        title=title,
        description=description,
        colour=colour,
    )
    embed.set_footer(text="\nMusic bot created by Aden Tran\n")
    return embed


def displayMenuYoutubeDL():
    title = "🎶🎵 Menu 🎶🎵"
    description = ""
    description += "▶️ `-p *song name*` <play/add a song to music queue>" + "\n"
    description += "⏸ `-pause` <pause the track>" + "\n"
    description += "⏯ `-resume` <resume the track>" + "\n"
    description += "⏩ `-skip` <skip to next song>" + "\n"
    description += "🛑 `-stop` <stop and disconnect>" + "\n"
    colour = discord.Colour.blue()
    embed = discord.Embed(
        title=title,
        description=description,
        colour=colour,
    )
    embed.set_footer(text="\nMusic Bot created by Aden Tran\n")
    return embed


def displaySongInfo(songInfo, color, timestamp, musicQueue, customMsg=""):
    colour = discord.Colour.light_gray()
    if color == "red":
        colour = discord.Colour.red()
        embed = discord.Embed(
            colour=colour,
            description=customMsg
        )
        return embed
    elif color == "green":
        colour = discord.Colour.green()
        if (songInfo):
            title = f"{songInfo['title']}"
            description = (songInfo['artist'] +
                           "\n\n" if songInfo['artist'] else "")
            description += (songInfo['album'] +
                            "\n\n" if songInfo['album'] else "")
            description += songInfo['view_count'] + \
                " views * " + songInfo['upload_date']
            url = f"{songInfo['webpage_url']}"
            embed = discord.Embed(
                title=title,
                url=url,
                description=description,
                colour=colour
            )
            currentTime = time.strftime('%H:%M:%S', time.gmtime(timestamp))
            maxDuration = timeStrToNum(songInfo['duration'])
            leadingZero = '0' if len(songInfo['duration']) == 7 else ''

            numSquare = 20
            redProgress = ''
            whiteProgress = '⬜' * (numSquare-1)

            if (timestamp == maxDuration):
                redProgress = '🟥' * numSquare
                whiteProgress = ''
            elif (timestamp > 0):
                redProgress = '🟥' * int((timestamp/maxDuration)*numSquare)
                whiteProgress = '⬜' * \
                    int((numSquare-1)-(timestamp/maxDuration)*(numSquare))

            queueList = "Up next ⌛:\n\n"
            if len(musicQueue) > 0:
                for i in range(0, len(musicQueue)):
                    queueList += (" → " if i == 0 else "") + \
                        "\t" + musicQueue[i][0]['title'] + "\n"
            else:
                queueList = ""

            footer = f"{currentTime} / {leadingZero}{songInfo['duration']}\n\n{redProgress}{whiteProgress}\n\n{queueList}"

            embed.set_thumbnail(
                url="https://c.tenor.com/ek8ccJEdkKkAAAAi/cat-noodles.gif")
            embed.set_image(url=songInfo['thumbnail'])
            embed.set_footer(text=footer)
            return embed
    return None


def timeStrToNum(timeStr):
    h, m, s = timeStr.split(':')
    timeNum = int(h) * 3600 + int(m) * 60 + int(s)
    return timeNum
