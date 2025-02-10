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

libertine_font_20 = ImageFont.truetype(
    "docs/font/LinLibertine_RI.ttf", 20
)
arimo_font_14 = ImageFont.truetype("docs/font/Arimo-BoldItalic.ttf", 14)

opensans_font_14 = ImageFont.truetype("docs/font/OpenSans-Regular.ttf", 14)
opensans_font_18 = ImageFont.truetype("docs/font/OpenSans-Regular.ttf", 18)
opensans_font_25 = ImageFont.truetype("docs/font/OpenSans-Bold.ttf", 25)
opensans_font_25_i = ImageFont.truetype("docs/font/OpenSans-BoldItalic.ttf", 25)
opensans_font_30 = ImageFont.truetype("docs/font/OpenSans-Bold.ttf", 32)

offset = 80

FONT_CARD_NAME = opensans_font_30
FONT_CARD_TEXT = opensans_font_25
FONT_CARD_TEXT_I = opensans_font_25_i
FONT_CARD_QUOTE = libertine_font_20
FONT_CARD_SUBTITLE = opensans_font_18
FONT_CARD_CATEGORY = arimo_font_14

COPYRIGHT_TEXT = "©️2024 Momvembers"
FONT_COPYRIGHT = opensans_font_14

class Card:
    BASECARD = Image.open("docs/images/background/beige.png")
    WIDTH, HEIGHT = BASECARD.size

    illustration_path = "docs/images/basic_illustration.PNG"
    size = 100
    horizon = 0
    vertical = 0
    fond_couleur = "Brun"
    card_name = "Carte"
    subtitle_no = 0
    type_bebe = ""
    subtitle_taille = 0
    subtitle_poids = 0
    card_category = "Novembabies"
    date_naissance = "01/01"
    signe_astro = "Scorpion"
    value_skill = 0
    attaque_1_symbol = None
    attaque_1_text = ""
    attaque_1_subtext = ""
    capacite_speciale_text = ""
    quote = ""

    def to_dict(self):
        return {
            "illustration_path": self.illustration_path,
            "size": self.size,
            "horizon": self.horizon,
            "vertical": self.vertical,
            "fond_couleur": self.fond_couleur,
            "card_name": self.card_name,
            "subtitle_no": self.subtitle_no,
            "type_bebe": self.type_bebe,
            "subtitle_taille": self.subtitle_taille,
            "subtitle_poids": self.subtitle_poids,
            "card_category": self.card_category,
            "date_naissance": self.date_naissance,
            "signe_astro": self.signe_astro,
            "value_skill": self.value_skill,
            "attaque_1_symbol": self.attaque_1_symbol,
            "attaque_1_text": self.attaque_1_text,
            "attaque_1_subtext": self.attaque_1_subtext,
            "capacite_speciale_text": self.capacite_speciale_text,
            "quote": self.quote,
        }

    def from_dict(self, data):
        self.illustration_path = data.get("illustration_path")
        self.size = data.get("size")
        self.horizon = data.get("horizon")
        self.vertical = data.get("vertical")
        self.fond_couleur = data.get("fond_couleur")
        self.card_name = data.get("card_name")
        self.subtitle_no = data.get("subtitle_no")
        self.type_bebe = data.get("type_bebe")
        self.subtitle_taille = data.get("subtitle_taille")
        self.subtitle_poids = data.get("subtitle_poids")
        self.card_category = data.get("card_category")
        self.date_naissance = data.get("date_naissance")
        self.signe_astro = data.get("signe_astro")
        self.value_skill = data.get("value_skill")
        self.attaque_1_text = data.get("attaque_1_text")
        self.attaque_1_subtext = data.get("attaque_1_subtext")
        self.attaque_1_symbol = data.get("attaque_1_symbol")
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

    fond_carte = Image.open(f"docs/images/background/{card_spec.fond_couleur}.png")
    card.paste(fond_carte, (0, 0), fond_carte)

    bandeau = Image.open(f"docs/images/bandeaux/Underbottom.png")
    card.paste(bandeau, (0, 6), bandeau)

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
        fill="black",
        font=FONT_CARD_SUBTITLE,
        anchor="mm",
    )

    width = draw.textlength(card_spec.card_category, FONT_CARD_CATEGORY)
    width = max(width, 40)

    card_category = Image.open(f"docs/images/bandeaux/{card_spec.card_category}.png")
    card.paste(card_category, (0, 0), card_category)

    card_name = card_spec.card_name
    draw.text(
        (width + 80, 53),
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

    attaque_1_symb = Image.open(
        f"docs/images/symbols/{card_spec.attaque_1_symbol}.png"
    )
    # card.paste(attaque_1_symb, (-230, -66), attaque_1_symb)
    card.paste(attaque_1_symb, (50, 612), attaque_1_symb)
    attaque_1_text = card_spec.attaque_1_text
    draw.text(
        (120, 625),
        text=attaque_1_text,
        align="center",
        fill="black",
        font=FONT_CARD_TEXT,
        spacing=12,
        anchor="lt"
    )

    attaque_1_subtext = card_spec.attaque_1_subtext
    draw.text(
        (120, 625+35),
        text=attaque_1_subtext,
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
