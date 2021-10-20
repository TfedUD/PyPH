#
# PyPH: A Plugin for aadding Passive-House data to LadybugTools Models
# 
# This component is part of the PH-Tools toolkit <https://github.com/PH-Tools>.
# 
# Copyright (c) 2021, PH-Tools and bldgtyp, llc <phtools@bldgtyp.com> 
# PyPH is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License, 
# or (at your option) any later version. 
# 
# PyPH is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# For a copy of the GNU General Public License
# see <https://github.com/PH-Tools/PyPH/blob/main/LICENSE>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>
#
"""
Assign Honeybee Rooms to a specific 'Buildiing Segment' within the PHX Model. In WUFI, this is used
as the 'Case', while in C3RRO this will be considered the 'Variant'. For PHIUS
projects, use this component to break mixed-use projects into separate residential-case
and non-residential-case variants.
-
EM October 20, 2021
    Args:
        name_:
        latitude_: (deg) 
        longitude_: (deg)
        altitude_: (m)
        daily_temp_variation_: (deg K) 
        avg_wind_speed_: ()
        copy_from_excel_: Copy/Paste from a PHPP-Style Climate data. Copy the 
            yellow cells (not the top line with ID / long / lat and not the left
            column with headings.)
    
    Returns:
        phx_climate_: A new PHX Climate Object. Apply this to a WUFI Config PyPH Component.
"""


import PHX.climate
import PyPH_Rhino.gh_utils
import PyPH_Rhino.climate

# --
import PyPH_GH._component_info_
reload(PyPH_GH._component_info_)
ghenv.Component.Name = "PyPH - Climate"
DEV = True
PyPH_GH._component_info_.set_component_params(ghenv, dev='OCT_20_2021')

if DEV:
    reload(PHX.climate)
    reload(PyPH_Rhino.climate)

# -- Climate
phx_climate_ = PHX.climate.Climate()
phx_climate_.name = name_ or '__unnamed_location__'
phx_climate_.summer_daily_temperature_swing = daily_temp_variation_ or 8.0
phx_climate_.average_wind_speed = avg_wind_speed_ or 4

# -- Location
phx_climate_.location.latitude = latitude_ or 40.6
phx_climate_.location.longitude = longitude_ or -73.8
phx_climate_.location.weather_station_elevation = altitude_ or 5.0
phx_climate_.location.climate_zone = 1
phx_climate_.location.hours_from_UTC = -4

# -- Monthly
phx_climate_.monthly_temperature_air.values = [1.2,-0.2,5.6,10.9,16.1,21.7,25.0,24.8,19.9,14.0,7.3,3.3,]
phx_climate_.monthly_temperature_dewpoint.values = [-4.3,-7.4,0.3,4.7,9.1,15.8,20.3,17.1,13.2,7.9,2.1,-2.8]
phx_climate_.monthly_temperature_sky.values = [-17.4,-20.0,-10.9,-4.8,1.0,9.8,14.5,8.4,5.8,-2.8,-8.6,-11.4]
phx_climate_.monthly_temperature_ground.values = []

phx_climate_.monthly_radiation_north.values = [21,29,34,39,56,60,59,50,34,30,20,16]
phx_climate_.monthly_radiation_east.values = [32,46,57,65,82,76,78,84,60,54,33,28]
phx_climate_.monthly_radiation_south.values = [83,106,103,86,80,73,78,104,97,129,87,87]
phx_climate_.monthly_radiation_west.values = [48,70,92,95,114,121,120,130,91,94,47,45]
phx_climate_.monthly_radiation_global.values = [50,72,111,133,170,176,177,182,124,109,62,46]

# -- Peak Loads
phx_climate_.peak_heating_1.temp = -6.7
phx_climate_.peak_heating_1.rad_north = 46
phx_climate_.peak_heating_1.rad_east = 80
phx_climate_.peak_heating_1.rad_south = 200
phx_climate_.peak_heating_1.rad_west = 113
phx_climate_.peak_heating_1.rad_global = 121

phx_climate_.peak_heating_2.temp = -4.2
phx_climate_.peak_heating_2.rad_north = 16
phx_climate_.peak_heating_2.rad_east = 22
phx_climate_.peak_heating_2.rad_south = 46
phx_climate_.peak_heating_2.rad_west = 26
phx_climate_.peak_heating_2.rad_global = 38

phx_climate_.peak_cooling.temp = 26.1
phx_climate_.peak_cooling.rad_north = 64
phx_climate_.peak_cooling.rad_east = 106
phx_climate_.peak_cooling.rad_south = 132
phx_climate_.peak_cooling.rad_west = 159
phx_climate_.peak_cooling.rad_global = 230

if copy_from_excel_:
    phx_climate_ = PyPH_Rhino.climate.parse_copy_from_excel(phx_climate_, copy_from_excel_)

# -- Preview
PyPH_Rhino.gh_utils.object_preview(phx_climate_)