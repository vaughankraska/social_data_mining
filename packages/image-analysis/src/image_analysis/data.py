import os
from PIL import Image
from typing import List
from sqlite3 import Connection
import pandas as pd


def get_images_dataframe(db: Connection) -> pd.DataFrame:
    cur = db.cursor()
    res = cur.execute("""
        SELECT
            a.author_id AS account_id,
            t.attachments AS image_id,
            a.account_type,
            a.lang,
            a.stance
        FROM
            accounts a
        JOIN
            tweets t
        ON
            a.author_id = t.author_id
        WHERE
            a.account_type IN ("Private individuals", "Business actors")
    """).fetchall()   # Since it"s images, have removed the english filter a.lang = "en"

    return pd.DataFrame(res)


def get_image(image_path: str) -> Image.Image:
    if os.path.exists(image_path):
        img = Image.open(image_path)
        return img
    else:
        raise FileNotFoundError(f"File {image_path} not found.")


def get_images(
        media_keys: List[str],
        media_dir: str = "./data/media"
        ) -> List[Image.Image]:
    images = []

    if not os.path.exists(media_dir):
        raise FileNotFoundError(f"The directory '{media_dir}' does not exist.")
    possible_extensions = [".jpg", ".png"]

    for key in media_keys:
        found = False
        for ext in possible_extensions:
            image_path = os.path.join(media_dir, f"{key}{ext}")
            try:
                img = get_image(image_path)
                images.append(img)
                found = True
                break
            except Exception as e:
                print(f"[!] Failed to get image file: {e}")
        if not found:
            print(f"[*] No image file found for key '{key}' in directory '{media_dir}'.")

    return images
