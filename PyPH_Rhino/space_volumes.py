# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to create new Space-Volumes and set attributes based on Rhino Geometry inputs"""

import PHX.spaces
import gh_io


def create_default_volume_geometry(IGH, _volume, _height=2.5):
    # type: (gh_io.IGH, float, float) -> tuple[list, float]
    """Creates a default volume-geometry space shape for a Volume Object

    Arguments:
    ----------
        * IGH (gh_io.IGH): The PyPH Grasshopper Interface Object
        * _volume: The Volume Object to build the default room for
        * _height (float): Default=2.5 (m)

    Returns:
    --------
        * tuple( list:(LBT Geometry), float: volume ):
            [0] A list of the new volume space geometry as LBT Geometry
            [1] The total volume (m3) for the geometry
    """

    if not _volume:
        return None

    extrusion_vector = IGH.grasshopper_components.UnitZ(_height)

    merged_floor_geom = IGH.merge_Face3D(_volume.floor.geometry)

    new_volume_geometry = []
    for _ in merged_floor_geom:
        for lbt_face3D in _:
            new_floor_srfc = IGH.convert_to_rhino_geom(lbt_face3D)
            new_volume_geometry.append(
                IGH.grasshopper_components.Extrude(new_floor_srfc, extrusion_vector)
            )

    total_volume = sum(
        IGH.grasshopper_components.Volume(g).volume for g in new_volume_geometry
    )
    volume_geom = IGH.convert_to_LBT_geom(new_volume_geometry)

    return (volume_geom, total_volume)


def create_volumes(IGH, _floors_dict, _space_geometry_dict):
    # type: (gh_io.IGH, dict, dict) -> dict
    """Creates a new Volume for each Floor input in the set. Will try and use any
    user-input space geometry to  form the Volume space-shape. Otherwise, will build
    default room shapes based on the Floor

    Arguments:
    ----------
        * _IGH (gh_io.IGH): The PyPH Grasshopper Interface Object
        * _floors_dict (dict): The dictionary of Floors to operate on
        * _space_geometry_dict (dict): The dictionary of user-input space geometry

    Returns:
    --------
        * (dict): A dict of the Volumes, organized by HB-Room
    """

    # --- Convert the input Space Geometry into a flat dict of Rhino Breps (joined)
    space_geometry_dict = {}
    for k, v in _space_geometry_dict.items():
        rh_srfcs = []
        for lbt_surfaces in v["Geometry"]:
            rh_srfcs.extend(IGH.convert_to_rhino_geom(lbt_surfaces))
        space_geometry_dict[k] = IGH.grasshopper_components.BrepJoin(rh_srfcs).breps

    # --- Create a new Volume for each Floor in the set
    # --- If it works, use user-input space geometry
    # --- Otherwise, build a default room Brep
    for hb_room_dict in _floors_dict.values():
        hb_room_dict["Volumes"] = []

        for list_of_floors in hb_room_dict["Floors"].values():

            for floor in list_of_floors:
                new_volume = PHX.spaces.Volume()
                new_volume.add_Floor(floor)

                merged_floor_geom = IGH.merge_Face3D(floor.geometry)
                rh_floor_surfaces = IGH.convert_to_rhino_geom(merged_floor_geom)

                for flr_srfc in rh_floor_surfaces:
                    for k, v in space_geometry_dict.items():
                        test_geometry = []
                        test_geometry.extend(flr_srfc)
                        test_geometry.append(v)

                        breps, closed = IGH.grasshopper_components.BrepJoin(
                            test_geometry
                        )

                        if closed is True:
                            new_volume.volume = IGH.grasshopper_components.Volume(
                                breps
                            ).volume
                            new_volume.volume_geometry = IGH.convert_to_LBT_geom(breps)
                            del space_geometry_dict[k]  # to speed up later tests

                # --- Add the default volume space, if needed
                if not new_volume.volume_geometry:
                    (
                        new_volume.volume_geometry,
                        new_volume.volume,
                    ) = create_default_volume_geometry(IGH, new_volume)

                hb_room_dict["Volumes"].append(new_volume)

        # #--- Clean up before we go
        del hb_room_dict["Floors"]
    return _floors_dict
