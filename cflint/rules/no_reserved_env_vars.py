from cfnlint.rules import CloudFormationLintRule, RuleMatch


class NoReservedEnvVars(CloudFormationLintRule):
    """Warns if any lambda functions are using reserved env var names"""
    id = 'W1348'
    shortdesc = 'Warns if any lambda functions are using reserved env var names'
    description = 'Warns if any lambda functions are using reserved env var names'
    source_url = 'https://bitbucket.com/keycomponent/cfn-python-lint-dw'
    tags = ['lambda', 'reserved keywords', 'environment variables']

    reservedEnvVars = [
        'LANG',
        'PATH',
        'LD_LIBRARY_PATH',
        'NODE_PATH',
        'PYTHONPATH',
        'GEM_PATH'
    ]

    @staticmethod
    def intersection(lst1, lst2):
        return list(set(lst1) & set(lst2))

    def match(self, cfn):
        matches = []

        resources = cfn.get_resources([])
        for resourceName, resource in resources.items():
            if resource['Type'] in ['AWS::Serverless::Function', 'AWS::Lambda::Function']:
                if 'Environment' in resource['Properties'] and 'Variables' in resource['Properties']['Environment']:
                    envVars = resource['Properties']['Environment']['Variables']
                    violations = self.intersection(envVars, self.reservedEnvVars)

                    if len(violations):
                        path = ['Resources', resourceName, 'Properties', 'Environment', 'Variables']
                        message = f'Found usage of reserved environment variable name(s) {",".join(violations)},' \
                                  f' this can cause runtime errors.'
                        matches.append(RuleMatch(path, message))

        return matches
