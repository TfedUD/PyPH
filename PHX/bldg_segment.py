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
import PHX.component
import PHX.spaces
import PHX.summer_ventilation
import PHX.programs.lighting
import PHX.programs.occupancy
import PHX.programs.ventilation
import PHX.programs.electric_equipment
import PHX.mechanicals.equipment
import PHX.mechanicals.systems
import PHX.infiltration
import PHX.ground
import PHX.appliances
import PHX.climate

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

        self.PHIUS2021_heating_demand = 15.0
        self.PHIUS2021_cooling_demand = 15.0
        self.PHIUS2021_heating_load = 10.0
        self.PHIUS2021_cooling_load = 10.0

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

        self.ventilation = PHX.programs.ventilation.RoomVentilation()
        self.lighting = PHX.programs.lighting.RoomLighting()
        self.occupancy = PHX.programs.occupancy.RoomOccupancy()
        self.electric_equipment = PHX.programs.electric_equipment.RoomElectricEquipment()
        self.mechanicals = PHX.mechanicals.systems.Mechanicals()

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
    """A PHX Thermal Zone. Contains one or more Rooms and relevant Zone-level attributes

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
        self.name = None
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

        self.appliance_set = PHX.appliances.ApplianceSet()
        self.summer_ventilation = PHX.summer_ventilation.SummerVent()
        self.occupancy = PHX.programs.occupancy.ZoneOccupancy()

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(Zone, cls).__new__(cls, *args, **kwargs)

    @property
    def mechanicals(self):
        """Return a single Mechanical Object which is a sum of all the Room Mechanicals"""
        return sum(room.mechanicals for room in self.rooms)

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
        new_obj.name = "Merged Zone"
        # -- Protect from None
        new_obj.volume_gross = (self.volume_gross or 0) + (other.volume_gross or 0)
        new_obj.volume_net = (self.volume_net or 0) + (other.volume_net or 0)
        new_obj.floor_area = (self.floor_area or 0) + (other.floor_area or 0)
        new_obj.floor_area_selection = 6  # user-defined
        new_obj.volume_net_selection = 6  # user-defined
        new_obj.volume_gross_selection = 6  # user-defined

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
        new_obj.appliance_set = self.appliance_set + other.appliance_set

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
        self.airflow_model = None
        self.calcScope = 4
        self.climate = PHX.climate.Climate()
        self.components = []
        self.count_generator = 0
        self.DIN4108 = {}
        self.foundations = [PHX.ground.Foundation()]
        self.geom = Geom()
        self.HaMT = {}
        self.has_been_changed_since_last_gen = False
        self.has_been_generated = False
        self.id = self._count
        self.infiltration = PHX.infiltration.Infiltration(self)
        self.name = ""
        self.numerics = None
        self.occupancy = PHX.programs.occupancy.BldgSegmentOccupancy()
        self.PHIUS_certification = PHIUSCertification()
        self.plugin = None
        self.relative_variant = True
        self.remarks = ""
        self.res = None
        self.target_room_names = []
        self.zones = []

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(BldgSegment, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def default(cls):
        if cls._default:
            return cls._default

        new_obj = cls()
        new_obj.name = "Default Building Segment"

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

    @property
    def mechanicals(self):
        """Return a single Mechanical Object which is a sum of all the Zone Mechanicals"""
        return sum(zone.mechanicals for zone in self.zones)

    def add_zones(self, _zones):
        # type: (list[PHX.bldg_segment.Zone]) -> None
        """Adds new PHX-Zones to the BldgSegment.

        Arguments:
        ----------
            * _zones (list[PHX.bldg_segment.Zone]): The list of new PHX Zones to add to the Bldg Segment

        Returns:
        --------
            * None
        """

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

        if not hasattr(_components, "__iter__"):
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
                    if compo.ext_exposure_zone_id == -1 and compo.int_exposure_zone_id == -1:
                        # -- Its a Shade
                        compo_groups["shades"].append(compo)
                    elif compo.assembly_id_num != -1:
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
                    compo_joined.name = "Component_Group"
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
            merged_zone = reduce(lambda a, b: a + b, self.zones)
            merged_zone.id = 1
            self.zones = [merged_zone]

            # -- Set the appliance Reference Quantity
            # -- As per PHIUS, if the building is single Zone, all appliances
            # -- should be set to 'PH Case' quantity
            for appliance in merged_zone.appliance_set:
                if appliance.type in {1, 2, 3, 7}:
                    appliance.reference_quantity = 1  # PH-Case

            # -- Merge all the Components
            for compo in self.components:
                if compo.ext_exposure_zone_id == -1 and compo.int_exposure_zone_id == -1:
                    # -- It is a Shade, so don't reset its exposure
                    continue
                compo.set_host_zone_name(self.zones[0])

            # Not Implemented Yet:
            # -- Update all the exposure names (for inter-zonal adjacencies)
            # -- Remove interior surfaces (and/or convert to Internal Mass Objects?)

            return None
