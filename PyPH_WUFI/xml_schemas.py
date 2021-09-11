# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""WUFI XML Output fields for all Objects

During export, XML builder will call the 'xml_data' property of each object
which returns a list of XML_Nodes, XML_Objects, or an XML_List, as defined in
each of the functions below.

Note: each function here should have the exact same name as its 'parent' but 
with an underscore in front. ie: '_Variant' maps to the 'Variant' parent class.
"""

from collections import namedtuple

import PHX.spaces

import PyPH_WUFI.xml_node
import PyPH_WUFI.selection
import PyPH_WUFI.prepare_data


def _WindowType(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.n),
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


# - Utilization Patterns
def _UtilizationPattern_Vent(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.name),
        PyPH_WUFI.xml_node.XML_Node("OperatingDays", _obj.operating_days),
        PyPH_WUFI.xml_node.XML_Node("OperatingWeeks", _obj.operating_weeks),
        PyPH_WUFI.xml_node.XML_Node("Maximum_DOS", _obj.utilization_rates.maximum.daily_op_sched),
        PyPH_WUFI.xml_node.XML_Node("Maximum_PDF", _obj.utilization_rates.maximum.frac_of_design_airflow),
        PyPH_WUFI.xml_node.XML_Node("Standard_DOS", _obj.utilization_rates.standard.daily_op_sched),
        PyPH_WUFI.xml_node.XML_Node("Standard_PDF", _obj.utilization_rates.standard.frac_of_design_airflow),
        PyPH_WUFI.xml_node.XML_Node("Basic_DOS", _obj.utilization_rates.basic.daily_op_sched),
        PyPH_WUFI.xml_node.XML_Node("Basic_PDF", _obj.utilization_rates.basic.frac_of_design_airflow),
        PyPH_WUFI.xml_node.XML_Node("Minimum_DOS", _obj.utilization_rates.minimum.daily_op_sched),
        PyPH_WUFI.xml_node.XML_Node("Minimum_PDF", _obj.utilization_rates.minimum.frac_of_design_airflow),
    ]


def _UtilizationPattern_NonRes(_obj):
    # type: (PHX.spaces.Space) -> list
    # cus' WUFI wants absent, not present...
    absent_fac = 1.0 - float(_obj.occupancy.utilization.annual_utilization_factor)
    if _obj.occupancy.people_per_area:
        m2_per_person = 1 / _obj.occupancy.people_per_area
    else:
        m2_per_person = 0

    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.occupancy.name),
        # -- Occupancy
        PyPH_WUFI.xml_node.XML_Node("BeginUtilization", _obj.occupancy.utilization.start_hour),
        PyPH_WUFI.xml_node.XML_Node("EndUtilization", _obj.occupancy.utilization.end_hour),
        PyPH_WUFI.xml_node.XML_Node("AnnualUtilizationDays", _obj.occupancy.utilization.annual_utilization_days),
        PyPH_WUFI.xml_node.XML_Node("RelativeAbsenteeism", absent_fac),
        # -- Lighting
        PyPH_WUFI.xml_node.XML_Node("IlluminationLevel", _obj.lighting.space_illumination),
        PyPH_WUFI.xml_node.XML_Node("HeightUtilizationLevel", _obj.lighting.installed_power_density),
        PyPH_WUFI.xml_node.XML_Node(
            "PartUseFactorPeriodForLighting", _obj.lighting.utilization.annual_utilization_factor
        ),
        PyPH_WUFI.xml_node.XML_Node("AverageOccupancy", m2_per_person),
        # PyPH_WUFI.xml_node.XML_Node("RoomSetpointTemperature", _obj._________),
        # PyPH_WUFI.xml_node.XML_Node("HeatingTemperatureReduction", _obj._________),
        # PyPH_WUFI.xml_node.XML_Node("DailyUtilizationHours", _obj._________),
        # PyPH_WUFI.xml_node.XML_Node("AnnualUtilizationHours", _obj._________),
        # PyPH_WUFI.xml_node.XML_Node("AnnualUtilizationHoursDaytime", _obj._________),
        # PyPH_WUFI.xml_node.XML_Node("AnnualUtilizationHoursNighttime", _obj._________),
        # PyPH_WUFI.xml_node.XML_Node("DailyHeatingOperationHours", _obj._________),
        # PyPH_WUFI.xml_node.XML_Node("DailyVentilationOperatingHours", _obj._________),
        # PyPH_WUFI.xml_node.XML_Node("NumberOfMaxTabsPerDay", _obj._________),
    ]


# - Constructions
def _Material(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.n),
        PyPH_WUFI.xml_node.XML_Node("ThermalConductivity", _obj.tConD),
        PyPH_WUFI.xml_node.XML_Node("BulkDensity", _obj.densB),
        PyPH_WUFI.xml_node.XML_Node("Porosity", _obj.poros),
        PyPH_WUFI.xml_node.XML_Node("HeatCapacity", _obj.hCapS),
        PyPH_WUFI.xml_node.XML_Node("WaterVaporResistance", _obj.difRes),
        PyPH_WUFI.xml_node.XML_Node("ReferenceW", _obj.refWC),
    ]


def _Layer(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("Thickness", _obj.thickness, "unit", "m"),
        PyPH_WUFI.xml_node.XML_Object("Material", _obj.material),
    ]


def _Assembly(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.n),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Assembly::Order_Layers", _obj.Order_Layers).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node(*PyPH_WUFI.selection.Selection("Assembly::Grid_Kind", _obj.Grid_Kind).xml_data),
        PyPH_WUFI.xml_node.XML_List(
            "Layers",
            [PyPH_WUFI.xml_node.XML_Object("Layer", _, "index", i) for i, _ in enumerate(_obj.Layers)],
        ),
    ]


# - Geometry
def _Vertex(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("X", round(_obj.x, 8)),
        PyPH_WUFI.xml_node.XML_Node("Y", round(_obj.y, 8)),
        PyPH_WUFI.xml_node.XML_Node("Z", round(_obj.z, 8)),
    ]


def _Polygon(_obj):
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


def _Geom(_obj):
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


def _ClimateLocation(_obj):
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


def _WP_Color(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("Alpha", _obj.alpha),
        PyPH_WUFI.xml_node.XML_Node("Red", _obj.red),
        PyPH_WUFI.xml_node.XML_Node("Green", _obj.green),
        PyPH_WUFI.xml_node.XML_Node("Blue", _obj.blue),
    ]


def _Component(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.n),
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


def _RoomVentilation(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.display_name),
        PyPH_WUFI.xml_node.XML_Node("Quantity", _obj.quantity),
        PyPH_WUFI.xml_node.XML_Node(*PyPH_WUFI.selection.Selection("WP_Room::Type", _obj.type).xml_data),
        PyPH_WUFI.xml_node.XML_Node("AreaRoom", _obj.floor_area_weighted, "unit", "m²"),
        PyPH_WUFI.xml_node.XML_Node("ClearRoomHeight", _obj.clear_height, "unit", "m"),
        PyPH_WUFI.xml_node.XML_Node("IdentNrUtilizationPatternVent", _obj.ventilation.utilization.id),
        PyPH_WUFI.xml_node.XML_Node("IdentNrVentilationUnit", _obj.ventilation.system.ventilator.id),
        PyPH_WUFI.xml_node.XML_Node(
            "DesignVolumeFlowRateSupply",
            _obj.ventilation.airflow_rates.supply,
            "unit",
            "m³/h",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "DesignVolumeFlowRateExhaust",
            _obj.ventilation.airflow_rates.extract,
            "unit",
            "m³/h",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "DesignFlowInterzonalUserDef",
            _obj.ventilation.airflow_rates.transfer,
            "unit",
            "m³/h",
        ),
    ]


def _RoomLoads_Occupancy(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.display_name),
        PyPH_WUFI.xml_node.XML_Node("IdentNrUtilizationPattern", _obj.occupancy.id),
        PyPH_WUFI.xml_node.XML_Node("ChoiceActivityPersons", 3, "choice", "Adult, standing or light work"),
        # PyPH_WUFI.xml_node.XML_Node("NumberOccupants", _obj.peak_occupancy),
        PyPH_WUFI.xml_node.XML_Node("FloorAreaUtilizationZone", _obj.floor_area_weighted),
    ]


def _Zone(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.n),
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Zone::GrossVolume_Selection", _obj.volume_gross_selection).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("GrossVolume", _obj.volume_gross, "unit"),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Zone::NetVolume_Selection", _obj.volume_net_selection).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("NetVolume", _obj.volume_net, "unit"),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Zone::FloorArea_Selection", _obj.floor_area_selection).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("FloorArea", _obj.floor_area, "unit"),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Zone::ClearanceHeight_Selection", _obj.clearance_height_selection).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("ClearanceHeight", _obj.clearance_height, "unit", "m"),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection(
                "Zone::SpecificHeatCapacity_Selection", _obj.spec_heat_cap_selection
            ).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("SpecificHeatCapacity", _obj.spec_heat_cap, "unit", "Wh/m²K"),
        PyPH_WUFI.xml_node.XML_List(
            "RoomsVentilation",
            [
                PyPH_WUFI.xml_node.XML_Object("Room", _, "index", i, "_RoomVentilation")
                for i, _ in enumerate(_obj.spaces)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "LoadsPersonsPH",
            [
                PyPH_WUFI.xml_node.XML_Object("LoadPerson", _, "index", i, "_RoomLoads_Occupancy")
                for i, _ in enumerate(_obj.spaces)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "HomeDevice",
            [PyPH_WUFI.xml_node.XML_Object("Device", _, "index", i) for i, _ in enumerate(_obj.appliances)],
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
            "Wh/m³",
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
            "Wh/m³",
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


def _Building(_obj):
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


# -- PHIUS Data
def _IntGainsData(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("EvaporationHeatPerPerson", _obj.int_gains_evap_per_person, "unit", "W"),
        PyPH_WUFI.xml_node.XML_Node("HeatLossFluschingWC", _obj.int_gains_flush_heat_loss),
        PyPH_WUFI.xml_node.XML_Node("QuantityWCs", _obj.int_gains_num_toilets, "unit", "-"),
        PyPH_WUFI.xml_node.XML_Node("RoomCategory", 1, _obj.int_gains_toilet_room_util_pat),
        PyPH_WUFI.xml_node.XML_Node("UseDefaultValuesSchool", _obj.int_gains_use_school_defaults),
        PyPH_WUFI.xml_node.XML_Node(
            "MarginalPerformanceRatioDHW", _obj.int_gains_dhw_marginal_perf_ratio, "unit", "-"
        ),
    ]


def _PH_Building(_obj):
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
        # PyPH_WUFI.xml_node.XML_Node("InternalGainsSetting", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("EnvelopeAirtightnessCoefficient", _obj.q50, "unit", "m³/m²h"),
        PyPH_WUFI.xml_node.XML_List(
            "FoundationInterfaces",
            [
                PyPH_WUFI.xml_node.XML_Object("FoundationInterface", _, "index", i)
                for i, _ in enumerate(_obj.foundations)
            ],
        ),
        PyPH_WUFI.xml_node.XML_Object("InternalGainsAdditionalData", _obj.int_gains_data),
    ]


def _PassivehouseData(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("PHIUS::PH_CertificateCriteria", _obj.certification_criteria).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("PHIUS::PH_SelectionTargetData", _obj.localization_selection_type).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("AnnualHeatingDemand", _obj.PHIUS2021_heating_demand, "unit", "kWh/m²a"),
        PyPH_WUFI.xml_node.XML_Node("AnnualCoolingDemand", _obj.PHIUS2021_cooling_demand, "unit", "kWh/m²a"),
        PyPH_WUFI.xml_node.XML_Node("PeakHeatingLoad", _obj.PHIUS2021_heating_load, "unit", "W/m²"),
        PyPH_WUFI.xml_node.XML_Node("PeakCoolingLoad", _obj.PHIUS2021_cooling_load, "unit", "W/m²"),
        PyPH_WUFI.xml_node.XML_List(
            "PH_Buildings",
            [PyPH_WUFI.xml_node.XML_Object("PH_Building", _, "index", i) for i, _ in enumerate(_obj.PH_Buildings)],
        ),
    ]


def _PH_ClimateLocation(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("Selection", _obj.Selection),
        PyPH_WUFI.xml_node.XML_Node("Latitude", _obj.Latitude),
        PyPH_WUFI.xml_node.XML_Node("HeightNNWeatherStation", _obj.HeightNNWeatherStation),
        PyPH_WUFI.xml_node.XML_Node("Longitude", _obj.Longitude),
        PyPH_WUFI.xml_node.XML_Node("dUTC", _obj.dUTC),
        PyPH_WUFI.xml_node.XML_Node("DailyTemperatureSwingSummer", _obj.DailyTemperatureSwingSummer),
        PyPH_WUFI.xml_node.XML_Node("AverageWindSpeed", _obj.AverageWindSpeed),
        PyPH_WUFI.xml_node.XML_Node("ClimateZone", _obj.ClimateZone),
        PyPH_WUFI.xml_node.XML_Node("GroundThermalConductivity", _obj.GroundThermalConductivity),
        PyPH_WUFI.xml_node.XML_Node("GroundHeatCapacitiy", _obj.GroundHeatCapacitiy),
        PyPH_WUFI.xml_node.XML_Node("GroundDensity", _obj.GroundDensity),
        PyPH_WUFI.xml_node.XML_Node("DepthGroundwater", _obj.DepthGroundwater),
        PyPH_WUFI.xml_node.XML_Node("FlowRateGroundwater", _obj.FlowRateGroundwater),
        PyPH_WUFI.xml_node.XML_Node("SelectionPECO2Factor", _obj.SelectionPECO2Factor),
        PyPH_WUFI.xml_node.XML_List(
            "TemperatureMonthly",
            [PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i) for i, _ in enumerate(_obj.TemperatureMonthly)],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "DewPointTemperatureMonthly",
            [
                PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i)
                for i, _ in enumerate(_obj.DewPointTemperatureMonthly)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "SkyTemperatureMonthly",
            [PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i) for i, _ in enumerate(_obj.SkyTemperatureMonthly)],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "GroundTemperatureMonthly",
            [PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i) for i, _ in enumerate(_obj.GroundTemperatureMonthly)],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "NorthSolarRadiationMonthly",
            [
                PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i)
                for i, _ in enumerate(_obj.NorthSolarRadiationMonthly)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "EastSolarRadiationMonthly",
            [PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i) for i, _ in enumerate(_obj.EastSolarRadiationMonthly)],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "SouthSolarRadiationMonthly",
            [
                PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i)
                for i, _ in enumerate(_obj.SouthSolarRadiationMonthly)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "WestSolarRadiationMonthly",
            [PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i) for i, _ in enumerate(_obj.WestSolarRadiationMonthly)],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "GlobalSolarRadiationMonthly",
            [
                PyPH_WUFI.xml_node.XML_Node("Item", _, "index", i)
                for i, _ in enumerate(_obj.GlobalSolarRadiationMonthly)
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


# -- HVAC
def _Ventilator_PH_Parameters(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("Quantity", _obj.Quantity),
        PyPH_WUFI.xml_node.XML_Node(
            "ElectricEfficiency",
            _obj.ElectricEfficiency,
            "unit",
            "Wh/m³",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "SubsoilHeatExchangeEfficiency",
            _obj.SubsoilHeatExchangeEfficiency,
            "unit",
            "-",
        ),
        PyPH_WUFI.xml_node.XML_Node(
            "HumidityRecoveryEfficiency",
            _obj.HumidityRecoveryEfficiency,
            "unit",
            "-",
        ),
        PyPH_WUFI.xml_node.XML_Node("VolumeFlowRateFrom", _obj.VolumeFlowRateFrom, "unit", "m³/h"),
        PyPH_WUFI.xml_node.XML_Node("VolumeFlowRateTo", _obj.VolumeFlowRateTo, "unit", "m³/h"),
        PyPH_WUFI.xml_node.XML_Node(
            "TemperatureBelowDefrostUsed",
            _obj.TemperatureBelowDefrostUsed,
            "unit",
            "°C",
        ),
        PyPH_WUFI.xml_node.XML_Node("FrostProtection", _obj.FrostProtection),
        PyPH_WUFI.xml_node.XML_Node("DefrostRequired", _obj.DefrostRequired),
        PyPH_WUFI.xml_node.XML_Node("NoSummerBypass", _obj.NoSummerBypass),
        PyPH_WUFI.xml_node.XML_Node("HRVCalculatorData", _obj.HRVCalculatorData),
        PyPH_WUFI.xml_node.XML_Node("Maximum_VOS", _obj.Maximum_VOS),
        PyPH_WUFI.xml_node.XML_Node("Maximum_PP", _obj.Maximum_PP),
        PyPH_WUFI.xml_node.XML_Node("Standard_VOS", _obj.Standard_VOS),
        PyPH_WUFI.xml_node.XML_Node("Standard_PP", _obj.Standard_PP),
        PyPH_WUFI.xml_node.XML_Node("Basic_VOS", _obj.Basic_VOS),
        PyPH_WUFI.xml_node.XML_Node("Basic_PP", _obj.Basic_PP),
        PyPH_WUFI.xml_node.XML_Node("Minimum_VOS", _obj.Minimum_VOS),
        PyPH_WUFI.xml_node.XML_Node("Minimum_PP", _obj.Minimum_PP),
        PyPH_WUFI.xml_node.XML_Node("AuxiliaryEnergy", _obj.AuxiliaryEnergy, "unit", "W"),
        PyPH_WUFI.xml_node.XML_Node("AuxiliaryEnergyDHW", _obj.AuxiliaryEnergyDHW, "unit", "W"),
        PyPH_WUFI.xml_node.XML_Node("InConditionedSpace", _obj.InConditionedSpace),
    ]


def _Ventilator(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.Name),
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("HVAC_Device::SystemType", _obj.SystemType).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("HVAC_Device::TypeDevice", _obj.TypeDevice).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Heating", _obj.UsedFor_Heating),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_DHW", _obj.UsedFor_DHW),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Cooling", _obj.UsedFor_Cooling),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Ventilation", _obj.UsedFor_Ventilation),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Humidification", _obj.UsedFor_Humidification),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Dehumidification", _obj.UsedFor_Dehumidification),
        PyPH_WUFI.xml_node.XML_Node("UseOptionalClimate", _obj.UseOptionalClimate),
        PyPH_WUFI.xml_node.XML_Node("IdentNr_OptionalClimate", _obj.IdentNr_OptionalClimate),
        PyPH_WUFI.xml_node.XML_Object("PH_Parameters", _obj.PH_Parameters),
        PyPH_WUFI.xml_node.XML_Node("HeatRecovery", _obj.PH_Parameters.HeatRecoveryEfficiency, "unit", "-"),
        PyPH_WUFI.xml_node.XML_Node(
            "MoistureRecovery",
            _obj.PH_Parameters.HumidityRecoveryEfficiency,
            "unit",
            "-",
        ),
    ]


def _HVAC_Device(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.Name),
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("HVAC_Device::SystemType", _obj.SystemType).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("HVAC_Device::TypeDevice", _obj.TypeDevice).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Heating", _obj.UsedFor_Heating),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_DHW", _obj.UsedFor_DHW),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Cooling", _obj.UsedFor_Cooling),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Ventilation", _obj.UsedFor_Ventilation),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Humidification", _obj.UsedFor_Humidification),
        PyPH_WUFI.xml_node.XML_Node("UsedFor_Dehumidification", _obj.UsedFor_Dehumidification),
        PyPH_WUFI.xml_node.XML_Node("UseOptionalClimate", _obj.UseOptionalClimate),
        PyPH_WUFI.xml_node.XML_Node("IdentNr_OptionalClimate", _obj.IdentNr_OptionalClimate),
    ]


def _HVAC_System_ZoneCover(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNrZone", _obj.idZoneCovered),
        PyPH_WUFI.xml_node.XML_Node("CoverageHeating", _obj.cover_heating),
        PyPH_WUFI.xml_node.XML_Node("CoverageCooling", _obj.cover_cooling),
        PyPH_WUFI.xml_node.XML_Node("CoverageVentilation", _obj.cover_ventilation),
        PyPH_WUFI.xml_node.XML_Node("CoverageHumidification", _obj.cover_humidification),
        PyPH_WUFI.xml_node.XML_Node("CoverageDehumidification", _obj.cover_dehumidification),
    ]


def _HVAC_System(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.n),
        PyPH_WUFI.xml_node.XML_Node(*PyPH_WUFI.selection.Selection("HVAC_System::Type", _obj.typeSys).xml_data),
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_List(
            "ZonesCoverage",
            [PyPH_WUFI.xml_node.XML_Object("ZoneCoverage", _, "index", i) for i, _ in enumerate(_obj.lZoneCover)],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "Devices",
            [PyPH_WUFI.xml_node.XML_Object("Device", _, "index", i) for i, _ in enumerate(_obj.lDevice)],
        ),
        PyPH_WUFI.xml_node.XML_Node("Distribution", _obj.distrib),
        PyPH_WUFI.xml_node.XML_Node("PHDistribution", _obj.PHdistrib),
    ]


def _HVAC(_obj):
    return [
        PyPH_WUFI.xml_node.XML_List(
            "Systems",
            [PyPH_WUFI.xml_node.XML_Object("System", _, "index", i) for i, _ in enumerate(_obj.lSystem)],
        ),
    ]


# -- Variant, Project
def _BldgSegment(_obj):
    """
    Note: For WUFI, each 'Building-Segment' will map to a separate 'Variant'.
    This is done for PHIUS modeling and allows for Non-Res and Res. sections
    of a building to be modeled in the same WUFI file, in different 'Cases'

    This function builds up the speccific tree WUIF requires with all interstitial layers/nodes
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

    # -- Create temporary objects / layers to collect the data in the right format
    # -- Building Object
    tBuilding = namedtuple(
        "Building",
        [
            "numerics",
            "airflow_model",
            "count_generator",
            "has_been_generated",
            "has_been_changed_since_last_gen",
            "components",
            "zones",
        ],
    )

    tbuilding_container = tBuilding(
        _obj.numerics,
        _obj.airflow_model,
        _obj.count_generator,
        _obj.has_been_generated,
        _obj.has_been_changed_since_last_gen,
        _obj.components,
        _obj.zones,
    )

    # --- PH_Building Object
    tIntGainsData = namedtuple(
        "IntGainsData",
        [
            "int_gains_evap_per_person",
            "int_gains_flush_heat_loss",
            "int_gains_num_toilets",
            "int_gains_toilet_room_util_pat",
            "int_gains_use_school_defaults",
            "int_gains_dhw_marginal_perf_ratio",
        ],
    )

    tPH_Building = namedtuple(
        "PH_Building",
        [
            "id",
            "occupancy_category",
            "occupancy_type",
            "building_status",
            "building_type",
            "occupancy_setting_method",
            "num_units",
            "num_stories",
            "q50",
            "n50",
            "foundations",
            "int_gains_data",
        ],
    )

    tPH_Building = tPH_Building(
        _obj.id,
        _obj.occupancy.category,
        _obj.occupancy.usage_type,
        _obj.PHIUS_certification.building_status,
        _obj.PHIUS_certification.building_type,
        2,
        _obj.occupancy.num_units,
        _obj.occupancy.num_stories,
        _obj.infiltration.q50,
        _obj.infiltration.n50,
        _obj.foundations,
        tIntGainsData(
            _obj.PHIUS_certification.int_gains_evap_per_person,
            _obj.PHIUS_certification.int_gains_flush_heat_loss,
            _obj.PHIUS_certification.int_gains_num_toilets,
            _obj.PHIUS_certification.int_gains_toilet_room_util_pat,
            _obj.PHIUS_certification.int_gains_use_school_defaults,
            _obj.PHIUS_certification.int_gains_dhw_marginal_perf_ratio,
        ),
    )

    # ---- PassivehouseData Object
    tPassivehouseData = namedtuple(
        "PassivehouseData",
        [
            "certification_criteria",
            "localization_selection_type",
            "PHIUS2021_heating_demand",
            "PHIUS2021_cooling_demand",
            "PHIUS2021_heating_load",
            "PHIUS2021_cooling_load",
            "PH_Buildings",
        ],
    )

    tPH_Data = tPassivehouseData(
        _obj.PHIUS_certification.certification_criteria,
        _obj.PHIUS_certification.localization_selection_type,
        _obj.PHIUS_certification.PHIUS2021_heating_demand,
        _obj.PHIUS_certification.PHIUS2021_cooling_demand,
        _obj.PHIUS_certification.PHIUS2021_heating_load,
        _obj.PHIUS_certification.PHIUS2021_cooling_load,
        [tPH_Building],
    )

    # --- Build the final output list
    return [
        PyPH_WUFI.xml_node.XML_Node("IdentNr", _obj.id),
        PyPH_WUFI.xml_node.XML_Node("Name", _obj.n),
        PyPH_WUFI.xml_node.XML_Node("Remarks", _obj.remarks),
        PyPH_WUFI.xml_node.XML_Object("Graphics_3D", _obj.geom),
        PyPH_WUFI.xml_node.XML_Object("Building", tbuilding_container),
        PyPH_WUFI.xml_node.XML_Object("ClimateLocation", _obj.cliLoc),
        PyPH_WUFI.xml_node.XML_Node("PlugIn", _obj.plugin),
        PyPH_WUFI.xml_node.XML_Object("HVAC", _obj.HVAC),
        PyPH_WUFI.xml_node.XML_Object("PassivehouseData", tPH_Data),
    ]


