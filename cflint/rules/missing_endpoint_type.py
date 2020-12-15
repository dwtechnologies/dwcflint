from cfnlint.rules import CloudFormationLintRule, RuleMatch


class MissingEndpointType(CloudFormationLintRule):
    """Warns if API gateways are missing endpoint types"""
    id = 'W1347'
    shortdesc = 'Warns if API gateways are missing endpoint types'
    description = 'Warns if API gateways are missing endpoint types such as REGIONAL, EDGE or PRIVATE'
    source_url = 'https://bitbucket.com/keycomponent/cfn-python-lint-dw'
    tags = ['apigateway', 'rest', 'api', 'http']

    def match(self, cfn):
        matches = []

        resources = cfn.get_resources([])
        for resourceName, resource in resources.items():
            if resource['Type'] == 'AWS::ApiGateway::RestApi' and not self.hasEndpointType(resource['Properties']):
                matches.append(RuleMatch(['Resources', resourceName],
                                         'Found RestApi without explicitly set endpoint type'))
            elif resource['Type'] == 'AWS::Serverless::Api' and not self.hasEndpointType(resource['Properties']):
                matches.append(RuleMatch(['Resources', resourceName],
                                         'Found SAM Api without explicitly set endpoint type'))

        return matches

    @staticmethod
    def hasEndpointType(props):
        return ('Parameters' in props and 'endpointConfigurationTypes' in props['Parameters']) or \
               ('EndpointConfiguration' in props and 'Types' in props['EndpointConfiguration']) or \
               ('EndpointConfiguration' in props and props['EndpointConfiguration'] in ['REGIONAL', 'EDGE', 'PRIVATE'])
