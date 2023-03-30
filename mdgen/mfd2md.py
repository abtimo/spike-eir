import pandas as pd
import xml.etree.ElementTree as ET
import xmlschema


def map_schemas(schema1_file, schema2_file, mapping_file):
    """Create a mapping file (.mfd) between two XSD schemas"""

    # Load the schemas
    schema1 = ET.parse(schema1_file).getroot()
    schema2 = ET.parse(schema2_file).getroot()

    # Create the mapping file
    mapping = ET.Element("Mapping")

    # Iterate over all elements in the first schema
    for el1 in schema1.iter():
        # Find all matching elements in the second schema
        xpath = el1.getroottree().getpath(el1)
        el2 = schema2.find(xpath)

        # If a matching element is found...
        if el2 is not None:
            # Create a MappingField element and set its attributes
            field = ET.SubElement(mapping, "MappingField")
            field.set("SourceSchema", schema1_file)
            field.set("TargetSchema", schema2_file)
            field.set("SourceField", el1.tag)
            field.set("TargetField", el2.tag)

    # Save the mapping to file
    ET.SubElement(mapping, "Comments", {"Value": "Mapping created by script"})
    tree = ET.ElementTree(mapping)
    tree.write(mapping_file)

    print(f"Mapping file created at {mapping_file}")


def mapping_to_md(mapping_file, md_file):
    """Convert a mapping .mfd file to a Markdown table"""

    # Open the mapping file (.mfd)
    tree = ET.parse(mapping_file)
    root = tree.getroot()

    # Create headers for Markdown table
    headers = ["Source field", "Target field", "Transformation"]

    # Create empty dataframe
    df = pd.DataFrame(columns=headers)

    # Iterate over elements inside <MappingField> tag
    for field in root.iter("MappingField"):
        row = {}
        row["Source field"] = field.find("SourceField").text
        row["Target field"] = field.find("TargetField").text
        row["Transformation"] = field.find("Transformation").text

        df = df.append(row, ignore_index=True)

    # Convert dataframe to Markdown table
    md_table = df.to_markdown(index=False)

    # Save Markdown table to file
    with open(md_file, "w") as f:
        f.write(md_table)

    print(f"Markdown table created at {md_file}")


def validate_xml(schema_file, xml_file):
    """Validate an XML file against a given XSD schema"""

    # Load the XSD schema
    xs = xmlschema.XMLSchema(schema_file)

    # Load the XML file
    try:
        xml = ET.parse(xml_file)
    except ET.ParseError as e:
        print(f"Invalid XML: {e}")
        return

    # Check if the XML is valid according to the schema
    try:
        xs.validate(xml)
        print("XML is valid")
    except xmlschema.exceptions.XMLSchemaValidationError as e:
        print(f"Invalid XML: {e}")


# Example usage
#map_schemas("path/to/schema1.xsd", "path/to/schema2.xsd", "path/to/mapping.mfd")
#mapping_to_md("path/to/mapping.mfd", "path/to/mapping_table.md")
#validate_xml("path/to/schema.xsd", "path/to/data.xml")

#from command line
#$ python mfd2md.py
#Markdown table created at ./MarketingExpenses2ExpReport.md
#$

mapping_to_md("./MarketingExpenses2ExpReport.mfd", "./MarketingExpenses2ExpReport.md")
