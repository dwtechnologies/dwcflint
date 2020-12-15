import unittest
import cfnlint.core

from tests.utils import getFileOrDefault, getDirOrDefault


class MatchingLogGroupsAndSubFiltersTest(unittest.TestCase):
    RULE_ID = 'E1342'

    def test_should_throw_error_for_log_groups_without_sub_filters(self):
        filename = getFileOrDefault('tests/test-data/cf.yaml', 'test-data/cf.yaml')
        template = cfnlint.decode.cfn_yaml.load(filename)
        cfnlint.core.configure_logging(None)
        rules = cfnlint.core.get_rules([getDirOrDefault('cflint/rules/', '../cflint/rules/')], [], [])
        matches = cfnlint.core.run_checks(filename, template, rules, ['eu-west-1'])

        self.assertGreater(len(matches), 0)
        filteredMatches = [match for match in matches if match.rule.id == self.RULE_ID]
        self.assertEqual(len(filteredMatches), 2)
        self.assertEqual(str(filteredMatches[1].path[1]), 'ExampledLogGroupWithoutMatchingSubscriptionFilter')

    def test_should_throw_error_for_sub_filters_without_log_groups(self):
        filename = getFileOrDefault('tests/test-data/cf.yaml', 'test-data/cf.yaml')
        template = cfnlint.decode.cfn_yaml.load(filename)
        cfnlint.core.configure_logging(None)
        rules = cfnlint.core.get_rules([getDirOrDefault('cflint/rules/', '../cflint/rules/')], [], [])
        matches = cfnlint.core.run_checks(filename, template, rules, ['eu-west-1'])

        self.assertGreater(len(matches), 0)
        filteredMatches = [match for match in matches if match.rule.id == self.RULE_ID]
        self.assertEqual(len(filteredMatches), 2)
        self.assertEqual(str(filteredMatches[0].path[1]), 'ExampleSubscriptionFilterWithoutMatchingLogGroup')


if __name__ == '__main__':
    unittest.main()
