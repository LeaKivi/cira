import requests
from random import *
import json
import mood

#initiate chat
response = requests.get("https://api.vk.com/method/groups.getLongPollServer?group_id=174367830&access_token=fbdc5bd3cff381a236f0f30a1b58982ca4ddf1508e03a6513af837d67184c6ffa064d2a6737a897bc012e&v=5.92")
resp_dict = json.loads(response.text)

key = resp_dict['response']['key']
ts = resp_dict['response']['ts']

print("chat initiated : ")
print(response.content)
print("----------------")

while 1:


    #poll events
    event_response = requests.get("https://lp.vk.com/wh174367830?act=a_check&key={}&ts={}&wait=25".format(key, ts))
    print("https://lp.vk.com/wh174367830?act=a_check&key={}&ts={}&wait=25".format(key, ts))

    #extract peer_id from response
    even_resp_dict = json.loads(event_response.text)
    ts = even_resp_dict['ts']

    print(ts)

    peer_id = 0
    for f in even_resp_dict['updates']:
        if f['type'] == 'message_new':
            peer_id = f['object']['peer_id']

    print("peer id")
    print(peer_id)
    print("----------------")
    if peer_id != 0 and peer_id != "-174367830":
        random_num = randint(1, 10000)
        #do the analysis and detect emotion and decide what to send to user
        detected_emotion = mood.checkMood(peer_id)
        print(detected_emotion)

        processed_response = "Hi I'm bot"
        bot_response = requests.get("https://api.vk.com/method/messages.send?peer_id={}&random_id={}&message={}&access_token=fbdc5bd3cff381a236f0f30a1b58982ca4ddf1508e03a6513af837d67184c6ffa064d2a6737a897bc012e&v=5.92"
                                    .format(peer_id, random_num, processed_response))

        print("Bot Response")
        print(bot_response.content)
