# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions used to build PHX Rooms from Honeybee Rooms"""

import PHX.bldg_segment
import honeybee.room
import loggers.HBJSON_loggers


@loggers.HBJSON_loggers.log_function_info
def create_PHX_Room_from_HB_room(_hb_room: honeybee.room.Room) -> PHX.bldg_segment.Room:
    room = PHX.bldg_segment.Room()
    room.name = _hb_room.display_name
    room.volume_gross = _hb_room.volume

    return room
