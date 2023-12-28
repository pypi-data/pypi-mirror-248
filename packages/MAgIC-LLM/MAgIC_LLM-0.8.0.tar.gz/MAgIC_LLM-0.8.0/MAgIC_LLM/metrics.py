import json
import re
import os

player_names =["Player 1","Player 2","Player 3"]
def judge(result_path, postfix):
    non_right_vote = 0
    non_total_vote = 0
        
    for path, post in zip(result_path, postfix):
        print(path, post)
        non_chameleon_right_vote = 0
        non_chameleon_vote = 0      

        for game_id in range(21):
            # print(f"{game_id}-tp0.json")
            fname = f"{path}/{game_id}{post}.json"
            if not os.path.exists(fname):
                continue
            with open(fname) as f:
                d = json.load(f)
                
                # chameleon = d["chameleon"] if "chameleon" in d else d["chameleon"]
                chameleon = d["undercover"] if "undercover" in d else d["chameleon"]
                votes = d["player_vote"] if "player_vote" in d else d["player_votes"]
                k = 0
                for pl in votes:
                    if pl != chameleon:
                        if votes[pl] == chameleon:
                            non_chameleon_right_vote += 1
                            k += 1
                        non_chameleon_vote +=1 
                # print(chameleon, votes, k, d["win_flag"])
        print(non_chameleon_right_vote, non_chameleon_vote)
        print(non_chameleon_right_vote/non_chameleon_vote)  
        non_right_vote += non_chameleon_right_vote
        non_total_vote += non_chameleon_vote
    print(non_right_vote/non_total_vote)  


def decept(result_path, postfix):
    print(result_path)
    win_num = 0.0
    total_num = 0.0
    for path, post in zip(result_path, postfix):
        win_results = {}

        for game_id in range(21):
            fname =f"{path}/{game_id}{post}.json"
            if not os.path.exists(fname):
                continue
            # print(fname)
            with open(fname) as f:
                d = json.load(f)
                # print(fn, d["win_flag"])
                if d["win_flag"] not in win_results:
                    win_results[d["win_flag"]] = 0
                win_results[d["win_flag"]] += 1
        for tag in win_results:
            if tag != 0:
                win_num += win_results[tag]
            total_num += win_results[tag]
        
        print(win_results)
    print(win_num, total_num)
    print(win_num/total_num)


def collabration(result_path, postfix):
    print(result_path)
    win_num = 0.0
    total_num = 0.0
    cost = 0.0
    agreed_proposal = 0.0

    for path, post in zip(result_path, postfix):
        win_results = {}
        
        for game_id in range(21):

            fname =f"{path}/{game_id}{post}.json"
            # print(fname)
            if not os.path.exists(fname):
                continue
            # print(fname)
            with open(fname) as f:
                d = json.load(f)
                if d["result"]=="agree":
                    if "vote" in d:
                        vote = list(d["vote"].values())[0]
                    else:
                        pattern = r"I vote for (Player \d+)"
                        match = re.search(pattern,  d["history"][-2]["content"])
                        assert match is not None
                        vote = match.group(1)

                    test_play_idx = player_names.index(d["test_player_name"])
                    voted_proposal = list(d["proposal"][vote].values())
                    print(voted_proposal,list(d["proposal"][d["test_player_name"]].values()))
                    if voted_proposal == list(d["proposal"][d["test_player_name"]].values()):
                        agreed_proposal += 1
                         
                    if "%" in voted_proposal[test_play_idx]:
                        cur_cost = float(voted_proposal[test_play_idx].replace("%",""))
                    elif "," in voted_proposal[test_play_idx]:
                        cur_cost = 100*(float(voted_proposal[test_play_idx].replace(",",""))/1000000)
                    else:
                        try:
                            cur_cost = float(voted_proposal[test_play_idx])
                        except:
                            print("cannot parse", voted_proposal[test_play_idx])
                            cur_cost = 30

                    cost += cur_cost

                if d["result"] not in win_results:
                    win_results[d["result"]] = 0
                win_results[d["result"]] += 1

        for tag in win_results:
            if tag == "agree":
                win_num += win_results[tag]
            total_num += win_results[tag]

        print(win_results)
    print(agreed_proposal, agreed_proposal/win_results["agree"])
    print(cost, cost/win_results["agree"])

    print(win_num, total_num)
    print(win_num/total_num)

