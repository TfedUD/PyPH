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
import PHX.programs.lighting
import PHX.programs.occupancy
import PHX.programs.ventilation
import PHX.infiltration
import PHX.ground
import PHX.appliances

# ------------------------------------------------------------------------------
class ZoneTypeError(Exception):
    def __init__(self, _in):
        self.message = 'Error: Expected input of type: "PHX.bldg_segment.Zone" Got: "{}"::"{}"?'.format(_in, type(_in))
        super(ZoneTypeError, self).__init__(self.message)


class GroupTypeNotImplementedError(Exception):
    def __init__(self, _in):
        self.message = 'Error: BuildingSegment grouping by Group Type: "{}" not implemented yet.'.format(str(_in))
        super(GroupTypeNotImplementedError, self).__init__(self.message)


# ------------------------------------------------------------------------------
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

        self.int_gains_evap_per_person = 15
        self.int_gains_flush_heat_loss = True
        self.int_gains_num_toilets = 1
        self.int_gains_toilet_room_util_pat = None
        self.int_gains_use_school_defaults = False
        self.int_gains_dhw_marginal_perf_ratio = None

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


# ------------------------------------------------------------------------------
class Room(PHX._base._Base):
    """A PHX-Room. Part of a PHX-Zone.

    BldgSegment_1
       +----Zone_1
       |      +----Room_1  #<-----
       |      |      +---Space_1
       |      |      +---Space_1
       |      +----Room_2
       +----Zone_2
       |      |

    Containts one or more PHX-Spaces and all the Program data (sched, loads) for the spaces
    """

    _count = 0

    def __init__(self):
        super(Room, self).__init__()
        self.id = self._count
        self.name = ""
        self.volume_gross = 0.0
        self.spaces = []

        self.ventilation = PHX.programs.ventilation.SpaceVentilation()
        self.lighting = PHX.programs.lighting.SpaceLighting()
        self.occupancy = PHX.programs.occupancy.SpaceOccupancy()

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(Room, cls).__new__(cls, *args, **kwargs)

    def add_spaces(self, _spaces):
        # type: (list[PHX.spaces.Space]) -> None
        """Adds new Rooms to the Zone"""

        if not isinstance(_spaces, list):
            _spaces = [_spaces]

        for space in _spaces:
            self.spaces.append(space)

    def __str__(self):
        return "PHX_{}: {}".format(self.__class__.__name__, self.name)


class Zone(PHX._base._Base):
    """A Thermal Zone. Contains one or more Rooms and relevant Zone-level attributes

    BldgSegment_1
       +----Zone_1  #<-----
       |      +----Room_1
       |      |      +---Space_1
       |      |      +---Space_1
       |      +----Room_2
       +----Zone_2
       |      |
    """

    _count = 0

    def __init__(self):
        super(Zone, self).__init__()
        self.id = self._count
        self.n = None
        self.typeZ = 1

        self.volume_gross = 0.0
        self.volume_gross_selection = 7
        self.volume_net = 0.0
        self.volume_net_selection = 4
        self.floor_area = 0.0
        self.floor_area_selection = 4
        self.clearance_height_selection = 2
        self.clearance_height = 2.5
        self.spec_heat_cap_selection = 2
        self.spec_heat_cap = 132

        self.rooms = []
        self.source_zone_identifiers = []

        self.appliances = PHX.appliances.ApplianceSet()
        self.summer_ventilation = PHX.summer_ventilation.SummerVent()
        self.occupancy = PHX.programs.occupancy.ZoneOccupancy()

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(Zone, cls).__new__(cls, *args, **kwargs)

    def add_rooms(self, _new_rooms):
        # type: (list[PHX.bldg_segment.Room]) -> None
        """Adds new Rooms to the Zone"""

        if not isinstance(_new_rooms, list):
            _new_rooms = [_new_rooms]

        for room in _new_rooms:
            self.rooms.append(room)

            self.volume_gross += room.volume_gross
            self.volume_gross_selection = 6  # user-defined

            for space in room.spaces:
                # -- Add to the zone totals
                self.volume_net += space.volume
                self.volume_net_selection = 6  # user-defined
                self.floor_area += space.floor_area_weighted
                self.floor_area_selection = 6  # user-defined

    @staticmethod
    def _floor_area_weighted_join(_a, _b, _attr_str):
        # type: (Zone, Zone, str) -> float
        """
        Util function to cleanly join together two Zone attributes, weighted
        by floor area handles ZeroDivisionErrors and None values
        """

        val_a = getattr(_a, _attr_str)
        val_b = getattr(_b, _attr_str)

        try:
            return ((val_a * _a.floor_area) + (val_b * _b.floor_area)) / (_a.floor_area + _b.floor_area)
        except ZeroDivisionError:
            return 0

    def __add__(self, other):
        # type: (Zone, Zone) -> Zone
        new_obj = self.__class__()

        # -- Add basic parameters
        new_obj.n = "Merged Zone"
        # -- Protect from None
        new_obj.volume_gross = (self.volume_gross or 0) + (other.volume_gross or 0)
        new_obj.volume_net = (self.volume_net or 0) + (other.volume_net or 0)
        new_obj.floor_area = (self.floor_area or 0) + (other.floor_area or 0)

        # -- Combine weighted paramaters
        new_obj.clearance_height = self._floor_area_weighted_join(self, other, "clearance_height")
        new_obj.spec_heat_cap = self._floor_area_weighted_join(self, other, "spec_heat_cap")

        # -- Combine Summer Ventilation, weighted by Zone volume
        new_obj.summer_ventilation = PHX.summer_ventilation.SummerVent.weighted_join(
            self.summer_ventilation,
            self.volume_gross,
            other.summer_ventilation,
            other.volume_gross,
        )

        # -- Extend rooms ventilation
        new_obj.rooms.extend(self.rooms)
        new_obj.rooms.extend(other.rooms)
        new_obj.source_zone_identifiers.extend([self.identifier, other.identifier])
        new_obj.source_zone_identifiers.extend(self.source_zone_identifiers)
        new_obj.source_zone_identifiers.extend(other.source_zone_identifiers)

        # -- Combine ApplianceSets
        new_obj.appliances = self.appliances + other.appliances

        # -- Combine Occupancies
        new_obj.occupancy = self.occupancy + other.occupancy

        return new_obj

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)


