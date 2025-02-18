import math
import os
import pandas as pd
import streamlit as st

from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
from typing import List, Dict, Any


st.set_page_config(
    page_title="Card Maker",
    page_icon="🃏",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "About": """### Card Maker 
    \nTemplate for cards for our family game.
    \n ---
    """
    },
) 


attack_folder = Path("docs/images/attacks")
attack_symb = [file.stem.capitalize() for file in attack_folder.iterdir() if file.is_file() and "rond_" not in file.name]

astro_folder = Path("docs/images/signes_astro")
signes_astro = [file.stem.capitalize() for file in astro_folder.iterdir() if file.is_file() and "astro" not in file.name]

def get_font(font_name:str, font_size: int, font_type:str = "R"):
    get_type = {
        "R" : "Regular",
        "B" : "Bold",
        "I" : "Italic",
        "BI" : "BoldItalic"
    }
    font_path = f"docs/font/{font_name}-{get_type[font_type]}.ttf"
    return ImageFont.truetype(font_path, font_size)

FONT_NAME = get_font("Athelas", 36, "B")
FONT_CARD_TEXT = get_font("Athelas", 32, "B")
FONT_CARD_TEXT_I = get_font("Athelas", 32, "BI")
FONT_CARD_QUOTE = get_font("Athelas", 20, "I")
FONT_CARD_SUBTITLE = get_font("OpenSans", 18, "R")
FONT_CATEGORY = get_font("Arimo", 14, "BI")

COPYRIGHT_TEXT = "©️2024 Momvembers"
FONT_COPYRIGHT = get_font("Athelas", 15, "R")

# 4 corners of illustration
X1, X2, Y1, Y2 = 39, 585, 86, 540
illustration_width = X2 - X1
illustration_height = Y2 - Y1

class Card:
    BASECARD = Image.open("docs/images/background.png")
    WIDTH, HEIGHT = BASECARD.size

    illustration_path = "docs/images/basic_illustration.PNG"
    zoom = 100
    horizon = 0
    vertical = 0
    name = "Carte"
    numero = 0
    type_bebe = ""
    taille = 0
    poids = 0
    category = "Novembabies"
    date_naissance = "01/01"
    signe_astro = signes_astro[0]
    attack_symbol = attack_symb[0]
    attack_text = ""
    attack_subtext = ""
    capacite_speciale_text = ""
    quote = ""

    def to_dict(self):
        return {
            "illustration_path": self.illustration_path,
            "zoom": self.zoom,
            "horizon": self.horizon,
            "vertical": self.vertical,
            "name": self.name,
            "numero": self.numero,
            "type_bebe": self.type_bebe,
            "taille": self.taille,
            "poids": self.poids,
            "category": self.category,
            "date_naissance": self.date_naissance,
            "signe_astro": self.signe_astro,
            "attack_symbol": self.attack_symbol,
            "attack_text": self.attack_text,
            "attack_subtext": self.attack_subtext,
            "capacite_speciale_text": self.capacite_speciale_text,
            "quote": self.quote,
        }

    def from_dict(self, data):
        self.illustration_path = data.get("illustration_path")
        self.zoom = data.get("zoom")
        self.horizon = data.get("horizon")
        self.vertical = data.get("vertical")
        self.name = data.get("name")
        self.numero = data.get("numero")
        self.type_bebe = data.get("type_bebe")
        self.taille = data.get("taille")
        self.poids = data.get("poids")
        self.category = data.get("category")
        self.date_naissance = data.get("date_naissance")
        self.signe_astro = data.get("signe_astro")
        self.attack_text = data.get("attack_text")
        self.attack_subtext = data.get("attack_subtext")
        self.attack_symbol = data.get("attack_symbol")
        self.capacite_speciale_text = data.get("capacite_speciale_text")
        self.quote = data.get("quote")


