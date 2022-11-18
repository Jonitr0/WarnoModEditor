# class for loading markdown strings from file
import logging

def get_md_text(file_name: str) -> str:
    try:
        with open("resources/markdown/" + file_name) as f:
            text = f.read()
    except Exception as e:
        logging.error("Error while reading .md file at " + file_name + ":" + str(e))
        return ""
    return text