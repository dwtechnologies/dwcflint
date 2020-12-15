import unittest

import cfnlint.core

from tests.utils import getFileOrDefault, getDirOrDefault, findMatchBySubstring


class WellFormedSubscriptionFiltersTest(unittest.TestCase):
    RULE_ID = 'E1339'

    def test_should_throw_error_for_cf_file_containing_malformed_filter_pattern(self):
        filename = getFileOrDefault('tests/test-data/cf.yaml', 'test-data/cf.yaml')
        template = cfnlint.decode.cfn_yaml.load(filename)
        cfnlint.core.configure_logging(None)
        rules = cfnlint.core.get_rules([getDirOrDefault('cflint/rules/', '../cflint/rules/')], [], [])
        matches = cfnlint.core.run_checks(filename, template, rules, ['eu-west-1'])

        self.assertGreater(len(matches), 0)
        filteredMatches = [match for match in matches if match.rule.id == self.RULE_ID]
        self.assertEqual(len(filteredMatches), 1)
        self.assertEqual(filteredMatches[0].message, "The FilterPattern of MallSalesReportSftpUploaderLogForwardSubscri\
ption was [time, uuid, app=overwatch, metric] which does not match the expected patterns ['[time, uuid, \
app=overwatch*, metric]', '[time, uuid, app=overwatch*, data]', '[time, uuid, level, app=overwatch*, metric]', \
'[time, uuid, level, app=overwatch*, data]']. This will prevent logs from being propagated to Kibana.")

    def test_should_not_throw_error_filter_pattern_with_ref(self):
        filename = getFileOrDefault('tests/test-data/logGroups.yaml', 'test-data/logGroups.yaml')
        template = cfnlint.decode.cfn_yaml.load(filename)
        cfnlint.core.configure_logging(None)
        rules = cfnlint.core.get_rules([getDirOrDefault('cflint/rules/', '../cflint/rules/')], [], [])
        matches = cfnlint.core.run_checks(filename, template, rules, ['eu-west-1'])

        self.assertGreater(len(matches), 0)
        filteredMatches = [match for match in matches if match.rule.id == self.RULE_ID]
        self.assertIsNone(findMatchBySubstring('YetAnotherAdditionalExampleSubscriptionFilter', filteredMatches))
        self.assertEqual(len(filteredMatches), 0)


if __name__ == '__main__':
    unittest.main()
