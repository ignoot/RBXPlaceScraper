import time
import requests
from discord_webhook import DiscordWebhook # REMOVE THIS IF YOU DO NOT WANT WEBHOOK, ALSO SCROLL DOWN AND REMOVE THE OTHER PLACE THAT INCLUDES WEBHOOKS.
import math

SecondLoopVariable = True
SetPriceB4Tax = 1.87 # Change this to add more or less items to your wanted to see list. This will show all items UNDER SetPriceB4Tax. Which does not include itself.

headers = {'content-type': 'application/json'}
json = {"operationName":"fetchExploreData","variables":{},"query":"query fetchExploreData {\n  funds {\n    group {\n      amount\n      rate\n      max\n      __typename\n    }\n    b4tax {\n      amount\n      rate\n      max\n      __typename\n    }\n    __typename\n  }\n  recentlySold {\n    name\n    itemId\n    price\n    __typename\n  }\n  items {\n    itemId\n    name\n    rap\n    price\n    purchaseToken\n    paymentMethods {\n      name\n      data\n      __typename\n    }\n    seller {\n      id\n      username\n      __typename\n    }\n    __typename\n  }\n}\n"}




def Loop():
    User = requests.post("https://gql.rbx.place/graphql", headers=headers, json=json)
    
    RawData = User.json()['data']['items']
    
    LoopVariable = -1
    
    LoopNumber = len(RawData)-1
    
    DataList = []

    

    while LoopVariable < LoopNumber:

        LoopVariable = LoopVariable+1
        TheUselessRAPDataThatsRounded = (int(RawData[LoopVariable]['rap'])/1000)
        TheUselessRAPDataThatsRounded = float(round(TheUselessRAPDataThatsRounded,1))
            
        if TheUselessRAPDataThatsRounded > 1: ## All items above 1k to be collected.

            ItemName = (str(RawData[LoopVariable]['name']))
            
            ItemPrice = float(round((RawData[LoopVariable]['price']),2))
            
            ItemRap = str(int(RawData[LoopVariable]['rap']))
            
            ItemRapSmall = str(int(RawData[LoopVariable]['rap'])-410)
            
            B4TaxPricePerK = float(round((ItemPrice / TheUselessRAPDataThatsRounded),2))

            AfterTaxPricePerK = float(round((B4TaxPricePerK * (1000/700)),2))
                    
            ListingData = f'{ItemName} | | Price of Item: {ItemPrice}$ | | RAP Value of item: {ItemRap} | | RAP - Small(410): {ItemRapSmall} | | ROBUX Rates B4 Tax: ${B4TaxPricePerK}/1k | | After Tax: ${AfterTaxPricePerK}/1k'


            if B4TaxPricePerK < SetPriceB4Tax:
                    
                DataList.append(f'{ListingData}')

			
    DataConnector = "\n".join(DataList)
    print(DataConnector)

    ##### REMOVE UNDER ME TO REMOVE WEBHOOKS ##### Note sometimes it will not go into disord servers as it will go over the 2000 character limit. Pasting each line seperately leads to rate limiting. Most efficiency in IDE
    
    webhook = DiscordWebhook(url=f'https://discordapp.com/api/webhooks/747547814510461038/yCEZKrtZDb4-l_5K8G7pL97h90LgzWElN9s6ebTKA6qOiYCtDs_RLnOuVfumWcW9-oLk', content=f'{DataConnector}')
    response = webhook.execute()

    ##### REMOVE ABOVE ME TO REMOVE WEBHOOKS ##### Note sometimes it will not go into disord servers as it will go over the 2000 character limit. Pasting each line seperately leads to rate limiting. Most efficiency in IDE


while SecondLoopVariable == True:
    
    time.sleep(5)# Change the number in here to change amount of time between each scrape.
    Loop()
    



