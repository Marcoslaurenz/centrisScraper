import json
from multiprocessing.dummy import current_process
from types import NoneType
from typing import Type
import requests
from bs4 import BeautifulSoup
import csv
from datetime import date
import re
from time import sleep

print("""
 _____            _        _ _____                      
/  __ \          | |      (_)  ___|                     
| /  \/ ___ _ __ | |_ _ __ _\ `--.  ___ _ __ __ _ _ __  
| |    / _ \ '_ \| __| '__| |`--. \/ __| '__/ _` | '_ \ 
| \__/\  __/ | | | |_| |  | /\__/ / (__| | | (_| | |_) |
 \____/\___|_| |_|\__|_|  |_\____/ \___|_|  \__,_| .__/ 
                                                 | |    
                                                 |_|   
""")
input("Press Enter: ")

s = requests.Session()

h1={'Host': 'www.centris.ca',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
'Accept-Language': 'es-CL,es;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate, br',
'Referer': 'https://www.centris.ca/en/lots~for-sale?view=Thumbnail',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'TE': 'Trailers'
}

r = s.get("https://www.centris.ca/en/lots~for-sale?view=Summary&uc=0",headers=h1)


num = 100
fields = ["Centris no","Type","Date Listed","Status","Address","Size","Active price","Taxes","Old prices","Zoning","Coordinates","Description"]
with open('results.csv', 'w', newline='') as file: 

    writer = csv.DictWriter(file, fieldnames = fields)
    writer.writeheader()
    payload = {"startPosition":"0"}
    conteo = s.post("https://www.centris.ca/Property/GetInscriptions", headers=h1, json=payload)
    jConvert = json.loads(conteo.text)

    arrai = jConvert["d"]
    result = arrai["Result"]
    countTotal = int(result["count"])
    print(countTotal)
    num = 1
    while num < countTotal:
        
        data = {"startPosition":num}
        num += 0
        print(str(num)+" Avance")
        r2 = s.post("https://www.centris.ca/Property/GetInscriptions", headers=h1, json=data)
        #print(r2.text)
        if "Features" in r2.text:
            with open("prueba.txt","a+") as t:
                t.write(str(num)+"\n")
            print("Extracting...")
            num += 1
            jsonData = json.loads(r2.text)
            elements = jsonData["d"]
            results = elements["Result"]
            html = results["html"]
            #print(html)
            soup = BeautifulSoup(html, "html.parser")
            #RawPrice
            try:
                latitude = soup.find("span", id="PropertyLat").text
            except:
                latitude = "Consult"
                
            
            try:
                longitude = soup.find("span", id="PropertyLng").text
            except:
                longitude = "Consult"
                
            
            try:
                centriID = soup.find("span", id="ListingId").text
            except:
                centriID = "Consult"
                
            
            try:
                price = soup.find("span", id="RawPrice").text
            except:
                price = "Consult"
                
            
            try:
                add = soup.find("h2", itemprop="address").text
            except:
                add = "Consult"
                
            
            try:
                zoni = soup.find_all("div", class_="carac-value")
            except:
                zoni = "Consult"
                
            try:
                tax = soup.find_all("span", class_="desc")
                print(tax)
            except:
                tax = "Consult"
                
            
            print("==========================================")
            for e in zoni:
                lotArea1 = str(zoni[0].text)
                lotArea = lotArea1.replace(",","")
                try:
                    zoning = zoni[1].text
                except IndexError:
                    zoning = zoni[0].text
                break  
            for t in tax:
                if "+" in t.text:
                    taxe = "YES"
                    print(taxe)
                    break
                else:
                    taxe = "NO"
                    print(taxe)
                    
       
            try:
                description1 = str(soup.find("div", itemprop="description").text)
                description = re.sub(r"^\s+|\s+$", "", description1)

                
            except AttributeError:
                description = 'Consult'
            type1 = str(soup.find("h1", itemprop="category").text)
            type = re.sub(r"^\s+|\s+$", "",type1)
            print("Title: "+str(results["title"])) 
            print("Count Results: "+str(results["count"]))
            print("Latitude: "+str(latitude))
            print("Latitude: "+str(longitude))
            print("Price: "+str(price))
            print("Address: "+str(add))
            print("Zoning: "+str(zoning))
            print("Lot Area: "+str(lotArea))
            print("Centri No: "+str(centriID))
            today = date.today()
            print("Today date is: ", today)
            # ["Centris no","Type","Date Listed","Status","Address","Size","Active price","Taxes","Old prices","Zoning","Coordinates","Description"]
            lot = [{'Centris no':centriID,"Type":type,'Date Listed':today,'Status':'Active','Address':add,'Size':lotArea,'Active price':price,'Taxes':taxe,'Old prices':'0,00','Zoning':zoning,'Coordinates': str(latitude)+"-"+str(longitude),'Description':description}]

                                                
            
            
                
            writer.writerows(lot)
        else:
            print(r2.text)
            print("********")
            
            
print("finished process")
sleep(5000)        

    # for line in results:
    #     print(line)
    # print("==========================================")
    # print("Title: "+str(results["title"])) 
    # print("countForPagingComponent: "+str(results["countForPagingComponent"])) 
    # print("Count Results: "+str(results["count"]))
    # break
