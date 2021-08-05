# -*- coding: utf-8 -*-
"""Utility functions for working with Ladybug-Tools objects"""

import honeybee.room
import statistics

def calc_HB_Room_avg_occupancy( _hb_room):
    # type: (honeybee.room.Room ) -> float
    """Returns the 'average' HB Room occupancy"""

    #-- Figure out the max occupancy (Num of People)
    peak_occupancy_per_area = _hb_room.properties.energy.people.people_per_area
    peak_occupancy = peak_occupancy_per_area * _hb_room.floor_area
    
    #-- Calc the Program's mean_occupancy, if needed
    if not hasattr( _hb_room.properties.energy.people.occupancy_schedule, 'mean_occupancy' ):
        # Get the hourly occupancy as list of 8760 decimal values ie: [0.6, 0.65 0.78, 0.93,...]
        mean_occupancy = statistics.mean( _hb_room.properties.energy.people.occupancy_schedule.values() )
    else:
        mean_occupancy = _hb_room.properties.energy.people.occupancy_schedule.mean_occupancy

    return peak_occupancy * mean_occupancy

def calc_HB_Room_total_ventilation_m3sec(_hb_room ):
    # type: (honeybee.room.Room) -> float
    """Returns the total peak ventilation airflow for a Honeybee Room
    
    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee Room to calculate values of.

    Returns:
    --------
        * (float): The Honeybee Room's total ventilation airflow in M3/second.
    """

    total_vent = 0.0
    total_vent += _hb_room.properties.energy.ventilation.air_changes_per_hour * _hb_room.volume
    total_vent += _hb_room.properties.energy.ventilation.flow_per_area * _hb_room.floor_area
    total_vent += _hb_room.properties.energy.ventilation.flow_per_zone

    room_avg_occupancy = calc_HB_Room_avg_occupancy(_hb_room)
    total_vent += _hb_room.properties.energy.ventilation.flow_per_person * room_avg_occupancy

    return total_vent