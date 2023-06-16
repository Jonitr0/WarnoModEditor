import logging

# TODO: add Götterdämmerung strings
STRINGS = {
    "BETUFEMGDL": "A-1-11th ACR",
    "SLWSVLLPZP": "Troop HQ",
    "DLZTKEQFFT": "1st Tank Platoon",
    "UQOKRWWLYC": "2nd Tank Platoon",
    "EBAXRQFWNO": "Recon Platoon",
    "FQMCKESHIX": "Air Defense Platoon",
    "HYKDXVFKPJ": "4311-VKK 431",
    "QPXHKBIWGL": "Führung",
    "OIQGCEKCDM": "1. Zug",
    "CRZWJJYXZT": "2. Zug",
    "OPDTEQBKBP": "Artillerie-Gruppe",
    "EHFLKHNINV": "Flak-Gruppe",
    "cha_1": "Air Support",
    "FCSWUWUIEP": "1-A-509th TFS",
    "ZOMQAFHITM": "Rota Komandovani",
    "SUJBJHQBBH": "Platoon HQ",
    "HBLUTIMQXB": "AA Platoon",
    "KPNJIRFMVK": "Artillery Platoon",
    "YHHKVXFYTB": "1-1-17y GvTP",
    "AEHXPSCGSH": "1st Platoon",
    "TXLIVWUPSM": "2nd Platoon",
    "WAKIQBNMIP": "3rd Platoon",
    "JFDLGUGPAH": "4th Platoon",
    "BIUSBBTLXM": "2-1-17y GvTP",
    "CDWDIWURMP": "1-1-35ya GvDShB",
    "cha_2": "Aviapodderzhka",
    "ZRMILCMBPM": "HQ-2-32nd Armored",
    "AFXAGTUHDY": "Support Group",
    "ZISMTAUYGO": "AA Group",
    "JYZDSITBSM": "Mortar Platoon",
    "SRHWTUYLYQ": "Logistics Group",
    "YRYIJYWVRT": "E-2-32nd Armored",
    "LGWJRRZQVH": "N-4-7th Cavalry",
    "MWICGOJROV": "1-900y DShBat.",
    "GHUYXATXPF": "2-900y DShBat.",
    "AIIMCNDONF": "Recon Platoon",
    "MMISGNOMQO": "AT Platoon",
    "OMMSABUJXJ": "Support Platoon",
}


def get_string(token: str):
    if not STRINGS.__contains__(token):
        logging.warning("String for token \"" + token + "\" not found!")
        return "String not found!"
    return STRINGS[token]
