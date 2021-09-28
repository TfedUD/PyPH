# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Functions used to build PHX Spaces from HB-Model inputs"""

import honeybee.room
import PHX.spaces


def create_PHX_Spaces_from_HB_room(_hb_room):
    # type: (honeybee.room.Room) -> list[PHX.spaces.Space]
    """Returns a list of new PHX-Spaces based on the Honeybee Room"""

    # --- Get any detailed user-determined Space info on the HB-Room
    user_determined_space_dict = _hb_room.user_data.get("phx", {}).get("spaces", [])

    spaces = []
    if user_determined_space_dict:
        # --- Build new Spaces based on the User-determined detailed inputs
        for space_dict in user_determined_space_dict.values():

            new_phx_space = PHX.spaces.Space.from_dict(space_dict)
            spaces.append(new_phx_space)
    else:
        # --- Build a default space for the zone, if no detailed spaces are provided
        new_phx_space = PHX.spaces.Space()
        new_phx_space.space_number = None
        new_phx_space.space_name = f"{_hb_room.display_name}_room"

        spaces.append(new_phx_space)

    return spaces
