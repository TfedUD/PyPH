import PHX.climate


def parse_copy_from_excel(_phx_climate, _input):
    # type: (PHX.climate.Climate, list) -> None
    """Parse copy/pasted data from PHPP/WUFI XLS format."""

    data = []
    for row in _input:
        data.append(row.split("\t"))

    _phx_climate.monthly_temperature_air.values = data[0][0:12]
    _phx_climate.monthly_temperature_dewpoint.values = data[6][0:12]
    _phx_climate.monthly_temperature_sky.values = data[7][0:12]

    _phx_climate.monthly_radiation_north.values = data[1][0:12]
    _phx_climate.monthly_radiation_east.values = data[2][0:12]
    _phx_climate.monthly_radiation_south.values = data[3][0:12]
    _phx_climate.monthly_radiation_west.values = data[4][0:12]
    _phx_climate.monthly_radiation_global.values = data[5][0:12]

    _phx_climate.peak_heating_1.temp = data[0][12]
    _phx_climate.peak_heating_1.rad_north = data[1][12]
    _phx_climate.peak_heating_1.rad_east = data[2][12]
    _phx_climate.peak_heating_1.rad_south = data[3][12]
    _phx_climate.peak_heating_1.rad_west = data[4][12]
    _phx_climate.peak_heating_1.rad_global = data[5][12]

    _phx_climate.peak_heating_2.temp = data[0][13]
    _phx_climate.peak_heating_2.rad_north = data[1][13]
    _phx_climate.peak_heating_2.rad_east = data[2][13]
    _phx_climate.peak_heating_2.rad_south = data[3][13]
    _phx_climate.peak_heating_2.rad_west = data[4][13]
    _phx_climate.peak_heating_2.rad_global = data[5][13]

    _phx_climate.peak_cooling.temp = data[0][14]
    _phx_climate.peak_cooling.rad_north = data[1][14]
    _phx_climate.peak_cooling.rad_east = data[2][14]
    _phx_climate.peak_cooling.rad_south = data[3][14]
    _phx_climate.peak_cooling.rad_west = data[4][14]
    _phx_climate.peak_cooling.rad_global = data[5][14]

    return _phx_climate
