from cfnlint.rules import CloudFormationLintRule, RuleMatch


class NoOldStyleSubscriptionFilters(CloudFormationLintRule):
    """Errors if any lambdas with nodejs 10.x runtimes use the old subscription filter pattern."""
    id = 'E1345'
    shortdesc = 'Throws error if any lambdas with nodejs 10.x use old style sub filter pattern'
    description = 'Throws error if any lambdas with nodejs 10.x use old style sub filter pattern'
    source_url = 'https://bitbucket.com/keycomponent/cflint'
    tags = ['cloudwatch', 'logging', 'logs', 'subscription-filters']

    oldStyleFilterPatterns = [
        "[time, uuid, app=overwatch*, metric]",
        "[time, uuid, app=overwatch*, data]",
    ]

    def match(self, cfn):
        matches = []

        lambdas = []
        subFilters = []

        resources = cfn.get_resources([])
        for resourceName, resource in resources.items():
            if self.isLambdaWithNewRuntime(resource):
                lambdas.append((resourceName, resource))
            if resource['Type'] == 'AWS::Logs::SubscriptionFilter':
                subFilters.append((resourceName, resource))

        for sf in subFilters:
            logGroupName = self.normalizeLogGroupName(sf)
            foundLambda = next((l for l in lambdas if l[1]['Properties']['FunctionName'] == logGroupName or
                                self.wrapInSub(l[0]) == logGroupName), None)
            found = foundLambda and sf[1]['Properties']['FilterPattern'] in self.oldStyleFilterPatterns
            if found:
                path = ['Resources', sf[0]]
                message = 'Found subscription filter with with old-style FilterPattern used by nodejs10.x lambda. \
This will prevent propagation of logs to Kibana. Use the new-style filter pattern with "level" as the third parameter.'
                matches.append(RuleMatch(path, message))

        return matches

    @staticmethod
    def wrapInSub(resourceName):
        return "{'Fn::Sub': '${" + str(resourceName) + "}'}"

    @staticmethod
    def normalizeLogGroupName(logGroup):
        return str(logGroup[1]['Properties']['LogGroupName']).replace('/aws/lambda/', '')

    @staticmethod
    def isLambdaWithNewRuntime(resource):
        return resource['Type'] in ['AWS::Serverless::Function', 'AWS::Lambda::Function'] and \
               resource['Properties']['Runtime'] == 'nodejs10.x'
