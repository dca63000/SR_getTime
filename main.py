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

wait = WebDriverWait(driver, 10)
time.sleep(10)

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
    opacity=re.findall(r"\d*\.?\d+", style) 
    if opacity[0] != str(1): # to be optimized
        continue
        
    #Song duration sum
    nb_songs +=1
    selector +=' td:nth-child(3)'
    time=driver.find_element(By.CSS_SELECTOR,selector).text
    min, sec = re.findall('\d+', time) #best way?
    playlist_length += datetime.timedelta(minutes=int(min), seconds=int(sec))

print("Nb songs to come: ", nb_songs, " duration: ", playlist_length)

#When will the active playlist end ?
# Dunno, how to get the start time of the ongoing [0] item ?

#For fun
now=datetime.datetime.now()
end=now+playlist_length
print(end)
