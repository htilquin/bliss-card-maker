import streamlit as st
import math
from PIL import Image, ImageFont, ImageDraw

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

# libertine_RI_20 = ImageFont.truetype("docs/font/LinLibertine_RI.ttf", 20)
arimo_BI_14 = ImageFont.truetype("docs/font/Arimo-BoldItalic.ttf", 14)

opensans_R_14 = ImageFont.truetype("docs/font/OpenSans-Regular.ttf", 14)
opensans_R_18 = ImageFont.truetype("docs/font/OpenSans-Regular.ttf", 18)
opensans_BI_25 = ImageFont.truetype("docs/font/OpenSans-BoldItalic.ttf", 25)
opensans_B_30 = ImageFont.truetype("docs/font/OpenSans-Bold.ttf", 32)

athelas_R_15 = ImageFont.truetype("docs/font/Athelas-Regular.ttf", 15)
athelas_I_20 = ImageFont.truetype("docs/font/Athelas-Italic.ttf", 20)
athelas_R_25 = ImageFont.truetype("docs/font/Athelas-Regular.ttf", 25)
athelas_B_32 = ImageFont.truetype("docs/font/Athelas-Bold.ttf", 32)
athelas_BI_32 = ImageFont.truetype("docs/font/Athelas-BoldItalic.ttf", 32)
athelas_R_32 = ImageFont.truetype("docs/font/Athelas-Regular.ttf", 32)
athelas_B_36 = ImageFont.truetype("docs/font/Athelas-Bold.ttf", 36)


offset = 80

FONT_CARD_NAME = athelas_B_36
FONT_CARD_TEXT = athelas_B_32
FONT_CARD_TEXT_I = athelas_BI_32
# FONT_CARD_QUOTE = libertine_RI_20
FONT_CARD_QUOTE = athelas_I_20
FONT_CARD_SUBTITLE = opensans_R_18
FONT_CARD_CATEGORY = arimo_BI_14

COPYRIGHT_TEXT = "©️2024 Momvembers"
FONT_COPYRIGHT = athelas_R_15

class Card:
    BASECARD = Image.open("docs/images/background.png")
    WIDTH, HEIGHT = BASECARD.size

    illustration_path = "docs/images/basic_illustration.PNG"
    size = 100
    horizon = 0
    vertical = 0
    card_name = "Carte"
    subtitle_no = 0
    type_bebe = ""
    subtitle_taille = 0
    subtitle_poids = 0
    card_category = "Novembabies"
    date_naissance = "01/01"
    signe_astro = "Scorpion"
    value_skill = 0
    attaque_symbol = None
    attaque_text = ""
    attaque_subtext = ""
    capacite_speciale_text = ""
    quote = ""

    def to_dict(self):
        return {
            "illustration_path": self.illustration_path,
            "size": self.size,
            "horizon": self.horizon,
            "vertical": self.vertical,
            "card_name": self.card_name,
            "subtitle_no": self.subtitle_no,
            "type_bebe": self.type_bebe,
            "subtitle_taille": self.subtitle_taille,
            "subtitle_poids": self.subtitle_poids,
            "card_category": self.card_category,
            "date_naissance": self.date_naissance,
            "signe_astro": self.signe_astro,
            "value_skill": self.value_skill,
            "attaque_symbol": self.attaque_symbol,
            "attaque_text": self.attaque_text,
            "attaque_subtext": self.attaque_subtext,
            "capacite_speciale_text": self.capacite_speciale_text,
            "quote": self.quote,
        }

    def from_dict(self, data):
        self.illustration_path = data.get("illustration_path")
        self.size = data.get("size")
        self.horizon = data.get("horizon")
        self.vertical = data.get("vertical")
        self.card_name = data.get("card_name")
        self.subtitle_no = data.get("subtitle_no")
        self.type_bebe = data.get("type_bebe")
        self.subtitle_taille = data.get("subtitle_taille")
        self.subtitle_poids = data.get("subtitle_poids")
        self.card_category = data.get("card_category")
        self.date_naissance = data.get("date_naissance")
        self.signe_astro = data.get("signe_astro")
        self.value_skill = data.get("value_skill")
        self.attaque_text = data.get("attaque_text")
        self.attaque_subtext = data.get("attaque_subtext")
        self.attaque_symbol = data.get("attaque_symbol")
        self.capacite_speciale_text = data.get("capacite_speciale_text")
        self.quote = data.get("quote")


