import os
import pandas as pd


class AttributeDatabase:
    def __init__(self):
        attribute_path = os.path.join(os.getcwd(), "data", "attributes.csv")
        attribute_df = pd.read_csv(attribute_path)
        self.attribute_dict = dict()
        self.attribute_list = list()
        for _, row in attribute_df.iterrows():
            entity_name = row["name"]
            dict_for_name = dict()
            for attribute in row.to_dict().keys():
                if attribute != "name":
                    self.attribute_list.append(attribute)
                    if row[attribute] == "x":
                        dict_for_name[attribute] = True
                    else:
                        dict_for_name[attribute] = False
            self.attribute_dict[entity_name] = dict_for_name

    def get_all_attributes(self) -> list[str]:
        return self.attribute_list

    def has_attribute(self, entity_name: str, attribute: str) -> bool:
        return self.attribute_dict[entity_name][attribute]
