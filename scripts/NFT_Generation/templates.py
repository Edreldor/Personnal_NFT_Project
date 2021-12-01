DUMMY_METADATA_TEMPLATE = {
    "name": "",
    "id": "",
    "description": "Friggin Eggs are 7,777 randomly generated NFTs. Eggs owners are part of our mission to explore how food will be included in the metaverse. More info on our website https://friggineggs.com",
    "image": "",
    "Website image": "",
}

METADATA_TEMPLATE = {
    "name": "",
    "id": "",
    "description": "Friggin Eggs are 7,777 randomly generated NFTs. Eggs owners are part of our mission to explore how food will be included in the metaverse. More info on our website https://friggineggs.com",

    "image": "",
    "Website image": "",

    "attributes": [
          {"trait_type": "Passive Income", "value": ""},
        {"trait_type": "Background Color", "value": ""},
        {"trait_type": "Background Pattern", "value": ""},
        {"trait_type": "Skin", "value": ""},
        {"trait_type": "Back", "value": ""},
        {"trait_type": "Eyes", "value": ""},
        {"trait_type": "Hat", "value": ""},
        {"trait_type": "Bottom", "value": ""},
        {"trait_type": "Tier", "value": ""},

        {"trait_type": "Egg Score",  "max_value": 16, "value": 0},
        {"trait_type": "Pattern Score",  "max_value": 10, "value": 0},
        {"trait_type": "Skin Score",  "max_value": 4, "value": 0},


        {"trait_type": "Back Score",  "max_value": 4, "value": 0},
        {"trait_type": "Eyes Score",  "max_value": 4, "value": 0},
        {"trait_type": "Hat Score",  "max_value": 4, "value": 0},
        {"trait_type": "Bottom Score",  "max_value": 4, "value": 0},
    ]
}

# ID: ["NAME", QUANTITY]
color_dict = {
    "0": ["Grey", 0],
    "1": ["Green", 0],
    "2": ["Turquoise", 0],
    "3": ["Blue", 0],
    "4": ["Purple", 0],
    "5": ["Red", 0],
    "6": ["Orange", 0],
    "7": ["Yellow", 0]
}

# ID: ["NAME", SCORE, QUANTITY]
pattern_dict = {
    "00": ["Empty", 0, 0],
    "01": ["Stripes", 1, 0],
    "02": ["Clouds", 2, 0],
    "03": ["Voronoi", 3, 0],
    "04": ["Binary", 4, 0],
    "05": ["Tada", 5, 0],
    "06": ["Mesh", 6, 0],
    "07": ["Pump", 7, 0],
    "08": ["Spiral", 8, 0],
    "09": ["Echo", 9, 0],
    "10": ["ETH Bills", 10, 0]
}

# ID: ["NAME", SCORE, QUANTITY]
skin_dict = {
    "00": ["Regular Egg", 1, 0],
    "01": ["Brown Egg", 2, 0],
    "02": ["White Egg", 3, 0],
    "03": ["Quail Egg", 4, 0]
}

# ID: ["NAME", SCORE, QUANTITY]
eyes_dict = {
    "00": ["Swag Glasses", 1, 0],
    "01": ["Yellow Striped Glasses", 1, 0],
    "02": ["Blue Striped Glasses", 1, 0],
    "03": ["Goggles", 1, 0],
    "04": ["Masquerade Mask", 1, 0],
    "05": ["Snorkle", 1, 0],
    "06": ["VR Set", 1, 0],
    "07": ["Star Glasses", 2, 0],
    "08": ["Sunglasses", 2, 0],
    "09": ["Elaborate Masquerade Mask", 2, 0],
    "10": ["Harry Potter Glasses", 2, 0],
    "11": ["DBZ Detector", 2, 0],
    "12": ["Night Vision Goggles", 2, 0],
    "13": ["Heart Glasses", 3, 0],
    "14": ["Happy Face Mask", 3, 0],
    "15": ["Sad Face Mask", 3, 0],
    "16": ["Crying holes", 3, 0],
    "17": ["3D Glasses", 4, 0],
    "18": ["XX", 4, 0],
    "19": ["Mystery Eyes", 4, 0]
}

# ID: ["NAME", SCORE, QUANTITY]
bottom_dict = {
    "00": ["Empty", 0, 0],
    "01": ["Cigarette", 1, 0],
    "02": ["Pillow", 1, 0],
    "03": ["Tube", 1, 0],
    "04": ["Blue Tie", 1, 0],
    "05": ["Pacifier", 1, 0],
    "06": ["Pipe", 1, 0],
    "07": ["Hay", 1, 0],
    "08": ["Harry Potter Scarf", 2, 0],
    "09": ["DBZ Cloud", 2, 0],
    "10": ["Car", 2, 0],
    "11": ["UFO", 2, 0],
    "12": ["Plane", 2, 0],
    "13": ["Mustache", 3, 0],
    "14": ["Pig Nose", 3, 0],
    "15": ["Cup", 3, 0],
    "16": ["Ice cream Stick", 3, 0],
    "17": ["Chicken Feet", 4, 0],
    "18": ["Broken Egg", 4, 0],
    "19": ["Duck Beak", 4, 0]
}