def consist_pgm(result_path, postfix):
    print(result_path)
    consist_num = 0.0
    total_num = 0.0
    player_names = ["Player 1", "Player 2", "Player 3"]

    gold_pgm_num = 0.0
    total_gold_pgm_num = 0.0

    inter_pgm_num = 0.0
    total_inter_pgm_num = 0.0

    for path, post in zip(result_path, postfix):
        
        if "chameleon" in path:
            if "non-chameleon" in path:
                eval_role = "non-chameleon"
            else:
                eval_role = "chameleon"
        elif "undercover" in path:
            if "non-undercover" in path:
                eval_role = "non-undercover"
            else:
                eval_role = "undercover"
        else:
            print("cannot find the game for ", path)


        for game_id in range(21):
            # print(game_id)
            target_players = []
            fname = f"{path}/{game_id}{post}.json"
            if not os.path.exists(fname):
                continue
            with open(fname) as f:
                d = json.load(f)
                
                if eval_role in d:
                    target_players.append(d[eval_role])
                else:
                    target_players = [p for p in player_names if p != d[eval_role.replace("non-","")]]
                # print(target_players)
                target_player_inds = [player_names.index(p) for p in target_players]

                for t in d["consistency_metric"]:
                    consist_num += sum([d["consistency_metric"][t][p] for p in target_players])
                    total_num += len(target_players) 
                
                for t in d["pgm_metric"]:
                    gold_pgm_num += sum([d["pgm_metric"][t]["gold"][p] for p in target_player_inds])  # pgm acc compared to gold roles 
                    total_gold_pgm_num += len(target_players)
                    inter_pgm_num += sum([d["pgm_metric"][t]["inter"][p] for p in target_player_inds])  # pgm acc compared to interview roles
                    total_inter_pgm_num += len(target_players) 

    print(consist_num, total_num)
    print(gold_pgm_num, total_gold_pgm_num)
    print(inter_pgm_num, total_inter_pgm_num)

    print(consist_num/total_num, gold_pgm_num/total_gold_pgm_num, inter_pgm_num/total_inter_pgm_num,  (gold_pgm_num+inter_pgm_num)/(total_inter_pgm_num+total_gold_pgm_num))





players = ["Player 1", "Player 2", "Player 3"]
def rational(result_path, postfix):
    
    print(result_path, postfix)
    

    def norm_decision(dec):
        dec = re.sub(r'\.<eos>$|\.$', '', dec.lower())
        if dec.find("cooperate")>=0:
            return "cooperate"
        else:
            return "defect"
    def extract_contribute(dec):
        pattern =r"I contribute (\d+)"
        match = re.search(pattern, dec)
        if match:
            bid = match.group(1)
        else:
            print(dec)
            print("cannot parse the decision")
            bid = 0
        # print(bid)
        return int(bid) if bid.isdigit() else 0

    # def norm_decision_public_good(dec):


    # decisions = {'cooperate':0, "defect":0}
    decisions = {'non-rational':0, "rational":0}

    for path, post in zip(result_path, postfix):
        test_game="public_good"
        if path.find("prisoner")>=0:
            test_game="prisoner"
        for game_id in range(21):
            # print(game_id)
            target_players = []
            with open(f"{path}/{game_id}{post}.json") as f:
                d = json.load(f)
                test_player_name = d["test_player_name"]
                test_player_idx = players.index(test_player_name)
            if test_game=="prisoner":

                for msg in d["history"]:
                    if msg["agent_name"].startswith("Player") and msg["visible_to"] == "Moderator" and msg["agent_name"]==test_player_name:
                        if norm_decision(msg["content"])=="defect":

                            decisions["rational"] += 1
                        else:
                            decisions["non-rational"] += 1
            else:
                cur_round_contributes = []
                
                for msg in d["history"]:
                    if msg["agent_name"].startswith("Player") and msg["visible_to"] == "Moderator":
                        cur_round_contributes.append(extract_contribute(msg["content"]))
                        if len(cur_round_contributes) == 3:
                            min_contribute = min(cur_round_contributes)
                            if cur_round_contributes[test_player_idx] == min_contribute:
                                decisions["rational"] += 1
                            else:
                                decisions["non-rational"] += 1
                            cur_round_contributes = []

                
    print(decisions["rational"]/sum(decisions.values()))



