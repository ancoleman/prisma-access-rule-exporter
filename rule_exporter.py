import panapi
from panapi.config import security, identity
import time
import json
import csv


def create_session():
    """

    Returns: Session Object

    """
    try:
        session = panapi.PanApiSession()
        session.authenticate()
        time.sleep(1)
        return session
    except Exception as e:
        return f'Failed with exception: {e}'


def get_rules(session, folders, rule_type='security'):
    """

    Args:
        session: Session object from create_session() function
        folders: List of Prisma Access folders to cycle through
        rule_type: security, decrypt, auth

    Returns:

    """
    # Stages Empty Dictionary for Rules
    rules_config = {}
    # Loops through each folder
    for folder in folders:
        # Creates a nested dict for folder in rules_config
        rules_config.update({folder: {}})
        # Loop through the rulebase positioning
        for position in ['pre', 'post']:
            if rule_type == 'security':
                rules = security.SecurityRule(
                    folder=folder,
                    position=position
                )
            if rule_type == 'auth':
                rules = identity.AuthenticationRule(
                    folder=folder,
                    position=position
                )
            if rule_type == 'decrypt':
                rules = security.DecryptionRule(
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
    return rules_config


############################################################
# Checks for matching rule IDs between positional rulebases
############################################################
def cleanup_duplicate_rules(folders, rules):
    """
        Args:
            folders: List of Prisma Access folders to cycle through
            rules: Dictionary of rules generated from the get_rules() function
    """
    for folder in folders:
        for position in ['pre', 'post']:
            if position in rules[folder]:
                if len(rules[folder][position]) > 0:
                    if position == 'pre':
                        for rule in rules[folder][position]:
                            if 'post' in rules[folder]:
                                for post_rule in rules[folder]['post']:
                                    if rule['id'] == post_rule['id']:
                                        rules[folder]['post'].remove(post_rule)
                    if position == 'post':
                        for rule in rules[folder][position]:
                            if 'pre' in rules[folder]:
                                for pre_rule in rules[folder]['post']:
                                    if rule['id'] == pre_rule['id']:
                                        rules[folder]['pre'].remove(pre_rule)


###############################
# Generates a JSON file output.
###############################
def generate_json_file(filename, rules):
    """
        Args:
            filename: the actual filename to generate for json
            rules: Dictionary of rules generated from the get_rules() function
    """
    with open(filename, 'w') as f:
        # Convert dictionary to JSON
        json.dump(rules, f, indent=4)


def generate_csv_rules(folders, rules_dict, type, suffix):
    """

    Args:
        suffix: Append string suffix to csv file
        folders: List of Prisma Access folders to cycle through
        rules_dict: Dictionary of rules generated from the get_rules() function
        type: Str value for the rule type to modify csv filename

    Returns:

    """
    for folder in folders:
        for position in ['pre', 'post']:
            if position in rules_dict[folder]:
                if len(rules_dict[folder][position]) > 0:
                    folder_data = rules_dict[folder][position]
                    new_csv = open(f'{folder.lower()}_{type.lower()}_{position}_{suffix}.csv', 'w')
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
