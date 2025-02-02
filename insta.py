#!/usr/bin/env python3

import csv
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_text_size(text, draw, font):
    """
    Ermittelt Textbreite und -höhe anhand von textbbox(...).
    Damit umgehst du die ggf. fehlende draw.textsize(...) bei älteren Pillow-Versionen.
    """
    bbox = draw.textbbox((0, 0), text, font=font)  # (left, top, right, bottom)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    return w, h

def wrap_text(text, draw, font, max_width):
    """
    Teilt den Text in mehrere Zeilen auf, sodass keine Zeile breiter als max_width ist.
    Gibt eine Liste von Zeilen zurück.
    """
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = (current_line + " " + word).strip()
        w, _ = get_text_size(test_line, draw, font)
        if w <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def main():
    # CSV-Datei
    input_csv = "input.csv"

    # Hintergrundbilder 1024×1024
    background_images = [
        "background1.png",
        "background2.png",
        "background3.png",
        "background4.png",
        "background5.png"
    ]

    # Schrift-Parameter
    font_path = "Arial.ttf"  # Anpassen an deinen Font
    font_size = 42
    text_color = (255, 255, 255)  # Weiß

    # Bildbreite/Höhe
    image_size = (1024, 1024)

    # Rand zum Bildrand
    margin = 100
    max_text_width = image_size[0] - 2 * margin

    # Zusätzlicher Zeilenabstand
    line_spacing = 10

    # Öffne CSV
    with open(input_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")

        for row in reader:
            spruch_nr = row["Spruch Nr."].strip()
            spruch = row["Spruch"].strip()

            # Zufälliges Hintergrundbild
            chosen_bg = random.choice(background_images)

            # Hintergrundbild laden, in RGBA konvertieren
            background = Image.open(chosen_bg).convert("RGBA")
            draw = ImageDraw.Draw(background)

            # Font laden
            font = ImageFont.truetype(font_path, font_size)

            # Text umbrechen
            lines = wrap_text(spruch, draw, font, max_text_width)

            # Gesamtbreite/-höhe des Textblocks berechnen
            max_line_width = 0
            total_text_height = 0
            for line in lines:
                w, h = get_text_size(line, draw, font)
                if w > max_line_width:
                    max_line_width = w
                total_text_height += h
            total_text_height += line_spacing * (len(lines) - 1)

            bg_width, bg_height = background.size

            # Position des Textblocks (zentriert)
            text_block_x = (bg_width - max_line_width) / 2
            text_block_y = (bg_height - total_text_height) / 2

            # --- Koordinaten für den Blur-Bereich ---
            padding = 20
            box_left = int(text_block_x - padding)
            box_top = int(text_block_y - padding)
            box_right = int(text_block_x + max_line_width + padding)
            box_bottom = int(text_block_y + total_text_height + padding)

            # --- Den Bereich aus dem Hintergrundbild ausschneiden ---
            blur_region = background.crop((box_left, box_top, box_right, box_bottom))

            # --- Weichzeichnen (GaussianBlur) ---
            blur_radius = 15  # Anpassen für stärkere/weichere Unschärfe
            blur_region = blur_region.filter(ImageFilter.GaussianBlur(blur_radius))

            # --- Den verschwommenen Bereich zurück auf das Originalbild setzen ---
            background.paste(blur_region, (box_left, box_top))

            # --- Text zeichnen ---
            current_y = text_block_y
            for line in lines:
                w, h = get_text_size(line, draw, font)
                line_x = (bg_width - w) / 2
                draw.text((line_x, current_y), line, font=font, fill=text_color)
                current_y += h + line_spacing

            # Vor dem Speichern in RGB konvertieren, um Transparenz zu entfernen
            background = background.convert("RGB")

            # Ausgabedatei
            output_filename = f"output_{spruch_nr}.png"
            background.save(output_filename)
            print(f"Erstellt: {output_filename} (Hintergrund: {chosen_bg})")

if __name__ == "__main__":
    main()