def _Date(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("Year", _obj.Year),
        PyPH_WUFI.xml_node.XML_Node("Month", _obj.Month),
        PyPH_WUFI.xml_node.XML_Node("Day", _obj.Day),
        PyPH_WUFI.xml_node.XML_Node("Hour", _obj.Hour),
        PyPH_WUFI.xml_node.XML_Node("Minutes", _obj.Minutes),
    ]


def _ProjectData(_obj):
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


def _Project(_obj):
    util_patter_collection_ventilation = PyPH_WUFI.prepare_data.build_vent_utilization_patterns_from_zones(_obj.zones)
    util_pattern_collection_NonRes = PyPH_WUFI.prepare_data.build_NonRes_utilization_patterns_from_zones(_obj.zones)

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
                for i, _ in enumerate(util_patter_collection_ventilation)
            ],
        ),
        PyPH_WUFI.xml_node.XML_List(
            "UtilizationPatternsPH",
            [
                PyPH_WUFI.xml_node.XML_Object("UtilizationPattern", _, "index", i)
                for i, _ in enumerate(util_pattern_collection_NonRes)
            ],
        ),
        # Note: For WUFI, each 'Building-Segment' will map to a separate 'Variant'.
        # This is done for PHIUS modeling and allows for Non-Res and Res. sections
        # of a building to be modeled in the same WUFI file, in different 'Cases'
        PyPH_WUFI.xml_node.XML_List(
            "Variants",
            [PyPH_WUFI.xml_node.XML_Object("Variant", _, "index", i) for i, _ in enumerate(_obj.building_segments)],
        ),
    ]


