# -*- coding: utf-8 -*-
"""Functions to create PHX Materiala, Assembly-Layers, and Construction Assemblies from HB-JSON"""

import honeybee.face
import honeybee_energy.material.opaque
import PHX.component
import PHX.assemblies
import PHX.window_types

#--- Assemblies
#-------------------------------------------------------------------------------
def create_new_NoMassMaterial_from_hb_mat( _hb_material: honeybee_energy.material.opaque.EnergyMaterialNoMass, _thickness: float=0.1) -> PHX.assemblies.Material:
    """

    Arguments:
    ----------
        * _hb_material (honeybee_energy.material.opaque.EnergyMaterialNoMass): The source Honeybee NoMass Material

    Returns:
    --------
        * (tuple[Material, Thickness]): A Tuple with [0]=WUFI Material, [1]=Thickness (meters)
    """
    
    new_material = PHX.assemblies.Material()
    new_material.n = _hb_material.display_name

    new_material.r_value = _hb_material.r_value
    new_material.tConD = (1/new_material.r_value)*_thickness

    return new_material, _thickness

def create_new_StandardMaterial_from_hb_mat( _hb_material: honeybee_energy.material.opaque.EnergyMaterial, _thickness: float) -> PHX.assemblies.Material:
    """

    Arguments:
    ----------
        * _hb_material (honeybee_energy.material.opaque.EnergyMaterial): The source Honeybee Standard Material

    Returns:
    --------
        * (tuple[Material, Thickness]): A Tuple with [0]=WUFI Material, [1]=Thickness (meters)
    """
    
    new_material = PHX.assemblies.Material()
    
    new_material.n = _hb_material.display_name
    new_material.tConD = _hb_material.conductivity
    new_material.densB = _hb_material.density
    new_material.hCapS = _hb_material.specific_heat

    return new_material, _thickness

def create_new_material_from_hb_mat( _hb_material ) -> PHX.assemblies.Material:
    """Creates a new PHX.assemblies.Material based on the parameters of a Honeybee Material

    Arguments:
    ----------
        * _hb_material (honeybee_energy.material.opaque.EnergyMaterial): The Honeybee 
            EnergyMaterial to use as the source

    Returns:
    --------
        * (tuple[PHX.assemblies.Material, Thickness]): Tuple
            [0]=PHX.assemblies.Material
            [1]=Thickness (meters)
    """
    
    if hasattr( _hb_material, 'thickness'):
        return create_new_StandardMaterial_from_hb_mat( _hb_material, _hb_material.thickness )
    elif not hasattr( _hb_material, 'thickness'):
        # NoMass Materials don't have a conductivity or thickness, only and R-Value
        # So for WP, use a default thickness of 0.100m for all NoMass Materials
        return create_new_NoMassMaterial_from_hb_mat( _hb_material , 0.100)
    else:
        raise Exception(f'Error: Cannot determine type of Honeybee Material: "{_hb_material}", type: "{type(_hb_material)}"')
        
def create_new_assembly_from_hb_face( _face: honeybee.face.Face ) -> PHX.assemblies.Assembly:
    """Create a new Construction Assembly based on a source Honeybee Face. Will use 
        the parameters found on the Honeybee Face's .properties.energy.construction and 
        .properties.energy.construction.materials in order to create the new Assembly and 
        any Materials for the Assembly Layers.

    Arguments:
    ----------
        * _face (honeybee.face.Face): The Honeyebee Face to use as the source
    
    Returns:
    --------
        * (PHX.assemblies.Assembly): A new Construction Assembly based on the Construction found on 
            the input Honeybee Face
    """
    
    assembly = PHX.assemblies.Assembly()
    assembly.n = _face.properties.energy.construction.display_name
    assembly.identifier = _face.properties.energy.construction.identifier

    #--- Build A Material dict { 'mat_name_1':idex_num, 'mat_name_2':index_num,... }
    materials = {}
    for i, material in enumerate( _face.properties.energy.construction.materials):
        materials[ material.display_name ] = i

    #--- Build the Layers of the Assembly
    for layer_name in _face.properties.energy.construction.layers:
        new_layer = PHX.assemblies.Layer()

        hb_material = _face.properties.energy.construction.materials[ materials[layer_name] ]
        new_layer.material, new_layer.thickness = create_new_material_from_hb_mat( hb_material )

        assembly.add_layer( new_layer )

    return assembly


#--- Windows
#-------------------------------------------------------------------------------
def create_new_window_type_from_hb_face( _face: honeybee.face.Face ) -> PHX.window_types.WindowType:
    """Create a new WindowType based on a source Honeybee Aperture. Will use 
        the parameters found on the Honeybee Aperture's .properties.energy.construction 
        in order to create the new WindowType

    Arguments:
    ----------
        * _face (honeybee.face.Face): The Honeyebee Face to use as the source
    
    Returns:
    --------
        * (WindowType): A new WindowType Object based on the Construction found on 
            the input Honeybee Aperture
    """
    
    new_window_type = PHX.window_types.WindowType()
    
    new_window_type.n = _face.properties.energy.construction.display_name
    new_window_type.identifier = _face.properties.energy.construction.identifier
    
    new_window_type.Uw = _face.properties.energy.construction.u_factor
    new_window_type.glazU = _face.properties.energy.construction.u_factor
    new_window_type.Ufr = _face.properties.energy.construction.u_factor
    new_window_type.gtr = _face.properties.energy.construction.solar_transmittance

    new_frame = PHX.window_types.WindowFrame()
    new_window_type.add_new_frame_element( new_frame, 'L' )

    return new_window_type

def set_compo_window_type_from_hb_aperture( _window_compo: PHX.component.Component, _hb_face: honeybee.face.Face, _window_type_collection):
    """Sets a Window Component's 'IdentNrAssembly' based on the Assembly of a Honeybee Aperture

    Arguments:
    ----------
        * _window_compo (PHX.component.Component): The Window Component to set the IdentNrAssembly of
        * _hb_face (honeybee.face.Face): The Honeybee Face. Will use the Face's Assembly Name as the key
        * _window_type_collection (WindowTypeCollection): The Project's 
            WindowTypeCollection with all the WindowType Information
    
    Returns:
    --------
        * (Component): The Component with the 'IdentNrAssembly' set based on the Honeybee Face's Assembly
    """

    hb_construction_identifier = _hb_face.properties.energy.construction.identifier
    window_type = _window_type_collection.get_window_type_by_identifier(hb_construction_identifier)

    _window_compo.idWtC = window_type.id

    return _window_compo