def csv_to_dict_list(uploaded_file) -> List[Dict[str, Any]]:
    """
    cols = maman,name,date_naissance,signe_astro,numero,taille,poids,type_bebe,
    attack_symbol,attack_text,attack_subtext,capacite_speciale,quote,category,zoom,horizon,vertical


    Convert a CSV file from Streamlit's file uploader into a list of dictionaries,
    sorted by the combination of 'maman' and 'prenom' values with an underscore between them.
    
    Parameters:
    -----------
    uploaded_file : UploadedFile
        The file object returned by st.file_uploader()
    
    Returns:
    --------
    List[Dict[str, Any]]
        A list where each item is a dictionary representing a row from the CSV,
        sorted by the combined maman_prenom value
    
    Example:
    --------
    >>> uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    >>> if uploaded_file is not None:
    >>>     data = csv_to_dict_list(uploaded_file)
    """
    try:
        # Read CSV file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Check if required columns exist
        if 'maman' in df.columns and 'name' in df.columns:
            # Create the combined column for sorting
            df['illustration_path'] = df['maman'].astype(str) + '_' + df['name'].astype(str) + ".jpg"
            
            df[["zoom"]] = df[["zoom"]].fillna(value=100).astype('int')
            df[["horizon", "vertical"]] = df[["horizon", "vertical"]].fillna(value=0).astype('int')
            df[["type_bebe"]] = df[["type_bebe"]].fillna(value="")
            df[["quote"]] = df[["quote"]].fillna(value="")
            df[["attack_symbol"]] = df[["attack_symbol"]].fillna(value="Rond1")

            # Sort DataFrame by the combined column
            df = df.sort_values(by='illustration_path')
            
            # Remove the temporary sorting column
            # df = df.drop('maman_prenom', axis=1)
        else:
            missing_cols = []
            if 'maman' not in df.columns:
                missing_cols.append('maman')
            if 'name' not in df.columns:
                missing_cols.append('name')
            st.warning(f"Columns {', '.join(missing_cols)} not found in CSV. Data will be returned unsorted.")
        
        # Convert DataFrame to list of dictionaries
        records = df.to_dict('records')
        
        return records
    
    except Exception as e:
        st.error(f"Error processing CSV file: {str(e)}")
        return []


def get_resized_dimensions(card_spec):
    illustration = Image.open(card_spec.illustration_path)
    width, height = illustration.size
    ratio = height / width

    if ratio > illustration_height / illustration_width :
        # largeur au moins de la largeur de la fenêtre
        new_width = int(illustration_width / 100 * card_spec.zoom)
        new_height = int(illustration_width / 100 * ratio * card_spec.zoom)

    else:
        # hauteur au moins de la hauteur de la fenêtre
        new_height = int(illustration_height / 100 * card_spec.zoom)
        new_width = int(illustration_height / 100 / ratio * card_spec.zoom)

    return new_width, new_height


def resize_illustration(card_spec, illustration):
    new_width, new_height = get_resized_dimensions(card_spec)
    resized_illustration = illustration.resize(
        (new_width, new_height),
        Image.LANCZOS,
    )
    return resized_illustration


def wrap_text(text, font, max_width, draw):
    """
    Wraps text to fit within the max_width.
    """
    words = text.split()
    lines = [] # Holds each line in the text box
    current_line = [] # Holds each word in the current line under evaluation.

    for word in words:
        # Check the width of the current line with the new word added
        test_line = ' '.join(current_line + [word])
        width = draw.textlength(test_line, font=font)
        if width <= max_width:
            current_line.append(word)
        else:
            # If the line is too wide, finalize the current line and start a new one
            lines.append(' '.join(current_line))
            current_line = [word]

    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))

    description = ""
    for line in lines:
        description += line + "\n"

    return description


