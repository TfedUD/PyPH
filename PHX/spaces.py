# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Space (Room) and Floor Area (iCFA / TFA) Classes
"""

import PHX._base
import PHX.serialization.from_dict
import PHX.occupancy
import PHX.lighting
import PHX.ventilation

# -- Errors
# ------------------------------------------------------------------------------
class SpaceVentilationInputError(Exception):
    def __init__(self, _in):
        self.message = (
            "Error: Please input PHX.ventilation.SpaceVentilation objects for"
            "FloorSegment 'ventilation'. Got: {}, type: {}".format(_in, type(_in))
        )
        super(SpaceVentilationInputError, self).__init__(self.message)


class FloorAreaWeightingInputError(Exception):
    def __init__(self):
        self.message = (
            "Error: Please set the Floor Segment's 'floor_area_gross' and 'weighting_factor' only."
            "Setting the 'floor_area_weighted' attribute directly is not allowed."
        )
        super(FloorAreaWeightingInputError, self).__init__(self.message)


class WeightingFactorInputError(Exception):
    def __init__(self, _in):
        self.message = (
            'Error: Cannot set FloorSegment "weighting_factor" to value: "{}".'
            "Input only numeric values between 0-1".format(_in)
        )
        super(WeightingFactorInputError, self).__init__(self.message)


class FloorAreaGrossInputError(Exception):
    def __init__(self, _in):
        self.message = (
            'Error: Cannot set FloorSegment "floor_area_gross" to value: "{}". Input only numeric values'.format(_in)
        )
        super(FloorAreaGrossInputError, self).__init__(self.message)


class VolumeMissingFloorError(Exception):
    def __init__(self, _in):
        self.message = 'Error: Cannot set ventilation for Volume: "{}". No Floor?'.format(_in)
        super(VolumeMissingFloorError, self).__init__(self.message)


class AddVolumeToSpaceNameError(Exception):
    def __init__(self, _name1, _name2):
        self.message = (
            'Error: Cannot add Volume with space_name: "{}" to'
            'Volume with name: "{}". Ensure names are the same before joining.'.format(_name1, _name2)
        )
        super(AddVolumeToSpaceNameError, self).__init__(self.message)


class AddVolumeToSpaceNumberError(Exception):
    def __init__(self, _num1, _num2):
        self.message = (
            'Error: Cannot add Volume with space_number: "{}" to'
            'Volume with number: "{}". Ensure Numbers are the same before joining.'.format(_num1, _num2)
        )
        super(AddVolumeToSpaceNumberError, self).__init__(self.message)


class AddVolumeToSpaceHostZoneIDError(Exception):
    def __init__(self, _num1, _num2):
        self.message = 'Error: Cannot add Volume with Host-Zone: "{}" to Volume with Host-Zone: "{}". Ensure HostZone IDs are the same before joining.'.format(
            _num1, _num2
        )

        super(AddVolumeToSpaceHostZoneIDError, self).__init__(self.message)


# -- Space Classes
# ------------------------------------------------------------------------------
class FloorSegment(PHX._base._Base):
    """An individual segment of floor area with some relevant attributes"""

    def __init__(self):
        super(FloorSegment, self).__init__()
        self._weighting_factor = 1.0
        self._floor_area_gross = 0.0
        self.space_name = None
        self.space_number = None
        self.geometry = []
        self.host_zone_identifier = None

        self.non_res_lighting = None
        self.non_res_motion = None
        self.non_res_usage = None

        self._ventilation = PHX.ventilation.SpaceVentilation()

    @property
    def ventilation(self):
        return self._ventilation

    @ventilation.setter
    def ventilation(self, _in):
        if not isinstance(_in, PHX.ventilation.SpaceVentilation):
            raise SpaceVentilationInputError(_in)

        self._ventilation = _in

    @property
    def weighting_factor(self):
        return self._weighting_factor

    @weighting_factor.setter
    def weighting_factor(self, _in):
        if _in is None:
            return
        try:
            val = float(_in)
            if val > 1.0:
                # In case input is not in decimal %
                self._weighting_factor = val / 100
            else:
                self._weighting_factor = val
        except ValueError:
            raise WeightingFactorInputError(_in)

    @property
    def floor_area_gross(self):
        return self._floor_area_gross

    @floor_area_gross.setter
    def floor_area_gross(self, _in):
        if _in is None:
            return
        try:
            self._floor_area_gross = float(_in)
        except ValueError:
            raise FloorAreaGrossInputError(_in)

    @property
    def floor_area_weighted(self):
        weighting = float(self.weighting_factor)
        fa_gross = float(self.floor_area_gross)

        return float(fa_gross * weighting)

    @floor_area_weighted.setter
    def floor_area_weighted(self, _in):
        """Not allowed"""
        raise FloorAreaWeightingInputError()

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._FloorSegment(cls, _dict)

    @property
    def display_name(self):
        return "{}-{}".format(self.space_number, self.space_name)

    def __str__(self):
        return "PHX_{}: {}".format(self.__class__.__name__, self.display_name)


class Floor(PHX._base._Base):
    """A single Volume's Floor, made of one or more FloorSegments"""

    def __init__(self):
        super(Floor, self).__init__()
        self.floor_segments = []

        self.space_name = None
        self.space_number = None
        self.host_zone_identifier = None

        self.non_res_lighting = None
        self.non_res_motion = None
        self.non_res_usage = None

        self._ventilation = PHX.ventilation.SpaceVentilation()

    @property
    def ventilation(self):
        return self._ventilation

    @ventilation.setter
    def ventilation(self, _in):
        if not isinstance(_in, PHX.ventilation.SpaceVentilation):
            raise SpaceVentilationInputError(_in)

        self._ventilation = _in
        for floor_segment in self.floor_segments:
            floor_segment.ventilation = _in  # -- Keep everything aligned

    @property
    def floor_area_gross(self):
        return sum(seg.floor_area_gross for seg in self.floor_segments)

    @property
    def floor_area_weighted(self):
        return sum(seg.floor_area_weighted for seg in self.floor_segments)

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Floor(cls, _dict)

    @property
    def display_name(self):
        return "{}-{}".format(self.space_number, self.space_name)

    def add_new_floor_segment(self, _new_flr_segs):
        """Adds new FloorSegment(s) to the Floor.floor_segments collection"""

        if not isinstance(_new_flr_segs, list):
            _new_flr_segs = [_new_flr_segs]

        for seg in _new_flr_segs:
            if seg in self.floor_segments:
                return

            self.floor_segments.append(seg)

            self.space_number = self._join_string_values(seg, "space_number")
            self.space_name = self._join_string_values(seg, "space_name")

            self.non_res_lighting = self._join_string_values(seg, "non_res_lighting")
            self.non_res_motion = self._join_string_values(seg, "non_res_motion")
            self.non_res_usage = self._join_string_values(seg, "non_res_usage")

            self.ventilation = self.ventilation + seg.ventilation
            seg.ventilation = self.ventilation  # Ensure equality of all ventilation params

            self.host_zone_identifier = self._join_string_values(seg, "host_zone_identifier")

    @property
    def geometry(self):
        """Return all of the Geometry of all the FloorSegments in a single list"""

        geom = []
        for floor_segment in self.floor_segments:
            geom.extend(floor_segment.geometry)
        return geom

    def _join_string_values(self, _new_flr_seg, _attr_name):
        """Helper Function: Clean join of string attribute values from two FloorSegment Attributes

        Arguments:
        ----------
            * _new_flr_seg (FloorSegment): The FloorSegment to add Attributes from
            * _attr_name (str): The Attribute to join

        Returns:
        --------
            * (str): The joined value
        """

        attr_values = set()

        new_val = getattr(_new_flr_seg, _attr_name, None)
        if new_val == "None":
            new_val = None
        attr_values.add(new_val)

        for each_flr_seg in self.floor_segments:
            exg_val = getattr(each_flr_seg, _attr_name, None)
            if exg_val == "None":
                exg_val = None
            attr_values.add(exg_val)

        if len(attr_values) != 1:
            msg = (
                'Error adding new FloorSegment to {}: Multiple values for "{}" found on the input FloorSegments'
                ' for Spaces: "{}" and ""'.format(
                    self.display_name,
                    _attr_name,
                    self.display_name,
                    _new_flr_seg.display_name,
                )
            )
            raise Exception(msg)

        return list(attr_values)[0]

    def __str__(self):
        return "PHX_{}: {} ({} FloorSegments)".format(
            self.__class__.__name__, self.display_name, len(self.floor_segments)
        )


