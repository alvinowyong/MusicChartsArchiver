from bs4 import BeautifulSoup
import requests
import itertools
import threading
import json
import datetime
import apple_scraper
import spotify_scraper
import mysql.connector
import os
import json
from mysql.connector import errorcode
sem = threading.Semaphore()

total = 0
counter = 0
try: 
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="password",
        database="spopplechart"
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

apple_links = {}
spotify_links = {}

def apple_playlist_scraper(apple_links):
    global counter
    for country, links in apple_links.items():
        sem.acquire()
        print("Scraping Apple data for " + country + " (" + str(counter) + " out of " + str(total) + ")", )
        sem.release()
        source = requests.get(links).text
        soup = BeautifulSoup(source, 'lxml')

        songs = []
        albums = []
        artists = []
        artworks = []

        count = 0
        for count, song in enumerate(soup.find_all('div', class_='songs-list-row__song-name')):
            songs.append(str(count + 1) + '.' + song.text)

        # isAlbum if False
        isAlbum = False
        for artist_album in soup.find_all('div', class_='songs-list__song-link-wrapper'):
            if (isAlbum):
                originalText = (artist_album.text).split()
                albums.append(" ".join(originalText).replace(" ,", ","))
                isAlbum = False
                continue
            else:
                originalText = (artist_album.text).split()
                artists.append(" ".join(originalText).replace(" ,", ","))
                isAlbum = True

        for artwork in soup.find_all('div', class_='media-artwork-v2--tracklist'):
            if artwork.picture.source['srcset'] != "":
                artworks.append(artwork.picture.source['srcset'].split()[0])
            else:
                artworks.append(artwork.picture.source['data-srcset'].split()[0])

        for (song,album,artist,artwork) in zip(songs,albums,artists,artworks):
            mycursor = mydb.cursor()
            sql = "INSERT INTO chart_record (date,country,position, song, album, artists, artwork, spotify, applemusic) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (datetime.datetime.now().date(),country,song.split('.', 1)[0], song.split('.', 1)[1], album, artist, artwork, 0, 1)

            try:
                mycursor.execute(sql,val)
                mydb.commit()
            except:
                None

        counter += 1

def spotify_playlist_scraper(spotify_links):
    global counter
    for country, links in spotify_links.items():
        playlist_id = links.split("/").pop()
        sem.acquire()
        print("Scraping Spotify data for " + country + " (" + str(counter) + " out of " + str(total) + ")", )
        sem.release()
        source = requests.get("https://open.spotify.com/playlist/" + playlist_id).text
        soup = BeautifulSoup(source, 'lxml')

        songs = []
        albums = []
        artists = []
        artworks = []

        position = 1
        for song in soup.find_all('a', class_='eWYxOj'):
            songs.append(str(position) + "." + song.text)
            position += 1

        for artist in soup.find_all('span', class_='Row__Subtitle-sc-brbqzp-1'):
            artists.append(artist.text)

        # for album in (json.loads(soup.find('script', id='initial-state').text)['entities']['items']['spotify:playlist:' + playlist_id]['tracks']['items']):
        #     albums.append(album['track']['album']['name'])

        # for artwork in (json.loads(soup.find('script', id='initial-state').text)['entities']['items']['spotify:playlist:' + playlist_id]['tracks']['items']):
        #     artworks.append(artwork['track']['album']['images'][2]['url'])

        for (song, album, artist, artwork) in zip(songs, albums, artists, artworks):
            mycursor = mydb.cursor()
            sql = "INSERT INTO chart_record (date,country,position, song, album, artists, artwork, spotify, applemusic) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (datetime.datetime.now().date(), country, song.split('.', 1)[0], song.split('.', 1)[1], album, artist, artwork, 1, 0)

            try:
                mycursor.execute(sql,val)
                mydb.commit()
                print("[Committed]", song, 'by', artist + ' (Album:', album + ')')
            except:
                print("[Skipped] Duplicate record found")
        counter += 1

def main():
    global total
    PATH = "./scraper_generated_apple_playlist.json"
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        f = open('scraper_generated_apple_playlist.json')
        apple_links = json.load(f)
    else:
        print("Either the file is missing or not readable")
        apple_scraper.main()
        
    PATH = "./scraper_generated_spotify_playlist.json"
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        f = open('scraper_generated_spotify_playlist.json')
        spotify_links = json.load(f)
    else:
        print("Either the file is missing or not readable")
        spotify_scraper.main()

    total = len(spotify_links) + len(apple_links) - 2
    
    try:
        thread_one = threading.Thread(target=spotify_playlist_scraper, args=(spotify_links, ))
        thread_two = threading.Thread(target=apple_playlist_scraper, args=(apple_links, ))
        thread_one.start()
        thread_two.start()
        thread_one.join()
        thread_two.join()
    except:
        print("Error: unable to start thread")
main()