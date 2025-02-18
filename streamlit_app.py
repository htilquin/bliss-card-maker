import json
import streamlit as st
from utils_app import *
from io import BytesIO
import zipfile

st.markdown("## Novembabies Card Maker !")
st.markdown("Petit outil pour faire des cartes à jouer personnalisées - Novembabies Edition.")

card_spec = Card()

card_spec.category = st.sidebar.selectbox(
    "Catégorie de la carte", ("Novembabies", "Bliss"),
).lower()
card_spec.name = st.sidebar.text_input("Nom de la  carte", value="Nom de la Carte", label_visibility="collapsed")
card_spec.date_naissance = st.sidebar.text_input("Date de naissance", value="01/01", label_visibility="collapsed")
card_spec.signe_astro = st.sidebar.selectbox("Signe Astro", signes_astro)

card_spec.numero = st.sidebar.number_input("Numéro", min_value=0, max_value=None)
card_spec.type_bebe = st.sidebar.text_input("Type du bébé", placeholder="Type du bébé", label_visibility="collapsed")
card_spec.taille = st.sidebar.number_input("Taille en cm", min_value=0, max_value=None)
card_spec.poids = st.sidebar.number_input("Poids en g", min_value=0, max_value=None)

card_spec.attack_symbol = st.sidebar.selectbox("Symbole Attaque", attack_symb)
card_spec.attack_text = st.sidebar.text_input(
    "Texte Attaque", value="Attaque Principale", label_visibility="collapsed",
)
card_spec.attack_subtext = st.sidebar.text_input(
    "Sous-Texte Attaque", label_visibility="collapsed", placeholder="Description attaque"
)

card_spec.capacite_speciale_text = st.sidebar.text_input(
    "Texte Capacité Spéciale", placeholder="Capacité Spéciale", label_visibility="collapsed",
    )

card_spec.quote = st.sidebar.text_area(
    "Mini citation de la carte", placeholder="Citation facultative", label_visibility="collapsed",
)

tab1, tab2 = st.tabs(
    ["Voir la Carte", "Traitement automatisé"]
)

with tab1:
    with st.expander("Modifier la photo"):
        illustration_path = st.file_uploader(
            "Sélectionner l'illustration",
            type=["png", "jpg", "jpeg"],
        )
        if illustration_path:
            card_spec.illustration_path = illustration_path

        card_spec.zoom = st.slider(
            "Changer la taille de la photo", min_value=100, max_value=300, value=100
        )

        new_width, new_heigth = get_resized_dimensions(card_spec)
        if card_spec.zoom > 100:
            card_spec.horizon = st.slider(
                "Déplacer photo horizontalement",
                min_value=0,
                max_value=max(new_width - illustration_width, 1),
                value=0,
            )
        if new_heigth > illustration_height:
            card_spec.vertical = st.slider(
                "Déplacer photo verticalement",
                min_value=0,
                max_value=max(new_heigth - illustration_height, 1),
                value=0,
            )

    illustration = Image.open(card_spec.illustration_path)
    card = make_card(card_spec, illustration)
    st.image(card, )
    buf = BytesIO()
    card.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Télécharger la carte",
        data=byte_im,
        file_name=f"{card_spec.name}.png",
    )


with tab2:
    uploaded_spec = st.file_uploader(
        """Sélectionner le **fichier** au format csv contenant les specs.""",
        type="csv",
    )

    uploaded_pics = st.file_uploader(
        "Sélectionner les **photos** correspondantes : nom de la photo = illustration_path.",
        accept_multiple_files=True,
    )

    sorted_pics = sorted(uploaded_pics, key=lambda d: d.name)

    if uploaded_spec and uploaded_pics:
        sorted_specs = csv_to_dict_list(uploaded_spec)
        # sorted_specs = sorted(the_specs)

        with BytesIO() as buffer:
            with zipfile.ZipFile(buffer, "w") as zipfile:
                # for specs in the_specs["cards"]:
                for specs, photo in zip(sorted_specs, sorted_pics):
                    print("Traitement de", specs["illustration_path"])  # , photo.name
                    card_from_spec = Card()
                    card_from_spec.from_dict(specs)
                    illustration = Image.open(BytesIO(photo.read()))
                    card_done = make_card(card_from_spec, illustration)
                    buf = BytesIO()
                    card_done.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    # st.image(card_done)
                    name = card_from_spec.illustration_path[:-4]
                    zipfile.writestr(f"{name}.png", byte_im)

            buffer.seek(0)

            btn = st.download_button(
                label="Download ZIP", data=buffer, file_name="file.zip"
            )
