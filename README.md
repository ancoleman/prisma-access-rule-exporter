# prisma-access-rule-exporter


[![license](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE) [![support](https://img.shields.io/badge/Support%20Level-Community-yellowgreen)](./SUPPORT.md)

## Description
Simple Export Script to output Security rules to JSON file.

### Requirements
* Python 3.9+
* OAUTH Service Account Credentials file
#### Example Credentials config.yaml
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
python3 rule-exporter.py
```

## Version History


* 0.1
    * Initial Release

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details