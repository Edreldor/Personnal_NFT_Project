from get_combination import get_final_combinations, display_preview
from create_img import create_all_img_and_save
from create_metadata import generate_dummies, generate_real_metadata
from upload_to_pinata import upload_to_pinata
import os.path
import os
import pickle
import time
import sys

FEATURE_FILE = "scripts/NFT_Generation/features.pkl"
LIST_ALL_FILE = "scripts/NFT_Generation/list_all.txt"
LIST_IMAGE_LINK_PINATA = "scripts/NFT_Generation/LIST_IMAGE_LINK_PINATA.txt"
LIST_IMAGE_LINK_WEBSITE = "scripts/NFT_Generation/LIST_IMAGE_LINK_WEBSITE.txt"

PLACEHOLDER_FILE = "import/placeholder.gif"

IMG_FILE_RAW = "export/img/{}.png"

DUMMY_METADATA_DIR = "export/dummies_metadata"
METADATA_DIR = "export/metadata"
IMG_DIR = "export/img"

WEBSITE_PLACEHOLDER = "https://friggineggs.com/data/placeholder/placeholder.gif"
WEBSITE_IMG_LINK_RAW = "https://friggineggs.com/data/nft/{}.png"


def generate_nft(features, list_all):
    display_preview(features)
    print(f"-> Number of NFT to be created: {len(list_all)}")
    print("")
    input("PRESS ENTER TO START GENERATING . . .")
    create_all_img_and_save(list_all, size=(512, 512), save=True)


def save_file(file, content):
    with open(file, 'wb') as f:
        pickle.dump(content, f)


def get_file(file):
    if os.path.exists(file):
        with open(file, 'rb') as f:
            loaded_content = pickle.load(f)
            return loaded_content
    return None


def erase_file(file):
    if os.path.exists(file):
        os.remove(file)


def delete_folder_content(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def reinitialise_all():
    erase_file(FEATURE_FILE)
    erase_file(LIST_ALL_FILE)
    erase_file(LIST_IMAGE_LINK_PINATA)
    delete_folder_content(DUMMY_METADATA_DIR)
    delete_folder_content(METADATA_DIR)
    delete_folder_content(IMG_DIR)


def start_generation(generate_img=True, reupload_to_pinata=True):
    if generate_img:
        reinitialise_all()
        features, list_all = get_final_combinations()
        generate_nft(features, list_all)

        # Save features into a local file
        save_file(FEATURE_FILE, features)

        # Save list_all into a local file
        save_file(LIST_ALL_FILE, list_all)

    features = get_file(FEATURE_FILE)
    list_all = get_file(LIST_ALL_FILE)
    list_pinata_link = get_file(LIST_IMAGE_LINK_PINATA)
    list_website_link = get_file(LIST_IMAGE_LINK_WEBSITE)

    # First Upload Dummy to pinata and create metadata, and upload those metadata to pinata
    print("uploading placeholder.gif to pinata . . .")
    t0 = time.time()
    placeholder_pinata_link = upload_to_pinata(PLACEHOLDER_FILE)
    print(f"DONE IN {time.time()-t0}SEC")
    generate_dummies(WEBSITE_PLACEHOLDER, placeholder_pinata_link, list_all)

    if list_pinata_link == None:
        list_pinata_link = []
    if list_website_link == None:
        list_website_link = []
    print("")
    print("uploading NFT images to pinata . . .")
    t0 = time.time()
    t_0 = t0
    # Allow to restart the uploading to pinata from where is stopped last time
    if reupload_to_pinata:
        start = 0
    else:
        start = len(list_pinata_link)
    for i in range(start, len(list_all)):
        name = str(i).zfill(4)
        list_pinata_link.append(upload_to_pinata(IMG_FILE_RAW.format(name)))
        list_website_link.append(WEBSITE_IMG_LINK_RAW.format(name))

        # Save the list of pinata and website links to save progression
        save_file(LIST_IMAGE_LINK_WEBSITE, list_website_link)
        save_file(LIST_IMAGE_LINK_PINATA, list_pinata_link)

        t1 = time.time()
        print(
            f"Image {name} uploaded at {list_pinata_link[-1]} in {t1-t0} sec")
        t0 = t1
    print(f"DONE IN {t0-t_0} SEC")

    generate_real_metadata(
        list_website_link, list_pinata_link, features, list_all)

    # Save the list of pinata and website links
    save_file(LIST_IMAGE_LINK_WEBSITE, list_website_link)
    save_file(LIST_IMAGE_LINK_PINATA, list_pinata_link)

    print("")
    print("ALL FILES SAVED.")

    print("")
    print("STARTING TO UPLOAD METADATA TO IPFS . . .")
    print("UPLOADING DUMMIES . . .")
    uri = upload_to_pinata(DUMMY_METADATA_DIR)
    print(f"DUMMIES FOLDER SUCCESFULLY UPLOADED AT {uri}")

    print("")
    print("UPLOADING REAL METADATA . . .")
    uri = upload_to_pinata(METADATA_DIR)
    print(f"REAL METADATA FOLDER SUCCESFULLY UPLOADED AT {uri}")

    print("")
    print("EVERYTHING IS DONE")


def main():
    if len(sys.argv) > 1:
        full_generation = sys.argv[1].lower() in ["false", "0", "n", "no"]
        full_generation = not full_generation
    else:
        full_generation = True
    if len(sys.argv) > 2:
        reupload_to_pinata = sys.argv[2].lower() in ["false", "0", "n", "no"]
        reupload_to_pinata = not reupload_to_pinata
    else:
        reupload_to_pinata = True
    print(f"FULL GENERATION: {full_generation}")
    print(f"REUPLOAD TO PINATA: {reupload_to_pinata}")
    input("PRESS ENTER TO CONTINUE . . .")
    start_generation(full_generation, reupload_to_pinata)


if __name__ == "__main__":
    main()
