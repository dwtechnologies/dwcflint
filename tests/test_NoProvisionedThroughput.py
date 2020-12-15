import unittest
import cfnlint.core

from tests.utils import getFileOrDefault, getDirOrDefault

RULE_ID = 'E1340'


class NoProvisionedThroughputTest(unittest.TestCase):
    def test_should_throw_error_if_provisioned_throughput_attrs_are_found(self):
        filename = getFileOrDefault('tests/test-data/cf.yaml', 'test-data/cf.yaml')
        template = cfnlint.decode.cfn_yaml.load(filename)
        cfnlint.core.configure_logging(None)
        rules = cfnlint.core.get_rules([getDirOrDefault('cflint/rules/', '../cflint/rules/')], ['W1337'], [])
        regions = ['eu-west-1']

        matches = cfnlint.core.run_checks(filename, template, rules, regions)

        self.assertGreater(len(matches), 0)
        filteredMatches = [match for match in matches if match.rule.id == RULE_ID]
        self.assertEqual(len(filteredMatches), 2)


if __name__ == '__main__':
    unittest.main()
