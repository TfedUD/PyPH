# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""
Functions for writing a Text XML file out to disk.
"""

from datetime import datetime
import os
import shutil


def write_XML_text_file(_file_address, _xml_text) -> None:
    """Write the PHX 'Project' object out to a file as WUFI-XML.

    Arguments:
    ----------
        * _file_address (str): The file path to save to
        * _xml_text: The XML text to write out to file
    """

    t = datetime.now()

    def clean_filename(_file_address):
        old_file_name, old_file_extension = os.path.splitext(_file_address)
        # old_file_name = _file_address.split(".xml")[0]
        t = datetime.now()
        return f"{old_file_name}_{t.month}_{t.day}_{t.hour}_{t.minute}_{t.second}{old_file_extension}"

    save_dir = os.path.dirname(_file_address)
    save_filename = os.path.basename(_file_address)
    save_filename_clean = clean_filename(save_filename)

    try:
        save_address_1 = os.path.join(save_dir, save_filename)
        save_address_2 = os.path.join(save_dir, save_filename_clean)
        with open(save_address_1, "w", encoding="utf8") as f:
            f.writelines(_xml_text)

        #  Make a working copy
        shutil.copyfile(save_address_1, save_address_2)

    except PermissionError:
        # - In case the file is being used by WUFI or something else, make a new copy.
        print(
            f"Target file: {save_filename} is currently being used by another process and is protected.\n"
            f"Writing to a new file: {save_address_2}"
        )

        with open(save_address_2, "w", encoding="utf8") as f:
            f.writelines(_xml_text)

    print("Done.")