model_results ={
    "non-chameleon":{
        "gpt3.5": {"path":"results/game_results/chosen_fixset1_gpt3.5-vs-gpt4_as_non-chameleon", "post":"-tp0"},
        "gpt4": {"path":"results/game_results/chosen_fixset1_gpt4-vs-gpt4_as_non-chameleon", "post":"-tp0"},
        "llama": {"path":"results/game_results/chosen_fixset1_llama-vs-gpt4_as_non-chameleon", "post":"-tp0-2"},
        "gpt3.5-pgm": {"path":"results/game_results/chosen_fixset1_gpt3.5-pgm-vs-gpt4_as_non-chameleon", "post":"-tp0-demopre"},
        "gpt4-pgm": {"path":"results/game_results/chosen_fixset1_gpt4-pgm-vs-gpt4_as_non-chameleon", "post":"-tp0-demopre"},
        "llama-pgm": {"path":"results/game_results/chosen_fixset1_llama-pgm-vs-gpt4_as_non-chameleon", "post":"-tp0"},
    },
    "chameleon":{
        "gpt3.5": {"path":"results/game_results/chosen_fixset1_gpt3.5-vs-gpt4_as_chameleon", "post":"-tp0"},
        "gpt4": {"path":"results/game_results/chosen_fixset1_gpt4-vs-gpt4_as_chameleon", "post":"-tp0"},
        "llama": {"path":"results/game_results/chosen_fixset1_llama-vs-gpt4_as_chameleon", "post":"-tp0-2"},
        "gpt3.5-pgm": {"path":"results/game_results/chosen_fixset1_gpt3.5-pgm-vs-gpt4_as_chameleon_tp0", "post":"-tp0"},
        "gpt4-pgm": {"path":"results/game_results/chosen_fixset1_gpt4-pgm-vs-gpt4_as_chameleon", "post":"-tp0"},
        "llama-pgm": {"path":"results/game_results/chosen_fixset1_llama-pgm-vs-gpt4_as_chameleon", "post":"-tp0"},
    },
    "non-chameleon_metric":{
        "gpt3.5": {"path":"results/metric/chosen_fixset1_gpt3.5-vs-gpt4_as_non-chameleon", "post":""},
        "gpt4": {"path":"results/metric/chosen_fixset1_gpt4-vs-gpt4_as_non-chameleon", "post":""},
        "llama": {"path":"results/metric/chosen_fixset1_llama-vs-gpt4_as_non-chameleon", "post":""},
        "gpt3.5-pgm": {"path":"results/metric/chosen_fixset1_gpt3.5-pgm-vs-gpt4_as_non-chameleon", "post":""},
        "gpt4-pgm": {"path":"results/metric/chosen_fixset1_gpt4-pgm-vs-gpt4_as_non-chameleon", "post":""},
        "llama-pgm": {"path":"results/metric/chosen_fixset1_llama-pgm-vs-gpt4_as_non-chameleon", "post":""},
    },
    "chameleon_metric":{
        "gpt3.5": {"path":"results/metric/chosen_fixset1_gpt3.5-vs-gpt4_as_chameleon", "post":""},
        "gpt4": {"path":"results/metric/chosen_fixset1_gpt4-vs-gpt4_as_chameleon", "post":""},
        "llama": {"path":"results/metric/chosen_fixset1_llama-vs-gpt4_as_chameleon", "post":""},
        "gpt3.5-pgm": {"path":"results/metric/chosen_fixset1_gpt3.5-pgm-vs-gpt4_as_chameleon", "post":""},
        "gpt4-pgm": {"path":"results/metric/chosen_fixset1_gpt4-pgm-vs-gpt4_as_chameleon", "post":""},
        "llama-pgm": {"path":"results/metric/chosen_fixset1_llama-pgm-vs-gpt4_as_chameleon", "post":""},
    },

    "non-undercover":{
        "gpt3.5": {"path":"results/undercover/gpt3.5-non-undercover_vs_gpt4", "post":""},
        "gpt4": {"path":"results/undercover/gpt4-non-undercover_vs_gpt4", "post":""},
        # "gpt4": {"path":"results/game_results/fix_set2_undercover_gpt4-non-undercover_vs_gpt4", "post":"-tp0"},
        "llama": {"path":"results/undercover/llama-non-undercover_vs_gpt4", "post":"-1"},
        "gpt3.5-pgm": {"path":"results/undercover/gpt3.5-pgm-non-undercover_vs_gpt4", "post":"-2"},
        "gpt4-pgm": {"path":"results/undercover/gpt4-pgm-non-undercover_vs_gpt4", "post":"-demo-dense-1"},
        "llama-pgm": {"path":"results/undercover/llama-pgm-non-undercover_vs_gpt4", "post":""},
    },
    "undercover":{
        "gpt3.5": {"path":"results/undercover/gpt3.5-undercover_vs_gpt4", "post":""},
        "gpt4": {"path":"results/undercover/gpt4-undercover_vs_gpt4", "post":""},
        "llama": {"path":"results/undercover/llama-undercover_vs_gpt4", "post":"-1"},
        "gpt3.5-pgm": {"path":"results/undercover/gpt3.5-pgm-undercover_vs_gpt4", "post":""},
        "gpt4-pgm": {"path":"results/undercover/gpt4-pgm-undercover_vs_gpt4", "post":"-demo-dense"},
        "llama-pgm": {"path":"results/undercover/llama-pgm-undercover_vs_gpt4", "post":""},
    },
    "prisoner":{
        "gpt3.5": {"path":"results/prisoner/gpt3.5-vs-gpt4_as_test_player", "post":"-1"},
        "gpt4": {"path":"results/prisoner/gpt4-vs-gpt4_as_test_player", "post":""},
        "llama": {"path":"results/prisoner/llama-vs-gpt4_as_test_player", "post":"-1"},
        "gpt3.5-pgm": {"path":"results/prisoner/gpt3.5-pgm-vs-gpt4_as_test_player", "post":"-2"},
        "gpt4-pgm": {"path":"results/prisoner/gpt4-pgm-vs-gpt4_as_test_player", "post":"-2"},
        "llama-pgm": {"path":"results/prisoner/gpt3.5-pgm-vs-gpt4_as_test_player", "post":"-2"},
    },
    "public_good":{
        "gpt3.5": {"path":"results/public_good/gpt3.5-vs-gpt4_as_test_player", "post":""},
        "gpt4": {"path":"results/public_good/gpt4-vs-gpt4_as_test_player", "post":""},
        "llama": {"path":"results/public_good/llama-vs-gpt4_as_test_player", "post":""},
        "gpt3.5-pgm": {"path":"results/public_good/gpt3.5-pgm-vs-gpt4_as_test_player", "post":"-2"},
        "gpt4-pgm": {"path":"results/public_good/gpt4-pgm-vs-gpt4_as_test_player", "post":"-2"},
        "llama-pgm": {"path":"results/public_good/gpt3.5-pgm-vs-gpt4_as_test_player", "post":"-2"},
    },
    "airport":{
        "gpt3.5": {"path":"results/airportfee/gpt3.5-vs-gpt4_as_test_player", "post":"-fix-p"},
        "gpt4": {"path":"results/airportfee/gpt4-vs-gpt4_as_test_player", "post":"-fix-p"},
        "llama": {"path":"results/airportfee/llama-vs-gpt4_as_test_player", "post":"-fix-1"},
        "gpt3.5-pgm": {"path":"results/airportfee/gpt3.5-pgm-vs-gpt4_as_test_player", "post":"-fix-p"},
        "gpt4-pgm": {"path":"results/airportfee/gpt4-pgm-vs-gpt4_as_test_player", "post":"-fix-p-2"},
        "llama-pgm": {"path":"results/airportfee/llama-pgm-vs-gpt4_as_test_player", "post":"-fix-p"},
    }
    
    

}

