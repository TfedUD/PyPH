# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""
WIP: Example workflow for importing and exising HBJSON file, building the PHX 
model objects, and exporting the PHX_Project out to a WUFI XML file.
"""

import PHX.project
import PHX.bldg_segment
import PHX.type_collections
import PHX.utilization_patterns
import PHX.hvac
import PyPH_WUFI.build_WUFI_xml

from PyPH_HBJSON.read_HBJSON_file import read_hb_json
import PyPH_HBJSON.create_PHX_Zones
from PyPH_HBJSON.create_PHX_components import (
    create_new_opaque_component_from_hb_face,
    set_compo_exterior_exposure_from_hb_face,
    set_compo_colors_by_hb_face,
    set_compo_assembly_from_hb_face,
    create_new_window_component_from_hb_aperture,
)
from PyPH_HBJSON.create_PHX_assemblies import (
    create_new_assembly_from_hb_face,
    create_new_window_type_from_hb_face,
    set_compo_window_type_from_hb_aperture,
)
import PyPH_HBJSON.create_PHX_BldgSegments


# --- Note: Path format in MAC OS (forward slash)
SOURCE_FILE = "sample/EM_sample_input_HBJSON/Sample_Input.hbjson"
TARGET_FILE_XML = "sample/EM_sample_output_WUFI_XML/Sample_Output.xml"

# ------------------------------------------------------------------------------
# --- Read in an existing HB_JSON and re-build the HB Objects
print("- " * 50)
print("> Reading in the HBJSON file...")
hb_model = read_hb_json(SOURCE_FILE)

# --- Build the Construction Assembly-Types, Window-Types
# ------------------------------------------------------------------------------
assmbly_collection = PHX.type_collections.AssemblyCollection()
window_type_collection = PHX.type_collections.WindowTypeCollection()
for room in hb_model.rooms:
    for face in room.faces:
        opaque_assembly = create_new_assembly_from_hb_face(face)
        assmbly_collection.add_new_assembly_to_collection(opaque_assembly)

        for aperture in face.apertures:
            new_window_type = create_new_window_type_from_hb_face(aperture)
            window_type_collection.add_new_window_type_to_collection(new_window_type)


# --- Set up the new Project
# ------------------------------------------------------------------------------
project_1 = PHX.project.Project()


# --- Build the Zones and Rooms
# ------------------------------------------------------------------------------
# --- Build all the Zones first. The Zones need to all be in place so that the exterior
# --- exposures for any adjacent-surfaces can be set with the proper ID number
# --- when building Components.
for room in hb_model.rooms:
    host_blg_segment = PyPH_HBJSON.create_PHX_BldgSegments.get_host_PHX_BldgSegment(
        project_1, room
    )
    new_zone = PyPH_HBJSON.create_PHX_Zones.create_PHX_Zone_from_HB_room(room)
    new_spaces = PyPH_HBJSON.create_PHX_Zones.create_PHX_Spaces_from_HB_room(room)
    new_zone.add_spaces(new_spaces)

    # -- Add to the zone's totals
    new_zone.volume_gross += room.volume
    new_zone.volume_gross_selection = 6  # user-defined

    host_blg_segment.add_zones(new_zone)

    # --
    # Note: for now, all Honeybee Rooms get a single 'System'. Might need to
    # change this in the future? Not sure when/if you would need more than 1 system?
    host_blg_segment.HVAC.default_system.add_zone_to_system_coverage(new_zone)
    host_blg_segment.HVAC.default_system.add_zone_ventilators_to_system(new_zone)

    # -- Figure out the Infiltration airflow / n50, q50
    room_infiltration = PyPH_HBJSON.create_PHX_Zones.calc_HB_room_infiltration(room)
    host_blg_segment.infiltration.annual_avg_airflow += room_infiltration

    # new_zone = add_default_res_appliance_to_zone( new_zone )

# # --- Bulild all the Components (Surfaces, Windows)
# # ----------------------------------------------------------------------------
for room in hb_model.rooms:
    host_blg_segment = PyPH_HBJSON.create_PHX_BldgSegments.get_host_PHX_BldgSegment(
        project_1, room
    )
    zone = host_blg_segment.get_zone_by_identifier(room.identifier)

    for face in room.faces:
        # -- Build the opaque Components
        opaque_compo = create_new_opaque_component_from_hb_face(face)
        opaque_compo.set_host_zone_name(zone)
        # opaque_compo = set_compo_interior_exposure_from_hb_face(opaque_compo, zone)
        opaque_compo = set_compo_exterior_exposure_from_hb_face(
            opaque_compo, face, host_blg_segment.zones
        )
        opaque_compo = set_compo_colors_by_hb_face(opaque_compo, face)
        opaque_compo = set_compo_assembly_from_hb_face(
            opaque_compo, face, assmbly_collection
        )

        # -- Add any Apertures found on the face
        for aperture in face.apertures:
            host_polygon_identifier = opaque_compo.polygons[0].identifier
            window_compo = create_new_window_component_from_hb_aperture(aperture, zone)
            window_compo = set_compo_window_type_from_hb_aperture(
                window_compo, aperture, window_type_collection
            )
            opaque_compo.add_window_as_child(window_compo, host_polygon_identifier)

            host_blg_segment.add_components(window_compo)

        # -- Pack the new Polygons & Components onto the BldgSegment.
        host_blg_segment.add_components(opaque_compo)


# --- Clean up the BuildingSegments
# ----------------------------------------------------------------------------
for seg in project_1.lBldgSegments:
    # -- This is (required?) for PHIUS Certification.
    # -- Sometimes might not want this though, so needs to be user-setting
    seg.merge_zones()
    seg.merge_components(by="assembly")


# # ----------------------------------------------------------------------------
project_1.add_assemblies_from_collection(assmbly_collection)
project_1.add_window_types_from_collection(window_type_collection)

# # --- Output the new Project to an XML file for WUFI
# # ----------------------------------------------------------------------------
print("> Writing out the XML file...")
PyPH_WUFI.build_WUFI_xml.write_Project_to_wp_xml_file(TARGET_FILE_XML, project_1)
