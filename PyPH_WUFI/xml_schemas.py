# -*- coding: utf-8 -*-
# -*- Python Version: 3.x -*-

"""WUFI XML Output fields for all Objects

During export, XML builder will call the 'xml_data' property of each object
which returns a list of XML_Nodes, XML_Objects, or an XML_List, as defined in
each of the functions below.

Note: each function here should have the exact same name as its 'parent' but 
with an underscore in front. ie: '_Variant' maps to the 'Variant' parent class.
"""

from .xml_node import XML_Node, XML_List, XML_Object
from .selection import Selection

def _WindowType(_obj):
	return [			
		XML_Node('IdentNr', _obj.id),
		XML_Node('Name', _obj.n),
		XML_Node('Uw_Detailed', _obj.detU),
		XML_Node('GlazingFrameDetailed', _obj.detGd),
		XML_Node('U_Value', _obj.Uw),
		XML_Node('FrameFactor', _obj.frF),
		XML_Node('SHGC_Hemispherical', _obj.trHem),
		XML_Node('U_Value_Glazing', _obj.glazU),
		XML_Node('U_Value_Frame', _obj.Ufr),
		XML_Node('Frame_Width_Left', _obj.lrtbFrW[0]),
		XML_Node('Frame_U_Left', _obj.lrtbFrU[0]),
		XML_Node('Glazing_Psi_Left', _obj.lrtbGlPsi[0]),
		XML_Node('Frame_Psi_Left', _obj.lrtbFrPsi[0]),
		XML_Node('MeanEmissivity', _obj.frEmisE),
		XML_Node('g_Value', _obj.gtr),
		]
	
def  _UtilizationVentilationPattern(_obj):
	return [
		XML_Node('IdentNr', _obj.id),
		XML_Node('Name', _obj.n),
		XML_Node('OperatingDays', _obj.OperatingDays),
		XML_Node('OperatingWeeks', _obj.OperatingWeeks),
		XML_Node('Maximum_DOS', _obj.Maximum_DOS),
		XML_Node('Maximum_PDF', _obj.Maximum_PDF),
		XML_Node('Standard_DOS', _obj.Standard_DOS),
		XML_Node('Standard_PDF', _obj.Standard_PDF),
		XML_Node('Basic_DOS', _obj.Basic_DOS),
		XML_Node('Basic_PDF', _obj.Basic_PDF),
		XML_Node('Minimum_DOS', _obj.Minimum_DOS),
		XML_Node('Minimum_PDF', _obj.Minimum_PDF),
	]

def _Material(_obj):
	return [
		XML_Node('Name', _obj.n),
		XML_Node('ThermalConductivity', _obj.tConD),
		XML_Node('BulkDensity', _obj.densB),
		XML_Node('Porosity', _obj.poros),
		XML_Node('HeatCapacity', _obj.hCapS),
		XML_Node('WaterVaporResistance', _obj.difRes),
		XML_Node('ReferenceW', _obj.refWC),
	]

def _Layer(_obj):
	return  [
		XML_Node('Thickness', _obj.id),
		XML_Object('Material', _obj.material),
	]

def _Assembly(_obj):
	return [
		XML_Node('IdentNr', _obj.id),
		XML_Node('Name', _obj.n),
		XML_Node( *Selection('Assembly::Order_Layers', _obj.Order_Layers).xml_data ),
		XML_Node( *Selection('Assembly::Grid_Kind', _obj.Grid_Kind).xml_data ),
		XML_List('Layers', [ XML_Object('Layer', _, 'index', i) for i,_ in enumerate(_obj.Layers)]),
	]

def _Vertex(_obj):
	return [
		XML_Node('IdentNr', _obj.id),
		XML_Node('X', round(_obj.x, 8)),
		XML_Node('Y', round(_obj.y, 8)),
		XML_Node('Z', round(_obj.z, 8)),
	]

def _Polygon(_obj):
	return [
		XML_Node('IdentNr', _obj.id),
		XML_Node('NormalVectorX', round(_obj.nVec.x, 10)),
		XML_Node('NormalVectorY', round(_obj.nVec.y, 10)),
		XML_Node('NormalVectorZ', round(_obj.nVec.z, 10)),
		XML_List('IdentNrPoints', [ XML_Node('IdentNr', _, 'index', i) for i,_ in enumerate(_obj.idVert)]),
		XML_List('IdentNrPolygonsInside', [ XML_Node('IdentNr', _, 'index', i) for i,_ in enumerate(_obj.children)]),
		]

