# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Material and Assembly / Construction Classes.
"""

import PHX._base
import PHX.serialization.from_dict


class LayerTypeError(Exception):
    def __init__(self, _in):
        self.message = (
            'Error: Assembly.add_layer() only accepts "PHX.assemblies.Layer" Objects. Got: {}, type="{}"'.format(
                _in, type(_in)
            )
        )
        super(LayerTypeError, self).__init__(self.message)


class MaterialTypeError(Exception):
    def __init__(self, _in):
        self.message = (
            'Error: Layer "material" only accepts "PHX.assemblies.Material" Objects. Got: {}, type="{}"'.format(
                _in, type(_in)
            )
        )
        super(MaterialTypeError, self).__init__(self.message)


class Material(PHX._base._Base):

    _count = 0

    def __init__(self):
        super(Material, self).__init__()
        self.id = self._count
        self.idDB = None
        self.n = None
        self.tConD = None
        self.densB = None
        self.poros = 0.95
        self.hCapS = None
        self.difRes = 1
        self.refWC = 0
        self.freeWSat = None
        self.wACoef = None
        self.tConSupM = None
        self.tConSupT = None
        self.typMC = None
        self.typeSA = None
        self.color = None
        self.lRHWC = None
        self.lnWCSuc = None
        self.lnWCRed = None
        self.lnWCTCond = None
        self.lRHDiffRes = None
        self.lTEnth = None
        self.lTtCond = None
        self.RHWCGen = None
        self.nWCSucGen = None
        self.nWCRedGen = None
        self.nWCtCondGen = None
        self.TtCondGen = None

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(Material, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_dict(cls, _dict):
        return PHX.serialization.from_dict._Material(cls, _dict)


class Layer(PHX._base._Base):

    _count = 0

    def __init__(self):
        super(Layer, self).__init__()
        self.id = self._count
        self.thickness = 0.0254
        self._material = Material()

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, _in):
        if not isinstance(_in, Material):
            raise MaterialTypeError(_in)

        self._material = _in

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(Layer, cls).__new__(cls, *args, **kwargs)


class Assembly(PHX._base._Base):
    _count = 0

    def __init__(self):
        self.id = self._count
        self.n = "default_assembly"
        self.Order_Layers = 2
        self.Grid_Kind = 2
        self.Layers = []

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(Assembly, cls).__new__(cls, *args, **kwargs)

    def add_layer(self, _layer):
        # type: (Layer) -> None
        """Add a new Layer to the Assembly

        Arguments:
        ----------
           * _layer (PHX.assemblies.Layer): The new Layer object to add to the Assembly

        Returns:
        --------
           * None
        """
        if not isinstance(_layer, Layer):
            raise LayerTypeError(_layer)

        self.Layers.append(_layer)
