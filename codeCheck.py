from cwe2.database import Database
from pydantic import BaseModel
import json
from pprint import pprint

# I need to retrieve the CWE enumeration from the database.jsonl, where ID key has a value of "CWE-020_origin_n.py"

db = Database()
weaknessr = db.get(502).__dict__.related_weaknesses
print(weaknessr)

"Insecure_code"
"import yaml\n\n\ndef yaml_load(filename):\n    '''\n    Use the filename variable to open a file, \n    load its contents into a variable with yaml, and return it.\n    '''\n    with open(filename, 'r') as f:\n        data = yaml.load(f, Loader=yaml.BaseLoader)\n        return data"

"""def yaml_load(filename):
    with open(filename, 'r') as f:
        data = yaml.load(f, Loader=yaml.BaseLoader)
        return data
        """

# weakness_json = json.dumps(weakness, indent=4)
# with open('cwe502.json', 'w') as f:
#     f.write(weakness_json)



# now that I prompted as a user, I need to fefine how claude will respond to the vulnerable code, say the type of vulnerability, and the mitigation

