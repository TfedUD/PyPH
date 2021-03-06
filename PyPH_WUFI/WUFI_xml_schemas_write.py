# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""WUFI XML Output structure for all Objects

During export, XML builder will search this module and return the schema
function for the PHX object. The schema function returns a list of XML_Nodes,
XML_Objects, or an XML_List, as defined in each of the functions below.

Note: each function here should have the exact same name as its 'parent' but 
with an underscore in front. ie: '_Variant' maps to the 'Variant' parent class.
"""

from PHX.mechanicals.systems import Mechanicals
import PHX.climate
from PHX.project import Project
from PHX.bldg_segment import BldgSegment, Zone
from PHX.appliances import Appliance

import PyPH_WUFI.xml_node
from PyPH_WUFI.xml_node import xml_writable
import PyPH_WUFI.selection
import PyPH_WUFI.WUFI_xml_convert_phx
from PyPH_WUFI.WUFI_xml_conversion_classes import (
    temp_Space,
    temp_MechanicalSystemsGroup,
    temp_MechanicalDevice,
    temp_PH_Climate,
    temp_PassiveHouseData,
    temp_PH_Building,
    temp_PH_Building_Internal_Gains,
    temp_Building,
    UtilizationPattern_NonRes,
)
from PyPH_WUFI.WUFI_xml_conversion_functions import (
    build_PassiveHouseData,
    build_Building,
    build_temp_Climate,
    build_temp_Mechanicals,
    build_temp_Project,
    build_temp_Zone,
    build_temp_RoomVentilation,
)

TOL = 2  # Value tolerance for rounding. ie; 9.84318191919 -> 9.84

# ------------------------------------------------------------------------------
def _WindowType(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.name),
        PyPH_WUFI.xml_node.XML_Node("Uw_Detailed", _obj.detU),
        PyPH_WUFI.xml_node.XML_Node("GlazingFrameDetailed", _obj.detGd),
        PyPH_WUFI.xml_node.XML_Node("U_Value", _obj.Uw),
        PyPH_WUFI.xml_node.XML_Node("FrameFactor", _obj.frF),
        PyPH_WUFI.xml_node.XML_Node("SHGC_Hemispherical", _obj.trHem),
        PyPH_WUFI.xml_node.XML_Node("U_Value_Glazing", _obj.glazU),
        PyPH_WUFI.xml_node.XML_Node("U_Value_Frame", _obj.Ufr),
        PyPH_WUFI.xml_node.XML_Node("Frame_Width_Left", _obj.lrtbFrW[0]),
        PyPH_WUFI.xml_node.XML_Node("Frame_U_Left", _obj.lrtbFrU[0]),
        PyPH_WUFI.xml_node.XML_Node("Glazing_Psi_Left", _obj.lrtbGlPsi[0]),
        PyPH_WUFI.xml_node.XML_Node("Frame_Psi_Left", _obj.lrtbFrPsi[0]),
        PyPH_WUFI.xml_node.XML_Node("MeanEmissivity", _obj.frEmisE),
        PyPH_WUFI.xml_node.XML_Node("g_Value", _obj.gtr),
    ]


# ------------------------------------------------------------------------------
# - Utilization Patterns
def _UtilizationPattern_Vent(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.name),
        PyPH_WUFI.xml_node.XML_Node("OperatingDays", _obj.operating_days),
        PyPH_WUFI.xml_node.XML_Node("OperatingWeeks", _obj.operating_weeks),
        PyPH_WUFI.xml_node.XML_Node("Maximum_DOS", round(_obj.utilization_rates.maximum.daily_op_sched, TOL)),
        PyPH_WUFI.xml_node.XML_Node("Maximum_PDF", round(_obj.utilization_rates.maximum.frac_of_design_airflow, TOL)),
        PyPH_WUFI.xml_node.XML_Node("Standard_DOS", round(_obj.utilization_rates.standard.daily_op_sched, TOL)),
        PyPH_WUFI.xml_node.XML_Node(
            "Standard_PDF", round(_obj.utilization_rates.standard.frac_of_design_airflow, TOL)
        ),
        PyPH_WUFI.xml_node.XML_Node("Basic_DOS", round(_obj.utilization_rates.basic.daily_op_sched, TOL)),
        PyPH_WUFI.xml_node.XML_Node("Basic_PDF", round(_obj.utilization_rates.basic.frac_of_design_airflow, TOL)),
        PyPH_WUFI.xml_node.XML_Node("Minimum_DOS", round(_obj.utilization_rates.minimum.daily_op_sched, TOL)),
        PyPH_WUFI.xml_node.XML_Node("Minimum_PDF", round(_obj.utilization_rates.minimum.frac_of_design_airflow, TOL)),
    ]


def _UtilizationPattern_NonRes(_obj: UtilizationPattern_NonRes) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.occupancy.name),
        # -- Occupancy
        PyPH_WUFI.xml_node.XML_Node("BeginUtilization", _obj.occupancy.schedule.start_hour),
        PyPH_WUFI.xml_node.XML_Node("EndUtilization", _obj.occupancy.schedule.end_hour),
        PyPH_WUFI.xml_node.XML_Node("AnnualUtilizationDays", _obj.occupancy.schedule.annual_utilization_days),
        PyPH_WUFI.xml_node.XML_Node("RelativeAbsenteeism", round(_obj.relative_absence_factor, TOL)),
        # -- Lighting
        PyPH_WUFI.xml_node.XML_Node("IlluminationLevel", round(_obj.lighting.loads.target_lux, 0)),
        PyPH_WUFI.xml_node.XML_Node("HeightUtilizationLevel", round(_obj.lighting.loads.watts_per_area, TOL)),
        PyPH_WUFI.xml_node.XML_Node(
            "PartUseFactorPeriodForLighting", round(_obj.lighting.schedule.relative_utilization_factor, TOL)
        ),
        # PyPH_WUFI.xml_node.XML_Node("AverageOccupancy", round(_obj.m2_per_person, TOL)),
    ]


# ------------------------------------------------------------------------------
# - Constructions
def _Material(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.name),
        PyPH_WUFI.xml_node.XML_Node("ThermalConductivity", _obj.tConD),
        PyPH_WUFI.xml_node.XML_Node("BulkDensity", _obj.densB),
        PyPH_WUFI.xml_node.XML_Node("Porosity", _obj.poros),
        PyPH_WUFI.xml_node.XML_Node("HeatCapacity", _obj.hCapS),
        PyPH_WUFI.xml_node.XML_Node("WaterVaporResistance", _obj.difRes),
        PyPH_WUFI.xml_node.XML_Node("ReferenceW", _obj.refWC),
    ]


def _Layer(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("Thickness", _obj.thickness, "unit", "m"),
        PyPH_WUFI.xml_node.XML_Object("Material", _obj.material),
    ]


def _Assembly(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.name),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Assembly::Order_Layers", _obj.Order_Layers).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node(*PyPH_WUFI.selection.Selection("Assembly::Grid_Kind", _obj.Grid_Kind).xml_data),
        PyPH_WUFI.xml_node.XML_List(
            "Layers",
            [PyPH_WUFI.xml_node.XML_Object("Layer", _, "index", i) for i, _ in enumerate(_obj.Layers)],
        ),
    ]


# ------------------------------------------------------------------------------
# - Geometry
def _Vertex(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("X", round(_obj.x, 8)),
        PyPH_WUFI.xml_node.XML_Node("Y", round(_obj.y, 8)),
        PyPH_WUFI.xml_node.XML_Node("Z", round(_obj.z, 8)),
    ]


def _Polygon(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("NormalVectorX", round(_obj.nVec.x, 10)),
        PyPH_WUFI.xml_node.XML_Node("NormalVectorY", round(_obj.nVec.y, 10)),
        PyPH_WUFI.xml_node.XML_Node("NormalVectorZ", round(_obj.nVec.z, 10)),
        PyPH_WUFI.xml_node.XML_List(
            "IdentNrPoints",
            [PyPH_WUFI.xml_node.XML_Node("IdentNr", _, "index", i) for i, _ in enumerate(_obj.idVert)],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "IdentNrPolygonsInside",
            [PyPH_WUFI.xml_node.XML_Node("IdentNr", _, "index", i) for i, _ in enumerate(_obj.children)],
        ),
    ]


def _Geom(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_List(
            "Vertices",
            [PyPH_WUFI.xml_node.XML_Object("Vertix", _, "index", i) for i, _ in enumerate(_obj.vertices)],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "Polygons",
            [PyPH_WUFI.xml_node.XML_Object("Polygon", _, "index", i) for i, _ in enumerate(_obj.polygons)],
        ),
    ]


def _ClimateLocation(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("Selection", _obj.Selection),
        PyPH_WUFI.xml_node.XML_Object("PH_ClimateLocation", _obj.PH_ClimateLocation),
        PyPH_WUFI.xml_node.XML_Node("CatalogueNr_DB", _obj.CatalogueNr_DB),
        PyPH_WUFI.xml_node.XML_Node("MapNr_DB", _obj.MapNr_DB),
        PyPH_WUFI.xml_node.XML_Node("Albedo", _obj.Albedo),
        PyPH_WUFI.xml_node.XML_Node("GroundReflShort", _obj.GroundReflShort),
        PyPH_WUFI.xml_node.XML_Node("GroundReflLong", _obj.GroundReflLong),
        PyPH_WUFI.xml_node.XML_Node("GroundEmission", _obj.GroundEmission),
        PyPH_WUFI.xml_node.XML_Node("CloudIndex", _obj.CloudIndex),
        PyPH_WUFI.xml_node.XML_Node("CO2concenration", _obj.CO2concenration),
        PyPH_WUFI.xml_node.XML_Node("Unit_CO2concentration", _obj.Unit_CO2concentration),
    ]


def _WP_Color(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("Alpha", _obj.alpha),
        PyPH_WUFI.xml_node.XML_Node("Red", _obj.red),
        PyPH_WUFI.xml_node.XML_Node("Green", _obj.green),
        PyPH_WUFI.xml_node.XML_Node("Blue", _obj.blue),
    ]


def _Component(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.name),
        PyPH_WUFI.xml_node.XML_Node("Visual", _obj.visC),
        PyPH_WUFI.xml_node.XML_Node(
            "InnerAttachment", _obj.int_exposure_zone_id, "choice", _obj.int_exposure_zone_name
        ),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Component::OuterAttachment", _obj.ext_exposure_zone_id).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node(*PyPH_WUFI.selection.Selection("Component::Type", _obj.type).xml_data),
        PyPH_WUFI.xml_node.XML_Node("IdentNrColorI", _obj.int_color_id),
        PyPH_WUFI.xml_node.XML_Node("IdentNrColorE", _obj.ext_color_id),
        PyPH_WUFI.xml_node.XML_Object("ColorExternUserDef", _obj.int_UD_color),
        PyPH_WUFI.xml_node.XML_Object("ColorInternUserDef", _obj.ext_UD_color),
        PyPH_WUFI.xml_node.XML_Node("IdentNr_ComponentInnerSurface", _obj.inner_srfc_compo_idNr),
        PyPH_WUFI.xml_node.XML_List(
            "IdentNrPolygons",
            [PyPH_WUFI.xml_node.XML_Node("IdentNr", _, "index", i) for i, _ in enumerate(_obj.polygon_id_list)],
        ),
        PyPH_WUFI.xml_node.XML_Node("IdentNrAssembly", _obj.assembly_id_num),
        PyPH_WUFI.xml_node.XML_Node("IdentNrWindowType", _obj.win_type_id_num),
    ]


# ------------------------------------------------------------------------------
# -- PHIUS Data
def _temp_PH_Building_Internal_Gains(_obj: temp_PH_Building_Internal_Gains) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("EvaporationHeatPerPerson", _obj.data.int_gains_evap_per_person, "unit", "W"),
        PyPH_WUFI.xml_node.XML_Node("HeatLossFluschingWC", _obj.data.int_gains_flush_heat_loss),
        PyPH_WUFI.xml_node.XML_Node("QuantityWCs", _obj.data.int_gains_num_toilets, "unit", "-"),
        PyPH_WUFI.xml_node.XML_Node("RoomCategory", 1, _obj.data.int_gains_toilet_room_util_pat),
        PyPH_WUFI.xml_node.XML_Node("UseDefaultValuesSchool", _obj.data.int_gains_use_school_defaults),
        PyPH_WUFI.xml_node.XML_Node(
            "MarginalPerformanceRatioDHW", _obj.data.int_gains_dhw_marginal_perf_ratio, "unit", "-"
        ),
    ]


def _temp_PH_Building(_obj: temp_PH_Building) -> list[xml_writable]:
    if _obj.occupancy_type == 1:
        type_category = "Occupancy::OccupancyTypeResidential"
    else:
        type_category = "Occupancy::OccupancyTypeNonResidential"

    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Occupancy::BuildingCategory", _obj.occupancy_category).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node(*PyPH_WUFI.selection.Selection(type_category, _obj.occupancy_type).xml_data),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("PHIUS::BuildingStatus", _obj.building_status).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("PHIUS::BuildingType", _obj.building_type).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("PHIUS::OccupancySettingMethod", _obj.occupancy_setting_method).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("NumberUnits", _obj.num_units, "unit", "-"),
        PyPH_WUFI.xml_node.XML_Node("CountStories", _obj.num_stories),
        PyPH_WUFI.xml_node.XML_Node("EnvelopeAirtightnessCoefficient", _obj.q50, "unit", "m??/m??h"),
        PyPH_WUFI.xml_node.XML_List(
            "FoundationInterfaces",
            [
                PyPH_WUFI.xml_node.XML_Object("FoundationInterface", _, "index", i)
                for i, _ in enumerate(_obj.foundations)
            ],
        ),
        PyPH_WUFI.xml_node.XML_Object("InternalGainsAdditionalData", _obj.int_gains),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection(
                "Mech_Summer::SummerHRVHumidityRecovery", _obj.summer_hrv_bypass_mode
            ).xml_data
        ),
    ]


def _temp_PassiveHouseData(_obj: temp_PassiveHouseData) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("PHIUS::PH_CertificateCriteria", _obj.certification_criteria).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("PHIUS::PH_SelectionTargetData", _obj.localization_selection_type).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("AnnualHeatingDemand", _obj.PHIUS2021_heating_demand, "unit", "kWh/m??a"),
        PyPH_WUFI.xml_node.XML_Node("AnnualCoolingDemand", _obj.PHIUS2021_cooling_demand, "unit", "kWh/m??a"),
        PyPH_WUFI.xml_node.XML_Node("PeakHeatingLoad", _obj.PHIUS2021_heating_load, "unit", "W/m??"),
        PyPH_WUFI.xml_node.XML_Node("PeakCoolingLoad", _obj.PHIUS2021_cooling_load, "unit", "W/m??"),
        PyPH_WUFI.xml_node.XML_List(
            "PH_Buildings",
            [PyPH_WUFI.xml_node.XML_Object("PH_Building", _, "index", i) for i, _ in enumerate(_obj.PH_Buildings)],
        ),
    ]


def _temp_PH_Climate(_obj: temp_PH_Climate) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("Selection", 6),  # -- User Defined
        PyPH_WUFI.xml_node.XML_Node("SelectionPECO2Factor", 1),
        PyPH_WUFI.xml_node.XML_Node("DailyTemperatureSwingSummer", _obj.summer_daily_temperature_swing),
        PyPH_WUFI.xml_node.XML_Node("AverageWindSpeed", _obj.average_wind_speed),
        # ---
        PyPH_WUFI.xml_node.XML_Node("Latitude", _obj.location.latitude, "unit", "??"),
        PyPH_WUFI.xml_node.XML_Node("Longitude", _obj.location.longitude, "unit", "??"),
        PyPH_WUFI.xml_node.XML_Node("HeightNNWeatherStation", _obj.location.weather_station_elevation, "unit", "m"),
        PyPH_WUFI.xml_node.XML_Node("dUTC", _obj.location.hours_from_UTC),
        PyPH_WUFI.xml_node.XML_Node("ClimateZone", _obj.location.climate_zone, "choice", "Not defined"),
        # ---
        PyPH_WUFI.xml_node.XML_Node("GroundThermalConductivity", _obj.ground.ground_thermal_conductivity),
        PyPH_WUFI.xml_node.XML_Node("GroundHeatCapacitiy", _obj.ground.ground_heat_capacitiy),
        PyPH_WUFI.xml_node.XML_Node("GroundDensity", _obj.ground.ground_density),
        PyPH_WUFI.xml_node.XML_Node("DepthGroundwater", _obj.ground.depth_groundwater),
        PyPH_WUFI.xml_node.XML_Node("FlowRateGroundwater", _obj.ground.flow_rate_groundwater),
        # ---
        PyPH_WUFI.xml_node.XML_List(
            "TemperatureMonthly",
            [
                PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i)
                for i, _ in enumerate(_obj.monthly_temperature_air.values)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "DewPointTemperatureMonthly",
            [
                PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i)
                for i, _ in enumerate(_obj.monthly_temperature_dewpoint.values)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "SkyTemperatureMonthly",
            [
                PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i)
                for i, _ in enumerate(_obj.monthly_temperature_sky.values)
            ],
        ),
        # PyPH_WUFI.xml_node.XML_List(
        #     "GroundTemperatureMonthly",
        #     [PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i) for i, _ in enumerate(_obj.monthly_temperature_ground.values)],
        # ),
        PyPH_WUFI.xml_node.XML_List(
            "NorthSolarRadiationMonthly",
            [
                PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i)
                for i, _ in enumerate(_obj.monthly_radiation_north.values)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "EastSolarRadiationMonthly",
            [
                PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i)
                for i, _ in enumerate(_obj.monthly_radiation_east.values)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "SouthSolarRadiationMonthly",
            [
                PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i)
                for i, _ in enumerate(_obj.monthly_radiation_south.values)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "WestSolarRadiationMonthly",
            [
                PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i)
                for i, _ in enumerate(_obj.monthly_radiation_west.values)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "GlobalSolarRadiationMonthly",
            [
                PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i)
                for i, _ in enumerate(_obj.monthly_radiation_global.values)
            ],
        ),
        PyPH_WUFI.xml_node.XML_Node("TemperatureHeating1", _obj.peak_heating_1.temp),
        PyPH_WUFI.xml_node.XML_Node("NorthSolarRadiationHeating1", _obj.peak_heating_1.rad_north),
        PyPH_WUFI.xml_node.XML_Node("EastSolarRadiationHeating1", _obj.peak_heating_1.rad_east),
        PyPH_WUFI.xml_node.XML_Node("SouthSolarRadiationHeating1", _obj.peak_heating_1.rad_south),
        PyPH_WUFI.xml_node.XML_Node("WestSolarRadiationHeating1", _obj.peak_heating_1.rad_west),
        PyPH_WUFI.xml_node.XML_Node("GlobalSolarRadiationHeating1", _obj.peak_heating_1.rad_global),
        PyPH_WUFI.xml_node.XML_Node("TemperatureHeating2", _obj.peak_heating_2.temp),
        PyPH_WUFI.xml_node.XML_Node("NorthSolarRadiationHeating2", _obj.peak_heating_2.rad_north),
        PyPH_WUFI.xml_node.XML_Node("EastSolarRadiationHeating2", _obj.peak_heating_2.rad_east),
        PyPH_WUFI.xml_node.XML_Node("SouthSolarRadiationHeating2", _obj.peak_heating_2.rad_south),
        PyPH_WUFI.xml_node.XML_Node("WestSolarRadiationHeating2", _obj.peak_heating_2.rad_west),
        PyPH_WUFI.xml_node.XML_Node("GlobalSolarRadiationHeating2", _obj.peak_heating_2.rad_global),
        PyPH_WUFI.xml_node.XML_Node("TemperatureCooling", _obj.peak_cooling.temp),
        PyPH_WUFI.xml_node.XML_Node("NorthSolarRadiationCooling", _obj.peak_cooling.rad_north),
        PyPH_WUFI.xml_node.XML_Node("EastSolarRadiationCooling", _obj.peak_cooling.rad_east),
        PyPH_WUFI.xml_node.XML_Node("SouthSolarRadiationCooling", _obj.peak_cooling.rad_south),
        PyPH_WUFI.xml_node.XML_Node("WestSolarRadiationCooling", _obj.peak_cooling.rad_west),
        PyPH_WUFI.xml_node.XML_Node("GlobalSolarRadiationCooling", _obj.peak_cooling.rad_global),
    ]


def _Climate(_obj: PHX.climate.Climate) -> list[xml_writable]:
    temp_climate = build_temp_Climate(_obj)

    return [
        PyPH_WUFI.xml_node.XML_Node("Selection", 1),  # -- User Defined
        PyPH_WUFI.xml_node.XML_Object("PH_ClimateLocation", temp_climate.PH_Climate),
    ]


# ------------------------------------------------------------------------------
# --Foundations
def _Foundation(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.name),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Foundation::FloorSlabType", _obj.floor_type).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Foundation::SettingFloorSlabType", _obj.floor_setting).xml_data
        ),
    ]


# ------------------------------------------------------------------------------
# -- Zones
def _Zone(_obj: Zone) -> list[xml_writable]:
    temp_Zone = build_temp_Zone(_obj)

    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.name),
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Zone::GrossVolume_Selection", _obj.volume_gross_selection).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("GrossVolume", round(_obj.volume_gross, TOL), "unit"),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Zone::NetVolume_Selection", _obj.volume_net_selection).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("NetVolume", round(_obj.volume_net, TOL), "unit"),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Zone::FloorArea_Selection", _obj.floor_area_selection).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("FloorArea", round(_obj.floor_area, TOL), "unit"),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Zone::ClearanceHeight_Selection", _obj.clearance_height_selection).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("ClearanceHeight", round(_obj.clearance_height, TOL), "unit", "m"),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection(
                "Zone::SpecificHeatCapacity_Selection", _obj.spec_heat_cap_selection
            ).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("SpecificHeatCapacity", round(_obj.spec_heat_cap, 0), "unit", "Wh/m??K"),
        # -- Room Loads (Occupancy, Ventilation, Lighting) and Appliances
        # ----------------------------------------------------------------------
        PyPH_WUFI.xml_node.XML_List(
            "RoomsVentilation",
            [
                PyPH_WUFI.xml_node.XML_Object("RoomVentilation", _, "index", i, "_RoomVentilation")
                for i, _ in enumerate(temp_Zone.spaces)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "LoadsLightingsPH",
            [
                PyPH_WUFI.xml_node.XML_Object("LoadsLighting", _, "index", i, "_RoomLoads_Lighting")
                for i, _ in enumerate(temp_Zone.spaces)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "LoadsPersonsPH",
            [
                PyPH_WUFI.xml_node.XML_Object("LoadsPerson", _, "index", i, "_RoomLoads_Occupancy")
                for i, _ in enumerate(temp_Zone.spaces)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "LoadsOfficeEquipmentsPH",
            [
                PyPH_WUFI.xml_node.XML_Object("LoadsOfficeEquipment", _, "index", i, "_RoomLoads_ElecEquipment")
                for i, _ in enumerate(temp_Zone.spaces)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "HomeDevice",
            [
                PyPH_WUFI.xml_node.XML_Object("Device", _, "index", i, _schema_name="_Appliance_Res")
                for i, _ in enumerate(_obj.appliance_set)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "LoadsAuxElectricitiesPH",
            [
                PyPH_WUFI.xml_node.XML_Object("LoadsAuxElectricity", _, "index", i, _schema_name="_Appliance_NonRes")
                for i, _ in enumerate(_obj.appliance_set)
            ],
        ),
        # -- Summer Ventilation
        # ----------------------------------------------------------------------
        PyPH_WUFI.xml_node.XML_Node(  # = same as winter
            "SummerMechanicalVentilationNight",
            _obj.summer_ventilation.avg_mech_ach,
            "unit",
            "1/h",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "SummerNaturalVentilationDay",
            _obj.summer_ventilation.day_window_ach,
            "unit",
            "1/h",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "SummerNaturalVentilationNight",
            _obj.summer_ventilation.night_window_ach,
            "unit",
            "1/h",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "MechanicalAutomaticControlledVentilation",
            _obj.summer_ventilation.additional_mech_ach,
            "unit",
            "1/h",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "SpecificPowerConsumptionAdditionalVentCooling",
            _obj.summer_ventilation.additional_mech_spec_power,
            "unit",
            "Wh/m??",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "ACHViaMechanicalVentilationExhaustAir",
            _obj.summer_ventilation.exhaust_ach,
            "unit",
            "1/h",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "SpecificPowerConsumption",
            _obj.summer_ventilation.exhaust_spec_power,
            "unit",
            "Wh/m??",
        ),
        # -- Zone Occupancy
        # ----------------------------------------------------------------------
        PyPH_WUFI.xml_node.XML_Node(
            "NumberBedrooms",
            _obj.occupancy.num_bedrooms,
            "unit",
            "-",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "OccupantQuantityUserDef",
            _obj.occupancy.num_occupants,
            "unit",
            "-",
        ),
    ]


def _temp_Building(_obj: temp_Building) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("Numerics", _obj.numerics),
        PyPH_WUFI.xml_node.XML_Node("AirFlowModel", _obj.airflow_model),
        PyPH_WUFI.xml_node.XML_List(
            "Components",
            [PyPH_WUFI.xml_node.XML_Object("Component", _, "index", i) for i, _ in enumerate(_obj.components)],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "Zones",
            [PyPH_WUFI.xml_node.XML_Object("Zone", _, "index", i) for i, _ in enumerate(_obj.zones)],
        ),
        PyPH_WUFI.xml_node.XML_Node("CountGenerated", _obj.count_generator),
        PyPH_WUFI.xml_node.XML_Node("HasBeenGenerated", _obj.has_been_generated),
        PyPH_WUFI.xml_node.XML_Node("HasBeenChangedSinceLastGeneration", _obj.has_been_changed_since_last_gen),
    ]


def _RoomVentilation(_temp_space: temp_Space) -> list[xml_writable]:
    temp_RoomVentilation = build_temp_RoomVentilation(_temp_space)

    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _temp_space.space.display_name),
        PyPH_WUFI.xml_node.XML_Node("Quantity", _temp_space.space.quantity),
        PyPH_WUFI.xml_node.XML_Node(*PyPH_WUFI.selection.Selection("WP_Room::Type", _temp_space.space.type).xml_data),
        PyPH_WUFI.xml_node.XML_Node("AreaRoom", round(_temp_space.space.floor_area_weighted, TOL), "unit", "m??"),
        PyPH_WUFI.xml_node.XML_Node("ClearRoomHeight", round(_temp_space.space.clear_height, TOL), "unit", "m"),
        PyPH_WUFI.xml_node.XML_Node("IdentNrUtilizationPatternVent", _temp_space.ventilation.schedule.id),
        PyPH_WUFI.xml_node.XML_Node("IdentNrVentilationUnit", temp_RoomVentilation.ventilator_id),
        PyPH_WUFI.xml_node.XML_Node(
            "DesignVolumeFlowRateSupply",
            round(_temp_space.ventilation.loads.supply, TOL),
            "unit",
            "m??/h",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "DesignVolumeFlowRateExhaust",
            round(_temp_space.ventilation.loads.extract, TOL),
            "unit",
            "m??/h",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "DesignFlowInterzonalUserDef",
            round(_temp_space.ventilation.loads.transfer, TOL),
            "unit",
            "m??/h",
        ),
    ]


def _RoomLoads_Occupancy(_temp_space: temp_Space) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _temp_space.space.display_name),
        PyPH_WUFI.xml_node.XML_Node("IdentNrUtilizationPattern", _temp_space.occupancy.id),
        PyPH_WUFI.xml_node.XML_Node("ChoiceActivityPersons", 3, "choice", "Adult, standing or light work"),
        PyPH_WUFI.xml_node.XML_Node("NumberOccupants", round(_temp_space.peak_occupancy, TOL), "unit", "-")
        # PyPH_WUFI.xml_node.XML_Node("FloorAreaUtilizationZone", round(_temp_space.space.floor_area_weighted, TOL)),
    ]


def _RoomLoads_Lighting(_temp_space: temp_Space) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _temp_space.space.display_name),
        PyPH_WUFI.xml_node.XML_Node("RoomCategory", _temp_space.occupancy.id, "choice"),
        PyPH_WUFI.xml_node.XML_Node("ChoiceLightTransmissionGlazing", 1, "choice", "Triple low-e glazing: 0.69"),
        PyPH_WUFI.xml_node.XML_Node("LightingControl", 1, "choice", "Manually"),
        PyPH_WUFI.xml_node.XML_Node("WithinThermalEnvelope", True),
        PyPH_WUFI.xml_node.XML_Node("MotionDetector", False),
        PyPH_WUFI.xml_node.XML_Node("FacadeIncludingWindows", False),
        PyPH_WUFI.xml_node.XML_Node(
            "FractionTreatedFloorArea", round(_temp_space.space_percent_floor_area_total, 4), "unit", "-"
        ),
        PyPH_WUFI.xml_node.XML_Node("DeviationFromNorth", 0, "unit", "??"),
        PyPH_WUFI.xml_node.XML_Node("RoomDepth", 999, "unit", "m"),
        PyPH_WUFI.xml_node.XML_Node("RoomWidth", 999, "unit", "m"),
        PyPH_WUFI.xml_node.XML_Node("RoomHeight", 999, "unit", "m"),
        PyPH_WUFI.xml_node.XML_Node("LintelHeight", 999, "unit", "m"),
        PyPH_WUFI.xml_node.XML_Node("WindowWidth", 999, "unit", "m"),
        PyPH_WUFI.xml_node.XML_Node(
            "InstalledLightingPower", round(_temp_space.lighting.loads.watts_per_area, TOL), "unit", "W/m??"
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "LightingFullLoadHours", round(_temp_space.lighting.schedule.EFLH, TOL), "unit", "hrs/a"
        ),
    ]


def _RoomLoads_ElecEquipment(_temp_space: temp_Space) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _temp_space.space.display_name),
        PyPH_WUFI.xml_node.XML_Node("RoomCategory", _temp_space.occupancy.id, "choice"),
        PyPH_WUFI.xml_node.XML_Node("ApplicationType", 7, "choice", "User defined"),
        PyPH_WUFI.xml_node.XML_Node("Quantity", 1),
        PyPH_WUFI.xml_node.XML_Node("WithinThermalEnvelope", True),
        PyPH_WUFI.xml_node.XML_Node("PowerRating", round(_temp_space.total_space_elec_wattage, TOL), "unit", "W"),
        PyPH_WUFI.xml_node.XML_Node(
            "UtilizationHoursYear", round(_temp_space.elec_equipment.schedule.EFLH, TOL), "unit", "hrs/a"
        ),
    ]


# ------------------------------------------------------------------------------
# -- Variant, Project
def _BldgSegment(_obj: BldgSegment) -> list[xml_writable]:
    """
    Note: For WUFI, each 'Building-Segment' will map to a separate 'Variant'.
    This is done for PHIUS modeling and allows for Non-Res and Res. sections
    of a building to be modeled in the same WUFI file, in different 'Cases'

    This function builds up the specific tree WUFI requires with all interstitial layers/nodes
    Final XML tree should look like:
      :
      |- Building
      |- PassivehouseData
      |   |-PH_Buildings
      |   :  |- PH_Building
      |      :   |-FoundationInterfaces
      |          |    |-FoundationInterface
      :          :    :
    """

    temp_Bldg = build_Building(_obj)
    temp_PHData = build_PassiveHouseData(_obj)

    # --- Build the final output list
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.name),
        PyPH_WUFI.xml_node.XML_Node("Remarks", _obj.remarks),
        PyPH_WUFI.xml_node.XML_Object("Graphics_3D", _obj.geom),
        PyPH_WUFI.xml_node.XML_Object("Building", temp_Bldg),
        PyPH_WUFI.xml_node.XML_Object("ClimateLocation", _obj.climate),
        PyPH_WUFI.xml_node.XML_Node("PlugIn", _obj.plugin),
        PyPH_WUFI.xml_node.XML_Object("PassivehouseData", temp_PHData),
        PyPH_WUFI.xml_node.XML_Object("HVAC", _obj.mechanicals, _schema_name="_Mechanicals"),
    ]


def _Date(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("Year", _obj.Year),
        PyPH_WUFI.xml_node.XML_Node("Month", _obj.Month),
        PyPH_WUFI.xml_node.XML_Node("Day", _obj.Day),
        PyPH_WUFI.xml_node.XML_Node("Hour", _obj.Hour),
        PyPH_WUFI.xml_node.XML_Node("Minutes", _obj.Minutes),
    ]


def _ProjectData(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("Customer_Name", _obj.cN),
        PyPH_WUFI.xml_node.XML_Node("Customer_Locality", _obj.cLoc),
        PyPH_WUFI.xml_node.XML_Node("Customer_PostalCode", _obj.cPostC),
        PyPH_WUFI.xml_node.XML_Node("Customer_Street", _obj.cStr),
        PyPH_WUFI.xml_node.XML_Node("Customer_Tel", _obj.cTel),
        PyPH_WUFI.xml_node.XML_Node("Customer_Email", _obj.cEmail),
        PyPH_WUFI.xml_node.XML_Node("Building_Name", _obj.bN),
        PyPH_WUFI.xml_node.XML_Node("Year_Construction", _obj.bYCon),
        PyPH_WUFI.xml_node.XML_Node("Building_Locality", _obj.bLoc),
        PyPH_WUFI.xml_node.XML_Node("Building_PostalCode", _obj.bPostC),
        PyPH_WUFI.xml_node.XML_Node("Building_Street", _obj.bStr),
        PyPH_WUFI.xml_node.XML_Node("OwnerIsClient", _obj.oIsC),
        PyPH_WUFI.xml_node.XML_Node("Owner_Name", _obj.oN),
        PyPH_WUFI.xml_node.XML_Node("Owner_Locality", _obj.oLoc),
        PyPH_WUFI.xml_node.XML_Node("Owner_PostalCode", _obj.oPostC),
        PyPH_WUFI.xml_node.XML_Node("Owner_Street", _obj.oStreet),
        PyPH_WUFI.xml_node.XML_Node("Responsible_Name", _obj.rN),
        PyPH_WUFI.xml_node.XML_Node("Responsible_Locality", _obj.rLoc),
        PyPH_WUFI.xml_node.XML_Node("Responsible_PostalCode", _obj.rPostC),
        PyPH_WUFI.xml_node.XML_Node("Responsible_Street", _obj.rStr),
        PyPH_WUFI.xml_node.XML_Node("Responsible_Tel", _obj.rTel),
        PyPH_WUFI.xml_node.XML_Node("Responsible_LicenseNr", _obj.rLic),
        PyPH_WUFI.xml_node.XML_Node("Responsible_Email", _obj.rEmail),
        PyPH_WUFI.xml_node.XML_Object("Date_Project", _obj.date),
        PyPH_WUFI.xml_node.XML_Node("WhiteBackgroundPictureBuilding", _obj.wBkg),
    ]


def _Project(_obj: Project) -> list[xml_writable]:
    """
    Note: For WUFI, each 'Building-Segment' will map to a separate 'Variant'.
    This is done for PHIUS modeling and allows for Non-Res and Res. sections
    of a building to be modeled in the same WUFI file, in different 'Cases'
    """

    temp_Project = build_temp_Project(_obj)

    return [
        PyPH_WUFI.xml_node.XML_Node("DataVersion", _obj.data_version),
        PyPH_WUFI.xml_node.XML_Node("UnitSystem", _obj.unit_system),
        PyPH_WUFI.xml_node.XML_Node("ProgramVersion", _obj.progVers),
        PyPH_WUFI.xml_node.XML_Node("Scope", _obj.calcScope),
        PyPH_WUFI.xml_node.XML_Node("DimensionsVisualizedGeometry", _obj.dimVisGeom),
        PyPH_WUFI.xml_node.XML_Object("ProjectData", _obj.projD),
        PyPH_WUFI.xml_node.XML_List(
            "Assemblies",
            [PyPH_WUFI.xml_node.XML_Object("Assembly", _, "index", i) for i, _ in enumerate(_obj.lAssembly)],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "WindowTypes",
            [PyPH_WUFI.xml_node.XML_Object("WindowType", _, "index", i) for i, _ in enumerate(_obj.lWindow)],
        ),
        PyPH_WUFI.xml_node.XML_List("SolarProtectionTypes", _obj.lSolProt),
        PyPH_WUFI.xml_node.XML_List(
            "UtilisationPatternsVentilation",
            [
                PyPH_WUFI.xml_node.XML_Object("UtilizationPatternVent", _, "index", i)
                for i, _ in enumerate(temp_Project.util_pattern_collection_ventilation)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "UtilizationPatternsPH",
            [
                PyPH_WUFI.xml_node.XML_Object("UtilizationPattern", _, "index", i)
                for i, _ in enumerate(temp_Project.util_pattern_collection_non_residential)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "Variants",
            [PyPH_WUFI.xml_node.XML_Object("Variant", _, "index", i) for i, _ in enumerate(_obj.building_segments)],
        ),
    ]


# ------------------------------------------------------------------------------
# -- Appliances
def _Appliance_dishwasher(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Appliances::Connection", _obj.dishwasher_water_connection).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection(
                "Appliances::DishwasherCapacityPreselection", _obj.dishwasher_capacity_type
            ).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("DishwasherCapacityInPlace", _obj.dishwasher_capacity, "unit", "-"),
    ]


def _Appliance_clothes_washer(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("UtilizationFactor", _obj.washer_utilization_factor, "unit", "-"),
        PyPH_WUFI.xml_node.XML_Node("MEF_ModifiedEnergyFactor", _obj.washer_modified_energy_factor, "unit", "-"),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Appliances::Connection", _obj.washer_connection).xml_data
        ),
    ]


def _Appliance_clothes_dryer(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Appliances::Dryer_Choice", _obj.dryer_type).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("GasConsumption", _obj.dryer_gas_consumption, "unit", "kWh"),
        PyPH_WUFI.xml_node.XML_Node("EfficiencyFactorGas", _obj.dryer_gas_consumption, "unit", "-"),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection(
                "Appliances::FieldUtilizationFactorPreselection", _obj.dryer_field_utilization_factor_type
            ).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("FieldUtilizationFactor", _obj.dryer_field_utilization_factor, "unit", "-"),
    ]


def _Appliance_fridge(_obj) -> list[xml_writable]:
    return []


def _Appliance_freezer(_obj) -> list[xml_writable]:
    return []


def _Appliance_fridge_freezer(_obj) -> list[xml_writable]:
    return []


def _Appliance_cooking(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Appliances::CookingWith", _obj.cooktop_type).xml_data
        ),
    ]


def _Appliance_PHIUS_MEL(_obj) -> list[xml_writable]:
    return []


def _Appliance_PHIUS_Lighting_Int(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node(
            "FractionHightEfficiency", round(_obj.lighting_frac_high_efficiency, TOL), "unit", "-"
        ),
    ]


def _Appliance_PHIUS_Lighting_Ext(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node(
            "FractionHightEfficiency", round(_obj.lighting_frac_high_efficiency, TOL), "unit", "-"
        ),
    ]


def _Appliance_Custom_Electric_per_Year(_obj) -> list[xml_writable]:
    return []


def _Appliance_Custom_Electric_per_Use(_obj) -> list[xml_writable]:
    return []


def _Appliance_NonRes(_obj: Appliance) -> list[xml_writable]:
    if _obj.type not in [21, 22, 23, 24]:
        # -- Not a NonRes appliance
        return []

    def _convert_appliance_type(_num: int):
        """Convert Non-Res type numbers from PHX to WUFI format"""
        convert = {
            23: 1,  # Cooktop
            21: 2,  # Dishwasher
            22: 3,  # Refigerator
            24: 4,  # User Defined
        }

        return convert.get(_num, 1)

    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.name),
        PyPH_WUFI.xml_node.XML_Node("RoomCategory", _obj.usage.id),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Appliances::ApplicationType", _convert_appliance_type(_obj.type)).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("ChoiceCooking", 1),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Appliances::ChoiceCooking", _obj.cooktop_type).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection(
                "Appliances::ChoiceDishwashingConection", _obj.dishwasher_water_connection
            ).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("Quantity", int(_obj.quantity)),
        PyPH_WUFI.xml_node.XML_Node("WithinThermalEnvelope", _obj.in_conditioned_space),
        PyPH_WUFI.xml_node.XML_Node("NumberMealsUtilizationDay", _obj.num_meals_per_day, "unit", "-"),
        PyPH_WUFI.xml_node.XML_Node("NormDemand", _obj.energy_demand_per_use, "unit", "kWh/d"),
        PyPH_WUFI.xml_node.XML_Node("UtilizationDaysYear", 1, "unit", "days/a"),
    ]


def _Appliance_Res(_obj: Appliance) -> list[xml_writable]:
    """Appliances have some basic shared params, then a bunch of custom params"""
    appliance_writer_funcs = {
        1: _Appliance_dishwasher,
        2: _Appliance_clothes_washer,
        3: _Appliance_clothes_dryer,
        4: _Appliance_fridge,
        5: _Appliance_freezer,
        6: _Appliance_fridge_freezer,
        7: _Appliance_cooking,
        13: _Appliance_PHIUS_MEL,
        14: _Appliance_PHIUS_Lighting_Int,
        15: _Appliance_PHIUS_Lighting_Ext,
        11: _Appliance_Custom_Electric_per_Year,
        17: _Appliance_Custom_Electric_per_Use,
        18: _Appliance_Custom_Electric_per_Use,
    }
    if _obj.type not in appliance_writer_funcs.keys():
        # -- Not a residential appliance
        return []

    # Fix the energy Norm.
    # WUFI uses '1' for both 'Use' and 'Day'
    energy_norm = PyPH_WUFI.selection.Selection(
        "Appliances::ReferenceEnergyDemandNorm", _obj.reference_energy_norm
    ).xml_data
    if energy_norm[1] == 99:
        energy_norm = (energy_norm[0], 1, energy_norm[2], energy_norm[3])

    # --------------------------------------------------------------------------
    # -- Build the basic params
    basic_params = [
        PyPH_WUFI.xml_node.XML_Node(*PyPH_WUFI.selection.Selection("Appliances::Type", _obj.type).xml_data),
        PyPH_WUFI.xml_node.XML_Node("Comment", _obj.comment),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Appliances::ReferenceQuantity", _obj.reference_quantity).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("InConditionedSpace", _obj.in_conditioned_space),
        PyPH_WUFI.xml_node.XML_Node(*energy_norm),
        PyPH_WUFI.xml_node.XML_Node("EnergyDemandNorm", round(_obj.energy_demand, TOL), "unit", "kWh"),
        PyPH_WUFI.xml_node.XML_Node("EnergyDemandNormUse", round(_obj.energy_demand_per_use, TOL), "unit", "kWh"),
        PyPH_WUFI.xml_node.XML_Node("CEF_CombinedEnergyFactor", _obj.combined_energy_facor, "unit", "-"),
    ]

    # --------------------------------------------------------------------------
    # -- Build the custom Params
    if _obj.type in [13, 14, 15] and _obj.reference_quantity == 5:
        # -- Cus' of the way they added the PHIUS appliances.
        basic_params.append(PyPH_WUFI.xml_node.XML_Node("Quantity", int(_obj.user_defined_total)))
    else:
        basic_params.append(PyPH_WUFI.xml_node.XML_Node("Quantity", int(_obj.quantity)))

    # --------------------------------------------------------------------------
    # -- Combine the Basic and the Custom Params
    return basic_params + appliance_writer_funcs.get(_obj.type)(_obj)


# ------------------------------------------------------------------------------
# -- HVAC
def _Mechanicals(_obj: Mechanicals) -> list[xml_writable]:
    temp_Mechanicals = build_temp_Mechanicals(_obj)

    return [
        PyPH_WUFI.xml_node.XML_List(
            "Systems",
            [
                PyPH_WUFI.xml_node.XML_Object("System", _, "index", i, _schema_name="_MechanicalSystemGroup")
                for i, _ in enumerate(temp_Mechanicals.mech_groups)
            ],
        ),
    ]


def _MechanicalSystemGroup(_obj: temp_MechanicalSystemsGroup) -> list[xml_writable]:

    return [
        PyPH_WUFI.xml_node.XML_Node("Name", "System Group {}".format(_obj.group_type_number)),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Mech_System::Type", _obj.group_type_number).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.group_type_number),
        PyPH_WUFI.xml_node.XML_List(
            "Devices",
            [
                PyPH_WUFI.xml_node.XML_Object("Device", _, "index", i, _schema_name="_HVAC_Device")
                for i, _ in enumerate(_obj.wufi_devices)
            ],
        ),
    ]


def _HVAC_Device(_obj: temp_MechanicalDevice) -> list[xml_writable]:
    node_items = [
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.name),
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Mech_Device::SystemType", _obj.system_type).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Mech_Device::TypeDevice", _obj.device_type).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Heating", _obj.system_usage.used_for_heating),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_DHW", _obj.system_usage.used_for_DHW),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Cooling", _obj.system_usage.used_for_cooling),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Ventilation", _obj.system_usage.used_for_ventilation),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Humidification", _obj.system_usage.used_for_humidification),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Dehumidification", _obj.system_usage.used_for_dehumidification),
        PyPH_WUFI.xml_node.XML_Node("UseOptionalClimate", _obj.system_usage.used_optional_climate),
        PyPH_WUFI.xml_node.XML_Node("IdentNr_OptionalClimate", _obj.system_usage.optional_climate_id_number),
    ]

    # -- For the different types of devices, add in their specific properties
    if _obj.device_type == 1:
        # -- Ventilator
        node_items.extend(_HVAC_Ventilator(_obj))
    elif _obj.device_type == 2:
        # -- Elec Space Heat / DHW
        node_items.extend(_HVAC_Elec_Heat_DHW(_obj))
    elif _obj.device_type == 8:
        # -- Water Storage
        node_items.extend(_HVAC_Water_Tank(_obj))

    return node_items


# -- HVAC Device | Ventilator
def _HVAC_Ventilator(_obj: temp_MechanicalDevice) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Object(
            "PH_Parameters", _obj.properties, _schema_name="_HVAC_Properities_Ventilation_PH"
        ),
        PyPH_WUFI.xml_node.XML_Object(
            "Ventilation_Parameters", _obj.properties, _schema_name="_HVAC_Properties_Ventilation"
        ),
        PyPH_WUFI.xml_node.XML_Node("HeatRecovery", _obj.properties.heat_recovery_efficiency, "unit", "-"),
        PyPH_WUFI.xml_node.XML_Node(
            "MoistureRecovery",
            _obj.properties.humidity_recovery_efficiency,
            "unit",
            "-",
        ),
    ]


def _HVAC_Properities_Ventilation_PH(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("Quantity", 1),
        PyPH_WUFI.xml_node.XML_Node(
            "ElectricEfficiency",
            _obj.electric_efficiency,
            "unit",
            "Wh/m??",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "SubsoilHeatExchangeEfficiency",
            _obj.subsoil_heat_exchange_efficiency,
            "unit",
            "-",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "HumidityRecoveryEfficiency",
            _obj.humidity_recovery_efficiency,
            "unit",
            "-",
        ),
        PyPH_WUFI.xml_node.XML_Node("VolumeFlowRateFrom", _obj.volume_flowrate_from, "unit", "m??/h"),
        PyPH_WUFI.xml_node.XML_Node("VolumeFlowRateTo", _obj.volume_flow_rate_to, "unit", "m??/h"),
        PyPH_WUFI.xml_node.XML_Node(
            "TemperatureBelowDefrostUsed",
            _obj.temperature_below_defrost_used,
            "unit",
            "??C",
        ),
        PyPH_WUFI.xml_node.XML_Node("FrostProtection", _obj.frost_protection),
        PyPH_WUFI.xml_node.XML_Node("DefrostRequired", _obj.defrost_required),
        PyPH_WUFI.xml_node.XML_Node("NoSummerBypass", _obj.no_summer_bypass),
        PyPH_WUFI.xml_node.XML_Node("HRVCalculatorData", _obj.hrv_calculator_data),
        PyPH_WUFI.xml_node.XML_Node("Maximum_VOS", _obj.maximum_vos),
        PyPH_WUFI.xml_node.XML_Node("Maximum_PP", _obj.maximum_pp),
        PyPH_WUFI.xml_node.XML_Node("Standard_VOS", _obj.standard_vos),
        PyPH_WUFI.xml_node.XML_Node("Standard_PP", _obj.standard_pp),
        PyPH_WUFI.xml_node.XML_Node("Basic_VOS", _obj.basic_vos),
        PyPH_WUFI.xml_node.XML_Node("Basic_PP", _obj.basic_pp),
        PyPH_WUFI.xml_node.XML_Node("Minimum_VOS", _obj.minimum_vos),
        PyPH_WUFI.xml_node.XML_Node("Minimum_PP", _obj.minimum_pp),
        PyPH_WUFI.xml_node.XML_Node("AuxiliaryEnergy", _obj.auxiliary_energy, "unit", "W"),
        PyPH_WUFI.xml_node.XML_Node("AuxiliaryEnergyDHW", _obj.auxiliary_energy_dhw, "unit", "W"),
        PyPH_WUFI.xml_node.XML_Node("InConditionedSpace", _obj.in_conditioned_space),
    ]


def _HVAC_Properties_Ventilation(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("CoverageWithinSystem", 1, "unit", "-"),
        PyPH_WUFI.xml_node.XML_Node("Unit", 51, "choice", "m??/h"),
        PyPH_WUFI.xml_node.XML_Node("Selection", 1, "choice", "Periodic day profiles"),
    ]


# -- HVAC Device | Elect Heater / DHW
def _HVAC_Elec_Heat_DHW(_obj: temp_MechanicalDevice) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Object(
            "PH_Parameters", _obj.properties, _schema_name="_HVAC_Properties_Elec_Heat_DHW_PH"
        ),
        PyPH_WUFI.xml_node.XML_Object(
            "DHW_Parameters", _obj.properties, _schema_name="_HVAC_Properties_Elec_Heat_DHW"
        ),
    ]


def _HVAC_Properties_Elec_Heat_DHW_PH(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("AuxiliaryEnergy", "unit", "W"),
        PyPH_WUFI.xml_node.XML_Node("AuxiliaryEnergyDHW", "unit", "W"),
        PyPH_WUFI.xml_node.XML_Node("InConditionedSpace", True),
    ]


def _HVAC_Properties_Elec_Heat_DHW(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("CoverageWithinSystem", 1, "unit", "-"),
        PyPH_WUFI.xml_node.XML_Node("Unit", 120, "choice", "Ltr/h"),
        PyPH_WUFI.xml_node.XML_Node("Selection", 1, "choice", "Periodic day profiles"),
    ]


# -- HVAC Device | Hot Water Tank
def _HVAC_Water_Tank(_obj: temp_MechanicalDevice) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Object("PH_Parameters", _obj.properties, _schema_name="_HVAC_Properties_Water_Tank_PH"),
        PyPH_WUFI.xml_node.XML_Object("DHW_Parameters", _obj.properties, _schema_name="_HVAC_Properties_Water_Tank"),
    ]


def _HVAC_Properties_Water_Tank_PH(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("SolarThermalStorageCapacity", _obj.volume, "unit", "Liter"),
        PyPH_WUFI.xml_node.XML_Node("StorageLossesStandby", "unit", "W/K"),
        PyPH_WUFI.xml_node.XML_Node("TotalSolarThermalStorageLosses", _obj.standby_loses, "unit", "W/K"),
        PyPH_WUFI.xml_node.XML_Node("InputOption", 1, "choice", "Specific total losses"),
        PyPH_WUFI.xml_node.XML_Node("AverageHeatReleaseStorage", "unit", "W"),
        PyPH_WUFI.xml_node.XML_Node("TankRoomTemp", "unit", "??C"),
        PyPH_WUFI.xml_node.XML_Node("TypicalStorageWaterTemperature", "unit", "??C"),
        PyPH_WUFI.xml_node.XML_Node("QauntityWS", _obj.quantity),
        PyPH_WUFI.xml_node.XML_Node("AuxiliaryEnergy", "unit", "W"),
        PyPH_WUFI.xml_node.XML_Node("AuxiliaryEnergyDHW", "unit", "W"),
        PyPH_WUFI.xml_node.XML_Node("InConditionedSpace", True),
    ]


def _HVAC_Properties_Water_Tank(_obj) -> list[xml_writable]:
    return [
        PyPH_WUFI.xml_node.XML_Node("CoverageWithinSystem", 1, "unit", "-"),
        PyPH_WUFI.xml_node.XML_Node("Unit", 120, "choice", "Ltr/h"),
        PyPH_WUFI.xml_node.XML_Node("Selection", 1, "choice", "Periodic day profiles"),
    ]
