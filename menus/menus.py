#!/share/imagedb/kamathv1/anaconda/bin/python
#A Slack bot that get's the week's menus from Lounasaika.net
#   and posts them to the #lunch channel on the aaltodl Slack 
#   portal(?) 
#
#Author: Vik Kamath

import json
import urllib
import yaml
import time
import schedule
from pyslack import SlackClient #From github.com/loisaidasam/pyslack

api_key = open('api_key.txt').read().strip()
#READ API KEY from a separate file, ignored using .gitignore
#api_key = api_key[0]
print api_key
client = SlackClient(api_key)


#The list of restaurants we're intersted in. 
#For now, it's Taffa, Tuas and Sodexo
restaurants = [u'T\u00e4ff\u00e4','TUAS-talo','Teekkariravintolat']

def get_menu():
    #From lounasaika.net
    url="http://www.lounasaika.net/api/v1/menus.json"
    #TODO: Put statements here the take of the condition
    #       that the request fails
    response = urllib.urlopen(url) 
    data=json.loads(response.read())  
    json.dump(data,open('menus.json','wb'))
    return data

def print_menu():
    data=get_menu()
    #Get the day of the week as a number. 0=Sunday,6=Saturday
    day_of_the_week = time.strftime("%w")
    day_of_the_week = int(day_of_the_week)-1 #For list indexing
    
    #Get menus for the day 
    for element in data:
        for x in element:
            if x=='name': #Only print the values of the restaurants we care about
                #cleaned_name = encoding.smart_str(element[x],encoding='ascii',errors='ignore')
                if element[x] in restaurants:#If the restaurant's the one we're interested in, 
                                             #then fetch the menus
                    menu = ""
    
                    #There's no CS on the menu, and 
                    #   all Sodexo's serve the same food.(Hopefully)
                    if element[x] == 'Teekkariravintolat':
                        menu = menu+"Sodexo :\n"
                    else:
                        menu = menu + element[x]+': \n'
                    if len(element['meals']['en']) > 0: #Restaurant might be closed
                                                        #or menu unavailable
                        for dish in element['meals']['en'][day_of_the_week]:
                            menu=menu+dish+"\n"
                    menu = menu+"---------------------"
                    client.chat_post_message('#lunch',menu,username='lounasbot')
                        #print element['meals']['en'][0] #Print the menu

def main():
    schedule.every().day.at("11:00").do(print_menu)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__=="__main__":
    main()
#TODO: 
#2. Hide API Key
#3. Fix case when Menus are blank - crawl myself?
#6. Put case for when the restaurant is closed for a particular day
#7. Clean data as soon as it comes - instead of looking through the whole thing all the time
#8. Try to fetch data only once every week instead of everyday


