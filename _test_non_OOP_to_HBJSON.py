from PyPH_HBJSON.read_HBJSON_file import read_hb_json
from _test_non_OOP_to_xml import write_to_wp_xml_file, XML_Node, XML_Object, XML_List

import honeybee_energy.construction.window


# --- Note: Path format in MAC OS (forward slash)
SOURCE_FILE = "sample/EM_sample_input_HBJSON/Sample_Input.hbjson"
TARGET_FILE_XML = "sample/EM_sample_output_WUFI_XML/Sample_Output.xml"


# ------------------------------------------------------------------------------
# --- Read in an existing HB_JSON and re-build the HB Objects
print("- " * 50)
print("> Reading in the HBJSON file...")
hb_model = read_hb_json(SOURCE_FILE)

# ------------------------------------------------------------------------------
# --- Build the Material Catalog
material_dict = {material.display_name: material for material in hb_model.properties.energy.materials}

# ------------------------------------------------------------------------------
# --- Build all the Assemblies
wp_assemblies_list = XML_List("Assemblies")
for hb_construction in hb_model.properties.energy.constructions:
    if isinstance(hb_construction, honeybee_energy.construction.window.WindowConstruction):
        continue

    wp_assembly = XML_Object("Assembly")
    wp_assemblies_list.add_XML_Object(wp_assembly)

    wp_assembly.add_child_node(XML_Node("IdentNr", wp_assembly.node_attr_value))
    wp_assembly.add_child_node(XML_Node("Name", hb_construction.display_name))
    wp_assembly.add_child_node(XML_Node("Order_Layers", 2, "choice", "from outside to inside"))
    wp_assembly.add_child_node(XML_Node("Grid_Kind", 2, "choice", "Medium"))

    # -- Build up the Assembly's Material Layers
    wp_Layer_list = XML_List("Layers")
    wp_assembly.add_child_node(wp_Layer_list)
    for i, layer_material_name in enumerate(hb_construction.layers):
        hb_material = material_dict.get(layer_material_name)
        wp_Layer = XML_Object("Layer")
        wp_Layer_list.add_XML_Object(wp_Layer)

        if hasattr(hb_material, "thickness"):
            wp_Layer.child_nodes.append(XML_Node("Thickness", hb_material.thickness))

        # -- Build the Layer's Material
        wp_Material = XML_Object("Material")
        wp_Layer.add_child_node(wp_Material)

        wp_Material.add_child_node(XML_Node("Name", hb_material.display_name))
        if hasattr(hb_material, "conductivity"):
            wp_Material.add_child_node(XML_Node("ThermalConductivity", hb_material.conductivity))
        elif hasattr(hb_material, "resistivity"):
            wp_Material.add_child_node(XML_Node("ThermalConductivity", (1 / hb_material.resistivity)))


write_to_wp_xml_file(TARGET_FILE_XML, wp_assemblies_list)