def _Geom(_obj):
	return [ 
		XML_List('Vertices', [ XML_Object('Vertix', _, 'index', i) for i,_ in enumerate(_obj.vertices)]),
		XML_List('Polygons', [ XML_Object('Polygon', _, 'index', i) for i,_ in enumerate(_obj.polygons)]),
	]

def _PassivehouseData(_obj):
	return []

def _PH_ClimateLocation(_obj):
    return [        
		XML_Node('Selection', _obj.Selection),
        XML_Node('Latitude', _obj.Latitude),
        XML_Node('HeightNNWeatherStation', _obj.HeightNNWeatherStation),
        XML_Node('Longitude', _obj.Longitude),
        XML_Node('dUTC', _obj.dUTC),
        XML_Node('DailyTemperatureSwingSummer', _obj.DailyTemperatureSwingSummer),
        XML_Node('AverageWindSpeed', _obj.AverageWindSpeed),
        XML_Node('ClimateZone', _obj.ClimateZone),
        XML_Node('GroundThermalConductivity', _obj.GroundThermalConductivity),
        XML_Node('GroundHeatCapacitiy', _obj.GroundHeatCapacitiy),
        XML_Node('GroundDensity', _obj.GroundDensity),
        XML_Node('DepthGroundwater', _obj.DepthGroundwater),
        XML_Node('FlowRateGroundwater', _obj.FlowRateGroundwater),
        XML_Node('SelectionPECO2Factor', _obj.SelectionPECO2Factor),

		XML_List('TemperatureMonthly', [XML_Node('Item', _, 'index', i) for i, _ in enumerate(_obj.TemperatureMonthly)] ),
		XML_List('DewPointTemperatureMonthly', [XML_Node('Item', _, 'index', i) for i, _ in enumerate(_obj.DewPointTemperatureMonthly)] ),
		XML_List('SkyTemperatureMonthly', [XML_Node('Item', _, 'index', i) for i, _ in enumerate(_obj.SkyTemperatureMonthly)] ),
		XML_List('GroundTemperatureMonthly', [XML_Node('Item', _, 'index', i) for i, _ in enumerate(_obj.GroundTemperatureMonthly)] ),
		XML_List('NorthSolarRadiationMonthly', [XML_Node('Item', _, 'index', i) for i, _ in enumerate(_obj.NorthSolarRadiationMonthly)] ),
		XML_List('EastSolarRadiationMonthly', [XML_Node('Item', _, 'index', i) for i, _ in enumerate(_obj.EastSolarRadiationMonthly)] ),
		XML_List('SouthSolarRadiationMonthly', [XML_Node('Item', _, 'index', i) for i, _ in enumerate(_obj.SouthSolarRadiationMonthly)] ),
		XML_List('WestSolarRadiationMonthly', [XML_Node('Item', _, 'index', i) for i, _ in enumerate(_obj.WestSolarRadiationMonthly)] ),
		XML_List('GlobalSolarRadiationMonthly', [XML_Node('Item', _, 'index', i) for i, _ in enumerate(_obj.GlobalSolarRadiationMonthly)] ),
					
		XML_Node('TemperatureHeating1', _obj.peak_heating_1.temp),
		XML_Node('NorthSolarRadiationHeating1', _obj.peak_heating_1.rad_north),
		XML_Node('EastSolarRadiationHeating1', _obj.peak_heating_1.rad_east),
		XML_Node('SouthSolarRadiationHeating1', _obj.peak_heating_1.rad_south),
		XML_Node('WestSolarRadiationHeating1', _obj.peak_heating_1.rad_west),
		XML_Node('GlobalSolarRadiationHeating1', _obj.peak_heating_1.rad_global),

		XML_Node('TemperatureHeating2', _obj.peak_heating_2.temp),
		XML_Node('NorthSolarRadiationHeating2', _obj.peak_heating_2.rad_north),
		XML_Node('EastSolarRadiationHeating2', _obj.peak_heating_2.rad_east),
		XML_Node('SouthSolarRadiationHeating2', _obj.peak_heating_2.rad_south),
		XML_Node('WestSolarRadiationHeating2', _obj.peak_heating_2.rad_west),
		XML_Node('GlobalSolarRadiationHeating2', _obj.peak_heating_2.rad_global),

		XML_Node('TemperatureCooling', _obj.peak_cooling.temp),
		XML_Node('NorthSolarRadiationCooling', _obj.peak_cooling.rad_north),
		XML_Node('EastSolarRadiationCooling', _obj.peak_cooling.rad_east),
		XML_Node('SouthSolarRadiationCooling', _obj.peak_cooling.rad_south),
		XML_Node('WestSolarRadiationCooling', _obj.peak_cooling.rad_west),
		XML_Node('GlobalSolarRadiationCooling', _obj.peak_cooling.rad_global),
		]

