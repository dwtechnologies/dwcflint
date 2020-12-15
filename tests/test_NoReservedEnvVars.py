import unittest
import cfnlint.core

from tests.utils import getFileOrDefault, getDirOrDefault


class NoReservedEnvVarsTest(unittest.TestCase):
    RULE_ID = 'W1348'

    def test_should_warn_for_usage_of_reserved_names_in_lambda_env_vars(self):
        filename = getFileOrDefault('tests/test-data/cf.yaml', 'test-data/cf.yaml')
        template = cfnlint.decode.cfn_yaml.load(filename)
        cfnlint.core.configure_logging(None)
        rules = cfnlint.core.get_rules([getDirOrDefault('cflint/rules/', '../cflint/rules/')], [], [self.RULE_ID])
        matches = cfnlint.core.run_checks(filename, template, rules, ['eu-west-1'])

        self.assertGreater(len(matches), 0)
        filteredMatches = [match for match in matches if match.rule.id == self.RULE_ID]
        self.assertEqual(len(filteredMatches), 2)
        self.assertIn('Found usage of reserved environment variable name(s) PATH, this can cause runtime errors.',
                      filteredMatches[0].message)
        self.assertIn('Found usage of reserved environment variable name(s) LANG, this can cause runtime errors.',
                      filteredMatches[1].message)


if __name__ == '__main__':
    unittest.main()
