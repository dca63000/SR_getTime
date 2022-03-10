# Selenium and Firefox webdriver setup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time, datetime, re

WEBDRIVER_PATH='/Users/cinca/Downloads/geckodriver'
options=Options()
options.add_argument('--headless')
service=Service(WEBDRIVER_PATH)

driver=Firefox(service=service, options=options)

# load Thorn playlist webpage
URL = 'https://thornbulle.streaming.lv/?sr_playlist'
driver.get(URL)

wait = WebDriverWait(driver, 5)
time.sleep(5)

print(driver.title)

# Check if active playlist item and sum all buffered songs duration

playlist_length=datetime.timedelta() #Active item of the playlist or not
nb_songs=0

#opacity 1 (actively added playlist) || 0.5 (std)
for i in range(1,100): #to be optimized, hardcoded 100 max
    line=i
    selector='tbody tr:nth-child('+str(line)+')' 
    try:
        attribute=driver.find_element(By.CSS_SELECTOR,selector)
    except BaseException:
        #print("stopped at line ", i)
        break
    style=attribute.get_attribute("style")
    
    #optimization needed, look only for 1 or 0, dependent on 1 or 0.5 expected values
    opacity=re.findall(r"\d", style) 
    if line==1:
        opacity = ['1']; # Sometimes style not defined for first line so hacked...
    if opacity[0] != str(1): # to be optimized
        break
        
    #Song duration sum
    nb_songs +=1
    get_time = selector+' td:nth-child(3)'
    get_song = selector+' td:nth-child(2)'
    time=driver.find_element(By.CSS_SELECTOR,get_time).text
    song=driver.find_element(By.CSS_SELECTOR,get_song).text
    print(song, " - ", time)
    items = re.findall('\d+', time) 
    if len(items)==1:
        min=items[0]
        sec=0
    elif len(items)>1:    
        min=items[0]
        sec=items[1]
    else:
        print("empty duration ? ", len(items))
    playlist_length += datetime.timedelta(minutes=int(min), seconds=int(sec))

print("Nb songs to come: ", nb_songs, " duration: ", playlist_length)
driver.quit()

#When will the active playlist end ?
# Dunno, how to get the start time of the ongoing [0] item ?

#For fun
now=datetime.datetime.now()
now=now.replace(hour=11,minute=0,second=0) # for now to be added by hand
end=now+playlist_length
print(end)
