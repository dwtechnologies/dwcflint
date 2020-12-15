import unittest
import cfnlint.core

from tests.utils import getFileOrDefault, getDirOrDefault


class WellFormedSubscriptionFiltersTest(unittest.TestCase):
    RULE_ID = 'W1344'

    def test_should_throw_error_for_cf_file_containing_malformed_filter_pattern(self):
        filename = getFileOrDefault('tests/test-data/cf.yaml', 'test-data/cf.yaml')
        template = cfnlint.decode.cfn_yaml.load(filename)
        cfnlint.core.configure_logging(None)
        rules = cfnlint.core.get_rules([getDirOrDefault('cflint/rules/', '../cflint/rules/')], [], [self.RULE_ID])
        matches = cfnlint.core.run_checks(filename, template, rules, ['eu-west-1'])

        self.assertGreater(len(matches), 0)
        filteredMatches = [match for match in matches if match.rule.id == self.RULE_ID]
        self.assertEqual(len(filteredMatches), 1)
        self.assertIn('One or more column names of ExampleTable contain reserved keywords: INDEX', filteredMatches[0].message)


if __name__ == '__main__':
    unittest.main()
