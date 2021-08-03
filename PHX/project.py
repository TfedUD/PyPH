# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Project Classes
"""

import PHX._base
import PHX.type_collections
from datetime import datetime
import PHX.type_collections#.UtilizationPatternsVentilationCollection()

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
        self.xml_tag = 'ProjectData', 
        self.cN = 'Client Name'
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
        self.lUtilNResPH = []
        self.lUtilVentPH = PHX.type_collections.CVent_Util_Patterns()
        self.lFile = []
        self.timeProf = {}
        self.lVariant = []
    
    def add_variant(self, *args) -> None:
        for var in args:
            self.lVariant.append( var )

    def add_assemblies_from_collection(self, _assmbly_c: PHX.type_collections.AssemblyCollection) -> None:
        """Extends the lAssembly list with all of the Assemblies from an AssemblyCollection Object
        
        Arguments:
        ----------
            * _assmbly_c (PHX.type_collections.AssemblyCollection): The PHX.type_collections.AssemblyCollection to get the Assemblies from 
        
        Returns:
        --------
            * None
        """
        self.lAssembly.extend( _assmbly_c.project_assemblies )

    def add_window_types_from_collection(self, _win_type_c: PHX.type_collections.WindowTypeCollection) -> None:
        """Extends the lWindow list with all of the window_types from an PHX.type_collections.AssemblyCollection Object
        
        Arguments:
        ----------
            * _win_type_c (PHX.type_collections.WindowTypeCollection): The WindowTypeCollection to get the WindowTypes from 
        
        Returns:
        --------
            * None
        """
        self.lWindow.extend( _win_type_c.window_types )

    # def add_vent_utilization_patterns_from_collection( self, _util_pattern_c:PHX.type_collections.UtilizationPatternsVentilationCollection) -> None:
    #     self.lUtilVentPH.extend( _util_pattern_c.utilization_patterns )



