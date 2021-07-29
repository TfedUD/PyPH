# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Variant Classes
"""

from ._base import _Base
from .geometry import Geom
from .hvac import HVAC, HVAC_System, HVAC_System_ZoneCover, HVAC_Device

class PassivehouseData(_Base):
    def __init__(self):
        super(PassivehouseData, self).__init__()

class Weather_PeakLoad:

    def __init__(self, _t, _rN, _rE, _rS, _rW, _rG):
        self.temp = _t
        self.rad_north = _rN
        self.rad_east = _rE
        self.rad_south = _rS
        self.rad_west = _rW
        self.rad_global = _rG

class PH_ClimateLocation(_Base):

    def __init__(self):
        super(PH_ClimateLocation, self).__init__()
        self.Selection = 6
        self.Latitude = 40.6
        self.HeightNNWeatherStation = 5
        self.Longitude = -73.8
        self.dUTC = -4
        self.HeightNNBuilding = None
        self.DailyTemperatureSwingSummer = 8
        self.AverageWindSpeed = 4
        self.ClimateZone = 1
        self.GroundThermalConductivity = 2
        self.GroundHeatCapacitiy = 1000
        self.GroundDensity = 2000
        self.DepthGroundwater = 3
        self.FlowRateGroundwater = 0.05
        self.SelectionPECO2Factor = 1

        self.TemperatureMonthly = [ 1.2,-0.2,5.6,10.9,16.1,21.7,25.0,24.8,19.9,14.0,7.3,3.3 ]
        self.NorthSolarRadiationMonthly = [21, 29, 34, 39, 56, 60, 59, 50, 34, 30, 20, 16]
        self.EastSolarRadiationMonthly = [32, 46, 57, 65, 82, 76, 78, 84, 60, 54, 33, 28]
        self.SouthSolarRadiationMonthly = [83, 106, 103, 86, 80, 73, 78, 104, 97, 129, 87, 87]
        self.WestSolarRadiationMonthly = [48, 70, 92, 95, 114, 121, 120, 130, 91, 94, 47, 45]
        self.GlobalSolarRadiationMonthly = [50, 72, 111, 133, 170, 176, 177, 182, 124, 109, 62, 46]
        self.DewPointTemperatureMonthly = [-4.3, -7.4, 0.3, 4.7, 9.1, 15.8, 20.3, 17.1, 13.2, 7.9, 2.1, -2.8]
        self.SkyTemperatureMonthly = [-17.4, -20.0, -10.9, -4.8, 1.0, 9.8, 14.5, 8.4, 5.8, -2.8, -8.6, -11.4]
        self.GroundTemperatureMonthly = []

        self.peak_heating_1 = Weather_PeakLoad( -6.7, 46, 80, 200, 113, 121)
        self.peak_heating_2 = Weather_PeakLoad( -4.2, 16, 22, 46, 26, 38)
        self.peak_cooling = Weather_PeakLoad( 26.1, 64, 106, 132, 159, 230)

class ClimateLocation(_Base):

    def __init__(self):
        super(ClimateLocation, self).__init__()
        self.Selection = 1
        self.PH_ClimateLocation = PH_ClimateLocation()
        self.IDNr_DB = None
        self.Name_DB = None
        self.Comment_DB = None
        self.Latitude_DB = None
        self.Longitude_DB = None
        self.HeightNN_DB = None
        self.dUTC_DB = None
        self.FileName_DB = None
        self.Type_DB = None
        self.CatalogueNr_DB = 0
        self.MapNr_DB = 0
        self.Albedo = -2
        self.GroundReflShort = 0.2
        self.GroundReflLong =0.1
        self.GroundEmission = 0.9
        self.CloudIndex = 0.66
        self.CO2concenration = 350
        self.Unit_CO2concentration = 48

class WP_Room(_Base):

    _count = 0

    def __init__(self):
        super(WP_Room, self).__init__()
        self.id = self._count
        self.n = 'default_room'
        self.type = 99
        self.idUPatV = 1
        self.idVUnit = 1
        self.quantity = 1
        self.area = None
        self.clearH = None
        self.design_flow_rate_supply = None
        self.design_flow_rate_extract = None

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable """
        cls._count += 1
        return super(WP_Room, cls).__new__(cls, *args, **kwargs)
    