class Volume(PHX._base._Base):
    """A single Volume, with a single Floor"""

    def __init__(self):
        super(Volume, self).__init__()
        self.space_name = None
        self.space_number = None
        self.host_zone_identifier = None

        self.floor = Floor()
        self._average_ceiling_height = 0.0
        self._volume = 0.0
        self.volume_geometry = []

        self._ventilation = PHX.ventilation.SpaceVentilation()

    @property
    def ventilation(self):
        return self._ventilation

    @ventilation.setter
    def ventilation(self, _in):
        if not self.floor:
            raise VolumeMissingFloorError(self.display_name)

        if not isinstance(_in, PHX.ventilation.SpaceVentilation):
            raise SpaceVentilationInputError(_in)

        self._ventilation = _in
        self.floor.ventilation = _in  # -- Keep everything aligned

    @property
    def floor_area_gross(self):
        return float(self.floor.floor_area_gross)

    @property
    def floor_area_weighted(self):
        return float(self.floor.floor_area_weighted)

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, _in):
        self._volume = float(_in)
        self._average_ceiling_height = float(self._volume / self.floor_area_gross)

    @property
    def average_ceiling_height(self):
        return self._average_ceiling_height

    @average_ceiling_height.setter
    def average_ceiling_height(self, _in):
        self._average_ceiling_height = float(_in)
        self._volume = float(self.floor_area_gross * self._average_ceiling_height)

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Volume(cls, _dict)

    @property
    def display_name(self):
        return "{}-{}".format(self.space_number, self.space_name)

    def set_Floor(self, _floor):
        """Sets the Floor Object for the Volume, sets the Volume's Attributes"""
        #
        #
        #
        #  TODO: Add checks in case non-uniform values are found (ie: new name != old name)
        #
        #
        #
        self.floor = _floor
        self.space_name = _floor.space_name
        self.space_number = _floor.space_number
        self.host_zone_identifier = _floor.host_zone_identifier

        self.ventilation = self.ventilation + _floor.ventilation
        _floor.ventilation = self.ventilation

    def __str__(self):
        return "PHX_{}: {} ({} FloorSegments)".format(
            self.__class__.__name__, self.display_name, len(self.floor.floor_segments)
        )


