import PHX.mechanicals.equipment


def test_EquipmentSet_serialization_empty(reset_mechanicals):
    o1 = PHX.mechanicals.equipment.EquipmentSet()
    d = o1.to_dict()

    o2 = PHX.mechanicals.equipment.EquipmentSet.from_dict(d)
    assert d == o2.to_dict()


def test_EquipmentSet_serialization_with_vent(reset_mechanicals):
    o1 = PHX.mechanicals.equipment.EquipmentSet()
    v1 = PHX.mechanicals.equipment.HVAC_Ventilator()
    o1.add_new_device_to_equipment_set(v1)
    d = o1.to_dict()

    o2 = PHX.mechanicals.equipment.EquipmentSet.from_dict(d)
    assert d == o2.to_dict()


def test_HVAC_Device_serialization(reset_mechanicals):
    o1 = PHX.mechanicals.equipment.HVAC_Device()
    d = o1.to_dict()

    o2 = PHX.mechanicals.equipment.HVAC_Device.from_dict(d)
    assert d == o2.to_dict()


def test_HVAC_Ventilator_serialization(reset_mechanicals):
    o1 = PHX.mechanicals.equipment.HVAC_Ventilator()
    d = o1.to_dict()

    o2 = PHX.mechanicals.equipment.HVAC_Ventilator.from_dict(d)
    assert d == o2.to_dict()


def test_HVAC_Ventilator_Default_serialization(reset_mechanicals):
    o1 = PHX.mechanicals.equipment.HVAC_Ventilator.default()
    d = o1.to_dict()

    o2 = PHX.mechanicals.equipment.HVAC_Ventilator.from_dict(d)
    assert d == o2.to_dict()


def test_HVAC_Ventilator_PH_Parameters_serialization(reset_mechanicals):
    o1 = PHX.mechanicals.equipment.HVAC_Ventilator_PH_Parameters()
    d = o1.to_dict()

    o2 = PHX.mechanicals.equipment.HVAC_Ventilator_PH_Parameters.from_dict(d)
    assert d == o2.to_dict()
