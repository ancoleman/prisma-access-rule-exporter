import rule_exporter

folders = ['Shared', 'Remote Networks', 'Mobile Users', 'Mobile Users Explicit Proxy']

#########
# Session
#########
session = rule_exporter.create_session()

################
# Security Rules
################
security_rules = rule_exporter.get_rules(session, folders)
rule_exporter.cleanup_duplicate_rules(folders, security_rules)
rule_exporter.generate_json_file('security_rules.json', security_rules)
rule_exporter.generate_csv_rules(folders, security_rules, type='security', suffix='rules')

##################
# Decryption Rules
##################
decryption_rules = rule_exporter.get_rules(session, folders, rule_type='decrypt')
rule_exporter.cleanup_duplicate_rules(folders, decryption_rules)
rule_exporter.generate_json_file('decryption_rules.json', decryption_rules)
rule_exporter.generate_csv_rules(folders, decryption_rules, type='decrypt', suffix='rules')

######################
# Authentication Rules
######################
auth_rules = rule_exporter.get_rules(session, folders, rule_type='auth')
rule_exporter.cleanup_duplicate_rules(folders, auth_rules)
rule_exporter.generate_json_file('auth_rules.json', auth_rules)
rule_exporter.generate_csv_rules(folders, auth_rules, type='auth', suffix='rules')

