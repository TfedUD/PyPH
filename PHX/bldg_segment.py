# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Building-Segment Classes. A complete Building/Project has one or more BldgSegment(s).

These can be thought of as 'wings' or 'sections' of a full building structure. Each
Segment can have its own occupancy types / top-level attributes and has one or more Zones within it.
"""

from collections import defaultdict
from functools import reduce

import PHX._base
import PHX.hvac
import PHX.component
import PHX.spaces
import PHX.summer_ventilation
import PHX.occupancy


class ZoneTypeError(Exception):
    def __init__(self, _in):
        self.message = 'Error: Expected input of type: "PHX.bldg_segment.Zone" Got: "{}"::"{}"?'.format(
            _in, type(_in)
        )
        super(ZoneTypeError, self).__init__(self.message)


class Geom(PHX._base._Base):
    """Geometry Collection"""

    def __init__(self):
        super(Geom, self).__init__()
        self.polygons = []

    @property
    def vertices(self):
        return (v for p in self.polygons for v in p.vertices)

    def add_component_polygons(self, _compos):
        # type: (list[PHX.component.Component]) -> None
        """Adds component's polygons to the Geometry's 'polygons' list

        Arguments:
        ----------
            * _compos (list[Component]): The components to add the polygons from
        """

        if not isinstance(_compos, list):
            _compos = [_compos]

        for compo in _compos:
            for poly in compo.polygons:
                if poly in self.polygons:
                    continue

                self.polygons.append(poly)


class PHIUSCertification(PHX._base._Base):
    def __init__(self):
        super(PHIUSCertification, self).__init__()
        self.certification_criteria = 3
        self.localization_selection_type = 2

        self.PHIUS2021_heating_demand = 20
        self.PHIUS2021_cooling_demand = 21
        self.PHIUS2021_heating_load = 22
        self.PHIUS2021_cooling_load = 23

        self.building_status = 1  # In Planning
        self.building_type = 1  # New Construction

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._PHIUSCertification(cls, _dict)


class Weather_PeakLoad:
    def __init__(self, _t, _rN, _rE, _rS, _rW, _rG):
        self.temp = _t
        self.rad_north = _rN
        self.rad_east = _rE
        self.rad_south = _rS
        self.rad_west = _rW
        self.rad_global = _rG


class PH_ClimateLocation(PHX._base._Base):
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

        self.TemperatureMonthly = [
            1.2,
            -0.2,
            5.6,
            10.9,
            16.1,
            21.7,
            25.0,
            24.8,
            19.9,
            14.0,
            7.3,
            3.3,
        ]
        self.NorthSolarRadiationMonthly = [
            21,
            29,
            34,
            39,
            56,
            60,
            59,
            50,
            34,
            30,
            20,
            16,
        ]
        self.EastSolarRadiationMonthly = [
            32,
            46,
            57,
            65,
            82,
            76,
            78,
            84,
            60,
            54,
            33,
            28,
        ]
        self.SouthSolarRadiationMonthly = [
            83,
            106,
            103,
            86,
            80,
            73,
            78,
            104,
            97,
            129,
            87,
            87,
        ]
        self.WestSolarRadiationMonthly = [
            48,
            70,
            92,
            95,
            114,
            121,
            120,
            130,
            91,
            94,
            47,
            45,
        ]
        self.GlobalSolarRadiationMonthly = [
            50,
            72,
            111,
            133,
            170,
            176,
            177,
            182,
            124,
            109,
            62,
            46,
        ]
        self.DewPointTemperatureMonthly = [
            -4.3,
            -7.4,
            0.3,
            4.7,
            9.1,
            15.8,
            20.3,
            17.1,
            13.2,
            7.9,
            2.1,
            -2.8,
        ]
        self.SkyTemperatureMonthly = [
            -17.4,
            -20.0,
            -10.9,
            -4.8,
            1.0,
            9.8,
            14.5,
            8.4,
            5.8,
            -2.8,
            -8.6,
            -11.4,
        ]
        self.GroundTemperatureMonthly = []

        self.peak_heating_1 = Weather_PeakLoad(-6.7, 46, 80, 200, 113, 121)
        self.peak_heating_2 = Weather_PeakLoad(-4.2, 16, 22, 46, 26, 38)
        self.peak_cooling = Weather_PeakLoad(26.1, 64, 106, 132, 159, 230)


class ClimateLocation(PHX._base._Base):
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
        self.GroundReflLong = 0.1
        self.GroundEmission = 0.9
        self.CloudIndex = 0.66
        self.CO2concenration = 350
        self.Unit_CO2concentration = 48


class Zone(PHX._base._Base):

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
        self.summer_ventilation = PHX.summer_ventilation.SummerVent()

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(Zone, cls).__new__(cls, *args, **kwargs)

    def add_spaces(self, _new_spaces):
        # type (list[PHX.spaces.Space]): -> None
        """Adds new Spaces (Rooms) to the BldgSegment"""

        if not isinstance(_new_spaces, list):
            _new_spaces = [_new_spaces]
        for space in _new_spaces:
            self.rooms_ventilation.append(space)

    def add_new_appliance(self, _appliance):
        # type (Appliance) -> None
        """Adds a new PHX-Appliance to the PHX-BldgSegment"""

        self.appliances.append(_appliance)

    @staticmethod
    def _clean_join(_a, _b):
        if not _a and not _b:
            return None
        elif not _a and _b:
            return _b
        elif _a and not _b:
            return _a
        else:
            return _a + _b

    def __add__(self, other):
        # type: (Zone, Zone) -> Zone
        new_obj = self.__class__()

        # -- Combine weighted paramaters first
        new_obj.clearance_height = (
            (self.clearance_height * self.floor_area)
            + (other.clearance_height * other.floor_area)
        ) / (self.floor_area + other.floor_area)

        new_obj.spec_heat_cap = (
            (self.spec_heat_cap * self.floor_area)
            + (other.spec_heat_cap * other.floor_area)
        ) / (self.floor_area + other.floor_area)

        # -- Combine Summer Ventilation, weighted by Zone volume
        new_obj.summer_ventilation = PHX.summer_ventilation.SummerVent.weighted_join(
            self.summer_ventilation,
            self.volume_gross,
            other.summer_ventilation,
            other.volume_gross,
        )

        # -- Add basic parameters
        new_obj.n = "Merged Zone"
        new_obj.volume_gross = self.volume_gross + other.volume_gross
        new_obj.volume_net = self._clean_join(self.volume_net, other.volume_net)
        new_obj.floor_area = self.floor_area + other.floor_area

        # -- Extend rooms, appliances
        new_obj.rooms_ventilation.extend(self.rooms_ventilation)
        new_obj.rooms_ventilation.extend(other.rooms_ventilation)
        new_obj.source_zone_identifiers.extend(self.source_zone_identifiers)
        new_obj.source_zone_identifiers.extend(other.source_zone_identifiers)
        new_obj.appliances.extend(self.appliances)
        new_obj.appliances.extend(other.appliances)

        return new_obj

    def __radd__(self, other):
        return self.__add__(other)


class BldgSegment(PHX._base._Base):
    """A Segment/Zone/Wing of a Project with one or more PHX-Zones inside.

    A single Structure/Project can have one or more Building-Segments.
    For WUFI-Passive, this class basically maps to a 'Variant'/'Case' at the Project level
    """

    _count = 0
    _default = None

    def __init__(self):
        super(BldgSegment, self).__init__()
        self.id = self._count
        self.target_room_names = []
        self.relative_variant = True  # WUFI shit
        self.n = ""
        self.remarks = ""
        self.geom = Geom()
        self.calcScope = 4
        self.HaMT = {}
        self.PHIUS_certification = PHIUSCertification()
        self.occupancy = PHX.occupancy.BldgSegmentOccupancy()
        self.DIN4108 = {}
        self.cliLoc = ClimateLocation()
        self.HVAC = PHX.hvac.HVAC()
        self.res = None
        self.plugin = None

        self.components = []
        self.zones = []

        self.numerics = None
        self.airflow_model = None
        self.count_generator = 0
        self.has_been_generated = False
        self.has_been_changed_since_last_gen = False

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(BldgSegment, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def default(cls):
        if cls._default:
            return cls._default

        new_obj = cls()
        new_obj.n = "Default BldgSegment"

        cls._default = new_obj
        return new_obj

    def add_zones(self, _zones):
        # type: (list[PHX.spaces.Zone]) -> None
        """Adds new Zones to the BldgSegment."""

        if not isinstance(_zones, list):
            _zones = [_zones]

        for z in _zones:
            if z in self.zones:
                continue
            if not isinstance(z, Zone):
                raise ZoneTypeError(z)

            self.zones.append(z)

    def add_components(self, _components):
        # type: (list[PHX.component.Component]) -> None
        """Adds new Components to the BldgSegment

        Arguments:
        ----------
            * _components ( list[Component] ): The Components to add to the BldgSegment

        Returns:
        --------
            * None
        """

        self.geom.add_component_polygons(_components)

        if not isinstance(_components, list):
            _compos = [_components]

        for c in _compos:
            if c in self.components:
                continue
            if not isinstance(c, PHX.component.Component):
                raise PHX.component.ComponentTypeError(c)
            self.components.append(c)

    def get_component_groups(self, group_by=None):
        # type: (str) -> dict[PHX.component.Component]
        """Gets the BldgSegment's components, grouped by some category

        Arguments:
        ----------
            _group_by (str): 'zone' | None

        Returns:
        -------
            * (dict): The Component groups Dictionary
        """

        compo_groups = defaultdict(list)

        if not group_by:
            compo_groups[self.id] = self.components

        elif str(group_by).upper() == "ZONE":

            # Group compos that are in the same zone, (and the same exposures)
            for compo in self.components:
                key = "IC_{}_EC_{}_TYP_{}".format(compo.idIC, compo.idEC, compo.type)
                compo_groups[key].append(compo)

        return compo_groups

    def get_zone_by_identifier(self, _zone_identifier_lookup):
        # type: (str) -> Zone | None
        """Returns a Zone from the BldgSegment's Zone list if it matches the specified Identifier

        Arguments:
        ----------
            * _zone_identifier_looup (str): The zone Identifier to lookup.
                ie: "4ef23cb3-89c5-4590-8069-dc395a183ac2"

        Returns:
        --------
            * (Zone | None): The Zone, if found, or None if no matches are found
        """

        for zone in self.zones:
            if zone.identifier == _zone_identifier_lookup:
                return zone
            elif _zone_identifier_lookup in zone.source_zone_identifiers:
                # -- If the zone has been joined previously
                return zone
        else:
            return None

    def merge_components(self, by="assembly"):
        # type: (str) -> None
        """Groups (joins) Components by the desginated characteristic.

        Note: this function will edit/change the BldgSegment.components list and
        will join Components together.

        Arguments:
        ----------
            * by (str): 'assembly', '...'

        Returns:
        --------
            * (None)
        """

        exg_compo_dict = self.get_component_groups(group_by="zone")
        new_compo_list = []

        if "ASSEMBLY" in str(by).upper():
            for zone_compos in exg_compo_dict.values():

                compo_groups = defaultdict(list)

                # -- Group by Assembly
                for compo in zone_compos:
                    if compo.idAssC != -1:
                        # -- Opaque Component
                        compo_groups[compo.idAssC].append(compo)
                    elif compo.idWtC != -1:
                        # -- Window Component
                        compo_groups[compo.idWtC].append(compo)
                    else:
                        compo_groups[-1].append(compo)

                # -- Join the groups into single new Component
                for compo_gr in compo_groups.values():
                    compo_joined = reduce(lambda a, b: a + b, compo_gr)
                    new_compo_list.append(compo_joined)

            # -- Replace the Component List with the new one
            self.components = new_compo_list

    def merge_zones(self):
        # type: (None) -> None
        """Merges all of the Zones together into a single Zone"""

        if len(self.zones) <= 1:
            return None
        else:
            zones_joined = reduce(lambda a, b: a + b, self.zones)
            zones_joined.id = 1
            self.zones = [zones_joined]

            # -- Merge all the Components
            # -- Update all the exposure names,
            # -- Remove interior surfaces (?!)
            for compo in self.components:
                compo.set_host_zone_name(self.zones[0])

            return None

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._BldgSegment(cls, _dict)
