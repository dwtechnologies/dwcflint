import unittest
import cfnlint.core
from tests.utils import findMatchBySubstring, getFileOrDefault, getDirOrDefault


class NoMissingLogGroupsTest(unittest.TestCase):
    RULE_ID = 'E1345'

    def test_should_throw_error_for_new_lambda_with_old_sub_filter_pattern(self):
        filename = getFileOrDefault('tests/test-data/logGroups.yaml', 'test-data/logGroups.yaml')
        template = cfnlint.decode.cfn_yaml.load(filename)
        cfnlint.core.configure_logging(None)
        rules = cfnlint.core.get_rules([getDirOrDefault('cflint/rules/', '../cflint/rules/')], [], [])
        matches = cfnlint.core.run_checks(filename, template, rules, ['eu-west-1'])

        self.assertGreater(len(matches), 0)
        filteredMatches = [match for match in matches if match.rule.id == self.RULE_ID]
        self.assertEqual(len(filteredMatches), 1)
        self.assertIsNotNone(findMatchBySubstring('YetAnotherExampleSubscriptionFilter', filteredMatches))


if __name__ == '__main__':
    unittest.main()