# result_path = ["results/game_results/chosen_fixset1_llama-vs-gpt4_as_chameleon","results/game_results/fix_set2_undercover_llama-undercover_vs_gpt4"]

# result_path = ["results/game_results/chosen_fixset1_llama-pgm-vs-gpt4_as_non-chameleon","results/game_results/fix_set2_undercover_llama-pgm-non-undercover_vs_gpt4"]
# result_path = ["results/game_results/chosen_fixset1_gpt4-pgm-vs-gpt4_as_chameleon","results/game_results/fix_set2_undercover_gpt4-pgm-undercover_vs_gpt4"]
# result_path = ["results/game_results/chosen_fixset1_llama-vs-gpt4_as_chameleon","results/game_results/fix_set2_undercover_llama-undercover_vs_gpt4"]

models = list(model_results["chameleon"].keys())
"Judgement"
print("=============Judgement===========")
for model in models:
    result_path = [model_results["non-chameleon"][model]["path"],model_results["non-undercover"][model]["path"]]
    postfix = [model_results["non-chameleon"][model]["post"],model_results["non-undercover"][model]["post"]]
    judge(result_path, postfix)
print("=============Deception===========")
for model in models:
    result_path = [model_results["chameleon"][model]["path"],model_results["undercover"][model]["path"]]
    postfix = [model_results["chameleon"][model]["post"],model_results["undercover"][model]["post"]]
    decept(result_path, postfix)
print("=============Conistency and Reasoning===========")
for model in models:
    result_path = [model_results["chameleon_metric"][model]["path"],model_results["undercover"][model]["path"],model_results["non-chameleon_metric"][model]["path"],model_results["non-undercover"][model]["path"]]
    postfix = [model_results["chameleon_metric"][model]["post"],model_results["undercover"][model]["post"],model_results["non-chameleon_metric"][model]["post"],model_results["non-undercover"][model]["post"]]
    consist_pgm(result_path, postfix)
print("=============Collaboration===========")
for model in models:
    result_path = [model_results["airport"][model]["path"]]
    postfix = [model_results["airport"][model]["post"]]
    collabration(result_path, postfix)
print("=============Rationality===========")
for model in models:
    result_path = [model_results["prisoner"][model]["path"],model_results["public_good"][model]["path"]]
    postfix = [model_results["prisoner"][model]["post"],model_results["public_good"][model]["post"]]
    rational(result_path, postfix)
exit()
