# prisma-access-rule-exporter


[![license](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE) [![support](https://img.shields.io/badge/Support%20Level-Community-yellowgreen)](./SUPPORT.md)

## Description
Simple Export Script to output rules to JSON file output.
Additionally, the script will export all folder rulebases into CSV.

### Requirements
* Python 3.9+
* OAUTH Service Account Credentials file

### Supported Rule Types
* Security
* Authentication
* Decryption

#### Example Credentials config.yaml
Create the config.yaml file in the root directory.
```yaml
---
scope: profile tsg_id:YOURTENANTID email
client_id: SA@YOURID.iam.panserviceaccount.com
client_secret: YOURSECRET
grant_type: client_credentials
token_url: https://auth.apps.paloaltonetworks.com/am/oauth2/access_token
```

### Example Usage
Currently, no CLI has been added to this project, so all parameters need to be added to the script.
#### Paramters
* folders = ['Shared', 'Remote Networks', 'Mobile Users', 'Mobile Users Explicit Proxy']
* position = ['pre','post']
* output_file = 'rules_config.json'

```
git clone https://github.com/ancoleman/prisma-access-rule-exporter
cd prisma-access-rule-exporter
```

```python
#Example from example.py
import rule_exporter

folders = ['Shared', 'Remote Networks', 'Mobile Users', 'Mobile Users Explicit Proxy']

session = rule_exporter.create_session()
security_rules = rule_exporter.get_rules(session, folders)
rule_exporter.cleanup_duplicates_rules(folders, security_rules)
rule_exporter.generate_json_file('security_rules.json', security_rules)
rule_exporter.generate_csv_rules(folders, security_rules, type='security', suffix='rules')
```


## Version History


* 0.1
    * Initial Release

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details