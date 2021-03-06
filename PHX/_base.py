# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
Base class for all PHX Objects. Note, this includes the to_dict() method but not 
the from_dict() method due to circular import problems.
"""

import uuid
import PHX.serialization.to_dict


class _Base(object):
    """PHX Object Base class."""

    def __init__(self):
        self.identifier = uuid.uuid4()
        self.user_data = {}

    @property
    def identifier_short(self):
        return str(self.identifier).split("-")[0]

    def __new__(cls, *args, **kwargs):
        """Included so that subclasses can customize their own __new__"""
        return super(_Base, cls).__new__(cls)

    def to_dict(self):
        """Serialize the Object into a dictionary

        Returns:
        --------
            * (dict) A dictionary with all the relevant object attributes
        """

        module = self.__class__.__module__
        class_name = self.__class__.__name__
        func = getattr(PHX.serialization.to_dict, "_{}".format(class_name))
        return func(self)

    def __str__(self):
        return "PHX_{}: ID-{}".format(self.__class__.__name__, self.identifier_short)

    def ToString(self):
        return str(self)

    def __repr__(self):
        return "{}(identifier={!r}, user_data={!r})".format(
            self.__class__.__name__, self.identifier_short, self.user_data
        )
