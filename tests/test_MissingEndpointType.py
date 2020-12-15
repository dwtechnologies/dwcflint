import unittest
import cfnlint.core
from tests.utils import getFileOrDefault, getDirOrDefault


class MissingEndpointTypeTest(unittest.TestCase):
    RULE_ID = 'W1347'

    def test_something(self):
        filename = getFileOrDefault('tests/test-data/networking.yaml', 'test-data/networking.yaml')
        template = cfnlint.decode.cfn_yaml.load(filename)
        cfnlint.core.configure_logging(None)
        rules = cfnlint.core.get_rules([getDirOrDefault('cflint/rules/', '../cflint/rules/')], [], [])
        matches = cfnlint.core.run_checks(filename, template, rules, ['eu-west-1'])

        self.assertGreater(len(matches), 0)
        filteredMatches = [match for match in matches if match.rule.id == self.RULE_ID]
        self.assertEqual(len(filteredMatches), 3)
        self.assertEqual(filteredMatches[0].path_string, 'Resources/RestApi3')
        self.assertEqual(filteredMatches[1].path_string, 'Resources/RestApi4')
        self.assertEqual(filteredMatches[2].path_string, 'Resources/RestApi5')


if __name__ == '__main__':
    unittest.main()
