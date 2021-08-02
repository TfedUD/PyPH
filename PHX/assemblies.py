# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""
PHX Material and Assembly / Construction Classes.
"""

import PHX._base

class Material(PHX._base._Base):
    
    _count = 1

    def __init__(self):
        super(Material, self).__init__()
        self.id = self._count
        self.idDB = None
        self.n = 'default_material'
        self.tConD = 1
        self.densB = 50
        self.poros = 0.95
        self.hCapS = 1000
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
        """Used so I can keep a running tally for the id variable """
        cls._count += 1
        return super(Material, cls).__new__(cls, *args, **kwargs)

class Layer(PHX._base._Base):

    _count = 0

    def __init__(self):
        super(Layer, self).__init__()
        self.id = self._count
        self.thickness = 0.0254
        self.material = Material()
    
    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable """
        cls._count += 1
        return super(Layer, cls).__new__(cls, *args, **kwargs)

class Assembly(PHX._base._Base):
    _count = 0

    def __init__(self):
        self.id = self._count
        self.n = 'default_assembly'
        self.Order_Layers = 2
        self.Grid_Kind = 2
        self.Layers = []
    
    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable """
        cls._count += 1
        return super(Assembly, cls).__new__(cls, *args, **kwargs)

    def add_layer(self, _layer: Layer) -> None:
        """Add a new Layer to the Assembly
        
        Arguments:
        ----------
            * _layer (Layer): The new Layer object to add to the Assembly
        
        Returns:
        --------
            * None
        """
        if not _layer:
            return

        if not isinstance(_layer, Layer):
            raise TypeError(f'Error: add_layer() only accepts "Layer" Objects. Got: {_layer}, type="{type(_layer)}"')
        
        self.Layers.append( _layer )


