from PyPH_WUFI.xml_node import XML_List
import PHX.appliances
import PyPH_WUFI.xml_object_data
import PyPH_WUFI.build_WUFI_xml


def test_basic_appliance_xml():
    new_appliance = PHX.appliances.Appliance()
    new_appliance.energy_demand = 100

    xml_text = PyPH_WUFI.build_WUFI_xml.create_project_xml_text(new_appliance)
    print(xml_text)

    assert '<EnergyDemandNorm unit="kWh">100</EnergyDemandNorm>' in xml_text
    # assert ... Other stuff about the XML text?
