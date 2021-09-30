# -- WORK IN PROGRESS --

# PyPH
The PyPH (Python for Passive House) project is a set of Python modules which make working with Passive House software such as WUFI, PHPP and C3RRO easier. The PyPH modules allow for import and export from the various tools by way of the common 'PHX' datamodel format. The PyPH project has several parts which allow for many different types of usage. These include:

![image](https://user-images.githubusercontent.com/69652712/133112245-e57c4e72-18dc-4f61-9811-7e74380ceb5d.png)


## PHX Model Schema:
* **PHX:** The generic data model format used by all specific software import/export tools.

## Model Creators:
* **PyPH_Rhino:** Tools for use within the Rhino/Grasshopper environment which allow for Passive House data to be added to Ladybug/Honeybee models.
* **PyPH_HBJSON:** Importer which allow for the conversion of a Honeybee JSON file (*.HBJSON) into a PHX model format.

## Model Exporters:
* **PyPH_PHPP:** Tools for exporting PHX models out to the Passive House Planning Package Excel model.
* **PyPH_C3RRO:** Tools for exporting PHX models out to C3RRO JSON format.
* **PyPH_WUFI:** Tools for Exporting PHX models out to a WUFI compatible XML document.