# -- Appliances
def _Appliance_dishwasher(_obj):
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


def _Appliance_clothes_washer(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("UtilizationFactor", _obj.washer_utilization_factor, "unit", "-"),
        PyPH_WUFI.xml_node.XML_Node("MEF_ModifiedEnergyFactor", _obj.washer_modified_energy_factor, "unit", "-"),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Appliances::Connection", _obj.washer_connection).xml_data
        ),
    ]


def _Appliance_clothes_dryer(_obj):
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


def _Appliance_fridge(_obj):
    return []


def _Appliance_freezer(_obj):
    return []


def _Appliance_fridge_freezer(_obj):
    return []


def _Appliance_cooking(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Appliances::CookingWith", _obj.cooktop_type).xml_data
        ),
    ]


def _Appliance_PHIUS_MEL(_obj):
    return []


def _Appliance_PHIUS_Lighting_Int(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("FractionHightEfficiency", _obj.lighting_frac_high_efficiency, "unit", "-"),
    ]


def _Appliance_PHIUS_Lighting_Ext(_obj):
    return [
        PyPH_WUFI.xml_node.XML_Node("FractionHightEfficiency", _obj.lighting_frac_high_efficiency, "unit", "-"),
    ]


def _Appliance_Custom_Electric_per_Year(_obj):
    return []