def make_card(card_spec: Card, illustration):
    card = card_spec.BASECARD.copy()
    draw = ImageDraw.Draw(card)

    resized_illustration = resize_illustration(card_spec, illustration)
    horizon = card_spec.horizon
    vertical = card_spec.vertical
    card.paste(resized_illustration, (X1 - horizon, Y1 - vertical))
    card.paste(card_spec.BASECARD, (0, 0), card_spec.BASECARD)

    draw.text(
        (card_spec.WIDTH - 35, card_spec.HEIGHT - 35),
        text=COPYRIGHT_TEXT,
        fill="black",
        font=FONT_COPYRIGHT,
        anchor="rb",
    )

    numero = f"N°{card_spec.numero :04d}  " if card_spec.numero > 0 else ""
    type_bebe = card_spec.type_bebe if card_spec.type_bebe else card_spec.signe_astro
    taille = f"  Taille : {card_spec.taille} cm" if card_spec.taille > 0 else ""
    kg = card_spec.poids // 1000
    gr = card_spec.poids % 1000
    gr = f"{gr:03d}" if gr>0 else "0"
    poids = f"  Poids : {kg},{gr} kg" if card_spec.poids > 0 else ""

    draw.text(
        (card_spec.WIDTH / 2, 558),
        text=f"{numero}Bébé {type_bebe.capitalize()}{taille}{poids}",
        fill="#634038",
        font=FONT_CARD_SUBTITLE,
        anchor="mm",
    )

    width = draw.textlength(card_spec.category, FONT_CATEGORY)
    width = max(width, 40)

    category = Image.open(f"docs/images/bandeaux/{card_spec.category}.png")
    card.paste(category, (0, 0), category)

    name = card_spec.name
    draw.text(
        (width + 80, 55),
        text=name,
        fill="black",
        font=FONT_NAME,
        anchor="lm",
    )

    draw.text(
        (card_spec.WIDTH-92, 56),
        text=card_spec.date_naissance,
        fill="black",
        font=FONT_CARD_TEXT,
        anchor="rm",
    )

    fond_signe_astro = Image.open(f"docs/images/signes_astro/astro_marron.png")
    card.paste(fond_signe_astro, (0, 0), fond_signe_astro)

    signe_astro = Image.open(f"docs/images/signes_astro/{card_spec.signe_astro.lower()}.png")
    signe_astro.thumbnail((32,32), Image.Resampling.LANCZOS)
    card.paste(signe_astro, (549, 43), signe_astro)

    fond_attaque = Image.open("docs/images/attacks/rond_marron.png")
    fond_attaque.thumbnail((40,40), Image.Resampling.LANCZOS)
    card.paste(fond_attaque, (58, 618), fond_attaque)
    
    attaque_symb = Image.open(
        f"docs/images/attacks/{card_spec.attack_symbol.lower()}.png"
    )
    attaque_symb.thumbnail((31,31), Image.Resampling.LANCZOS)
    card.paste(attaque_symb, (63, 622), attaque_symb)
    attack_text = card_spec.attack_text
    draw.text(
        (120, 625),
        text=attack_text,
        align="center",
        fill="black",
        font=FONT_CARD_TEXT,
        spacing=12,
        anchor="lt"
    )

    attack_subtext = wrap_text(card_spec.attack_subtext, FONT_CARD_SUBTITLE, 470, draw)

    draw.multiline_text(
        (120, 625+35),
        text=attack_subtext,
        align="left",
        fill="black",
        font=FONT_CARD_SUBTITLE,
        spacing=6,
        # anchor="lt"
    )

    dimensions = draw.textbbox(
        (0,0),
        text=attack_subtext,
        font=FONT_CARD_SUBTITLE,
        )
    text_height = dimensions[3]-dimensions[1]

    capacite_speciale_text = card_spec.capacite_speciale_text
    if capacite_speciale_text and len(capacite_speciale_text)>0:
        draw.text(
                (60, 700+text_height),
                text=f"Capacité spéciale : {capacite_speciale_text}",
                align="center",
                fill="black",
                font=FONT_CARD_TEXT_I,
                spacing=12,
                anchor="lm"
            )

    quote = card_spec.quote
    draw.text(
        (55, card_spec.HEIGHT - 80),
        text=f"« {quote} »" if quote else "",
        # align="center",
        anchor="lm",
        fill="black",
        font=FONT_CARD_QUOTE,
    )
    return card


footer = """<style>
a:link , a:visited{
color: red;
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: gray;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with 💖 by <a style='display: block; text-align: center;' href="https://htilquin.github.io/" target="_blank">Hélène T.</a></p>
</div>
"""