def get_resized_dimensions(card_spec):
    illustration = Image.open(card_spec.illustration_path)
    x, y = illustration.size
    ratio = y / x

    new_x = int((card_spec.WIDTH - offset) / 100 * card_spec.size)
    new_y = int((card_spec.WIDTH - offset) / 100 * ratio * card_spec.size)

    return new_x, new_y


def resize_illustration(card_spec):
    illustration = Image.open(card_spec.illustration_path)
    size = card_spec.size
    x, y = illustration.size
    ratio = y / x

    resized_illustration = illustration.resize(
        (
            int((card_spec.WIDTH - offset) / 100 * size),
            int((card_spec.WIDTH - offset) / 100 * ratio * size),
        ),
        Image.LANCZOS,
    )
    return resized_illustration


def make_card(card_spec: Card):
    card = card_spec.BASECARD.copy()
    draw = ImageDraw.Draw(card)

    resized_illustration = resize_illustration(card_spec)
    horizon = card_spec.horizon
    vertical = card_spec.vertical
    card.paste(resized_illustration, (-horizon + offset // 2, -vertical + offset // 2))
    card.paste(card_spec.BASECARD, (0, 0), card_spec.BASECARD)

    draw.text(
        (card_spec.WIDTH - 35, card_spec.HEIGHT - 35),
        text=COPYRIGHT_TEXT,
        fill="black",
        font=FONT_COPYRIGHT,
        anchor="rb",
    )

    numero = f"N°{card_spec.subtitle_no :04d}  " if card_spec.subtitle_no > 0 else ""
    type_bebe = card_spec.type_bebe if card_spec.type_bebe else card_spec.signe_astro
    taille = f"  Taille : {card_spec.subtitle_taille} cm" if card_spec.subtitle_taille > 0 else ""
    kg = card_spec.subtitle_poids // 1000
    gr = card_spec.subtitle_poids % 1000
    gr = f"{gr:03d}" if gr>0 else "0"
    poids = f"  Poids : {kg},{gr} kg" if card_spec.subtitle_poids > 0 else ""

    draw.text(
        (card_spec.WIDTH / 2, 558),
        text=f"{numero}Bébé {type_bebe.capitalize()}{taille}{poids}",
        fill="#634038",
        font=FONT_CARD_SUBTITLE,
        anchor="mm",
    )

    width = draw.textlength(card_spec.card_category, FONT_CARD_CATEGORY)
    width = max(width, 40)

    card_category = Image.open(f"docs/images/bandeaux/{card_spec.card_category}.png")
    card.paste(card_category, (0, 0), card_category)

    card_name = card_spec.card_name
    draw.text(
        (width + 80, 55),
        text=card_name,
        fill="black",
        font=FONT_CARD_NAME,
        anchor="lm",
    )

    draw.text(
        (card_spec.WIDTH-85, 56),
        text=card_spec.date_naissance,
        fill="black",
        font=FONT_CARD_TEXT,
        anchor="rm",
    )

    signe_astro = Image.open(f"docs/images/signes_astro/{card_spec.signe_astro}.png")
    # card.paste(signe_astro, (549, 43), signe_astro)
    card.paste(signe_astro, (254, -642), signe_astro)

    attaque_symb = Image.open(
        f"docs/images/attacks/{card_spec.attaque_symbol}.png"
    )
    # card.paste(attaque_symb, (-230, -66), attaque_symb)
    card.paste(attaque_symb, (50, 612), attaque_symb)
    attaque_text = card_spec.attaque_text
    draw.text(
        (120, 625),
        text=attaque_text,
        align="center",
        fill="black",
        font=FONT_CARD_TEXT,
        spacing=12,
        anchor="lt"
    )

    attaque_subtext = card_spec.attaque_subtext
    draw.text(
        (120, 625+35),
        text=attaque_subtext,
        align="center",
        fill="black",
        font=FONT_CARD_SUBTITLE,
        spacing=12,
        anchor="lt"
    )

    capacite_speciale_text = card_spec.capacite_speciale_text
    if len(capacite_speciale_text)>0:
        draw.text(
                (60, 725),
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
