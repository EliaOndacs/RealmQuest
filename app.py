#  -RealmQuest game and Luncher-



#  =modding libraries=

import random,time
import base64,keyboard
import hashlib,wave
import websocket,socket

# =end of modding libraries=

# =realmQuestLuncher modules=

import os
import json
import winsound
import platform
import tomllib
import requests

# =end of realmQuestLuncher modules=

# =variables=
BeepFreq = 500
dir_path = os.path.dirname(os.path.realpath(__file__))
#using a private library for now on a localhost api. merge actual function to the project later.s
elia_lts = "http://127.0.0.1:5000/lts"
try:
    r = requests.request("GET",elia_lts)
    with open("lts.py","w") as f:f.write(r.text)
    del r
except requests.exceptions.ConnectionError:
    pass
from lts import *
if ListWithoutSpaceToString(["test","1"]) == "o_O":
    exit()
# =end of variables=


# =functions=

def END():
    print()
    print("see you next time :) .")
    winsound.Beep(BeepFreq,100)
    winsound.Beep(BeepFreq-100,100)
    winsound.Beep(BeepFreq-200,100)
    winsound.Beep(BeepFreq-300,100)
    winsound.Beep(BeepFreq-400,100)
    exit()

# =end of functions=

# =classes=

class Location:
    def __init__(self, name):
        self.name:str = name
        self.actions:dict = {}
        self.superActions:dict = {}
        self.rAtt:dict = {}
        self.achievements:list = []
        self.rActions:list = []
        self.BHLoader:list = []
        self.lock:bool = False
        self.startup:str|None = None

    def add_Attribute_control(self,attribute_name,require_value):
       self.rAtt[attribute_name] = require_value

    def check_lock(self,performed_actions,Instance_attribute):
        if len(self.rActions) == 0:
            self.lock = False
            return
        token = 0
        for i in self.rActions:
            if i[0] == "!":
                if i[1:] not in performed_actions:
                    token += 1
            else:
                if i in performed_actions:
                    token += 1
        for i in self.rAtt:
            if self.rAtt[i] == Instance_attribute[i]:
                token += 1
        if token == (len(self.rActions)+len(list(self.rAtt))):
            self.lock = False
            self.rActions = []
            self.rAtt = {}
            return
        self.lock = True

    def add_behavior(self,path):
        self.BHLoader.append(path)

    def add_superActions(self,actionName,action):
        self.superActions[actionName] = action

    def add_rActions(self,action):
        self.rActions.append(action)
        self.lock = True

    def add_action(self, action, result):
        self.actions[action] = result

    def add_achievement(self, name, actions, dis, end=False,END_text="",ATTRIBUTE={},bh=[]):
        self.achievements.append({"name": name, "actions": actions, "dis":dis, "end":end,"endText":END_text,"attribute":ATTRIBUTE, "bh":bh})

    def execute_actions(self,al:list,game):
        print(f"Welcome to {self.name}!")
        while True:
            print('-'*10)
            for action in self.actions:
                print(f"- {action}")
            print("="*10)
            action = input("which action you want to do?\n\t:")
            winsound.Beep(BeepFreq,100)
            if action == "." or action == "BACK":
                break
            elif action == "exit":
                END()
            elif action == "att" or action == "ATTRIBUTES":
                print("your player attributes are this:")
                for i in Instance_Attribute:
                    print(f"- {i}: {Instance_Attribute[i]}")
                continue
            elif action == "paths" or action == "ACHIEVEMENTS":
                print("all of the loaded achievements.")
                for i in self.achievements:
                    print(f"- {i["name"]}: {"✓" if ("#"+(i["name"])) in performed_Actions else "✗"}")
                continue
            print("="*10)
            if len(action) > 0:
                if action[0] == ".":
                    result = self.perform_superAction(action[1:])
                else:
                    result = self.perform_action(action)
                if result != -1:al.append(action)
                game.check_all_achievements(al,game)
        return al

    def perform_superAction(self, action):
        if action in self.superActions:
            winsound.Beep(BeepFreq+150,100)
            exec(self.superActions[action],globals(),locals())
        else:
            winsound.Beep(BeepFreq+800,100)
            print(f"Unknown SuperAction: {action}")
            return -1

    def load_BHStack(self,g):
        for item_Path in self.BHLoader:
            with open(os.path.join(dir_path,"mods",item_Path), "rb") as f:
                ob_data = tomllib.load(f)
                for name in ob_data:
                    if name == "author":
                        g.authors.append(ob_data[name])
                        continue
                    if name == "player":
                        for _name in ob_data[name]:
                            if _name == "age":
                                Instance_Attribute["age"] = ob_data[name][_name]
                            if _name == "health":
                                Instance_Attribute["health"] = ob_data[name][_name]
                            Instance_Attribute[_name] = ob_data[name][_name]

    def perform_action(self, action):
        if action in self.actions:
            print(self.actions[action])
            winsound.Beep(BeepFreq+100,100)
        else:
            print(f"Unknown action: {action}")
            return -1

    def check_achievements(self, performed_actions,g):
        for achievement in self.achievements:
            token = 0
            for item in set(achievement["actions"]):
                if item[0] == "!":
                    if item[1:] not in performed_Actions:
                        token += 1
                else:
                    if item in performed_Actions:
                        token += 1
            for item in achievement["attribute"]:
                if achievement["attribute"][item] == Instance_Attribute[item]:
                    token += 1
            if token == (len(achievement["actions"])+len(achievement["attribute"])):
                for _ in set(achievement["actions"]):
                    if _[0] == "!":
                        pass
                    else:
                        performed_Actions.remove(_)
                if achievement["end"] == False:
                    winsound.Beep(BeepFreq*2,200)
                else:
                    winsound.Beep(BeepFreq*2,100)
                for item in achievement["bh"]:
                    with open(os.path.join(dir_path,"mods",item), "rb") as f:
                        ob_data = tomllib.load(f)
                        for name in ob_data:
                            if name == "author":
                                g.authors.append(ob_data[name])
                                continue
                            if name == "player":
                                for _name in ob_data[name]:
                                    if _name == "age":
                                        Instance_Attribute["age"] = ob_data[name][_name]
                                    if _name == "health":
                                        Instance_Attribute["health"] = ob_data[name][_name]
                                    Instance_Attribute[_name] = ob_data[name][_name]
                print(f"Achievement unlocked at {self.name}: {achievement['name']}")
                print(f"description: {achievement["dis"]}")
                performed_Actions.append(f"#{achievement["name"]}")
                if achievement["end"] == True:
                    print("-+"*10)
                    print(achievement["endText"])
                    END()

class Game:
    def __init__(self):
        self.locations = {}
        self.authors:list = []

    def add_location(self, location):
        self.locations[location.name] = location

    def load_mods(self):
        mods_folder = os.path.join(dir_path,"mods")
        for filename in os.listdir(mods_folder):
            if filename.endswith(".json"):
                with open(os.path.join(mods_folder, filename), "r") as file:
                    of_data = json.load(file)
                    for Structure in of_data:
                        if Structure == "author":
                            self.authors.append(of_data[Structure])
                            continue
                        ld = of_data[Structure]
                        location_name = ld["name"]
                        location = Location(location_name)
                        if "startup" in ld:
                            location_startup_text = ld["startup"]
                            location.startup = location_startup_text
                        for items in ld.get("required_actions",[]):
                            location.add_rActions(items)
                        for action, result in ld["actions"].items():
                            location.add_action(action, result)
                        if "required_attribute" in ld:
                            for attribute, required_value in ld["required_attribute"].items():
                                location.add_Attribute_control(attribute, required_value)
                        for achievement in ld.get("achievements", []):
                            END = False
                            END_text:str = ""
                            ATTRIBUTE:dict = {}
                            bh = [r"templates\achievement.toml"]
                            if "bh" in achievement:
                                bh.extend(achievement["bh"])
                            if "attribute" in achievement:
                                ATTRIBUTE = achievement["attribute"]
                            if "end" in achievement and "endText" in achievement:
                                END = achievement["end"]
                                END_text = achievement["endText"]
                            location.add_achievement(achievement["name"], achievement["actions"], achievement["description"],END,END_text,ATTRIBUTE,bh)
                        if "SuperActions" in ld:
                            for action, result in ld["SuperActions"].items():
                                location.add_superActions(action, result)
                        else:
                            pass
                        location.add_behavior(r"templates\location.toml")
                        if "BH" in ld:
                            for item in ld.get("HB",[]):
                                location.add_behavior(item)
                        self.add_location(location)
            elif filename.endswith(".toml"):
                with open(os.path.join(mods_folder, filename), "rb") as f:
                    ob_data = tomllib.load(f)
                    for name in ob_data:
                        if name == "author":
                            self.authors.append(ob_data[name])
                            continue
                        if name == "player":
                            for _name in ob_data[name]:
                                if _name == "age":
                                    Instance_Attribute["age"] = ob_data[name][_name]
                                if _name == "health":
                                    Instance_Attribute["health"] = ob_data[name][_name]
                                Instance_Attribute[_name] = ob_data[name][_name]

    def visit_location(self, location_name, al: list):
        if location_name in self.locations:
            self.locations[location_name].load_BHStack(self)
            if self.locations[location_name].startup != None:
                print(self.locations[location_name].startup)
            return self.locations[location_name].execute_actions(al,game)
        else:
            print(f"Unknown location: {location_name}")

    def perform_action(self, location_name, action):
        if location_name in self.locations:
            self.locations[location_name].perform_action(action)
        else:
            print(f"Unknown location: {location_name}")

    def check_achievements(self, location_name, performed_actions,g):
        if location_name in self.locations:
            self.locations[location_name].check_achievements(performed_actions,g)
        else:
            print(f"Unknown location: {location_name}")

    def check_all_achievements(self, performed_actions,g):
        for location_name, location in self.locations.items():
            location.check_achievements(performed_actions,g)

# =end of classes=

# =main entry=


if __name__ == "__main__":
    #############
    os.system("@Call stc.bat")
    os.system("cls" if os.name == "nt" else "clear")
    print("-\\"*(os.get_terminal_size().columns // 2))
    print("!# checking app security. mypy-result.")
    with open("mypy.result",'r') as f:
        if f.readline().replace("\n","") == "Success: no issues found in 2 source files":
            pass
        else:
            print("WARNING: you are playing on a corrupted version of ReamQuestLuncher.\ngame can be modified in a not professional way.")
        f.close()
    print("-# going forward.")
    #############
    print("loading game")
    performed_Actions:list = []
    Instance_Attribute:dict = {"age":15,"health":100}
    game = Game()
    winsound.Beep(50,100)
    print("loading mods")
    winsound.Beep(50,100)
    game.load_mods()
    winsound.Beep(1100,500)
    print("boom. your in the game.")
    while True:
        ############################
        cycle_data = {'pa':performed_Actions,"ia":Instance_Attribute}
        ############################
        print("-"*10)
        #
        for name,obj in game.locations.items():
            obj.check_lock(performed_Actions,Instance_Attribute)
            if obj.lock == True:
                continue
            print(f"- {name}")
        #
        print("="*10)
        location = input("which location do you want to visit?\n\t:")
        winsound.Beep(BeepFreq,100)
        print("="*10)
        match location.split():
            case ["save",name]:
                with open(os.path.join(dir_path,"SAVES",name+".rqs.json"),"w") as jsonFile:
                    json.dump(cycle_data,jsonFile,indent=4)
                    jsonFile.close()
                continue
            case ["load",name]:
                with open(os.path.join(dir_path,"SAVES",name+".rqs.json"),"r") as jsonFile:
                    data = json.load(jsonFile)
                    performed_Actions = data["pa"]
                    Instance_Attribute = data["ia"]
                    jsonFile.close()
                continue
            case ["map",*_achievementName]:
                achievementName = ListWithoutSpaceToString(_achievementName)
                for location_name in game.locations:
                    for i in game.locations[location_name].achievements:
                        if i["name"] == achievementName and ("#"+(i["name"])) in performed_Actions:
                            print(f"the following:{achievementName} achievement:")
                            print(f"achievement name:{i["name"]}")
                            print(f"description:{i["dis"]}")
                            print(f"performed_actions:{str(i["actions"]).replace("[","").replace("]","")}")
                continue
        if location == "exit":
            break
        elif location == "reload":
            with open(os.path.join(dir_path,"SAVES","runtime","$tmp.rqs.json"),"w") as jsonFile:
                json.dump(cycle_data,jsonFile,indent=4)
                jsonFile.close()
            print("reloading game")
            performed_Actions = []
            Instance_Attribute = {"age":15,"health":100}
            game = Game()
            winsound.Beep(50,100)
            print("loading mods")
            winsound.Beep(50,100)
            game.load_mods()
            winsound.Beep(1100,500)
            print("your game got reloaded..")
            with open(os.path.join(dir_path,"SAVES","runtime","$tmp.rqs.json"),"r") as jsonFile:
                data = json.load(jsonFile)
                performed_Actions = data["pa"]
                Instance_Attribute = data["ia"]
                jsonFile.close()
            os.remove(os.path.join(dir_path,"SAVES","runtime","$tmp.rqs.json"));
            continue
        elif location == "paths" or location == "ACHIEVEMENTS":
            print("all of the loaded achievements.")
            for location_name in game.locations:
                for i in game.locations[location_name].achievements:
                    print(f"- {i["name"]}: {"✓" if ("#"+(i["name"])) in performed_Actions else "✗"}")
            continue
        elif location == "credits":
            print("authors of the instance of the game that you are playing are:")
            said = []
            for names in game.authors:
                if names not in said:
                    print(f"» {names}")
                    said.append(names)
            print()
            print("credit for the RealmQuest Luncher:")
            print("» EliaOndacs.")
            continue
        elif location == "att" or location == "ATTRIBUTES":
            print("your player attributes are this:")
            for i in Instance_Attribute:
                print(f"- {i}: {Instance_Attribute[i]}")
            continue
        elif not game.locations.__contains__(location):
            print("location not defined!.")
            continue
        if game.locations[location].lock == True:
            print("location is locked!")
            print("actions needed to be performed:")
            for i in game.locations[location].rActions:
                print(f"- {i}")
            print(" and your player attribute needs to be this:")
            for i in game.locations[location].rAtt:
                print(f"- {i}:{game.locations[location].rAtt[i]}")
            print("~"*10)
            continue
        performed_Actions = game.visit_location(location,performed_Actions)
    END()

# =end of main entry=
