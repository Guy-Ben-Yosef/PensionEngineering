import pandas as pd
import os
import xml.etree.ElementTree as ET
import io
import warnings

if __name__ == '__main__':
    FIRST_YEAR = 1999
    LAST_YEAR = 2023
    id_to_name_mapper = {}

    df = pd.DataFrame(columns=['id', 'period', 'yield'])

    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        data_path = r".\Data\{}.xml".format(year)
        with open(data_path, 'r', encoding="utf8") as f:
            data_as_string = io.StringIO(f.read())

        tree = ET.parse(data_as_string)
        root = tree.getroot()

        valid_tags = ["ID_KRN", "TKF_DIVUACH", "TSUA_NOMINALI_BFOAL"]
        data = []
        for row in root.findall('ROW'):
            data_dict = {}
            for child in row:
                if (child.tag in valid_tags) and (not child.text):
                    continue
                if child.tag == "ID_KRN":
                    data_dict["id"] = child.text
                elif child.tag == "SHM_KRN":
                    name = child.text
                elif child.tag == "TKF_DIVUACH":
                    data_dict["period"] = child.text
                elif child.tag == "TSUA_NOMINALI_BFOAL":
                    data_dict["yield"] = float(child.text)

            if data_dict["id"] in id_to_name_mapper.keys():
                if id_to_name_mapper[data_dict["id"]] != name:
                    warn_str = f"""\nSame ID has different names
                    \nID\t\t{data_dict['id']}
                    \nName1\t{id_to_name_mapper[data_dict['id']]}
                    \nName2\t{name}\n"""
                    warnings.warn(warn_str)
            else:
                id_to_name_mapper[data_dict["id"]] = name
            data.append(data_dict)

        df = pd.concat([df, pd.DataFrame(data)])

    df.to_csv(r".\Data\YieldData.csv", index=False)
