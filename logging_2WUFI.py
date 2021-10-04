import logging
import os
import pathlib


def configure():
    # -- Setup the log Directory
    log_path = pathlib.PurePath("LOG", "PyPH_WUFI", "this_is_a_file_name.txt")
    if not os.path.exists(log_path.parent):
        os.makedirs(log_path.parent)

    # -- Log to File: | PyPH_HBJSON.creat_PHX_Ventilation.PHX_ventilation_from_hb_room
    logger_1 = logging.getLogger("PHX_ventilation_from_hb_room")
    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    file_handler.setLevel("DEBUG")
    formater = logging.Formatter("%(asctime)s %(message)s")
    file_handler.setFormatter(formater)
    logger_1.addHandler(file_handler)
