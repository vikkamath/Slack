#!/share/imagedb/kamathv1/anaconda/bin/python
import json
import urllib
import yaml

#The list of restaurants we're intersted in. 
restaurants = ['Taffa','TUAS-talo','Teekkariravintolat']

#From lounasaika.net
url="http://www.lounasaika.net/api/v1/menus.json"
#TODO: Put statements here the take of the condition
#       that the request fails
response = urllib.urlopen(url) 
print response
data=json.loads(response.read())  
#json.dump(data,open('menus.json','wb'))

for element in data:
    for x in element:
        if x=='name': #Only print the values of the restaurants we care about
            if element[x] in restaurants:
                if x=='meals': #Only the Menu. Nothing else
                    print len(element[x]["en"]) #The English version
                    print element[x]["en"][0]
                else:
                    print x
                    print element[x]
    break