class Space(PHX._base._Base):
    """
    The 'Space' is the primary spatial unit for a Passive House model. This would roughly
    map to a 'Zone' in EnergyPlus or 'Room' in Honeybee. The main difference is
    that the 'Space' contains information on all its sub-areas (Volumes) and
    TFA/iCFA floor segments and floor areas.

    Space_01
      |
      +-- Volume_01
      |     |
      |     +-- Floor
      |         |
      |         +--FloorSegement_01
      |         +--FloorSegement_02
      |
      +-- Volume_02
      |     |
      |     +-- Floor
      |         |
      |         +--FloorSegement_03
      |         +--FloorSegement_04
      .
    """

    def __init__(self):
        super(Space, self).__init__()
        self.quantity = 1
        self.type = 99  # -- User-Defined
        self.space_name = None
        self.space_number = None
        self.host_zone_identifier = None

        self.volume = 0.0
        self.volumes = []

        self.equipment = None
        self.ventilation = PHX.ventilation.SpaceVentilation()
        self.occupancy = PHX.occupancy.SpaceOccupancy.default()
        self.lighting = PHX.lighting.SpaceLighting.default()

    @property
    def ventilation(self):
        return self._ventilation

    @ventilation.setter
    def ventilation(self, _in):
        if not isinstance(_in, PHX.ventilation.SpaceVentilation):
            raise SpaceVentilationInputError(_in)

        self._ventilation = _in

        # -- Reset all the Volume Ventilations as well
        for volume in self.volumes:
            volume.ventilation = _in

    @property
    def clear_height(self):
        """Return the area-weighted average ceiling height of the Space's volumes"""

        total_gross_areas = 0.0
        total_fa_weighted_clg = 0.0
        for v in self.volumes:
            total_gross_areas += v.floor_area_gross
            total_fa_weighted_clg += v.floor_area_gross * v.average_ceiling_height

        return total_fa_weighted_clg / total_gross_areas

    @property
    def floor_area_weighted(self):
        total = 0.0
        for v in self.volumes:
            total += float(v.floor_area_weighted)

        return total

    @property
    def peak_occupancy(self):
        return float(self.floor_area_weighted) * float(self.occupancy.people_per_area)

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Space(cls, _dict)

    @property
    def display_name(self):
        return "{}-{}".format(self.space_number, self.space_name)

    def add_new_volume(self, _new_volume):
        # type : (PHX.spaces.Space, PHX.spaces.Volume) -> None
        """Adds a new Volume onto the Space. Verifies that the names/numbers/hosts match

        Arguments:
        ---------
            * _new_volume (Volume): The new Volume object to add to the Space

        Returns:
        --------
            * None
        """

        # -- Make sure the new volume can be added to the Space
        if not self.space_name:
            self.space_name = _new_volume.space_name
        else:
            if self.space_name != _new_volume.space_name:
                raise AddVolumeToSpaceNameError(_new_volume.space_name, self.space_name)

        if not self.space_number:
            self.space_number = _new_volume.space_number
        else:
            if self.space_number != _new_volume.space_number:
                raise AddVolumeToSpaceNumberError(_new_volume.space_number, self.space_number)

        if not self.host_zone_identifier:
            self.host_zone_identifier = _new_volume.host_zone_identifier
        else:
            if self.host_zone_identifier != _new_volume.host_zone_identifier:
                raise AddVolumeToSpaceHostZoneIDError(_new_volume.host_zone_identifier, self.host_zone_identifier)

        # -- Set the Space's Ventilation Properties
        # -- This will also ripple down to the FloorSegment level
        # -- resetting all the 'ventilation' objects for all the Objects
        self.ventilation = self.ventilation + _new_volume.ventilation

        # -- Set the Volume's Ventilation Properties
        # -- to ensure that everything matches
        _new_volume.ventilation = self.ventilation

        # -- Update the total numeric Volume (m3)
        self.volume += _new_volume.volume

        # -- Add the new Volume to Space's list
        self.volumes.append(_new_volume)

    def __str__(self):
        return "PHX_{}: {} ({} Volumes)".format(self.__class__.__name__, self.display_name, len(self.volumes))
