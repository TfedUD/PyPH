import PHX.bldg_segment
import honeybee.room
import PyPH_HBJSON.create_PHX_Ventilation
import PHX.spaces


def create_PHX_Room_from_HB_room(_hb_room: honeybee.room.Room) -> PHX.bldg_segment.Room:
    room = PHX.bldg_segment.Room()
    room.name = _hb_room.display_name
    room.volume_gross = _hb_room.volume

    # -- Set the Programs
    room.ventilation = PyPH_HBJSON.create_PHX_Ventilation.PHX_ventilation_from_hb_room(_hb_room)

    return room
