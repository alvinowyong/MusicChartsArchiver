import urllib.request
from bs4 import BeautifulSoup
import pycountry
import time
import threading
import sys
import json

sem = threading.Semaphore()
flag = 0

def scraper():
    global flag
    for i, country in enumerate(pycountry.countries):
        sem.acquire()
        if i >= len(pycountry.countries) - 1:
            sem.release()
            sys.exit()
        elif i < flag:
            sem.release()
            continue
        else :
            print("Scraping Google for", country.alpha_2, ":", i, "out of", len(pycountry.countries) - 1)
            flag += 1
        sem.release()
        name = country.name.encode('ascii', 'ignore').decode('ascii')
        url = "https://www.google.com/search?q=Top%20100:%20" +  name.replace(" ", "%20") + "%20-%20Apple%20Music"

        # Perform the request
        request = urllib.request.Request(url)

        # Set a normal User Agent header
        request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
        
        failed = True
        while failed:
            try:
                raw_response = urllib.request.urlopen(request).read()
                failed = False
            except Exception as e:
                print("Error fetching data... Retrying.")
                time.sleep(5)
                err = e
                continue
        
        # Read the repsonse as a utf-8 string
        html = raw_response.decode("utf-8")

        # Construct the soup object
        soup = BeautifulSoup(html, 'html.parser')

        # Find all the search result <a>
        divs = soup.find_all('a', href=True)
        for i, div in enumerate(divs):
            if i > 20:
                break
            # Append key value into dictionary
            if div['href'].startswith("https://music.apple.com") and div['href'].find("top-100-" + name.lower()) != -1:
                apple_playlist[country.alpha_2] = div['href']
                break                             

try:
    apple_playlist = {}

    thread_one = threading.Thread(target=scraper, args=())
    thread_two = threading.Thread(target=scraper, args=())
    thread_three = threading.Thread(target=scraper, args=())
    thread_one.start()
    thread_two.start()
    thread_three.start()
    thread_one.join()
    thread_two.join()
    thread_three.join()
except:
   print("Error: unable to start thread")

print("thread cleaned up")
print(apple_playlist)
with open("scraper_generated_apple_playlist.json", "w") as myfile:
    myfile.write(json.dumps(apple_playlist, indent = 4))
