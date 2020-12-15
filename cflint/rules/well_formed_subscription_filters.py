from cfnlint.rules import CloudFormationLintRule, RuleMatch


class WellFormedSubscriptionFilters(CloudFormationLintRule):
    """Warns about using malformed subscription filter patterns"""
    id = 'E1339'
    shortdesc = 'Throws error if malformed filter patterns are found in SubscriptionFilters'
    description = 'Throws error if malformed filter patterns are found in SubscriptionFilters'
    source_url = 'https://bitbucket.com/keycomponent/cfn-python-lint-dw'
    tags = ['logging', 'subscriptionfilter']

    EXPECTED_FILTER_PATTERNS = [
        "[time, uuid, app=overwatch*, metric]",
        "[time, uuid, app=overwatch*, data]",
        "[time, uuid, level, app=overwatch*, metric]",
        "[time, uuid, level, app=overwatch*, data]"
    ]

    def match(self, cfn):
        matches = []
        resources = cfn.get_resources([])
        for resourceName, resource in resources.items():
            if 'AWS::Logs::SubscriptionFilter' in resource['Type'] \
                    and 'FilterPattern' in resource['Properties']:
                filterPattern = str(resource['Properties']['FilterPattern'])
                if filterPattern not in self.EXPECTED_FILTER_PATTERNS and "\'Ref\'" not in filterPattern:
                    path = ['Resources', resourceName, 'Properties', 'FilterPattern']
                    message = f'The FilterPattern of {resourceName} was {filterPattern} which does not match the \
expected patterns {self.EXPECTED_FILTER_PATTERNS}. This will prevent logs from being propagated to Kibana.'
                    matches.append(RuleMatch(path, message))
        return matches
