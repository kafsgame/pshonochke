import os
import pbot
import requests
try:
    import emoji
except Exception:
    os.system('pip install emoji')
    import emoji
import subprocess
from time import sleep
import warnings
from random import randint

f = open('token.txt', 'r')
token = f.read()
f.close()
ruschar = "йцукенгшщзхъфывапролджэячсмитьбюё"
def load_accounts():
    accounts = []

    f = open("msgbase.txt", "r")
    tokens = f.read()
    f.close()
    tokens += "\n"
    account = []
    raw_account = ""
    str_start = 0
    for i in range(len(tokens)):
        if tokens[i] == "\n":
            elem_start = 0
            raw_account = tokens[str_start:i]
            raw_account += ":"
            for j in range(len(raw_account)):
                if raw_account[j] == ":":
                    account.append(raw_account[elem_start:j])
                    elem_start = j+1
            accounts.append(account)
            account = []
            str_start = i+1
    return accounts

keys = load_accounts()
def getMessages():
    text = []
    f = open("startMessages.txt","r")
    users = f.read()
    f.close()
    users +="\n"
    str_start = 0
    for i in range(len(users)):
        if users[i] == "\n":
            text.append(users[str_start:i])
            str_start = i+1
    return text

def send_message(msg, token, chat_id, make_reply = False):
    data = {'content': msg[0], 'tts': False}
    # Create reply to a message
    if make_reply:
        reply_data = {
            'channel_id': chat_id,
            'message_id': msg[1]
        }
        data['message_reference'] = reply_data
    session = requests.Session()
    r = session.post(
        f'https://discord.com/api/v9/channels/{chat_id}/messages', json=data, headers={'authorization': f'{token}'}, verify=False)
    return r.json()

def get_discord_messages(token, chat_id,count=100):
    r = requests.get(
        f'https://discord.com/api/v9/channels/{chat_id}/messages?limit={count}',
        headers={'authorization': f'{token}'})
    return r.json()


startMessages = getMessages()
warnings.filterwarnings("ignore")
a = subprocess.check_output('cd', shell=True)

chat = input('Введите ссылку на чат   ')
delay = int(input('Задержка в секундах    '))
delaywaiting = int(input('Задержка между отправкой сообщений, когда никто не пометил      '))


f = open('token.txt', 'r')
token = f.read()
f.close()
i = 0
was = []
me = send_message(['hi guys'],token, chat[len(chat)-18::])['author']['id']
sleep(delay)
while True:
    try:
        dialog = pbot.Dialog('53a8d349-5dee-4767-9ee2-60f152be5837', 'MrCreepTon')
        ctt = False

        msgs = get_discord_messages(token, chat[len(chat)-18::])
        replys = []
        for msg in msgs:
            if('referenced_message' in msg):
                if(msg['referenced_message']['author']['id'] == me):
                    if(msg not in was):
                        replys.append(msg)

        if replys == []:
            num = randint(0, len(startMessages)-1)
            msg_input =startMessages[num]
            send_message([msg_input], token, chat[len(chat)-18::])
            sleep(delaywaiting)
            continue
        replys.reverse()
        for reply in replys:
            i += 1
            if reply in was:
                continue
            text = reply['content']
            print(text)
            answ = dialog.sendMessage(text)
            for key in keys:
                if(key[0] == text):
                    if(key[1] != ""):
                        answ = f"{key[1]}."
            for char in ruschar:
                if(char in answ):
                    print(112)
                    answ = dialog.sendMessage(text)
                    for charr in ruschar:
                        if(charr in answ):
                            f = open('msgbase.txt','r')
                            msgbase = f.read()
                            f.close()
                            f = open('msgbase.txt', 'w')
                            f.write(msgbase+f'{text}:\n')
                            f.close()
                            ctt = True
                            break
            if ctt:
                continue
            if answ == "My name is ρBot.":
                answ = 'My name is Pasha.'
            if(answ == "My partner's name is qBot"):
                answ =  "My partner's name is pashas"
            if "no" in answ:
                if "answer" in answ:
                    f = open('msgbase.txt', 'r')
                    msgbase = f.read()
                    f.close()
                    f = open('msgbase.txt', 'w')
                    f.write(msgbase + f'{text}:\n')
                    f.close()
                    was.append(reply)
                    continue
            print(answ," : ",emoji.demojize(answ)[:len(answ)-1:])
            if(answ[len(answ)-1]):
                answ = emoji.demojize(answ[:len(answ)-1:])
            else:
                answ = emoji.demojize(answ[:len(answ):])
            send_message([answ,reply['id']],token,chat[len(chat)-18::], True)
            was.append(reply)
            sleep(delay)
    except Exception as e:
        print(e.args)
        continue
