import requests
import json
import os
import dotenv
dotenv.load_dotenv()

API_HASH = TG_BOT = os.getenv('TG_BOT_TOKEN')

clientjson  = json.loads(open('mytelegrammodules/database/db.json','r').read())
chatid = list(clientjson.keys())


base_url = "https://api.telegram.org/bot{}/sendMessage?parse_mode=MARKDOWN".format(API_HASH)

update = """‎ ‎ ‎ ‎ ‎ ‎ ‎***@DalBhatPowerBot*** \n‎ ‎ ‎ ‎ ‎ ‎ ‎__(NEW UPDATE!!)__
This is to inform you that the bot has started working again and we've pushed some updates.\n

‎ ‎ ‎ ‎ ‎ ‎ ‎***Changelogs:***
\t - Added Facebook Video Download support, but you need to pass `/fb <link>` command

__For more and guide to use :__ Issue /help command.__

\t We've now all these features :
\n
‎ ‎ ‎ ‎ ‎ ‎ ‎***NEPAL***
\t - Nepali Datetime
\t - Nepali Dictionary
\t - NEPSE
\t - Nepali Rashifal
\n
‎ ‎ ‎ ‎ ‎ ‎ ‎***Social Medias***
\t - Facebook (Only Videos)
\t - Twitter (Beta - Occasional Errors, send link again, must work)
\t - Tiktok (Videos Without Watermark)
\t - Instagram (Videos/ Posts / Reels/ Public Stories) 
\t - Youtube
\t - Audios and Videos from supported sites

‎ ‎ ‎ ‎ ‎ ‎ ‎Have a Great DAy !✨"""

for chat_id in chatid:
    parameters = {
        "chat_id" : chat_id,
        "text" : update}
    resp = requests.get(base_url, data = parameters)
    response_txt=json.loads(resp.text.encode('utf8'))
    print (json.dumps(response_txt, indent=2))

print("Program Ended")
