from cfnlint.rules import CloudFormationLintRule, RuleMatch


class MatchingLogGroupsAndSubscriptionFilters(CloudFormationLintRule):
    """Errors if any subscription filters lack corresponding log groups and vice versa"""
    id = 'E1342'
    shortdesc = 'Throws errors for orphaned log groups and subscription filters'
    description = 'Throws errors for orphaned log groups and subscription filters'
    source_url = 'https://bitbucket.com/keycomponent/cfn-python-lint-dw'
    tags = ['cloudwatch', 'logging', 'logs', 'log-groups', 'subscription-filters']

    # noinspection PyMethodMayBeStatic
    def match(self, cfn):
        matches = []

        logGroupsAndSubFilters = []

        resources = cfn.get_resources([])
        for resourceName, resource in resources.items():
            if resource['Type'] == 'AWS::Logs::LogGroup':
                logGroupsAndSubFilters.append((resourceName, resource))
            if resource['Type'] == 'AWS::Logs::SubscriptionFilter':
                logGroupsAndSubFilters.append((resourceName, resource))

        subFilters = list(filter(lambda x: x[1]['Type'] == 'AWS::Logs::SubscriptionFilter', logGroupsAndSubFilters))
        logGroups = list(filter(lambda x: x[1]['Type'] == 'AWS::Logs::LogGroup', logGroupsAndSubFilters))

        matches.extend(self.findComplementOfLists(
            subFilters, logGroups, 'Subscription filter missing matching log group'))
        matches.extend(self.findComplementOfLists(
            logGroups, subFilters, 'Log group missing matching subscription filter'))

        return matches

    @staticmethod
    def findComplementOfLists(listA, listB, message):
        matches = []
        for listAElement in listA:
            logGroupName = listAElement[1]['Properties']['LogGroupName']
            isFound = False
            for listBElement in listB:
                if listBElement[1]['Properties']['LogGroupName'] == logGroupName:
                    isFound = True
                    break
            if not isFound:
                path = ['Resources', listAElement[0]]
                matches.append(RuleMatch(path, message))
        return matches
