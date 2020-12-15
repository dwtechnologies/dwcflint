import unittest
import cfnlint.core
from tests.utils import getFileOrDefault, getDirOrDefault


class MissingLogRetentionPeriodTest(unittest.TestCase):
    RULE_ID = 'W1346'

    def test_should_throw_error_for_cf_file_containing_log_groups_without_retention_periods(self):
        filename = getFileOrDefault('tests/test-data/logGroups.yaml', 'test-data/logGroups.yaml')
        template = cfnlint.decode.cfn_yaml.load(filename)
        cfnlint.core.configure_logging(None)
        rules = cfnlint.core.get_rules([getDirOrDefault('cflint/rules/', '../cflint/rules/')], [], [])
        matches = cfnlint.core.run_checks(filename, template, rules, ['eu-west-1'])

        self.assertGreater(len(matches), 0)
        filteredMatches = [match for match in matches if match.rule.id == self.RULE_ID]
        self.assertEqual(len(filteredMatches), 2)


if __name__ == '__main__':
    unittest.main()
