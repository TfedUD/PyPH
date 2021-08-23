# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Project Classes
"""

from collections import defaultdict
import PHX._base
import PHX.bldg_segment
import PHX.type_collections
from datetime import datetime
import PHX.type_collections  # .UtilizationPatternsVentilationCollection()


class Date(PHX._base._Base):
    def __init__(self):
        super(Date, self).__init__()
        self.Year = datetime.now().year
        self.Month = datetime.now().month
        self.Day = datetime.now().day
        self.Hour = datetime.now().hour
        self.Minutes = datetime.now().minute


class ProjectData(PHX._base._Base):
    def __init__(self):
        super(ProjectData, self).__init__()
        self.xml_tag = ("ProjectData",)
        self.cN = "Client Name"
        self.cLoc = ""
        self.cPostC = ""
        self.cStr = ""
        self.cTel = "000-000-0000"
        self.cEmail = "client@email.com"
        self.bN = ""
        self.bYCon = "2021"
        self.bLoc = "Town"
        self.bPostC = "zip"
        self.bStr = "Address"
        self.oIsC = False
        self.oN = ""
        self.oLoc = ""
        self.oPostC = ""
        self.oStreet = ""
        self.rN = ""
        self.rLoc = ""
        self.rPostC = ""
        self.rStr = ""
        self.rTel = ""
        self.rLic = ""
        self.rEmail = ""
        self.date = Date()
        self.wBkg = True


class Project(PHX._base._Base):
    def __init__(self):
        super(Project, self).__init__()
        self.data_version = 48
        self.unit_system = 1
        self.progVers = "3.2.0.1"
        self.calcScope = 3
        self.dimVisGeom = 2
        self.projD = ProjectData()
        self.lMaterial = []
        self.lAssembly = []
        self.lWindow = []
        self.lSolProt = []
        self.lOverhang = []
        # self.lUtilNResPH = []
        self.utilization_patterns = PHX.type_collections.Occupancy_Util_Pattern_Collection()
        self.lUtilVentPH = PHX.type_collections.Ventilation_Util_Pattern_Collection()
        self.lFile = []
        self.timeProf = {}
        self._bldg_segments = {}

    @property
    def lBldgSegments(self):
        return self._bldg_segments.values()

    def add_segment(self, *args) -> None:
        for seg in args:
            if isinstance(seg, PHX.bldg_segment.BldgSegment):
                self._bldg_segments[seg.identifier] = seg
            else:
                msg = "Error: Input must be type PHX.bldg_segment.BldgSegment." 'Got: "{}"'.format(seg)
                raise TypeError(msg)

    def get_segment_by_identifier(self, _identifier):
        for seg in self.lBldgSegments:
            if str(seg.identifier) == str(_identifier):
                return seg
        else:
            return None

    def add_assemblies_from_collection(self, _assmbly_c: PHX.type_collections.AssemblyCollection) -> None:
        """Extends the lAssembly list with all of the Assemblies from an
            AssemblyCollection Object

        Arguments:
        ----------
            * _assmbly_c (PHX.type_collections.AssemblyCollection): The
                PHX.type_collections.AssemblyCollection to get the Assemblies from

        Returns:
        --------
            * None
        """
        self.lAssembly.extend(_assmbly_c.project_assemblies)

    def add_window_types_from_collection(self, _win_type_c: PHX.type_collections.WindowTypeCollection) -> None:
        """Extends the lWindow list with all of the window_types from an
            PHX.type_collections.AssemblyCollection Object

        Arguments:
        ----------
            * _win_type_c (PHX.type_collections.WindowTypeCollection): The
                WindowTypeCollection to get the WindowTypes from

        Returns:
        --------
            * None
        """
        self.lWindow.extend(_win_type_c.window_types)

    def collect_utilization_patterns_from_zones(self):
        """Set the Project Utilization Patterns based on the values in the
        BldgSegment / Zones / Rooms
        """

        for v in self.lBldgSegments:
            for z in v.zones:
                for r in z.spaces:
                    self.lUtilVentPH.add_to_collection(r.ventilation.utilization_pattern)
