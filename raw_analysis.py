import pandas as pd
import os
import xml.etree.ElementTree as ET
import io
import warnings


def read_xml_file(file_path):
    """
    Read an XML file and return an ElementTree object.
    :param file_path:
    :return: ElementTree object
    """
    with open(file_path, 'r', encoding="utf8") as f:
        data_as_string = io.StringIO(f.read())
    return ET.parse(data_as_string)


def parse_xml_data(tree, id_to_name_mapper):
    """
    Parse the XML data and return a list of dictionaries.
    :param tree: An ElementTree object to parse.
    :param id_to_name_mapper: Dictionary tracking the ID to name mapping.
    :return: List of dictionaries to be converted into a DataFrame.
    """
    root = tree.getroot()
    valid_tags = ["ID_KRN", "TKF_DIVUACH", "TSUA_NOMINALI_BFOAL"]  # The tags we want to parse
    data = []
    for row in root.findall('ROW'):  # Iterate over all the rows in the XML file
        data_dict = {}
        name = None
        for child in row:
            if (child.tag in valid_tags) and (not child.text):  # If the tag is valid but the text is empty
                continue
            if child.tag == "ID_KRN":
                data_dict["id"] = child.text
            elif child.tag == "SHM_KRN":
                name = child.text
            elif child.tag == "TKF_DIVUACH":
                data_dict["period"] = child.text
            elif child.tag == "TSUA_NOMINALI_BFOAL":
                data_dict["yield"] = float(child.text)

        # Look for ID with different names
        check_id_name_mismatch(data_dict["id"], name, id_to_name_mapper)
        data.append(data_dict)
    return data


def check_id_name_mismatch(id, name, mapper):
    """
    Check if the same ID has different names.
    :param id: String ID
    :param name: Hebrew name matching the ID
    :param mapper: Dictionary tracking the ID to name mapping.
    """
    if id in mapper.keys():  # If the ID is already in the mapper
        if mapper[id] != name:  # If the name is different than the one in the mapper
            warn_str = f"""\nSame ID has different names
            \nID\t\t{id}
            \nName1\t{mapper[id]}
            \nName2\t{name}\n"""
            warnings.warn(warn_str)
    else:
        mapper[id] = name  # Add the ID to the mapper


if __name__ == '__main__':
    FIRST_YEAR = 1999
    LAST_YEAR = 2023
    id_to_name_mapper = {}

    df = pd.DataFrame(columns=['id', 'period', 'yield'])  # Initialize an empty DataFrame

    # Iterate over all the XML files
    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        data_path = os.path.join(".", "Data", f"{year}.xml")
        tree = read_xml_file(data_path)
        data = parse_xml_data(tree, id_to_name_mapper)

        # Concatenate the data to the DataFrame
        df = pd.concat([df, pd.DataFrame(data)])

    # Save the DataFrame to a CSV file
    df.to_csv(os.path.join(".", "Data", "YieldData.csv"), index=False)

    print("#" * 70 + "\n" + "#" + " " * 68 + "#")
    print("#    " + "Finished parsing XML files. Data saved to Data\YieldData.csv" + "    #")
    print("#" + " " * 68 + "#" + "\n" + "#" * 70)

    # Print the mapper
    print("\nID to Name Mapper")
    for key, value in id_to_name_mapper.items():
        print(f"{key.rjust(5)}\t\t{value}")
