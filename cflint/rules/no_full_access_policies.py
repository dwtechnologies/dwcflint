from cfnlint.rules import CloudFormationLintRule, RuleMatch


class NoFullAccessPolicies(CloudFormationLintRule):
    """Warns about using full-access policies, such as AmazonS3FullAccess"""
    id = 'W1337'
    shortdesc = 'Warns about using full-access policies, such as AmazonS3FullAccess'
    description = 'Warns about using full-access policies, such as AmazonS3FullAccess'
    source_url = 'https://bitbucket.com/keycomponent/cfn-python-lint-dw'
    tags = ['iam', 'policies']

    riskyPolicySuffixes = {
        "AWSAppSyncInvokeFullAccess",
        "AWSApplicationDiscoveryServiceFullAccess",
        "AWSBatchFullAccess",
        "AWSCertificateManagerFullAccess",
        "AWSCertificateManagerPrivateCAFullAccess",
        "AWSCloudHSMFullAccess",
        "AWSCloudTrailFullAccess",
        "AWSCodeCommitFullAccess",
        "AWSCodeDeployFullAccess",
        "AWSCodePipelineFullAccess",
        "AWSCodeStarFullAccess",
        "AWSDataPipeline_FullAccess",
        "AWSDeviceFarmFullAccess",
        "AWSDirectConnectFullAccess",
        "AWSDirectoryServiceFullAccess",
        "AWSElasticBeanstalkFullAccess",
        "AWSElementalMediaConvertFullAccess",
        "AWSElementalMediaPackageFullAccess",
        "AWSElementalMediaStoreFullAccess",
        "AWSFMAdminFullAccess",
        "AWSGlueConsoleFullAccess",
        "AWSGlueConsoleSageMakerNotebookFullAccess",
        "AWSGreengrassFullAccess",
        "AWSHealthFullAccess",
        "AWSImportExportFullAccess",
        "AWSIoT1ClickFullAccess",
        "AWSIoTAnalyticsFullAccess",
        "AWSIoTFullAccess",
        "AWSLambdaFullAccess",
        "AWSMarketplaceFullAccess",
        "AWSMarketplaceImageBuildFullAccess",
        "AWSMarketplaceMeteringFullAccess",
        "AWSMigrationHubFullAccess",
        "AWSMobileHub_FullAccess",
        "AWSOpsWorksFullAccess",
        "AWSOrganizationsFullAccess",
        "AWSPriceListServiceFullAccess",
        "AWSServiceCatalogAdminFullAccess",
        "AWSServiceCatalogEndUserFullAccess",
        "AWSStepFunctionsConsoleFullAccess",
        "AWSStepFunctionsFullAccess",
        "AWSStorageGatewayFullAccess",
        "AWSWAFFullAccess",
        "AWSXrayFullAccess",
        "AlexaForBusinessFullAccess",
        "AmazonAPIGatewayInvokeFullAccess",
        "AmazonAppStreamFullAccess",
        "AmazonAthenaFullAccess",
        "AmazonChimeFullAccess",
        "AmazonCloudDirectoryFullAccess",
        "AmazonConnectFullAccess",
        "AmazonDynamoDBFullAccess",
        "AmazonDynamoDBFullAccesswithDataPipeline",
        "AmazonEC2ContainerRegistryFullAccess",
        "AmazonEC2ContainerServiceFullAccess",
        "AmazonEC2FullAccess",
        "AmazonECS_FullAccess",
        "AmazonESFullAccess",
        "AmazonElastiCacheFullAccess",
        "AmazonElasticFileSystemFullAccess",
        "AmazonElasticMapReduceFullAccess",
        "AmazonElasticTranscoder_FullAccess",
        "AmazonFreeRTOSFullAccess",
        "AmazonGlacierFullAccess",
        "AmazonGuardDutyFullAccess",
        "AmazonInspectorFullAccess",
        "AmazonKinesisAnalyticsFullAccess",
        "AmazonKinesisFirehoseFullAccess",
        "AmazonKinesisFullAccess",
        "AmazonKinesisVideoStreamsFullAccess",
        "AmazonLexFullAccess",
        "AmazonMQFullAccess",
        "AmazonMachineLearningFullAccess",
        "AmazonMacieFullAccess",
        "AmazonMechanicalTurkCrowdFullAccess",
        "AmazonMechanicalTurkFullAccess",
        "AmazonMobileAnalyticsFullAccess",
        "AmazonPollyFullAccess",
        "AmazonRDSFullAccess",
        "AmazonRedshiftFullAccess",
        "AmazonRekognitionFullAccess",
        "AmazonRoute53AutoNamingFullAccess",
        "AmazonRoute53DomainsFullAccess",
        "AmazonRoute53FullAccess",
        "AmazonS3FullAccess",
        "AmazonSESFullAccess",
        "AmazonSNSFullAccess",
        "AmazonSQSFullAccess",
        "AmazonSSMFullAccess",
        "AmazonSageMakerFullAccess",
        "AmazonSumerianFullAccess",
        "AmazonTranscribeFullAccess",
        "AmazonVPCFullAccess",
        "AmazonWorkMailFullAccess",
        "AmazonZocaloFullAccess",
        "AutoScalingConsoleFullAccess",
        "AutoScalingFullAccess",
        "CloudFrontFullAccess",
        "CloudSearchFullAccess",
        "CloudWatchEventsFullAccess",
        "CloudWatchFullAccess",
        "CloudWatchLogsFullAccess",
        "ComprehendFullAccess",
        "ElasticLoadBalancingFullAccess",
        "IAMFullAccess",
        "NeptuneConsoleFullAccess",
        "NeptuneFullAccess",
        "ResourceGroupsandTagEditorFullAccess",
        "SimpleWorkflowFullAccess",
    }

    def match(self, cfn):
        matches = []

        resources = cfn.get_resources([])
        for resourceName, resource in resources.items():
            if 'ManagedPolicyArns' in resource['Properties']:
                policyList = [i[self.findIndexOrDefault(i, '/', -1) + 1:] for i in
                              resource['Properties']['ManagedPolicyArns'] if isinstance(i, str)]
                intersection = list(set(policyList) & self.riskyPolicySuffixes)
                if len(intersection):
                    path = ['Resources', resourceName]
                    formattedPolicyList = ', '.join(intersection)
                    message = f'The policies of {resourceName} contain overly broad policies: {formattedPolicyList}'
                    matches.append(RuleMatch(path, message))

            policies = resource['Properties'].get('Policies', [])
            for i in range(0, len(policies)):
                policyDocument = policies[i]
                if 'PolicyDocument' in policyDocument:
                    for actions in [i.get('Action', []) for i in policyDocument['PolicyDocument']['Statement']]:
                        for action in actions:
                            if action.endswith(':*'):
                                path = ['Resources', resourceName, 'Properties', 'Policies']
                                message = f'The policies of {resourceName} contain too broad policy actions: {action}'
                                matches.append(RuleMatch(path, message))

        return matches

    @staticmethod
    def findIndexOrDefault(string, substring, defaultValue):
        try:
            return string.rindex(substring)
        except ValueError:
            return defaultValue
