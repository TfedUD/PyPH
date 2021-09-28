# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""
WIP: Example workflow for importing and exising HBJSON file, building the PHX 
model objects, and exporting the PHX_Project out to a WUFI XML file.
"""

import PHX.project
import PHX.bldg_segment
import PyPH_WUFI.type_collections
import PyPH_WUFI.build_WUFI_xml

from PyPH_HBJSON.read_HBJSON_file import read_hb_json
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
import PyPH_HBJSON.create_PHX_Zones
import PyPH_HBJSON.create_PHX_Rooms
import PyPH_HBJSON.infiltration

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
assmbly_collection = PyPH_WUFI.type_collections.AssemblyCollection()
window_type_collection = PyPH_WUFI.type_collections.WindowTypeCollection()
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

# ------------------------------------------------------------------------------
# --- Build all the Rooms and Thermal-Zones first. The Thermal-Zones need to all be in place so that the Component's exterior
# --- exposures for any adjacent-surfaces can be set with the proper ID number when building Components.
for room in hb_model.rooms:
    phx_BldgSegment = PyPH_HBJSON.create_PHX_BldgSegments.get_host_PHX_BldgSegment(project_1, room)
    phx_Zone = PyPH_HBJSON.create_PHX_Zones.get_host_PHX_Zone(phx_BldgSegment, room)
    phx_Room = PyPH_HBJSON.create_PHX_Rooms.create_PHX_Room_from_HB_room(room)
    phx_Spaces = PyPH_HBJSON.create_PHX_Zones.create_PHX_Spaces_from_HB_room(room)

    phx_Room.add_spaces(phx_Spaces)
    phx_Zone.add_rooms(phx_Room)
    phx_BldgSegment.add_zones(phx_Zone)

    phx_BldgSegment.HVAC_system.add_zone_to_system_coverage(phx_Zone)

# --
# host_blg_segment.HVAC.default_system.add_zone_ventilators_to_system(new_zone)

# -- Figure out the Infiltration airflow / n50, q50
# room_infiltration_m3s = PyPH_HBJSON.infiltration.calc_HB_room_infiltration(room)
# room_infiltration_m3h = room_infiltration_m3s * 3600

# host_blg_segment.infiltration.annual_avg_airflow += room_infiltration_m3h

# # # --- Build all the Components (Surfaces, Windows)
# # # ----------------------------------------------------------------------------
for room in hb_model.rooms:
    phx_BldgSegment = PyPH_HBJSON.create_PHX_BldgSegments.get_host_PHX_BldgSegment(project_1, room)
    phx_Zone = PyPH_HBJSON.create_PHX_Zones.get_host_PHX_Zone(phx_BldgSegment, room)

    for face in room.faces:
        # -- Build the opaque Components
        opaque_compo = create_new_opaque_component_from_hb_face(face)
        opaque_compo.set_host_zone_name(phx_Zone)
        # opaque_compo = set_compo_interior_exposure_from_hb_face(opaque_compo, zone)
        opaque_compo = set_compo_exterior_exposure_from_hb_face(opaque_compo, face, phx_BldgSegment.zones)
        opaque_compo = set_compo_colors_by_hb_face(opaque_compo, face)
        opaque_compo = set_compo_assembly_from_hb_face(opaque_compo, face, assmbly_collection)

        # -- Add any Apertures found on the face
        for aperture in face.apertures:
            host_polygon_identifier = opaque_compo.polygons[0].identifier
            window_compo = create_new_window_component_from_hb_aperture(aperture, phx_Zone)
            window_compo = set_compo_window_type_from_hb_aperture(window_compo, aperture, window_type_collection)
            opaque_compo.add_window_as_child(window_compo, host_polygon_identifier)

            phx_BldgSegment.add_components(window_compo)

        # -- Pack the new Polygons & Components onto the BldgSegment.
        phx_BldgSegment.add_components(opaque_compo)


# # --- Clean up the BuildingSegments
# # ----------------------------------------------------------------------------
# for seg in project_1.building_segments:
#     # -- This is (required?) for PHIUS Certification.
#     # -- Sometimes might not want this though, so needs to be user-setting
#     seg.merge_zones()
#     seg.merge_components(by="assembly")

# # ----------------------------------------------------------------------------
project_1.add_assemblies_from_collection(assmbly_collection)
project_1.add_window_types_from_collection(window_type_collection)

# # --- Output the new Project to an XML file for WUFI
# # ----------------------------------------------------------------------------
print("> Writing out the XML file...")
PyPH_WUFI.build_WUFI_xml.write_Project_to_wp_xml_file(TARGET_FILE_XML, project_1)
