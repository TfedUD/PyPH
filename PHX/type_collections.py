# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Type Collection Classes for organizing Assembly, Window and Utilization Patterns
"""

import PHX.assemblies
import PHX.window_types
import PHX.utilization_patterns
import PHX._base

class UtilizationPatternsVentilationCollection(PHX._base._Base):
    def __init__(self):
        super(UtilizationPatternsVentilationCollection, self).__init__()
        self._utilization_patterns = {}
    
    @property
    def utilization_patterns(self):
        return self._utilization_patterns.values()
   
    def add_new_utilization_pattern_to_collection(self, _utilization_pattern: PHX.utilization_patterns.UtilizationVentilationPattern) -> None:
        """Adds a PHX.utilization_patterns.UtilizationVentilationPattern to the collection's dictionary 
        
        Arguments:
        ----------
            * _utilization_pattern (PHX.utilization_patterns.UtilizationVentilationpattern): 
                The new PHX.utilization_patterns.UtilizationVentilationpattern to add to the collection
        Returns:
        --------
            * None
        """
        self._utilization_patterns[ _utilization_pattern.identifier ] = _utilization_pattern

    def get_utiliztion_pattern_by_identifier( self, _utilization_pattern_identifier: str ) -> PHX.utilization_patterns.UtilizationVentilationPattern:
        """Searches the PHX.utilization_patterns.UtilizationPatternsVentilationCollection 
            for a Utilization Pattern with a specific Identifier Key
        
        Arguments:
        ----------
            * _utilization_pattern_identifier (str): The PHX.assemblies.Assembly Identifier to search for
        
        Returns:
        --------
            * (PHX.utilization_patterns.UtilizationVentilationPattern): The 
                PHX.utilization_patterns.UtilizationPattern Object matching the 
                input Identifier, or None if not found
        """
        
        return self._utilization_patterns.get( _utilization_pattern_identifier )

class WindowTypeCollection(PHX._base._Base):
        
    def __init__(self):
        super(WindowTypeCollection, self).__init__()
        self._window_types = {}
    
    @property
    def window_types(self):
        return self._window_types.values()

    def add_new_window_type_to_collection(self, _window_type: PHX.window_types.WindowType) -> None:
        """Adds a WindowType to the collection dictionary 
        
        Arguments:
        ----------
            * _window_type (PHX.window_types.WindowType): The new WindowType to add to the collection
        Returns:
        --------
            * None
        """
        self._window_types[ _window_type.identifier ] = _window_type

    def get_window_type_by_identifier( self, _window_type_identifier: str ) -> PHX.window_types.WindowType:
        """Searches the WindowTypeCollection for a WindowType with a specific Identiier Key
        
        Arguments:
        ----------
            * _window_type_identifier (str): The Assembly Identifier to search for
        
        Returns:
        --------
            * (PHX.window_types.WindowType): The WindowType Object matching the input Identifier, or None if not found
        """
        
        return self._window_types.get( _window_type_identifier )

class AssemblyCollection(PHX._base._Base):
    """Collection of all the Assemblies in the Project
    
    Attributes:
    -----------
        * project_assemblies (dict): A Dictionary of all the Assemblies in the
            Collection, with the key=Assembly Name, value=Assembly
    """
    
    def __init__(self):
        super(AssemblyCollection, self).__init__()
        self._project_assemblies = {}

    @property
    def project_assemblies(self):
        return self._project_assemblies.values()

    def get_assembly_by_name(self, _assembly_name: str) -> PHX.assemblies.Assembly:
        """Searches the AssemblyCollection for an Assembly with a specific Name
        
        Arguments:
        ----------
            * _assembly_name (str): The Assembly Name to search for
        
        Returns:
        --------
            * (PHX.assemblies.Assembly): The Assembly matching the input Name, or None if not found
        """
        
        return self._project_assemblies.get( _assembly_name )

    def add_new_assembly_to_collection(self, _assembly: PHX.assemblies.Assembly) -> None:
        """Adds an Assembly to the collection dictionary 
        
        Arguments:
        ----------
            * _assembly (PHX.assemblies.Assembly): The new Assembly to add to the collection
        Returns:
        --------
            * None
        """
        self._project_assemblies[_assembly.identifier] = _assembly
