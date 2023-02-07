import rule_exporter

folders = ['Shared', 'Remote Networks', 'Mobile Users', 'Mobile Users Explicit Proxy']
################
# Security Rules
################
security_rules = rule_exporter.get_rules(folders)
rule_exporter.cleanup_duplicates_rules(folders, security_rules)
rule_exporter.generate_json_file('security_rules.json', security_rules)
rule_exporter.generate_csv_rules(folders, security_rules, type='security')

##################
# Decryption Rules
##################
decryption_rules = rule_exporter.get_rules(folders, rule_type='decrypt')
rule_exporter.cleanup_duplicates_rules(folders, decryption_rules)
rule_exporter.generate_json_file('decryption_rules.json', decryption_rules)
rule_exporter.generate_csv_rules(folders, decryption_rules, type='decrypt')

