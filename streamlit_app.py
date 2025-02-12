import json
import streamlit as st
from utils_app import *
from io import BytesIO
import zipfile

st.markdown("## Novembabies Card Maker !")
st.markdown("Petit outil pour faire des cartes à jouer personnalisées - Novembabies Edition.")

card_spec = Card()

card_spec.card_category = st.sidebar.selectbox(
    "Catégorie de la carte", ("Novembabies", "Bliss"),
).lower()
card_spec.card_name = st.sidebar.text_input("Nom de la  carte", value="Nom de la Carte", label_visibility="collapsed")
card_spec.date_naissance = st.sidebar.text_input("Date de naissance", value="01/01", label_visibility="collapsed")
card_spec.signe_astro = st.sidebar.selectbox(
    "Signe Astro", ("Vierge", "Balance", "Scorpion", "Sagittaire"),
).lower()

card_spec.subtitle_no = st.sidebar.number_input("Numéro", min_value=0, max_value=None)
card_spec.type_bebe = st.sidebar.text_input("Type du bébé", placeholder="Type du bébé", label_visibility="collapsed")
card_spec.subtitle_taille = st.sidebar.number_input("Taille en cm", min_value=0, max_value=None)
card_spec.subtitle_poids = st.sidebar.number_input("Poids en g", min_value=0, max_value=None)


symbols_1 = [
    # "Biberon",
    # "Peigne",
    # "Thermomètre",
    # "Caca",
    "Rond1",
    "Rond2",
]

card_spec.attaque_symbol = st.sidebar.selectbox("Symbole Attaque", symbols_1)
card_spec.attaque_text = st.sidebar.text_input(
    "Texte Attaque", value="Attaque Principale", label_visibility="collapsed",
)
card_spec.attaque_subtext = st.sidebar.text_input(
    "Sous-Texte Attaque", label_visibility="collapsed", placeholder="Description attaque"
)

card_spec.capacite_speciale_text = st.sidebar.text_input(
    "Texte Capacité Spéciale", placeholder="Capacité Spéciale", label_visibility="collapsed",
    )

card_spec.quote = st.sidebar.text_area(
    "Mini citation de la carte", placeholder="Citation facultative", label_visibility="collapsed",
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Voir la Carte", "Voir les Specs", "Charger Specs", "Fusionner les Specs"]
)

with tab1:
    with st.expander("Modifier la photo"):
        illustration_path = st.file_uploader(
            "Sélectionner l'illustration",
            type=["png", "jpg", "jpeg"],
        )
        if illustration_path:
            card_spec.illustration_path = illustration_path

        card_spec.size = st.slider(
            "Changer la taille de la photo", min_value=100, max_value=300, value=100
        )

        new_x, new_y = get_resized_dimensions(card_spec)
        if card_spec.size > 100:
            card_spec.horizon = st.slider(
                "Déplacer photo horizontalement",
                min_value=0,
                max_value=max(new_x - card_spec.WIDTH + offset, 1),
                value=0,
            )
        if new_y > int(0.69 * card_spec.HEIGHT) - offset:
            card_spec.vertical = st.slider(
                "Déplacer photo verticalement",
                min_value=0,
                max_value=max(new_y - int(0.69 * card_spec.HEIGHT) + offset, 1),
                value=0,
            )

    card = make_card(card_spec)
    st.image(card, )
    buf = BytesIO()
    card.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Télécharger la carte",
        data=byte_im,
        file_name=f"{card_spec.card_name}.png",
    )


# with tab2:
#     dict_of_spec = card_spec.to_dict()
#     st.write(dict_of_spec)
#     st.download_button(
#         "Download the specs",
#         json.dumps(dict_of_spec),
#         file_name=f"{card_spec.card_name}.json",
#     )

# with tab3:
#     uploaded_spec = st.file_uploader(
#         """Sélectionner le **fichier** contenant les specs au format json, 
#         doit être une liste même s'il n'y a qu'une carte !""",
#         type=["txt", "json"],
#     )

#     uploaded_pics = st.file_uploader(
#         "Sélectionner les **photos** correspondantes : nom de la photo = illustration_path.",
#         accept_multiple_files=True,
#     )

#     sorted_pics = sorted(uploaded_pics, key=lambda d: d.name)

#     if uploaded_spec and uploaded_pics:
#         the_specs = json.loads(uploaded_spec.read())
#         sorted_specs = sorted(the_specs)

#         with BytesIO() as buffer:
#             with zipfile.ZipFile(buffer, "w") as zipfile:
#                 # for specs in the_specs["cards"]:
#                 for specs, photo in zip(sorted_specs, sorted_pics):
#                     print(specs["illustration_path"])  # , photo.name
#                     card_from_spec = Card()
#                     card_from_spec.from_dict(specs)
#                     card_done = make_card(card_from_spec)
#                     buf = BytesIO()
#                     card_done.save(buf, format="PNG")
#                     byte_im = buf.getvalue()
#                     # st.image(card_done)
#                     zipfile.writestr(f"{card_from_spec.card_name}.png", byte_im)

#             buffer.seek(0)

#             btn = st.download_button(
#                 label="Download ZIP", data=buffer, file_name="file.zip"
#             )

# with tab4:
#     pass
