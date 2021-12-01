from pathlib import Path
import os
import time
from PIL import Image

CURRENT_DIR = Path(os.getcwd())
IMPORT_DIR = CURRENT_DIR / "import"
EXPORT_DIR = CURRENT_DIR / "export"


def get_image(img_id, category):
    list_mendatory = ["BACKGROUND_COLOR", "SKIN", "EYES"]
    if category not in list_mendatory and img_id == "00":
        return None
    else:
        img = Image.open(
            IMPORT_DIR / category / (img_id + ".png"))
        return img


def get_image_from_name(id_name, size=(1024, 1024)):
    background_color_id = id_name[0]
    pattern_id = id_name[1: 3]
    skin_id = id_name[3: 5]
    back_id = id_name[5: 7]
    eyes_id = id_name[7: 9]
    hat_id = id_name[9: 11]
    bottom_id = id_name[11: 13]

    background_color_img = get_image(
        background_color_id, "BACKGROUND_COLOR")
    pattern_img = get_image(
        pattern_id, "PATTERN")
    skin_img = get_image(
        skin_id, "SKIN")
    back_img = get_image(
        back_id, "BACK")
    eyes_img = get_image(
        eyes_id, "EYES")
    hat_img = get_image(
        hat_id, "HAT")
    bottom_img = get_image(
        bottom_id, "BOTTOM")

    final_img = assemble_nft(background_color_img, skin_img,
                             eyes_img, pattern_img, back_img, hat_img, bottom_img, size=size)

    return final_img


def assemble_nft(background_color_img, skin_img, eyes_img, pattern_img=None, back_img=None, hat_img=None, bottom_img=None, size=(2048, 2048)):
    new_img = background_color_img.copy()
    if pattern_img != None:
        new_img.paste(pattern_img, (0, 0), pattern_img)
    new_img.paste(skin_img, (0, 0), skin_img)
    new_img.paste(eyes_img, (0, 0), eyes_img)
    if back_img != None:
        new_img.paste(back_img, (0, 0), back_img)
    if hat_img != None:
        new_img.paste(hat_img, (0, 0), hat_img)
    if bottom_img != None:
        new_img.paste(bottom_img, (0, 0), bottom_img)
    if size != (2048, 2048):
        return new_img.convert('RGB').resize(size)
    else:
        return new_img.convert('RGB')


def create_all_img_and_save(list_all, size=(512, 512), save=False):
    t0 = time.time()
    t_0 = t0
    print("")
    print("STARTING IMAGE GENERATION . . .")
    print("")
    for i in range(len(list_all)):
        id_nft = str(i).zfill(4)
        img = get_image_from_name(list_all[i], size=size)
        t1 = time.time()
        print(f"Image {id_nft} created in {t1-t0} sec.")
        if save:
            img.save(EXPORT_DIR / "img" / (id_nft + '.png'))
            t2 = time.time()
            print(f"Saved in {t2-t1} sec.")
            t0 = t2
        else:
            img.show()
            t0 = t1
        print("")
    print(f"GENERATION FINISHED IN {t0-t_0} sec.")


if __name__ == "__main__":
    print(IMPORT_DIR)
    print(EXPORT_DIR)
    create_all_img_and_save(
        ["0000000000000", "1010101010101"], size=(1024, 1024), save=True)