# ID: ["NAME", SCORE, QUANTITY]
back_dict = {
    "00": ["Empty", 0, 0],
    "01": ["Green Shell", 1, 0],
    "02": ["Blue Shell", 1, 0],
    "03": ["Nail", 1, 0],
    "04": ["Red Button", 1, 0],
    "05": ["Lever", 1, 0],
    "06": ["Bandage", 1, 0],
    "07": ["Monkey Tail", 1, 0],
    "08": ["Green Spiked Shell", 2, 0],
    "09": ["Blue Spiked Shell", 2, 0],
    "10": ["Plug Tail", 2, 0],
    "11": ["Worm", 2, 0],
    "12": ["Tissue", 2, 0],
    "13": ["Shuriken", 2, 0],
    "14": ["Angel Wings", 3, 0],
    "15": ["Devil Tail", 3, 0],
    "16": ["Rocket", 3, 0],
    "17": ["Help Pannel", 3, 0],
    "18": ["Lucky 4-Leaf Clover", 4, 0],
    "19": ["Dart", 4, 0],
    "20": ["Chicken Wings", 4, 0]
}

# ID: ["NAME", SCORE, QUANTITY]
hat_dict = {
    "00": ["Empty", 0, 0],
    "01": ["Red Cap", 1, 0],
    "02": ["Blue Cap", 1, 0],
    "03": ["Soldier Beret", 1, 0],
    "04": ["Cowboy Hat", 1, 0],
    "05": ["Chef Hat", 1, 0],
    "06": ["Ribbon", 1, 0],
    "07": ["Bunny Hat", 1, 0],
    "08": ["Pink Flower", 1, 0],
    "09": ["Blue Beret", 1, 0],
    "10": ["Red Beer Cap", 2, 0],
    "11": ["Blue Beer Cap", 2, 0],
    "12": ["Viking Helmet", 2, 0],
    "13": ["Axe", 2, 0],
    "14": ["Sword", 2, 0],
    "15": ["Harry Potter Hat", 2, 0],
    "16": ["Aureole", 3, 0],
    "17": ["Devil Horns", 3, 0],
    "18": ["Arrow In Apple", 3, 0],
    "19": ["Mario Crown", 3, 0],
    "20": ["Panties", 4, 0],
    "21": ["Duck Toy", 4, 0],
    "22": ["Chicken Comb", 4, 0]
}

# SCORE: ["TIER", "background_color_id", QUANTITY]
TIERS = {
    1: ["", "", 0],
    2: ["", "", 0],
    3: ["Just an Egg", "0", 0],
    4: ["Just an Egg", "0", 0],
    5: ["Cool Egg", "1", 0],
    6: ["Cool Egg", "1", 0],
    7: ["Eggcelent Egg", "2", 0],
    8: ["Eggcelent Egg", "2", 0],
    9: ["Dope Egg", "3", 0],
    10: ["Dope Egg", "3", 0],
    11: ["Super Dope Egg", "4", 0],
    12: ["Super Dope Egg", "4", 0],
    13: ["Friggin Egg", "5", 0],
    14: ["Friggin Egg", "5", 0],
    15: ["Fuckin Friggin Egg", "6", 0],
    16: ["Motha Fuckin Friggin Egg", "7", 0]
}

# NFT SCORE: NUMBER OF NFT OF THE CORRESPONDING RAIRTY TO BE CREATED
RARITY_CURVE_FINAL = {
    0: 0,
    1: 0,
    2: 0,      # MAX = 184
    3: 600,    # MAX = 1400
    4: 1450,   # MAX = 3528
    5: 1700,   # MAX = 12870
    6: 1400,   # MAX = 12354
    7: 1000,   # MAX = 5832
    8: 587,    # MAX = 19890
    9: 370,    # MAX = 11700
    10: 210,   # MAX = 5152
    11: 150,   # MAX = 15810
    12: 110,   # MAX = 8770
    13: 85,    # MAX = 4080
    14: 60,    # MAX = 1480
    15: 35,    # MAX = 432
    16: 20     # MAX = 81
}

RARITY_CURVE = {
    0: 0,
    1: 0,
    2: 0,       # MAX = 184
    3: 1,       # MAX = 1400
    4: 1,       # MAX = 3528
    5: 1,       # MAX = 12870
    6: 1,       # MAX = 12354
    7: 1,       # MAX = 5832
    8: 5,       # MAX = 19890
    9: 3,       # MAX = 11700
    10: 2,      # MAX = 5152
    11: 1,      # MAX = 15810
    12: 1,      # MAX = 8770
    13: 8,      # MAX = 4080
    14: 6,      # MAX = 1480
    15: 3,      # MAX = 432
    16: 2       # MAX = 81
}

# FEATURE NAME: corresponding dic = ID: ["NAME", SCORE, QUANTITY]
NFT_FEATURES = {
    "BACKGROUND_COLOR": color_dict,
    "PATTERN": pattern_dict,
    "SKIN": skin_dict,
    "BACK": back_dict,
    "EYES": eyes_dict,
    "HAT": hat_dict,
    "BOTTOM": bottom_dict
}
