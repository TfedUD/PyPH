# PyPH_WUFI
PyPH_WUFI classes are used to export a PHX data model into an XML document which is compatible with WUFI-Passive. 

# PyPH_WUFI Compatability:
PyPH_WUFI XML format is compatible with WUFI-Passive v3.2.0.1

# PyPH_WUFI Behavior:
The PyPH_WUFI exporter is used to create a WUFI compatible XML document from a source PHX data model. This XML file can be opened from WUFI and should include all basic PHX objects and attributes. 

During export, PyPH_WUFI functions are used to read PHX object data, and export/format only the WUFI-relevant data in the proper structure. When a PHX object is exported, a corresponding 'XML Schema' for the PHX Object is looked up in the **PyPH_WUFI.xml_schemas** module, which is then used to format the XML structure for that PHXObject. Note that **only** fields that are listed in this module will be exported for each PHX Object. This allows for customization of the output relative to the PHX Object's attributes.

XML Node format, including attribute handling, is done using the **XML_Node** classes. Note that attribute behavior for XML nodes which use standardized formating (enums) is handled using the functions found in the **PyPH_WUFI.selection_options** module. Note that the options in these lists are the ones visible within the WUFI GUI Application, and may not represent the full list of allowable options.


# PyPH_WUFI Python Version:
All PyPH_WUFI Classes should be written to comply with **Python 3.9+** format.

# PyPH_WUFI Usage:
Primary usage is relatively straightforward once the **PHX_Project** object is built: 

```python
>>> from PyPH_WUFI.build_WUFI_xml import write_Project_to_wp_xml_file

# Supply the output path:
>>> xml_save_file_address = "C:\My_Folder\my_save_file.xml"   

# Supply the Project:
>>> PHX_Project_Object = My_Project

# Convert the PHX_Project into a WUFI XML file:
>>> write_Project_to_wp_xml_file( xml_save_file_address, PHX_Project_Object )
```

