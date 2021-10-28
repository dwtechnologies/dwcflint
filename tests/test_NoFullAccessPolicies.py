import unittest
import cfnlint.core

from tests.utils import getFileOrDefault, getDirOrDefault


class NoFullAccessPoliciesTest(unittest.TestCase):

    def test_should_find_matches_for_cf_file_with_full_access_policies(self):
        filename = getFileOrDefault('tests/test-data/cf.yaml', 'test-data/cf.yaml')
        template = cfnlint.decode.cfn_yaml.load(filename)
        cfnlint.core.configure_logging(None)
        rules = cfnlint.core.get_rules([getDirOrDefault('cflint/rules/', '../cflint/rules/')], ['E1338'], [])
        regions = ['eu-west-1']

        matches = cfnlint.core.run_checks(filename, template, rules, regions)

        self.assertGreater(len(matches), 0)
        filteredMatches = [match for match in matches if match.rule.id == 'W1337']
        self.assertEqual(len(filteredMatches), 10)
        self.assertIn('AmazonSQSFullAccess', filteredMatches[0].message)
        self.assertIn('AmazonDynamoDBFullAccess', filteredMatches[0].message)

    def test_should_handle_cf_file_with_mixed_policies(self):
        filename = getFileOrDefault('tests/test-data/oldServerless.yml', 'test-data/oldServerless.yml')
        template = cfnlint.decode.cfn_yaml.load(filename)
        cfnlint.core.configure_logging(None)
        rules = cfnlint.core.get_rules([getDirOrDefault('cflint/rules/', '../cflint/rules/')], [], [])
        regions = ['eu-west-1']

        matches = cfnlint.core.run_checks(filename, template, rules, regions)

        filteredMatches = [match for match in matches if match.rule.id == 'W1337']
        self.assertEqual(len(filteredMatches), 0)


if __name__ == '__main__':
    unittest.main()
