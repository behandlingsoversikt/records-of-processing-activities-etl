import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()


def transform_records(r_file):
    records = openfile(r_file)
    transformed_records = {}
    print("Total number of extracted records: " + str(len(records)))
    for record_id in records:
        transformed_records[record_id] = transform_record(records[record_id])
    return transformed_records


def transform_organizations(o_file):
    organizations = openfile(o_file)
    transformed_representatives = {}
    print("Total number of extracted organizations: " + str(len(organizations)))
    for org_id in organizations:
        transformed_representatives[org_id] = transform_representatives(organizations[org_id])
    return transformed_representatives


def openfile(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)


def transform_record(old_dict):
    new_dict = {}
    no_id_dict = omit_id(old_dict)
    for key in no_id_dict:
        if key == "recordId":
            new_dict["_id"] = no_id_dict[key]
        else:
            new_dict[key] = no_id_dict[key]
    return new_dict


def transform_representatives(old_dict):
    new_dict = {}
    no_id_dict = omit_id(old_dict)
    for key in no_id_dict:
        if key == "organizationId":
            new_dict["_id"] = no_id_dict[key]
        else:
            new_dict[key] = no_id_dict[key]
    return new_dict


def omit_id(old_dict):
    new_dict = {}
    for key in old_dict:
        if not (key == '_id' or key == 'id'):
            new_dict[key] = old_dict[key]
    return new_dict


records_file = args.outputdirectory + "mongo_records.json"
organizations_file = args.outputdirectory + "mongo_organizations.json"
output_records = args.outputdirectory + "transformed_records.json"
output_representatives = args.outputdirectory + "transformed_representatives.json"

with open(output_records, 'w', encoding="utf-8") as outfile:
    json.dump(transform_records(records_file), outfile, ensure_ascii=False, indent=4)

with open(output_representatives, 'w', encoding="utf-8") as outfile:
    json.dump(transform_organizations(organizations_file), outfile, ensure_ascii=False, indent=4)
