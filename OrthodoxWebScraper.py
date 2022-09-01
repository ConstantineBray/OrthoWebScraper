#Orthodox WebScraper
#Prints Orthodox Christian feast days into my discord server, janky but it gets the job done
#3/24/2022

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import discord


client = discord.Client()

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.holytrinityorthodox.com/htc/orthodox-calendar/")
saints = driver.find_element(by=By.CLASS_NAME, value="normaltext")

individual_saints = saints.text.split("\n")






def saintPrint(saintNumber):

     

    saintSpecific = driver.find_elements(by=By.CLASS_NAME, value="cal-main")
    saint = individual_saints[saintNumber]
    print(saint[1:])
    

    for i in range(len(saintSpecific)+1):
        try:
            if saintSpecific[i].text in saint:
                link =  saintSpecific[i].get_attribute("href")
                driver.get(link)
                description = driver.find_elements(By.CLASS_NAME, "ofd_los_body")

                try:
                    descText = description[1].text + description[3].text
                except:
                    descText = description[1].text
                driver.get("https://www.holytrinityorthodox.com/htc/orthodox-calendar/")  
                return saint[1:], descText
        except Exception:
            pass
    return saint[1:], ""

    
def search_google(search_query):
    search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}"
    image_url = ""

    # open browser and begin search
    driver.get(search_url)
    elements = driver.find_elements_by_class_name('rg_i')

    count = 0
    for e in elements:
        # get images source url
        e.click()
        time.sleep(2)
        element = driver.find_elements_by_class_name('v4dQwb')

        # Google image web site logic
        if count == 0:
            big_img = element[0].find_element_by_class_name('n3VNCb')
        else:
           big_img = element[1].find_element_by_class_name('n3VNCb')

        image_url = big_img.get_attribute("src")

        count += 1

        # Stop get and save after 5
        if count == 1:
            break
    driver.get("https://www.holytrinityorthodox.com/htc/orthodox-calendar/")
    return image_url


       
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # Grabs the saint's feastday based on a given integer
    if message.content.startswith('!saint'):
        saintNum = int(message.content.replace('!saint ', ""))
    if message.content.startswith('!saint'):
        s, d = saintPrint(saintNum)
        iconUrl = search_google(s)
        if len(s + d) > 2000:
            n = 2000
            split_string = [d[i:i+n] for i in range(0, len(d), n)]
            await message.channel.send(s + "\n")
            for i in range(len(split_string)):
                await message.channel.send(split_string[i])
            await message.channel.send(iconUrl)
        else:
            print(d)
            await message.channel.send(s + "\n" + d)
            await message.channel.send(iconUrl)
    # Lists out the feastdays and their listed integers
    if message.content.startswith('!feasts'):
        list = ""
        for i in range(len(individual_saints)):
            list = (list + "\n" + str(i) + ". "+ individual_saints[i][1:])
        await message.channel.send(list)
        print(list)
    # Prints the daily scripture readings
    if message.content.startswith("!readings"):
        readings = driver.find_elements(By.PARTIAL_LINK_TEXT, ":")
        rList = ""
        for i in range(len(readings)):
            rList = (rList + "\n" +  readings[i].text)
        await message.channel.send(rList)


#Discord Authentication Token goes here
client.run("")


time.sleep(10)
driver.quit()