def _ClimateLocation(_obj):
	return [
		XML_Node('Selection', _obj.Selection),
		XML_Object('PH_ClimateLocation', _obj.PH_ClimateLocation),
		XML_Node('CatalogueNr_DB', _obj.CatalogueNr_DB),
		XML_Node('MapNr_DB', _obj.MapNr_DB),
		XML_Node('Albedo', _obj.Albedo),
		XML_Node('GroundReflShort', _obj.GroundReflShort),
		XML_Node('GroundReflLong', _obj.GroundReflLong),
		XML_Node('GroundEmission', _obj.GroundEmission),
		XML_Node('CloudIndex', _obj.CloudIndex),
		XML_Node('CO2concenration', _obj.CO2concenration),
		XML_Node('Unit_CO2concentration', _obj.Unit_CO2concentration),
	]

def _WP_Color(_obj):
	return [		
		XML_Node('Alpha', _obj.alpha),
		XML_Node('Red', _obj.red),
		XML_Node('Green', _obj.green),
		XML_Node('Blue', _obj.blue),
		]

def _Component(_obj):
	return [
		XML_Node('IdentNr', _obj.id),
		XML_Node('Name', _obj.n),
		XML_Node('Visual', _obj.visC),
		XML_Node('InnerAttachment', _obj.idIC, 'choice', _obj.nmIC),
		XML_Node(*Selection('Component::OuterAttachment', _obj.idEC).xml_data),
		XML_Node(*Selection('Component::Type', _obj.type).xml_data),
		XML_Node('IdentNrColorI', _obj.id_color_int),
		XML_Node('IdentNrColorE', _obj.id_color_ext),
		XML_Object('ColorExternUserDef', _obj.ud_colog_int),
		XML_Object('ColorInternUserDef', _obj.ud_colog_ext),
		XML_Node('IdentNr_ComponentInnerSurface', _obj.inner_srfc_compo_idNr),
		XML_List('IdentNrPolygons', [ XML_Node('IdentNr', _, 'index', i) for i,_ in enumerate(_obj.polygon_id_list)]),
		XML_Node('IdentNrAssembly', _obj.idAssC),
		XML_Node('IdentNrWindowType', _obj.idWtC),
	]

def _WP_Room(_obj):
	return [
		XML_Node('Name', _obj.n),
		XML_Node( *Selection('WP_Room::Type', _obj.type).xml_data),
		XML_Node('IdentNrUtilizationPatternVent', _obj.idUPatV),
		XML_Node('IdentNrVentilationUnit', _obj.idVUnit),
		XML_Node('Quantity', _obj.quantity),
		XML_Node('DesignVolumeFlowRateSupply', _obj.design_flow_rate_supply),
		XML_Node('DesignVolumeFlowRateExhaust', _obj.design_flow_rate_extract),
	]

def _Zone(_obj):
	return [
		XML_Node('Name', _obj.n),
		XML_Node('IdentNr', _obj.id),
		XML_Node( *Selection('Zone::GrossVolume_Selection', _obj.volume_gross_selection).xml_data ),
		XML_Node('GrossVolume', _obj.volume_gross, 'unit'),
		XML_Node( *Selection('Zone::NetVolume_Selection', _obj.volume_net_selection).xml_data ),
		XML_Node('NetVolume', _obj.volume_net, 'unit'),
		XML_Node( *Selection('Zone::FloorArea_Selection', _obj.floor_area_selection).xml_data ),
		XML_Node('FloorArea', _obj.floor_area, 'unit'),
		XML_Node( *Selection('Zone::ClearanceHeight_Selection', _obj.clearance_height_selection).xml_data ),
		XML_Node('ClearanceHeight', _obj.clearance_height, 'unit', 'm'),
		XML_Node( *Selection('Zone::SpecificHeatCapacity_Selection', _obj.spec_heat_cap_selection).xml_data ),
		XML_Node('SpecificHeatCapacity', _obj.spec_heat_cap, 'unit', 'Wh/m²K'),
		XML_List('RoomsVentilation', [XML_Object('Room', _, 'index', i) for i, _ in enumerate(_obj.rooms_ventilation)]),
		XML_List('HomeDevice', [XML_Node('Device', _, 'index', i) for i, _ in enumerate(_obj.appliances)]),
	]

