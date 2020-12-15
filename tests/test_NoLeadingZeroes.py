import unittest
import cfnlint.core

from tests.utils import getFileOrDefault, getDirOrDefault


class NoLeadingZeroesTest(unittest.TestCase):
    def test_should_throw_error_for_cf_file_containing_leading_zeroes(self):
        filename = getFileOrDefault('tests/test-data/cf.yaml', 'test-data/cf.yaml')
        template = cfnlint.decode.cfn_yaml.load(filename)
        cfnlint.core.configure_logging(None)
        rules = cfnlint.core.get_rules([getDirOrDefault('cflint/rules/', '../cflint/rules/')], ['W1337'], [])
        regions = ['eu-west-1']

        matches = cfnlint.core.run_checks(filename, template, rules, regions)

        self.assertGreater(len(matches), 0)
        filteredMatches = [match for match in matches if match.rule.id == 'E1338']
        self.assertEqual(len(filteredMatches), 3)
        self.assertTrue('value 0600586' in filteredMatches[0].message)
        self.assertEqual(filteredMatches[0].path_string, 'Mappings/dev/examplemall-locationA/machineid')
        self.assertTrue('value 02500381' in filteredMatches[1].message)
        self.assertEqual(filteredMatches[1].path_string, 'Mappings/dev/examplemall-locationB/machineid')
        self.assertTrue('value 01' in filteredMatches[2].message)
        self.assertEqual(filteredMatches[2].path_string, 'Resources/ScheduledSalesPollerRole01/Properties/Targets/Id')


if __name__ == '__main__':
    unittest.main()
