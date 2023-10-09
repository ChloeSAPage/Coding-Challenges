import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml

user_list = R"XML\files\user-list.xml"
mailing_list = R"XML\files\mailing-list.xml"

tree = ET.parse(user_list)
root = tree.getroot()

# User List
user_info = []

for user in root.findall("user"):
    forename = user.find("forename")
    surname = user.find("surname")
    email = user.find("email")
    user_dic = {}
    # Forename
    if forename is not None:
        forename = forename.text
        forename = forename.strip()
        user_dic["firstname"] = forename
    else:
        user_dic["firstname"] = ""
        
    # Surname
    if surname is not None:
        surname = surname.text
        surname = surname.strip()
        user_dic["lastname"] = surname
    else:
        user_dic["lastname"] = ""
    
    # Email  
    if email is not None:
        email = email.text
        email = email.strip()
        user_dic["email"] = email

    user_info.append(user_dic)

# Mailing List

tree_mailing = ET.parse(mailing_list)
root_mailing = tree_mailing.getroot()

mailing_info = []
for subscriber in root_mailing:
    dic = subscriber.attrib
    mailing_info.append(dic)

mailing_info_new = []
for dictionary in mailing_info:
    dictionary_new = {}
    # Given Name
    try:
        dictionary_new['firstname'] = dictionary['givenname'].strip()
    except KeyError:
        dictionary_new['firstname'] = ""
    
    # Family Name
    try:
        dictionary_new['lastname'] = dictionary['familyname'].strip()
    except KeyError:
        dictionary_new['lastname'] = ""
    
    # Email
    dictionary_new['email'] = dictionary['email'].strip()
    mailing_info_new.append(dictionary_new)

# Combining the dictionaries

final = user_info

for mailing_dict in mailing_info_new:
    duplicate = False
    
    for index, final_dict in enumerate(final):
        if final_dict["email"] == mailing_dict["email"]:
            duplicate = True
            if final_dict["lastname"] == "" and mailing_dict["lastname"] != "":
                final[index]["lastname"] = mailing_dict["lastname"]
            if final_dict["firstname"] == "" and mailing_dict["firstname"] != "":
                final[index]["firstname"] = mailing_dict["firstname"]
                
    if duplicate == False:
        final.append(mailing_dict)

print(f"THIS IS FINAL {final}")


# Making the XML File

my_item_func = lambda x: "entry"
xml = dicttoxml(final, custom_root="list", attr_type=False, item_func=my_item_func,
                xml_declaration=True, include_encoding=True)
dom = parseString(xml)
xml = dom.toprettyxml()


# Write to XML File

with open("target.xml", "w") as file:
    file.writelines(xml)
    
with open("target.xml", "r") as file:
    data = file.readlines()
    
data[0] = '<?xml version="1.0" encoding="UTF-8"?>' + "\n" + '<!DOCTYPE users SYSTEM "target.dtd">' + "\n"

with open("target.xml", "w") as file:
    file.writelines(data)