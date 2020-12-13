# Standard library imports
import os
import json
import pathlib

home = pathlib.Path(__file__).parent.absolute()


def identifyChats():
    chats = {}

    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

    for d in os.listdir(path):
        if d.startswith("messages") and os.path.isdir(f'{path}/{d}'):
            for f in os.listdir(f'{path}/{d}/inbox'):
                name = f.lower().split('_')[0]
                hefe = f'{path}/{d}/inbox/{f}'

                if name not in chats:
                    chats[name] = [hefe]
                else:
                    chats[name].append(hefe)
                
    return chats


# Gets the json(s) with desired messages
def getJsons(chats):
    jsons = []
    for ch in chats:
        for file in os.listdir(ch):
            if file.startswith("message") and file.endswith(".json"):
                jsons.append(f"{ch}/{file}")
            if file == "message_1.json":
                with open(f"{ch}/{file}") as last:
                    data = json.load(last)
                    title = decode(data["title"])
                    names = getNames(data)
    if not jsons:
        raise Exception("NO JSON FILES IN THIS CHAT")
    return (jsons, title, names)

# Gets the desired messages
def getMsgs(jsons):
    messages = []
    for j in jsons:
        with open(j) as data:
            data = json.load(data)
            messages.extend(data["messages"])
    messages = sorted(messages, key=lambda k: k["timestamp_ms"])
    decodeMsgs(messages)
    return messages

# Gets names of the participants in the chat
def getNames(data):
    ns = []
    for i in data["participants"]:
        ns.append(i["name"].encode('iso-8859-1').decode('utf-8'))
    if len(ns) == 1:
        ns.append(ns[0])
    return ns

# Decodes a string from the Facebook encoding
def decode(word):
    return word.encode('iso-8859-1').decode('utf-8')

# Decodes all messages from the Facebook encoding
def decodeMsgs(messages):
    for m in messages:
        m["sender_name"] = m["sender_name"].encode('iso-8859-1').decode('utf-8')
        if "content" in m:
            m["content"] = m["content"].encode('iso-8859-1').decode('utf-8')
        if "reactions" in m:
            for r in m["reactions"]:
                r["reaction"] = r["reaction"].encode('iso-8859-1').decode('utf-8')
                r["actor"] = r["actor"].encode('iso-8859-1').decode('utf-8')
    return messages
