import json

Prefix = "!!online"
Prefix = "!!ol"
PluginName = "OnlineList"
DataPath = "plugins/" + PluginName + "/data.json"
ConfigFilePath = "plugins/config/" + PluginName + ".json"

# global
data = []
flag = False

def joined_info(msg):
    if "logged in with entity id" in msg:
        if "[local]" in msg:
            return [True, "bot", msg.split('[')[0]]
        else:
            return [True, "player", msg.split('[')[0]]
    else:
        return [False]

def load_data():
    global data
    try:
        with open(DataPath) as file:
            data = json.load(file, encoding='utf8')
    except:
        return

def save_data():
    global data
    try:
        with open(DataPath, "w") as file:
            json.dump(data, file)
    except:
        return

def add_data(name, isbot):
    global data
    load_data()
    new = {"name" : name, "isbot" : isbot}
    data.append(new)
    save_data()

def delete_data(name):
    global data
    load_data()
    for i in range(0, len(data)):
        if data[i]["name"] == name:
            del data[i]
            save_data()
            return

def show_list(server, info):
    global data
    load_data()
    server.reply(info, "§a在线列表：§r")
    for i in range(0, len(data)):
        msg = data[i]["name"]
        if data[i]["isbot"]:
            msg += " §6(bot)§r"
        server.reply(info, msg)

def get_online_list():
    global data
    load_data()
    return data

def is_online(player):
    online_list = get_online_list()
    for i in range(0, len(online_list)):
        if player == online_list[i]["name"]:
            return True
    return False

def is_bot(player):
    online_list = get_online_list()
    for i in range(0, len(online_list)):
        if player == online_list[i]["name"]:
            if online_list[i]["isbot"]:
                return True
    return False

def on_load(server, module):
    server.add_help_message(Prefix, "获取玩家列表 | 自动识别bot")

def on_mcdr_stop(server):
    print("on_mcdr_stop")
    global data
    load_data()
    data = []
    save_data()

def on_player_left(server, player):
    global data
    load_data()
    delete_data(player)

def on_info(server, info):

    content = info.content
    splited_content = content.split()

    if info.source == 0 and not info.is_player:
        player_info = joined_info(content)
        # server.say(player_info)
        if player_info[0]:
            if player_info[1] == "bot":
                add_data(player_info[2], True)
            if player_info[1] == "player":
                add_data(player_info[2], False)

    if len(splited_content) == 0 or splited_content[0] != Prefix:
        return
    if content == Prefix:
        show_list(server, info)
        return
    server.reply(info, "§c格式错误§r")
    return


