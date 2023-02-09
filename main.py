import requests
from zipfile import ZipFile
import os

def main():
    # Get the user's API key. Ask for the key if existing key not found. Save it in a text file. DO NOT SHARE THE TEXT FILE!
    apikey = ""
    try:
        keyfile = open("apikey.txt", "rt")
    except FileNotFoundError as e:
        print("apikey.txt not found, creating")
        keyfile = open("apikey.txt", "tx")
        keyfile.close()
        print("Get your API key and paste it into apikey.txt, and run this script again\n"\
              "Link to get your API key:\nhttps://mod.io/me/access")
        return
    
    apikey = keyfile.read()
    keyfile.close()
    if len(apikey) == 0: 
        print("Invalid API key in apikey.txt")
        return
    print("API key read\n")

    # DRG mod.io page: https://mod.io/g/drg

    # Get the DRG game ID from the API in case it chances in the future
    rq = requests.get(
        "https://api.mod.io/v1/games?api_key={}".format(apikey)
        )
    if (not rq.ok):
        print("API request failed. Check your API key. Request status code", rq.status_code)
        return
    
    resp = rq.json()
    games = [x for x in resp["data"]]
    game_id = ""
    for x in games:
        if x["name_id"] == "drg":
            game_id = x["id"]
            print("DRG game ID found:", game_id)

    if (game_id == ""):
        print("DRG game ID not found. API response style has probably changed.")
        return

    # Ask for the mod ID
    while True:
        mod_id = input(
            "Give the ID of the mod here. The ID should look something like 2749417," \
            " and is found under Resource ID in the mod page." \
            " CTRL + C or empty input to stop.\n").strip()  # Remove whitespace
        if mod_id == "":
            return
        
        rq = requests.get(
            "https://api.mod.io/v1/games/{}/mods/{}?api_key={}".format(game_id, mod_id, apikey))
        if (not rq.ok):
            print("Mod fetching failed. Check the mod ID.")
            continue
        
        mod = rq.json()

        # Print direct download link
        dl_link = mod["modfile"]["download"]["binary_url"]
        mod_name = mod["name"]
        file_name = mod["modfile"]["filename"]
        print("Mod \"{}\" download link:\n{}\n".format(mod_name, dl_link))

        print("Downloading mod...")
        rq = requests.get(dl_link)
        if (not rq.ok):
            print("Failed to download")
            return
        if not os.path.exists("downloaded/"):  # Create "downloaded" directory
            os.mkdir("downloaded/")
        if not os.path.exists("temp/"):
            os.mkdir("temp/")
        with open("temp/{}".format(file_name), "w+b") as f:
            f.write(rq.content)

        print("Mod zip downloaded, extracting...")
        zf = ZipFile("temp/{}".format(file_name))
        zf.extractall("downloaded/")
        zf.close()

        print("Mod extracted, deleting zip...")
        os.remove("temp/{}".format(file_name))

        print("Done\n")


try:
    main()
except KeyboardInterrupt:
    pass