class BldgSegment(PHX._base._Base):
    """A Segment/Part/Wing of a Project with one or more PHX-Zones inside.

    BldgSegment_1 #<-----
       +----Zone_1
       |      +----Room_1
       |      |      +---Space_1
       |      |      +---Space_1
       |      +----Room_2
       +----Zone_2
       |      |

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
        self.occupancy = PHX.programs.occupancy.BldgSegmentOccupancy()
        self.infiltration = PHX.infiltration.Infiltration(self)
        self.foundations = [PHX.ground.Foundation()]
        self.DIN4108 = {}
        self.cliLoc = ClimateLocation()
        self.HVAC_system = PHX.hvac.HVAC_System()
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
        new_obj.n = "Default Building Segment"

        cls._default = new_obj
        return new_obj

    @property
    def total_envelope_area(self):
        return sum((_.exposed_area or 0) for _ in self.components)

    @property
    def total_volume_net(self):
        return sum((_.volume_net or 0) for _ in self.zones)

    @property
    def total_volume_gross(self):
        return sum((_.volume_gross or 0) for _ in self.zones)

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

        if not isinstance(_components, list):
            _components = [_components]

        for c in _components:
            if c in self.components:
                continue

            if not isinstance(c, PHX.component.Component):
                raise PHX.component.ComponentTypeError(c)

            self.components.append(c)
            self.geom.add_component_polygons(c)

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
                key = "IC_{}_EC_{}_TYP_{}".format(compo.int_exposure_zone_id, compo.ext_exposure_zone_id, compo.type)
                compo_groups[key].append(compo)

        else:
            raise GroupTypeNotImplementedError(group_by)

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
            if str(zone.identifier) == str(_zone_identifier_lookup):
                return zone
            else:
                # -- If the zone has been joined previouslyz
                for identifier in zone.source_zone_identifiers:
                    if str(_zone_identifier_lookup) in str(identifier):
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
            * by (str): default='assembly', ...

        Returns:
        --------
            * (None)
        """

        exg_compo_dict = self.get_component_groups(group_by="zone")
        new_compo_list = []

        if "ASSEMBLY" in str(by).upper():
            for zone_compos in exg_compo_dict.values():

                compo_groups = defaultdict(list)

                # -- Group by Assembly Number
                for compo in zone_compos:
                    if compo.assembly_id_num != -1:
                        # -- Its a normal Opaque Component
                        compo_groups[compo.assembly_id_num].append(compo)
                    elif compo.win_type_id_num != -1:
                        # -- Its a Window Component
                        compo_groups[compo.win_type_id_num].append(compo)
                    else:
                        # -- Its some other type?
                        compo_groups[-1].append(compo)

                # -- Join all the Components in each group into single new Component
                for compo_gr in compo_groups.values():
                    compo_joined = reduce(lambda a, b: a + b, compo_gr)
                    new_compo_list.append(compo_joined)

            # -- Replace the Component List with the new one
            self.components = new_compo_list
        else:
            raise GroupTypeNotImplementedError(by)

    def merge_zones(self):
        # type: (None) -> None
        """Merges all of the Zones together into a single Zone"""

        if len(self.zones) <= 1:
            return None
        else:
            zones_joined = reduce(lambda a, b: a + b, self.zones)
            zones_joined.id = 1
            self.zones = [zones_joined]

            # -- Set the appliance Reference Quantity
            # -- As per PHIUS, if the building is single Zone, all appliances
            # -- should be set to 'PH Case' quantity
            for appliance in zones_joined.appliances.appliances:
                if appliance.type in {1, 2, 3, 7}:
                    appliance.reference_quantity = 1  # PH-Case

            # -- Merge all the Components
            # -- Update all the exposure names,
            # -- Remove interior surfaces (?!)
            for compo in self.components:
                compo.set_host_zone_name(self.zones[0])

            return None
