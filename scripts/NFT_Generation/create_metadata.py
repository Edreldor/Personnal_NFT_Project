from templates import METADATA_TEMPLATE, DUMMY_METADATA_TEMPLATE, TIERS
import os
import json

dummy_metadata_dir = "export/dummies_metadata/"
metadata_dir = "export/metadata/"


def save_json(file, content):
    data_json = json.dumps(content)
    if os.path.exists(file):
        os.remove(file)
    with open(file, 'x') as f:
        f.write(data_json)


def get_score_with_name(name, features):
    bck = name[5:7]
    eyes = name[7:9]
    hat = name[9:11]
    bottom = name[11:13]

    score_bck = features["BACK"][bck][1]
    score_eyes = features["EYES"][eyes][1]
    score_hat = features["HAT"][hat][1]
    score_bottom = features["BOTTOM"][bottom][1]

    score_total = score_bck + score_eyes + score_hat + score_bottom

    return score_total


def generate_dummies(link_to_dummy, link_to_dummy_pinata, list_all):
    print("")
    print("STARTING THE GENERATION OF DUMMY METADATA . . .")
    metadata = DUMMY_METADATA_TEMPLATE
    metadata["image"] = link_to_dummy_pinata
    metadata["Website image"] = link_to_dummy
    for i in range(len(list_all)):
        metadata["name"] = f"FrigginEgg#{str(i+1).zfill(4)}"
        metadata["id"] = i
        save_json(dummy_metadata_dir + str(i) + ".json", metadata)
    print("DUMMY METADATAS SAVED.")


def generate_real_metadata(image_link_list, pinata_link_list, features, list_all):
    print("")
    print("STARTING THE GENERATION OF REAL METADATA . . .")
    metadata = METADATA_TEMPLATE
    for i in range(len(list_all)):
        metadata["name"] = f"FrigginEgg#{str(i+1).zfill(4)}"
        metadata["id"] = i
        metadata["image"] = pinata_link_list[i]
        metadata["Website image"] = image_link_list[i]

        # For passive income
        if features["PATTERN"][list_all[i][1:3]][1] == 10:
            metadata["attributes"][0]["value"] = True
        else:
            metadata["attributes"][0]["value"] = False

        # For the names:
        metadata["attributes"][1]["value"] = features["BACKGROUND_COLOR"][list_all[i][0]][0]
        metadata["attributes"][2]["value"] = features["PATTERN"][list_all[i][1:3]][0]
        metadata["attributes"][3]["value"] = features["SKIN"][list_all[i][3:5]][0]
        metadata["attributes"][4]["value"] = features["BACK"][list_all[i][5:7]][0]
        metadata["attributes"][5]["value"] = features["EYES"][list_all[i][7:9]][0]
        metadata["attributes"][6]["value"] = features["HAT"][list_all[i][9:11]][0]
        metadata["attributes"][7]["value"] = features["BOTTOM"][list_all[i][11:13]][0]
        score = get_score_with_name(list_all[i], features)
        metadata["attributes"][8]["value"] = TIERS[score][0]

        # For the scores:
        metadata["attributes"][9]["value"] = score
        metadata["attributes"][10]["value"] = features["PATTERN"][list_all[i][1:3]][1]
        metadata["attributes"][11]["value"] = features["SKIN"][list_all[i][3:5]][1]
        metadata["attributes"][12]["value"] = features["BACK"][list_all[i][5:7]][1]
        metadata["attributes"][13]["value"] = features["EYES"][list_all[i][7:9]][1]
        metadata["attributes"][14]["value"] = features["HAT"][list_all[i][9:11]][1]
        metadata["attributes"][15]["value"] = features["BOTTOM"][list_all[i][11:13]][1]

        save_json(metadata_dir + str(i) + ".json", metadata)
    print("REAL METADATAS SAVED.")