class Zone(_Base):
    
    _count = 0
    
    def __init__(self):
        super(Zone, self).__init__()
        self.id = self._count
        self.n = None
        self.typeZ = 1
        self.volume_gross = None
        self.volume_gross_selection = 7
        self.volume_net = None
        self.volume_net_selection = 4
        self.floor_area = None
        self.floor_area_selection = 4
        self.clearance_height_selection = 2
        self.clearance_height = 2.5
        self.spec_heat_cap_selection = 2
        self.spec_heat_cap = 132
        self.rooms_ventilation = []
        self.source_zone_identifiers = []
        self.appliances = []
    
    @property
    def wp_display_name(self):
        return f'Zone {self.id}: {self.n}'

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable """
        cls._count += 1
        return super(Zone, cls).__new__(cls, *args, **kwargs)
    
    def add_new_WP_room(self, _new_room):
        self.rooms_ventilation.append( _new_room )

    def add_new_appliance(self, _appliance):
        self.appliances.append( _appliance )

class Building(_Base):
    
    def __init__(self):
        super(Building, self).__init__()
        self.lComponent = []
        self.lZone = []
        self.numerics = None
        self.airflow_model = None
        self.count_generator = 0
        self.has_been_generated = False
        self.has_been_changed_since_last_gen = False
    
    def add_zones(self, _zones): #-> None
        """Adds a new Zone to the Building
        
        Arguments:
        ----------
            * _zone (list[Zone]): The new Zones to add to the Building
        """
        if not isinstance( _zones, list):
            _zones = [ _zones ]

        self.lZone.extend( _zones )
    
    def add_components(self, _compos): #-> None
        """Adds new component to the variant.building.lComponent 
        
        Arguments:
        ----------
            * _compos (list[Component]): The Components to add to the Building 
                lComponent list
        """
        
        if not isinstance(_compos, list):
            _compos = [ _compos ]

        self.lComponent.extend( _compos )

    def get_zone_by_identifier(self, _zone_identifier_lookup): #-> Optional[Zone]
        for zone in self.lZone:
            if zone.identifier == _zone_identifier_lookup:
                return zone
            elif _zone_identifier_lookup in zone.source_zone_identifiers:
                #-- If the zone has been joined previously
                return zone
        else:
            return None

class Variant(_Base):
    _count = 0

    def __init__(self):
        super(Variant, self).__init__()
        self.id = self._count
        self.target_room_names = []
        self.relative_variant = True
        self.n = ""
        self.remarks = ""
        self.geom = Geom()
        self.calcScope = 4
        self.HaMT = {}
        self.PHIUS = PassivehouseData()
        self.DIN4108 = {}
        self.cliLoc = ClimateLocation()
        self.building = Building()
        self.HVAC = HVAC()
        self.res = None
        self.plugin = None
    
    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable """
        cls._count += 1
        return super(Variant, cls).__new__(cls, *args, **kwargs)
    
    def add_zones(self, _zones): #-> None
        """Adds new Zones to the Variant 
        
        Arguments:
        ----------
            * _zones (list[Zone]): The Zones to add to the Variant
        
        Returns:
        --------
            * None
        """

        self.building.add_zones( _zones )
    
    def add_components(self, _components): #-> None
        """Adds new Components to the Variant 
        
        Arguments:
        ----------
            * _components ( list[Component] ): The Components to add to the Variant 
        
        Returns:
        --------
            * None
        """

        self.building.add_components( _components )
        self.geom.add_component_polygons( _components )

    def add_default_venilation_system(self):# -> None
        """Adds a Default HVAC Sytem to the Variant that will be assigned to all
            of the Zones in the Variant.
        
        Arguments:
        ----------
            * None
        
        Returns:
        --------
            * None
        """
        default_hvac_system = HVAC_System()
        default_hvac_system.n = 'default_hvac_system'
        for zone in self.building.lZone:
            new_zone_hvac = HVAC_System_ZoneCover()
            new_zone_hvac.idZone = zone.id
            default_hvac_system.add_new_zone_hvac_system( new_zone_hvac )

        mech_vent_device = HVAC_Device()
        default_hvac_system.add_new_hvac_device( mech_vent_device )

        self.HVAC.add_system( default_hvac_system )

    @property
    def zones(self):
        return self.building.lZone

    def get_zone_by_identifier(self, _zone_identifier_lookup):# -> Optional[Zone]
        return self.building.get_zone_by_identifier( _zone_identifier_lookup )