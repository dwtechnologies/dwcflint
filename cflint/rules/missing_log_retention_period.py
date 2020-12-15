from cfnlint.rules import CloudFormationLintRule, RuleMatch


class MissingLogGroupRetentionPeriod(CloudFormationLintRule):
    """Warns if log groups are missing retention periods"""
    id = 'W1346'
    shortdesc = 'Warns if log groups are missing retention periods'
    description = 'Warns if log groups are missing retention periods, as this will default to logs being stored ' \
                  'indefinitely'
    source_url = 'https://bitbucket.com/keycomponent/cfn-python-lint-dw'
    tags = ['logs', 'log groups', 'retention', 'cloudwatch']

    def match(self, cfn):
        matches = []

        resources = cfn.get_resources([])
        for resourceName, resource in resources.items():
            if resource['Type'] == 'AWS::Logs::LogGroup' and 'RetentionInDays' not in resource['Properties']:
                matches.append(RuleMatch(['Resources', resourceName], 'Found log group missing log retention period'))

        return matches
