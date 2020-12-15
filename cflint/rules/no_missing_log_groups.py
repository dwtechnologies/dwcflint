from cfnlint.rules import CloudFormationLintRule, RuleMatch


class NoMissingLogGroups(CloudFormationLintRule):
    """Errors if any lambdas do not have corresponding log groups."""
    id = 'E1341'
    shortdesc = 'Throws error if any lambdas do not have corresponding log groups'
    description = 'Throws error if any lambdas do not have corresponding log groups'
    source_url = 'https://bitbucket.com/keycomponent/cfn-python-lint-dw'
    tags = ['cloudwatch', 'logging', 'logs', 'log-groups', 'subscription-filters']

    # noinspection PyMethodMayBeStatic
    def match(self, cfn):
        matches = []

        lambdas = []
        logGroups = []

        resources = cfn.get_resources([])
        for resourceName, resource in resources.items():
            if resource['Type'] in ['AWS::Serverless::Function', 'AWS::Lambda::Function']:
                lambdas.append((resourceName, resource))
            if resource['Type'] == 'AWS::Logs::LogGroup':
                logGroups.append((resourceName, resource))

        for l in lambdas:
            lambdaName = str(l[1]['Properties']['FunctionName'])
            resourceName = "{'Fn::Sub': '${" + str(l[0]) + "}'}"
            foundLogGroups = list(filter(
                lambda x: self.normalizeLogGrpName(x) in [lambdaName, resourceName], logGroups))
            if not len(foundLogGroups):
                path = ['Resources', l[0]]
                message = 'Found lambda without matching log group'
                matches.append(RuleMatch(path, message))

        return matches

    @staticmethod
    def normalizeLogGrpName(logGroup):
        return str(logGroup[1]['Properties']['LogGroupName']).replace('/aws/lambda/', '')
