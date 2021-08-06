# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PHX Type Collection Classes for organizing Assembly, Window and Ventilization-Utilization Patterns"""

import PHX.assemblies
import PHX.window_types
import PHX.utilization_patterns
import PHX._base


class Collection(PHX._base._Base):
    def __init__(self):
        super(Collection, self).__init__()
        self._items = {}
        self._allowed_types = object

    @property
    def items(self):
        # type: () -> list
        return self._items.values()

    def get_item_by_identifier(self, _identifier):
        # type: (str) -> typing.Any
        return self._items[_identifier]

    def add_to_collection(self, _item):
        # type: (typing.Any) -> None
        if not isinstance(_item, self._allowed_types):
            msg = (
                'Error: Cannot add "{}" to Collection: "{}" only'
                'objects of type: "{}" allowed'.format(
                    type(_item), self.__class__.__name__, self._allowed_types
                )
            )
            raise TypeError(msg)

        self._items[_item.id] = _item


class CVent_Util_Patterns(Collection):
    """Collection of Ventilation Utilization Patterns"""

    def __init__(self):
        super(CVent_Util_Patterns, self).__init__()
        self._allowed_types = PHX.utilization_patterns.UtilizationPattern_Ventilation
        self.add_to_collection(
            PHX.utilization_patterns.UtilizationPattern_Ventilation.default()
        )


class WindowTypeCollection(PHX._base._Base):
    def __init__(self):
        super(WindowTypeCollection, self).__init__()
        self._window_types = {}

    @property
    def window_types(self):
        return self._window_types.values()

    def add_new_window_type_to_collection(
        self, _window_type: PHX.window_types.WindowType
    ) -> None:
        """Adds a WindowType to the collection dictionary

        Arguments:
        ----------
            * _window_type (PHX.window_types.WindowType): The new WindowType to add to the collection
        Returns:
        --------
            * None
        """
        self._window_types[_window_type.identifier] = _window_type

    def get_window_type_by_identifier(
        self, _window_type_identifier: str
    ) -> PHX.window_types.WindowType:
        """Searches the WindowTypeCollection for a WindowType with a specific Identiier Key

        Arguments:
        ----------
            * _window_type_identifier (str): The Assembly Identifier to search for

        Returns:
        --------
            * (PHX.window_types.WindowType): The WindowType Object matching the input Identifier, or None if not found
        """

        return self._window_types.get(_window_type_identifier)


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

        return self._project_assemblies.get(_assembly_name)

    def add_new_assembly_to_collection(
        self, _assembly: PHX.assemblies.Assembly
    ) -> None:
        """Adds an Assembly to the collection dictionary

        Arguments:
        ----------
            * _assembly (PHX.assemblies.Assembly): The new Assembly to add to the collection
        Returns:
        --------
            * None
        """
        self._project_assemblies[_assembly.identifier] = _assembly
