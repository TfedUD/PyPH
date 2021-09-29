# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""PyPH_WUFI classes to organize 'Type' Collections up at the Project level"""

import PHX.assemblies
import PHX.window_types
import PyPH_WUFI.utilization_patterns


class AddToCollectionError(Exception):
    def __init__(self, _in, _class_nm, _allowed_types):
        self.message = 'Error: Cannot add "{}" to Collection: "{}" only objects of type: "{}" allowed'.format(
            type(_in), _class_nm, _allowed_types
        )
        super(AddToCollectionError, self).__init__(self.message)


class Collection:
    """Collection base class"""

    def __init__(self):
        super(Collection, self).__init__()
        self._items = {}
        self._allowed_types = object

    def __iter__(self):
        for _ in self.items:
            yield _

    @property
    def items(self):
        # type: () -> list
        return self._items.values()

    def get_item_by_identifier(self, _identifier):
        # type: (str) -> object
        return self._items[_identifier]

    def add_to_collection(self, _item, _key=None, _reset_count=False):
        # type: (object, str | None, bool) -> None
        """Add a new Item (of allowed type) to the Collection.

        Arguments:
        ----------
            * _item (Any): The new Object to add to the Collection
            * _key (str | None): The key to use for the item dict
            * _reset_count (bool): True=Reset the item's .id attr to match the Collection

        Returns:
        --------
            * None
        """

        if not isinstance(_item, self._allowed_types):
            raise AddToCollectionError(_item, self.__class__.__name__, self._allowed_types)

        if _key:
            if _key not in self._items.keys():
                if _reset_count:
                    _item.id = len(self._items.keys()) + 1
                self._items[_key] = _item
            else:
                if _reset_count:
                    _item.id = self._items[_key].id
        elif hasattr(_item, "id"):
            self._items[_item.id] = _item

        else:
            self._items[id(_item)] = _item


class UtilPat_Collection_Ventilation(Collection):
    def __init__(self):
        super(UtilPat_Collection_Ventilation, self).__init__()
        self._allowed_types = PyPH_WUFI.utilization_patterns.UtilizationPattern_Vent


class UtilizationPatternCollection_PH_NonRes(Collection):
    def __init__(self):
        super(UtilizationPatternCollection_PH_NonRes, self).__init__()
        self._allowed_types = PyPH_WUFI.utilization_patterns.UtilizationPattern_NonRes


class WindowTypeCollection:
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
        self._window_types[_window_type.identifier] = _window_type

    def get_window_type_by_identifier(self, _window_type_identifier: str) -> PHX.window_types.WindowType:
        """Searches the WindowTypeCollection for a WindowType with a specific Identiier Key

        Arguments:
        ----------
            * _window_type_identifier (str): The Assembly Identifier to search for

        Returns:
        --------
            * (PHX.window_types.WindowType): The WindowType Object matching the input Identifier, or None if not found
        """

        return self._window_types.get(_window_type_identifier)


class AssemblyCollection:
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
