import pathlib

import tensorflow as tf

# TODO: Replace with custom model variant
model = tf.keras.applications.MobileNetV2(input_shape=None,
                                          include_top=True,
                                          weights="imagenet")

GERMAN_LABELS = {
    "reel": "eine Rolle",
    "cellular_telephone": "ein Handy",
    "modem": "ein Modem",
    "computer_keyboard": "eine Tastatur",
    "space_bar": "eine Leertaste",
    "consomme": "eine Brühe",
    "cup": "eine Tasse",
    "espresso": "ein Espresso",
    "face_powder": "Gesichtspuder",
    "soap_dispenser": "Seifenspender",
    "sarong": "ein Sarong",
    "swimming_trunks": "eine Badehose",
    "loupe": "eine Lupe",
    "CD_player": "ein CD-Player",
    "reflex_camera": "eine Foto-Kamera",
    "lighter": "ein Feuerzeug",
    "switch": "ein Schalter",
    "crossword_puzzle": "ein Kreuzworträtsel",
    "stethoscope": "ein Stethoskop",
    "wallet": "ein Portemonnaie",
    "iPod": "ein iPod",
    "mouse": "eine Maus",
    "magnetic_compass": "ein Kompass",
    "strainer": "ein Sieb",
    "pill_bottle": "eine Pillendose",
    "handkerchief": "ein Taschentuch",
    "saltshaker": "ein Salzstreuer",
    "eggnog": "Eierlikör",
    "ballpoint": "ein Kugelschreiber",
    "chain": "eine Kette",
    "loudspeaker": "ein Lautsprecher",
    "remote_control": "eine Fernbedienung",
    "combination_lock": "ein Zahlenschloss",
    "thimble": "ein Fingerhut",
    "hook": "ein Haken",
    "whistle": "eine Pfeife",
    "paper_towel": "ein Papierhandtuch"
}


def decode_label(prediction):
    original_label = tf.keras.applications.mobilenet_v2.decode_predictions(prediction, top=1)[0][0][1]
    return GERMAN_LABELS[original_label] if original_label in GERMAN_LABELS else original_label
