import requests
import random
import json
import mood

# initiate chat
response = requests.get(
    "https://api.vk.com/method/groups.getLongPollServer?group_id=174367830&access_token=fbdc5bd3cff381a236f0f30a1b58982ca4ddf1508e03a6513af837d67184c6ffa064d2a6737a897bc012e&v=5.92")
resp_dict = json.loads(response.text)

key = resp_dict['response']['key']
ts = resp_dict['response']['ts']

print("chat initiated : ")
print(response.content)
print("----------------")
# Sentences we'll respond with if the user greeted us
# Sentences we'll respond with if the user greeted us
GREETING_KEYWORDS = ("hello", "hey", "hi", "greetings", "sup")
GREETING_JOY_RESPONSES = ["Hi {}, how was your day?", "Hello {}. How are you?", "Hi {}! Nice to see you! How are you doing?"]
GREETING_SAD_RESPONSES = ["'Hi {}, how are you today?", "Hey {}, I'm glad you wrote me, how are you?"]

HRY_JOY_KEYWORDS = ("good", "everything", "fine")
HRY_JOY_RESPONSES = ["Glad to hear. Can I do anything?", "That's good. Can I help you with something?", ]

SUG_JOY_KEYWORDS = ("suggest", "music", "suggestions", "listen")
SUG_JOY_RESPONSES = ["Sure! Check this one out", "Yep! Try this one: ", "Most certainly! Check this one "]

TY_JOY_POS_KEYWORDS = ("thanks", "thank you", "nice", "!")
TY_JOY_POS_RESPONSES = ["You are welcome", "Glad I could help", "Anytime"]

HRY_SAD_KEYWORDS = ("good", "fine", "ok",)
HRY_SAD_RESPONSES = ["Talk to me", "Anything on you mind?"]

WH_0_SAD_KEYWORDS = ("sucks", "hate", "bad")
WH_0_SAD_RESPONSES = ["Why do you say so?", "Can you tell me why?", "What made you feel that way?"]

WH_1_SAD_KEYWORDS = ("can't", "concentrate", "anything", "sad", "nothing", "confused")
WH_1_SAD_RESPONSES = ["I see... Did you try listen to music? I heard it can help"]

SUG_SAD_KEYWORDS = ("suggest", "suggestion", "recommend", "something", "Haven't", "heard", "?", "what")
SUG_SAD_RESPONSES = ["Sure! Check this one out", "Yep! Try this one: ", "Most certainly! Check this one "]

TY_SAD_POS_KEYWORDS = ("wow", "thanks", "really", "helped")
TY_SAD_POS_RESPONSES = ["You are most welcome", "Glad I could help", "Anytime"]

TY_SAD_NEG_KEYWORDS = ("not", "helping...", "nothing's", "changed", "doesn't", "help")
TY_SAD_NEG_RESPONSES = ["Sorry it didn't help. Let's try smth else ... (to be continued...)"]

ATTACHMENTS_Concentration = ("video-16108331_456253513", "audio762177_338483985", "audio-2000765891_456239030")


def check_for_responses(emotion, sentence, name):
    for word in sentence.split():
        print(word.lower())
        rand_item = "Please repeat"
        need_sug = "0"
        if emotion == "joy":
            if word.lower() in GREETING_KEYWORDS:
                rand_item = GREETING_JOY_RESPONSES[random.randrange(len(GREETING_JOY_RESPONSES))]
                rand_item = rand_item.format(name)
                need_sug = "0"
            if word.lower() in HRY_JOY_KEYWORDS:
                rand_item = HRY_JOY_RESPONSES[random.randrange(len(HRY_JOY_RESPONSES))]
                need_sug = "0"
            if word.lower() in SUG_JOY_KEYWORDS:
                rand_item = SUG_JOY_RESPONSES[random.randrange(len(SUG_JOY_RESPONSES))]
                need_sug = "1"
                print(rand_item)
                print(need_sug)
            if word.lower() in TY_JOY_POS_KEYWORDS:
                rand_item = TY_JOY_POS_RESPONSES[random.randrange(len(TY_JOY_POS_RESPONSES))]
                need_sug = "0"
        elif emotion == "sadness":
            if word.lower() in GREETING_KEYWORDS:
                rand_item = GREETING_SAD_RESPONSES[random.randrange(len(GREETING_SAD_RESPONSES))]
                rand_item = rand_item.format(name)
                need_sug = "0"
            if word.lower() in HRY_SAD_KEYWORDS:
                rand_item = HRY_SAD_RESPONSES[random.randrange(len(HRY_SAD_RESPONSES))]
                need_sug = "0"
            if word.lower() in WH_0_SAD_KEYWORDS:
                rand_item = WH_0_SAD_RESPONSES[random.randrange(len(WH_0_SAD_RESPONSES))]
                need_sug = "0"
            if word.lower() in WH_1_SAD_KEYWORDS:
                rand_item = WH_1_SAD_RESPONSES[random.randrange(len(WH_1_SAD_RESPONSES))]
                need_sug = "0"
            if word.lower() in SUG_SAD_KEYWORDS:
                rand_item = SUG_SAD_RESPONSES[random.randrange(len(WH_1_SAD_RESPONSES))]
                need_sug = "1"
            if word.lower() in TY_SAD_POS_KEYWORDS:
                rand_item = TY_SAD_POS_RESPONSES[random.randrange(len(TY_SAD_POS_RESPONSES))]
                need_sug = "0"
            if word.lower() in TY_SAD_NEG_KEYWORDS:
                rand_item = TY_SAD_NEG_RESPONSES[random.randrange(len(TY_SAD_NEG_RESPONSES))]
                need_sug = "0"
    return [rand_item, need_sug]


# _questions


while 1:

    # poll events
    event_response = requests.get("https://lp.vk.com/wh174367830?act=a_check&key={}&ts={}&wait=25".format(key, ts))
    print("https://lp.vk.com/wh174367830?act=a_check&key={}&ts={}&wait=25".format(key, ts))

    # extract peer_id from response
    even_resp_dict = json.loads(event_response.text)
    ts = even_resp_dict['ts']
    peer_id = 0
    for f in even_resp_dict['updates']:
        if f['type'] == 'message_new':
            peer_id = f['object']['peer_id']
            text = f['object']['text']

    if peer_id != 0 and peer_id != "-174367830":
        random_num = random.randint(1, 10000)
        # do the analysis and detect emotion and decide what to send to user
        detected_emotion = mood.checkMood(peer_id)
        print(detected_emotion)

        # print(mood.checkMood(peer_id))

        processed_response = check_for_responses(detected_emotion, text, "Human")

        attachment = ""
        if processed_response[1] == "1":
            attachment = ATTACHMENTS_Concentration[random.randrange(len(ATTACHMENTS_Concentration))]

        bot_response = requests.get(
            "https://api.vk.com/method/messages.send?peer_id={}&random_id={}&message={}&attachment={}&access_token=fbdc5bd3cff381a236f0f30a1b58982ca4ddf1508e03a6513af837d67184c6ffa064d2a6737a897bc012e&v=5.92"
            .format(peer_id, random_num, processed_response[0], attachment))

        print("Bot Response")
        print(bot_response.content)

