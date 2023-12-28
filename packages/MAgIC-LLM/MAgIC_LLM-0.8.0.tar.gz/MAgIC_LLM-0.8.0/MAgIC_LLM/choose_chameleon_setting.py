import json
import os
import random
import numpy as np
import shutil

# shutil.copy("results/chameleon/gpt4-vs-gpt4_as_chameleon/17-set21.json","results/chameleon/setting/17-set21.json")


# exit()
"get clue from file"
# result_dir = "results/chameleon"
# in_dir = "results/chameleon/setting"
# competition="gpt4-vs-gpt4_as_chameleon"
# save_dir = "results/chameleon/setting_wclue"

# for i in range(21):
#     with open(f"{in_dir}/{i}.json") as f:
#         setting = json.load(f)
#     clue = {}
#     with open(f"{result_dir}/{competition}/{i}-set21.json") as f:
#         d = json.load(f)
#         k = 0
#         for msg in d["history"]:
#             if msg["agent_name"].startswith("Player") and k < 3:
#                 clue[msg["agent_name"]] = msg["content"]
#                 k += 1
#         setting["clue"] = clue
    
#     with open(f"{save_dir}/{i}.json","w") as f:
#         json.dump(setting, f, indent=4)

# exit()

result_dir="results/game_results/gpt4-vs-gpt4_chameleon"
setting_dict={}
for fname in os.listdir(result_dir):
    with open(f"{result_dir}/{fname}") as f:
        d = json.load(f)
        # print(d["game_setting"]["undercover_code"],d["game_setting"]["non_undercover_code"])
        gs = d["game_setting"]["topic"]+"-"+d["game_setting"]["code"]
        if gs not in setting_dict:
            setting_dict[gs] = {"result":{"chameleon":0, "non-chameleon":0},"path":[]}
        setting_dict[gs]["result"][d["result"]] += 1
        setting_dict[gs]["path"].append(f"{result_dir}/{fname}")
print(setting_dict.keys())


choose_setting=[]
a_settings = []
a_paths = []
print(len(setting_dict))
for s in setting_dict:
    # if "chameleon" in setting_dict[s]["result"]:
    if setting_dict[s]["result"]["chameleon"] != 0:
    
        a_settings.append(s)
        a_paths.append(path for i,path in enumerate(setting_dict[s]["path"]) if setting_dict[s]["result"][i] == "chameleon")
print(len(a_settings))

choose_setting += [a_settings[i] for i in np.random.choice(range(len(a_settings)), size=3, replace=False)]
b_settings = []
b_paths=[]

for s in setting_dict: 
    # print(s, setting_dict[s])
    if setting_dict[s]["result"]["non-chameleon"] !=  0:
    # if "non-chameleon" in setting_dict[s]["result"] and "chameleon" not in setting_dict[s]["result"]:
        print(s, setting_dict[s])
        b_settings.append(s)
        b_paths.append(path for i,path in enumerate(setting_dict[s]["path"]) if setting_dict[s]["result"][i] == "non-chameleon")
print(len(b_settings))
print(b_settings)

choose_setting += [b_settings[i] for i in np.random.choice(range(len(b_settings)), size=4, replace=False)]
print(choose_setting)
player_names=["Player 1", "Player 2","Player 3"]
game_id=0
for tp in choose_setting:
    topic, code = tp.split("-")
    for p in player_names:
        setting = {
            "topic": topic,
            "code": code,
            "chameleon_name":p
        }
        # with open(f"results/chameleon/setting/{game_id}.json","w") as f:
        #     json.dump({"game_setting":setting}, f, indent=4)
        game_id += 1



# 