from pyrogram import Client, filters
import spotipy
from spotipy.oauth2 import SpotifyOAuth

with open("userbot.info", "r") as file:
    lines = file.readlines()
    prefix_userbot = lines[2].strip()

# Вам необходимо написать ваш client_id и client_secret в файл "spotifyapi.info".
# Также для модуля необходимо зайти на сайт SpotifyAPI(https://developer.spotify.com/)
# Зарегистрироваться, создать приложение, и написать в строку Redirect URIs это: http://localhost:8080
# (без этого не будет работать модуль)

with open("spotifyapi.info", "r") as file:
    lines = file.readlines()
    client_id = lines[0].strip()
    client_secret = lines[1].strip()

cinfo = f"🎵`{prefix_userbot}spnow`"
ccomand = " Текущий статус Spotify."

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8080",
                                               scope="user-read-playback-state"))


def command_spnow(app):
    @app.on_message(filters.me & filters.command("spnow", prefixes=prefix_userbot))
    def send_now_playing(_, message):
        track_info = get_current_track_info()
        if track_info:
            track, artist, duration, progress, cover_url = track_info
            message.reply_text(f"**🎵Пользователь слушает**:\n`{artist} - {track}`\n**{progress} - {duration}**\n[Обложка трека]({cover_url})")
        else:
            message.reply_text("**❌В данный момент ничего не воспроизводится.**")


def get_current_track_info():
    try:
        current_track = sp.current_playback()
        if current_track is not None:
            track = current_track['item']['name']
            artist = current_track['item']['artists'][0]['name']
            duration_ms = current_track['item']['duration_ms']
            progress_ms = current_track['progress_ms']
            cover_url = current_track['item']['album']['images'][0]['url']
            duration = divmod(duration_ms // 1000, 60)
            progress = divmod(progress_ms // 1000, 60)
            return track, artist, f"{duration[0]}:{duration[1]:02d}", f"{progress[0]}:{progress[1]:02d}", cover_url
        else:
            message.reply_text("**❌Ошибка.**")
    except Exception as e:
        print(f"Ошибка при получении текущего трека: {e}")
        return None

print("Модуль spnow загружен!")
