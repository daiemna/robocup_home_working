from ruamel.yaml import YAML
import json

def load_yaml(path):
    with open(path, 'r') as yfile:
        yml = YAML()
        return yml.load(yfile)


def fjson(json_dict):
        return json.dumps(json_dict, indent=3)