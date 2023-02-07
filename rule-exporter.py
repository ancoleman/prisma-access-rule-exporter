import panapi
from panapi.config import security
import time
import json
import csv

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
csv_suffix = 'rules'

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

############################################################
# Checks for matching rule IDs between positional rulebases
############################################################
for folder in folders:
    for position in ['pre', 'post']:
        if position in rules_config[folder]:
            if len(rules_config[folder][position]) > 0:
                if position == 'pre':
                    for rule in rules_config[folder][position]:
                        if 'post' in rules_config[folder]:
                            for post_rule in rules_config[folder]['post']:
                                if rule['id'] == post_rule['id']:
                                    rules_config[folder]['post'].remove(post_rule)
                if position == 'post':
                    for rule in rules_config[folder][position]:
                        if 'pre' in rules_config[folder]:
                            for pre_rule in rules_config[folder]['post']:
                                if rule['id'] == pre_rule['id']:
                                    rules_config[folder]['pre'].remove(pre_rule)

###############################
# Generates a JSON file output.
###############################
with open(output_file, 'w') as f:
    # Convert dictionary to JSON
    json.dump(rules_config, f, indent=4)

for folder in folders:
    for position in ['pre', 'post']:
        if position in rules_config[folder]:
            if len(rules_config[folder][position]) > 0:
                folder_data = rules_config[folder][position]
                new_csv = open(f'{folder}_{position}_{csv_suffix}.csv', 'w')
                csv_writer = csv.writer(new_csv)
                count = 0

                for item in folder_data:
                    if count == 0:
                        # Writing headers of CSV file
                        header = item.keys()
                        csv_writer.writerow(header)
                        count += 1

                    # Writing data of CSV file
                    csv_writer.writerow(item.values())
                new_csv.close()
