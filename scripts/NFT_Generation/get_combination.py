import random
import numpy as np
from templates import RARITY_CURVE, NFT_FEATURES, TIERS


def from_dict_to_list_id_score(dic):
    """
    Input:
        - dic: dict type -> "id" : ("feature name", score, number of time used (initially 0))

    Output:
        - list_id_score: list type -> [("id", score), . . .]
    """
    list_id_score = []
    for id in dic:
        list_id_score.append((id, dic[id][1]))
    return list_id_score


def get_combination(lst1, lst2, lst3, lst4, n, target):
    """
    get n unique combinations of features in the 4 lists so that the total score == target

    Inputs:
        - lst1: list -> [("id", score), . . .]
        - lst2: list -> [("id", score), . . .]
        - lst3: list -> [("id", score), . . .]
        - lst4: list -> [("id", score), . . .]
    Output:
        - res: return the list of unique combination
    """
    def get_combinations(candidates):
        res = []

        def fn(arr, start):
            s = sum(arr)

            if target <= 4 and len(arr) >= 1:
                if arr[-1] == 2:
                    return

            if target <= 10 and len(arr) >= 1:
                if arr[-1] == 4:
                    return

            if target <= 6 and len(arr) >= 1:
                if arr[-1] == 3:
                    return

            if s == target and len(arr) == len(candidates):
                res.append(arr[:])
                return
            if s > target:
                return

            if start >= len(candidates):
                return

            for i in range(len(candidates[start])):
                arr.append(candidates[start][i])
                fn(arr, start+1)
                arr.pop()

        fn([], 0)
        return res

    tmp1 = {}
    tmp2 = {}
    tmp3 = {}
    tmp4 = {}

    for ch, v in lst1:
        tmp1.setdefault(v, []).append(ch)
    for ch, v in lst2:
        tmp2.setdefault(v, []).append(ch)
    for ch, v in lst3:
        tmp3.setdefault(v, []).append(ch)
    for ch, v in lst4:
        tmp4.setdefault(v, []).append(ch)

    candidates = []
    candidates.append(list(tmp1))
    candidates.append(list(tmp2))
    candidates.append(list(tmp3))
    candidates.append(list(tmp4))

    all_comb = get_combinations(candidates)

    res = []
    for _ in range(n):
        while True:
            s = ""
            comb = random.choice(all_comb)
            j = 1
            for v in comb:
                if j == 1:
                    s += random.choice(tmp1[v])
                elif j == 2:
                    s += random.choice(tmp2[v])
                elif j == 3:
                    s += random.choice(tmp3[v])
                elif j == 4:
                    s += random.choice(tmp4[v])
                j += 1
            if s not in res:
                res.append(s)
                break
    return res


def get_skin():
    """
    The skin rarity system is not linked to the main system here
    """
    return(np.random.choice(
        ['00', '01', '02', '03'],
        1,
        p=[0.5, 0.3, 0.15, 0.05]
    )[0])


def get_score_with_name(name):
    bck = name[2:4]
    eyes = name[4:6]
    hat = name[6:8]
    bottom = name[8:10]

    score_bck = NFT_FEATURES["BACK"][bck][1]
    score_eyes = NFT_FEATURES["EYES"][eyes][1]
    score_hat = NFT_FEATURES["HAT"][hat][1]
    score_bottom = NFT_FEATURES["BOTTOM"][bottom][1]

    score_total = score_bck + score_eyes + score_hat + score_bottom

    return score_total


def get_pattern(flat_list):
    random.shuffle(flat_list)

    best_pattern_list = flat_list[0:20]
    others = flat_list[20:]

    for i in range(len(best_pattern_list)):
        best_pattern_list[i] = best_pattern_list[i][0] + \
            "10" + best_pattern_list[i][1:]

    for i in range(len(others)):
        pattern = np.random.choice(
            ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09'],
            1,
            p=[0.7, 0.085, 0.06, 0.045, 0.035, 0.025, 0.02, 0.015, 0.01, 0.005]
        )[0]
        others[i] = others[i][0] + \
            pattern + others[i][1:]

    flat_list = np.concatenate((best_pattern_list, others)).tolist()
    random.shuffle(flat_list)
    return(flat_list)


def get_background_color_id(score):
    return(TIERS[score][1])


def extend_list_all(list_all):
    """
    Return a flat array of the id names shuffles:
    ["name1", "name2", . . .]

    with the namme formated like so:
        "ABBCCDDEEFFGG"

        - A -> id of background color
        - BB -> id of pattern
        - CC -> id of skin
        - DD -> id of back
        - EE -> id of eyes
        - FF -> id of hat
        - GG -> id of bottom

    For this project, with the corresponding rarity curve, the list return should be of length 7777
    """
    # flatten the list and get background color according to the rarity, and the skin
    list_all_extended = []
    for i in range(len(list_all)):
        for j in range(len(list_all[i])):
            list_all_extended.append(
                get_background_color_id(i) + get_skin() + list_all[i][j])
    list_all_extended = get_pattern(list_all_extended)
    return list_all_extended


def get_final_combinations():
    """
    Return a list of all combination according to the chosen rarity curve,
    according to these different dict (in templates.py):
        - "BACK": back_dict,
        - "EYES": eyes_dict,
        - "HAT": hat_dict,
        - "BOTTOM": bottom_dict
        - RARITY_CURVE
    """
    list_all = []

    # For compatibility with the get_combination function
    BCK = from_dict_to_list_id_score(NFT_FEATURES["BACK"])
    EYES = from_dict_to_list_id_score(NFT_FEATURES["EYES"])
    HAT = from_dict_to_list_id_score(NFT_FEATURES["HAT"])
    BOT = from_dict_to_list_id_score(NFT_FEATURES["BOTTOM"])

    for i in range(17):
        if RARITY_CURVE[i] > 0:
            list_all.append(get_combination(
                BCK, EYES, HAT, BOT, n=RARITY_CURVE[i], target=i))
        else:
            list_all.append([])

    list_all = extend_list_all(list_all)

    # update the dict NFT_FEATURES to get the number of times each feature is being used
    for i in range(len(list_all)):
        # Background color doesn't have rarity score, so indice of quantity is 1 instead of 2
        NFT_FEATURES["BACKGROUND_COLOR"][list_all[i][0:1]][1] += 1
        NFT_FEATURES["PATTERN"][list_all[i][1:3]][2] += 1
        NFT_FEATURES["SKIN"][list_all[i][3:5]][2] += 1
        NFT_FEATURES["BACK"][list_all[i][5:7]][2] += 1
        NFT_FEATURES["EYES"][list_all[i][7:9]][2] += 1
        NFT_FEATURES["HAT"][list_all[i][9:11]][2] += 1
        NFT_FEATURES["BOTTOM"][list_all[i][11:13]][2] += 1

    return (NFT_FEATURES, list_all)


def display_preview(features):
    for categorie in features:
        print(f"CATEGORY: {categorie}")
        for id in features[categorie]:
            if categorie != "BACKGROUND_COLOR":
                print(f"Image {id} : {features[categorie][id][0]}")
                print(f" - - - - - Rarity score: {features[categorie][id][1]}")
                print(f" - - - - - Used {features[categorie][id][2]} times")
                print("")
            else:
                print(f"Background color {id} : {features[categorie][id][0]}")
                print(f" - - - - - Used {features[categorie][id][1]} times")
                print("")
        print("")
        print("")


if __name__ == "__main__":
    features, list_all = get_final_combinations()
    display_preview(features)
    print(f"-> Number of NFT to be created: {len(list_all)}")
