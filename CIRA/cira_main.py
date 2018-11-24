import requests
import random
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
# Sentences we'll respond with if the user greeted us
GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up")

GREETING_JOY_RESPONSES = ["Hi {}, how was your day?", "Hello {}. How are you?", "Hi {}! Nice to see you!"]
GREETING_SAD_RESPONSES = ["'Hi {}, how are you today?", "Hey {}, I'm glad you wrote me", "Hey {}! What's on your mind?"]

HRY_POS_KEYWORDS = ("Good", "I'm good, actually", "Everything is fine!")
HRY_JOY_RESPONSES = ["Glad to hear", "That's good"]
HRY_SAD_RESPONSES = []


def check_for_responses(emotion, sentence):
    for word in sentence.split():
        print(word.lower())
        if word.lower() in GREETING_KEYWORDS and emotion == "joy":
            rand_item = GREETING_JOY_RESPONSES[random.randrange(len(GREETING_JOY_RESPONSES))]
            return rand_item
        elif word.lower() in GREETING_KEYWORDS and emotion == "sadness":
            random.shuffle(GREETING_SAD_RESPONSES, random)
            return GREETING_SAD_RESPONSES[0]

while 1:

    #poll events
    event_response = requests.get("https://lp.vk.com/wh174367830?act=a_check&key={}&ts={}&wait=25".format(key, ts))
    print("https://lp.vk.com/wh174367830?act=a_check&key={}&ts={}&wait=25".format(key, ts))

    #extract peer_id from response
    even_resp_dict = json.loads(event_response.text)
    ts = even_resp_dict['ts']
    peer_id = 0
    for f in even_resp_dict['updates']:
        if f['type'] == 'message_new':
            peer_id = f['object']['peer_id']
            text = f['object']['text']

    if peer_id != 0 and peer_id != "-174367830":
        random_num = random.randint(1, 10000)
        #do the analysis and detect emotion and decide what to send to user

        #print(mood.checkMood(peer_id))

        processed_response = check_for_responses("happy", text)

        bot_response = requests.get("https://api.vk.com/method/messages.send?peer_id={}&random_id={}&message={}&access_token=fbdc5bd3cff381a236f0f30a1b58982ca4ddf1508e03a6513af837d67184c6ffa064d2a6737a897bc012e&v=5.92"
                                    .format(peer_id, random_num, processed_response))

        print("Bot Response")
        print(bot_response.content)


