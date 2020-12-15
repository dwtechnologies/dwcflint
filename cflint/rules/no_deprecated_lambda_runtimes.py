from cfnlint.rules import CloudFormationLintRule, RuleMatch


class NoDeprecatedLambdaRuntimes(CloudFormationLintRule):
    """Warns if any lambda functions using deprecated runtimes are used"""
    id = 'W1343'
    shortdesc = 'Warns if any lambda functions using deprecated runtimes are used'
    description = 'Warns if any lambda functions using deprecated runtimes are used'
    source_url = 'https://bitbucket.com/keycomponent/cfn-python-lint-dw'
    tags = ['lambda', 'runtime', 'function', 'deprecation']

    deprecatedRuntimes = ['nodejs8.10']

    def match(self, cfn):
        matches = []

        resources = cfn.get_resources([])
        for resourceName, resource in resources.items():
            if resource['Type'] in ['AWS::Serverless::Function', 'AWS::Lambda::Function']:
                param = resource['Properties']['Runtime']
                if 'Runtime' in resource['Properties'] and param in self.deprecatedRuntimes:

                    path = ['Resources', resourceName, 'Properties', 'Runtime']
                    message = f'Found lambda using deprecated runtime "{param}", this lambda will stop working after ' \
                              f'the EOL date of this runtime!'
                    matches.append(RuleMatch(path, message))

        return matches