def _Building(_obj):
    return [
		XML_Node('Numerics', _obj.numerics),
		XML_Node('AirFlowModel', _obj.airflow_model),
		XML_List('Components', [XML_Object('Component', _, 'index', i) for i, _ in enumerate(_obj.lComponent)]),
		XML_List('Zones', [XML_Object('Zone', _, 'index', i) for i, _ in enumerate(_obj.lZone)] ),
		XML_Node('CountGenerated', _obj.count_generator),
		XML_Node('HasBeenGenerated', _obj.has_been_generated),
		XML_Node('HasBeenChangedSinceLastGeneration', _obj.has_been_changed_since_last_gen),
		]

def _HVAC_PH_Parameters(_obj):
	return [
		XML_Node('HumidityRecoveryEfficiency', _obj.HumidityRecoveryEfficiency),
		XML_Node('ElectricEfficiency', _obj.ElectricEfficiency),
		XML_Node('FrostProtection', _obj.FrostProtection),
		XML_Node('Quantity', _obj.Quantity),
		XML_Node('ElectricEfficiency', _obj.ElectricEfficiency),
		XML_Node('SubsoilHeatExchangeEfficiency', _obj.SubsoilHeatExchangeEfficiency),
		XML_Node('HumidityRecoveryEfficiency', _obj.HumidityRecoveryEfficiency),
		XML_Node('VolumeFlowRateFrom', _obj.VolumeFlowRateFrom),
		XML_Node('VolumeFlowRateTo', _obj.VolumeFlowRateTo),
		XML_Node('TemperatureBelowDefrostUsed', _obj.TemperatureBelowDefrostUsed),
		XML_Node('FrostProtection', _obj.FrostProtection),
		XML_Node('DefrostRequired', _obj.DefrostRequired),
		XML_Node('NoSummerBypass', _obj.NoSummerBypass),
		XML_Node('HRVCalculatorData', _obj.HRVCalculatorData),
		XML_Node('Maximum_VOS', _obj.Maximum_VOS),
		XML_Node('Maximum_PP', _obj.Maximum_PP),
		XML_Node('Standard_VOS', _obj.Standard_VOS),
		XML_Node('Standard_PP', _obj.Standard_PP),
		XML_Node('Basic_VOS', _obj.Basic_VOS),
		XML_Node('Basic_PP', _obj.Basic_PP),
		XML_Node('Minimum_VOS', _obj.Minimum_VOS),
		XML_Node('Minimum_PP', _obj.Minimum_PP),
		XML_Node('AuxiliaryEnergy', _obj.AuxiliaryEnergy),
		XML_Node('AuxiliaryEnergyDHW', _obj.AuxiliaryEnergyDHW),
		XML_Node('InConditionedSpace', _obj.InConditionedSpace),
	]

def _HVAC_Device(_obj):
	return [
		XML_Node('Name', _obj.Name),
		XML_Node('IdentNr', _obj.IdentNr),
		XML_Node(*Selection('HVAC_Device::SystemType', _obj.SystemType).xml_data),
		XML_Node(*Selection('HVAC_Device::TypeDevice', _obj.TypeDevice).xml_data),
		XML_Node('UsedFor_Heating', _obj.UsedFor_Heating),
		XML_Node('UsedFor_DHW', _obj.UsedFor_DHW),
		XML_Node('UsedFor_Cooling', _obj.UsedFor_Cooling),
		XML_Node('UsedFor_Ventilation', _obj.UsedFor_Ventilation),
		XML_Node('UsedFor_Humidification', _obj.UsedFor_Humidification),
		XML_Node('UsedFor_Dehumidification', _obj.UsedFor_Dehumidification),
		XML_Node('Ventilation_Parameters', _obj.Ventilation_Parameters),
		XML_Node('UseOptionalClimate', _obj.UseOptionalClimate),
		XML_Node('IdentNr_OptionalClimate', _obj.IdentNr_OptionalClimate),
		XML_Object('PH_Parameters', _obj.PH_Parameters),
		XML_Node('HeatRecovery', _obj.HeatRecovery),
		XML_Node('MoistureRecovery', _obj.MoistureRecovery),
	]

def _HVAC_System_ZoneCover(_obj):
	return [
		XML_Node('IdentNrZone', _obj.n),
		XML_Node('CoverageHeating', _obj.czHCVHD[0]),
		XML_Node('CoverageCooling', _obj.czHCVHD[1]),
		XML_Node('CoverageVentilation', _obj.czHCVHD[2]),
		XML_Node('CoverageHumidification', _obj.czHCVHD[3]),
		XML_Node('CoverageDehumidification', _obj.czHCVHD[4]),
	]

