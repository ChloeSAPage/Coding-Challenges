import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml

def extract_user_info(root):
    user_info = []

    for user in root.findall("user"):
        forename = user.find("forename")
        surname = user.find("surname")
        email = user.find("email")

        user_dic = {
            "firstname": forename.text.strip() if forename is not None else "",
            "lastname": surname.text.strip() if surname is not None else "",
            "email": email.text.strip() if email is not None else ""
        }

        user_info.append(user_dic)

    return user_info

def extract_mailing_info(root_mailing):
    mailing_info = []

    for subscriber in root_mailing:
        dic = subscriber.attrib

        dictionary_new = {
            'firstname': dic.get('givenname', '').strip(),
            'lastname': dic.get('familyname', '').strip(),
            'email': dic['email'].strip()
        }

        mailing_info.append(dictionary_new)

    return mailing_info

def combine_dictionaries(user_info, mailing_info_new):
    final = user_info.copy()

    for mailing_dict in mailing_info_new:
        for final_dict in final:
            if final_dict["email"] == mailing_dict["email"]:
                if final_dict["lastname"] == "" and mailing_dict["lastname"]:
                    final_dict["lastname"] = mailing_dict["lastname"]
                if final_dict["firstname"] == "" and mailing_dict["firstname"]:
                    final_dict["firstname"] = mailing_dict["firstname"]
                break
        else:  # If no matching email is found
            final.append(mailing_dict)

    return final

def generate_xml(final):
    my_item_func = lambda x: "entry"
    xml = dicttoxml(final, custom_root="list", attr_type=False, item_func=my_item_func,
                    xml_declaration=True, include_encoding=True)
    dom = parseString(xml)
    return dom.toprettyxml()

def save_to_file(xml_data, file_path):
    with open(file_path, "w") as file:
        file.write(xml_data)

# Usage
user_list_path = R"files\user-list.xml"
mailing_list_path = R"files\mailing-list.xml"

tree = ET.parse(user_list_path)
root = tree.getroot()

user_info = extract_user_info(root)

tree_mailing = ET.parse(mailing_list_path)
root_mailing = tree_mailing.getroot()

mailing_info_new = extract_mailing_info(root_mailing)

final = combine_dictionaries(user_info, mailing_info_new)

xml_data = generate_xml(final)

file_path = "target.xml"
save_to_file(xml_data, file_path)

with open(file_path, "r") as file:
    data = file.readlines()

data[0] = '<?xml version="1.0" encoding="UTF-8"?>' + "\n" + '<!DOCTYPE users SYSTEM "target.dtd">' + "\n"

with open(file_path, "w") as file:
    file.writelines(data)