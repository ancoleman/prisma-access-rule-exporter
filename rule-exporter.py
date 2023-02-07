import panapi
from panapi.config import security
import time
import json

# This session requires the panapi SDK, as well as the modified
# version to perform the listing properly for security rules
session = panapi.PanApiSession()
session.authenticate()
# Add sleep for bug in dependency library with OAUTH
time.sleep(1)

# You can modify this list if you only want a specific folder
folders = ['Shared', 'Remote Networks', 'Mobile Users', 'Mobile Users Explicit Proxy']

# You can change the name of the output file here
output_file = 'rules_config.json'

# Stages Empty Dictionary for Rules
rules_config = {}
# Loops through each folder
for folder in folders:
    # Creates a nested dict for folder in rules_config
    rules_config.update({folder: {}})
    # Loop through the rulebase positioning
    for position in ['pre', 'post']:
        rules = security.SecurityRule(
            folder=folder,
            position=position
        )
        response = rules.list(session)
        # If the response was none, nothing is populated in the dict for that folder or position
        if response is not None:
            # Check if the response has items in a list or if the list is empty
            if len(response) > 0:
                # Stage an empty list to hold object payload values
                rules_list = []
                for rule in response:
                    # Check if the rule is actually contained in that specified folder, or in shared.
                    if rule.folder == folder:
                        # Cleanup from the output, _headers attribute is of no value for parsing
                        delattr(rule, '_headers')
                        # Add rule to the rules list
                        rules_list.append(rule.payload)
                # Add all rules for folder and position to the dictionary
                rules_config[folder].update({position: rules_list})

###############################
# Generates a JSON file output.
###############################
with open(output_file, 'w') as f:
    # Convert dictionary to JSON
    json.dump(rules_config, f, indent=4)