def _HVAC_System(_obj):
	return [
		XML_Node('Name', _obj.n),
		XML_Node(*Selection('HVAC_System::Type', _obj.typeSys).xml_data),
		XML_Node('IdentNr', _obj.id),
		XML_List('ZonesCoverage', [XML_Object('ZoneCoverage', _, 'index', i) for i, _ in enumerate(_obj.lZoneCover)]),
		XML_List('Devices', [XML_Object('Device', _, 'index', i) for i, _ in enumerate(_obj.lDevice)]),
		XML_Node('Distribution', _obj.distrib),
		XML_Node('PHDistribution', _obj.PHdistrib),
	]

def _HVAC(_obj):
    return [
		XML_List('Systems', [XML_Object('System', _, 'index', i) for i, _ in enumerate(_obj.lSystem)]),
	]

def _Variant(_obj):
	return [ 
		XML_Node('IdentNr', _obj.id),
		XML_Node('Name', _obj.n),
		XML_Node('Remarks', _obj.remarks),
		XML_Object('Graphics_3D', _obj.geom),
		XML_Object('ClimateLocation', _obj.cliLoc),
		XML_Object('Building', _obj.building),
		XML_Object('PassivehouseData', _obj.PHIUS),
		XML_Node('PlugIn', _obj.plugin),
		XML_Object('HVAC', _obj.HVAC),
		]

def _Date(_obj):
	return [
		XML_Node('Year', _obj.Year),
		XML_Node('Month', _obj.Month),
		XML_Node('Day', _obj.Day),
		XML_Node('Hour', _obj.Hour),
		XML_Node('Minutes', _obj.Minutes),
		]

def _ProjectData(_obj):
    return [
		XML_Node('Customer_Name', _obj.cN),
		XML_Node('Customer_Locality', _obj.cLoc),
		XML_Node('Customer_PostalCode', _obj.cPostC),
		XML_Node('Customer_Street', _obj.cStr),
		XML_Node('Customer_Tel', _obj.cTel),
		XML_Node('Customer_Email', _obj.cEmail),
		XML_Node('Building_Name', _obj.bN),
		XML_Node('Year_Construction', _obj.bYCon),
		XML_Node('Building_Locality', _obj.bLoc),
		XML_Node('Building_PostalCode', _obj.bPostC),
		XML_Node('Building_Street', _obj.bStr),
		XML_Node('OwnerIsClient', _obj.oIsC),
		XML_Node('Owner_Name', _obj.oN),
		XML_Node('Owner_Locality', _obj.oLoc),
		XML_Node('Owner_PostalCode', _obj.oPostC),
		XML_Node('Owner_Street', _obj.oStreet),
		XML_Node('Responsible_Name', _obj.rN),
		XML_Node('Responsible_Locality', _obj.rLoc),
		XML_Node('Responsible_PostalCode', _obj.rPostC),
		XML_Node('Responsible_Street', _obj.rStr),
		XML_Node('Responsible_Tel', _obj.rTel),
		XML_Node('Responsible_LicenseNr', _obj.rLic),
		XML_Node('Responsible_Email', _obj.rEmail),
		XML_Object('Date_Project', _obj.date),
		XML_Node('WhiteBackgroundPictureBuilding', _obj.wBkg),
		]

def _Project(_obj):
	return [
		XML_Node('DataVersion', _obj.data_version),
        XML_Node('UnitSystem', _obj.unit_system),
		XML_Node('ProgramVersion', _obj.progVers),
		XML_Node('Scope', _obj.calcScope),
		XML_Node('DimensionsVisualizedGeometry', _obj.dimVisGeom),
		XML_Object('ProjectData', _obj.projD),
		XML_List('Assemblies', [XML_Object('Assembly', _, 'index', i) for i, _ in enumerate(_obj.lAssembly)] ),
		XML_List('WindowTypes', [XML_Object('WindowType', _, 'index', i) for i, _ in enumerate(_obj.lWindow)] ),
		XML_List('SolarProtectionTypes', _obj.lSolProt),
		XML_List('UtilisationPatternsVentilation', [XML_Object('UtilizationPatternVent', _, 'index', i) for i, _ in enumerate(_obj.lUtilVentPH)] ),
		XML_List('Variants', [XML_Object('Variant', _, 'index', i) for i, _ in enumerate(_obj.lVariant)] ),
	]