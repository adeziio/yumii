import os
import discord
from discord.ext import commands, tasks
from MusicYoutubeDL import MusicYoutubeDL
from music_utils import displaySongInfo

Bot = commands.Bot(command_prefix='-')
musicObj = MusicYoutubeDL(Bot)
musicObjstatus = musicObj.getStatus()
musicObjActivity = musicObj.getActivity()
timestamp = 0

Bot.add_cog(musicObj)


@Bot.event
async def on_ready():
    print("yumii is online!")
    change_status.start()


@tasks.loop(seconds=1)
async def change_status():
    global musicObjstatus
    global musicObjActivity
    global timestamp
    timestamp += 1

    musicQueue = musicObj.music_queue if musicObj.music_queue else []

    if musicObjstatus != musicObj.getStatus() or musicObjActivity != musicObj.getActivity():
        musicObjstatus = musicObj.getStatus()
        musicObjActivity = musicObj.getActivity()
        timestamp = 0
        await Bot.change_presence(status=musicObj.getStatus(), activity=musicObj.getActivity())
        if (musicObj.currentDisplay is not None):
            try:
                await musicObj.currentDisplay.edit(embed=displaySongInfo(musicObj.getSongInfo(), "green", timestamp, musicQueue, ""))
            except:
                currentDisplay = await musicObj.displaySongInfo(musicObj.getSongInfo(), "green", timestamp, musicQueue, "")
                musicObj.setCurrentDisplay(currentDisplay)
        else:
            currentDisplay = await musicObj.displaySongInfo(musicObj.getSongInfo(), "green", timestamp, musicQueue, "")
            musicObj.setCurrentDisplay(currentDisplay)

    if musicObj.getIsPlaying() == False:
        timestamp = 0
        if (musicObj.currentDisplay is not None):
            if (musicObj.getSongInfo()):
                try:
                    await musicObj.currentDisplay.delete()
                except:
                    None
        await Bot.change_presence(status=musicObj.getStatus(), activity=discord.Activity(type=discord.ActivityType.listening, name="YouTube Music"))
        musicObj.setCurrentDisplay(None)
        await musicObj.vc_disconnect()
    else:
        try:
            await musicObj.currentDisplay.edit(embed=displaySongInfo(musicObj.getSongInfo(), "green", timestamp, musicQueue, ""))
        except:
            None

Bot.run(os.getenv('YUMII_TOKEN'))
