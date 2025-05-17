from instagrapi import Client
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv("SECRET.env")

username = os.getenv("IG_USERNAME")
password = os.getenv("IG_PASSWORD")

# Login
cl = Client()
cl.login(username, password)

# Pfad zum Bilderordner
images_folder = os.path.dirname(os.path.abspath(__file__))
posted_log = "posted.txt"

# Stelle sicher, dass du keine doppelten Bilder postest
if not os.path.exists(posted_log):
    with open(posted_log, "w") as f:
        pass

with open(posted_log, "r") as f:
    posted = f.read().splitlines()

# Finde das nächste Bild, das noch nicht gepostet wurde
for img in sorted(os.listdir(images_folder)):
    if img.startswith("output_") and img.lower().endswith((".jpg", ".jpeg", ".png")) and img not in posted:
        image_path = os.path.join(images_folder, img)
        cl.photo_upload(image_path, caption=f"Jeder Schritt, jeder Griff bringt dich näher an dein Ziel nicht nur am Fels, sondern auch im Leben. Geh raus, atme tief durch, wachse über dich hinaus. #Wandern #Klettern #Motivation #ClimbingLife")
        with open(posted_log, "a") as f:
            f.write(img + "\n")
        break