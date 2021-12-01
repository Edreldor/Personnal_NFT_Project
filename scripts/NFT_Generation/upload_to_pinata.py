import os
from os import listdir
from os.path import isfile, join
import sys
from pathlib import Path
import requests
from set_env_var import set_env_var

PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"

filepath = "import/placeholder.gif"

pinata_image_base_url = "https://gateway.pinata.cloud/ipfs/{}"


def main():
    if len(sys.argv) == 2:
        command = sys.argv[1]

        if command.lower() in ["-unpin", "-u"]:
            print("UNPINNING ALL FILES . . .")
            unpin_all()
        else:
            print("DID NOT RECOGNISE COMMAND")

    elif len(sys.argv) == 3:
        command = sys.argv[1]
        filepath = sys.argv[2]
        if command.lower() in ["-pin", "-p", "-pinfile"]:
            print(f"PINNING {filepath} . . .")
            link = upload_to_pinata(filepath)
            print(f"View file at: {link}")
    else:
        print("DID NOT RECOGNISE COMMAND")


def upload_to_pinata(_filepath):
    """
        Pin any file, or directory, to Pinata's IPFS nodes
        More: https://docs.pinata.cloud/api-pinning/pin-file
    """
    set_env_var()
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }
    current_working_dir = os.getcwd()

    def get_all_files(dir: str):
        """get a list of absolute paths and relative paths to every file located in the directory"""
        abspaths, relativepaths, filenames = [], [], []
        dirname = _filepath.split("/")[-1:][0]
        for root, dirs, files_ in os.walk(os.path.abspath(dir)):
            for file in files_:
                abspaths.append(os.path.join(root, file))
                relativepaths.append(dirname + "/" + file)
                filenames.append(file)
        return abspaths, relativepaths, filenames

    if os.path.isdir(_filepath):
        all_files_abs, all_files_rel, filenames = get_all_files(_filepath)
        os.chdir(Path(_filepath).parent)
        print("STARTING UPLOADING ALL FILES IN FOLDER . . .")
        files = [("file", (all_files_rel[i], open(all_files_abs[i], "rb")))
                 for i in range(len(all_files_abs))]
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files=files,
            headers=headers,
        )
    else:
        filename = _filepath.split("/")[-1:][0]
        files = {"file": (filename, open(_filepath, 'rb'))}

    response = requests.post(
        PINATA_BASE_URL + endpoint,
        files=files,
        headers=headers,
    )
    os.chdir(current_working_dir)
    return(pinata_image_base_url.format(response.json()["IpfsHash"]))


def unpin_all():
    set_env_var()
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }
    pinList_endpoint = "data/pinList?status=pinned&pageLimit=1000"
    unpin_endpoint = "pinning/unpin/{}"

    # First, get the list of All pinned files
    print(f"Sending request to {PINATA_BASE_URL + pinList_endpoint}")
    response = requests.get(
        PINATA_BASE_URL + pinList_endpoint,
        headers=headers,
    )
    response = response.json()
    number_pinned = response["count"]
    list_hash_pinned = []
    print(f"START UNPINNING {number_pinned} FILES. . .")
    row_number = len(response["rows"])
    print(f"number of rows: {row_number}")
    for i in range(row_number):
        hash = response["rows"][i]["ipfs_pin_hash"]
        list_hash_pinned.append(hash)
        link_to_pinned_file = PINATA_BASE_URL + unpin_endpoint.format(hash)
        print(f"row {i} multi-hash: {hash}")
        unpin_response = requests.delete(
            link_to_pinned_file,
            headers=headers
        )
        print(f"File {i}: {unpin_response}")


def pin_dir_to_pinata(dirPath):
    set_env_var()
    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }

    dirname = dirPath.split("/")[-1:][0]
    os.chdir(Path(dirPath).parent)
    print(os.getcwd())

    onlyfiles = [join(dirname, f)
                 for f in listdir(dirname) if isfile(join(dirname, f))]
    print(onlyfiles)
    data = []
    for file in onlyfiles:
        with Path(file).open("rb") as f:
            binary = f.read()
            data.append((file, binary))
    files = {"file": [(file, open(file, 'rb')) for file in onlyfiles]}
    response = requests.post(
        PINATA_BASE_URL + endpoint,
        files=files,
        headers=headers,
    )
    return(pinata_image_base_url.format(response.json()["IpfsHash"]))


if __name__ == "__main__":
    main()
