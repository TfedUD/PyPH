# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*

"""
PHX Window Type Classes
"""

import PHX._base


class WindowFrame(PHX._base._Base):
    def __init__(self):
        super(WindowFrame, self).__init__()
        self.frame_width = 0.1
        self.frame_u_factor = 1
        self.frame_psi_glazing = 0.04
        self.frame_psi_install = 0.04


class WindowType(PHX._base._Base):

    _count = 0

    def __init__(self):
        super(WindowType, self).__init__()
        self.id = self._count
        self.idDB = None
        self.name = "default_window_type"
        self.detU = True
        self.detGd = False
        self.Uw = 2.5
        self.frF = 0.75
        self.trHem = 0.5
        self.secDispH = None
        self.lwEmis = 0.8
        self.glazU = 2.5
        self.Ufr = 2.5
        self.trHemShade = None
        self.frSWAbs = 0.5
        self.frEmisE = 0.8
        self.frEmisI = 0.8
        self.gtr = 0.4
        self.lAngleTr = []
        self.lWLayer = []
        self.lrtbFrW = [None, None, None, None]
        self.lrtbFrU = [None, None, None, None]
        self.lrtbGlPsi = [None, None, None, None]
        self.lrtbFrPsi = [None, None, None, None]

    def __new__(cls, *args, **kwargs):
        """Used so I can keep a running tally for the id variable"""
        cls._count += 1
        return super(WindowType, cls).__new__(cls, *args, **kwargs)

    def add_new_frame_element(self, _frame, _edge_id="L"):
        if not _frame:
            return

        frame_positions = {
            "L": 0,
            "R": 1,
            "T": 2,
            "B": 3,
        }

        # -- Which frame edge to set
        frame_pos = frame_positions.get(str(_edge_id).upper(), 0)

        self.lrtbFrW[frame_pos] = _frame.frame_width
        self.lrtbFrU[frame_pos] = _frame.frame_u_factor
        self.lrtbGlPsi[frame_pos] = _frame.frame_psi_glazing
        self.lrtbFrPsi[frame_pos] = _frame.frame_psi_install
