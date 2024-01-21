import pandas as pd
import xml.etree.ElementTree as ET


def print_hierarchy(element, level=0):
    """
    Recursively print the hierarchy of an XML element.

    :param element: An XML element to print the hierarchy for.
    :param level: The current depth level in the XML document.
    """
    print('  ' * level + element.tag)
    for child in element:
        print_hierarchy(child, level + 1)


def parse_xml_to_df(xml_file, record_tag):
    """
    Parse an XML file and convert it into a pandas DataFrame.

    :param xml_file: Path to the XML file.
    :param record_tag: The tag of the XML elements that you want to convert into DataFrame rows.
    :return: A pandas DataFrame.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    all_records = []
    for item in root.findall(f".//{record_tag}"):  # Adjust the path as necessary
        record = {}
        for child in item:
            record[child.tag] = child.text
        all_records.append(record)

    return pd.DataFrame(all_records)


if __name__ == '__main__':
    # Usage example
    xml_file_path = r'.\Data\pension-2013.xml'  # Replace with the path to your XML file
    record_tag = 'DESCRIPTION'  # Replace with the tag of your main records

    df = parse_xml_to_df(xml_file_path, record_tag)
    print(df.head())