def _Appliance_Custom_Electric_per_Use(_obj):
    return []


def _Appliance(_obj):
    """Appliances have some basic shared params, then a bunch of custom params"""

    appliances = {
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

    # Fix the energy Norm.
    # WUFI uses '1' for both 'Use' and 'Day'
    energy_norm = PyPH_WUFI.selection.Selection(
        "Appliances::ReferenceEnergyDemandNorm", _obj.reference_energy_norm
    ).xml_data
    if energy_norm[1] == 99:
        energy_norm = (energy_norm[0], 1, energy_norm[2], energy_norm[3])

    # -- Build the basic params
    basic_params = [
        PyPH_WUFI.xml_node.XML_Node(*PyPH_WUFI.selection.Selection("Appliances::Type", _obj.type).xml_data),
        PyPH_WUFI.xml_node.XML_Node("Comment", _obj.comment),
        PyPH_WUFI.xml_node.XML_Node(
            *PyPH_WUFI.selection.Selection("Appliances::ReferenceQuantity", _obj.reference_quantity).xml_data
        ),
        PyPH_WUFI.xml_node.XML_Node("InConditionedSpace", _obj.in_conditioned_space),
        PyPH_WUFI.xml_node.XML_Node(*energy_norm),
        PyPH_WUFI.xml_node.XML_Node("EnergyDemandNorm", _obj.energy_demand, "unit", "kWh"),
        PyPH_WUFI.xml_node.XML_Node("EnergyDemandNormUse", _obj.energy_demand_per_use, "unit", "kWh"),
        PyPH_WUFI.xml_node.XML_Node("CEF_CombinedEnergyFactor", _obj.combined_energy_facor, "unit", "-"),
    ]

    # -- cus' of the bullshit with PHIUS that they pulled. Lazy fuckers
    if _obj.type in [13, 14, 15] and _obj.reference_quantity == 5:
        basic_params.append(PyPH_WUFI.xml_node.XML_Node("Quantity", int(_obj.user_defined_total)))
    else:
        basic_params.append(PyPH_WUFI.xml_node.XML_Node("Quantity", int(_obj.quantity)))

    return basic_params + appliances.get(_obj.type)(_obj)
