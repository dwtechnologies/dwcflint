from cfnlint.rules import CloudFormationLintRule, RuleMatch


class NoProvisionedThroughput(CloudFormationLintRule):
    """Errors if any DynamoDB instances using ProvisionedThroughput are found"""
    id = 'E1340'
    shortdesc = 'Throws error if DynamoDB instances using ProvisionedThroughput are found'
    description = 'Throws error if DynamoDB instances using ProvisionedThroughput are found'
    source_url = 'https://bitbucket.com/keycomponent/cfn-python-lint-dw'
    tags = ['dynamodb', 'pricing', 'billing']

    def match(self, cfn):
        matches = []

        resources = cfn.get_resources([])
        for resourceName, resource in resources.items():
            if 'ProvisionedThroughput' in resource['Properties']:
                path = ['Resources', resourceName, 'Properties', 'ProvisionedThroughput']
                message = f'Found a DynamoDB instance setup to use ProvisionedThroughput. Instances should always ' \
                          f'use "BillingMode: PAY_PER_REQUEST"'
                matches.append(RuleMatch(path, message))
            if 'GlobalSecondaryIndexes' in resource['Properties']:
                for idx, gsi in enumerate(resource['Properties']['GlobalSecondaryIndexes']):
                    if 'ProvisionedThroughput' in gsi:
                        path = ['Resources', resourceName, 'Properties', 'GlobalSecondaryIndexes', idx, 'ProvisionedThroughput']
                        message = f'Found a DynamoDB index setup to use ProvisionedThroughput. Indexes should ' \
                                  f'always use "BillingMode: PAY_PER_REQUEST" as configured on the instance level.'
                        matches.append(RuleMatch(path, message))

        return matches
