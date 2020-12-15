import unittest
import cflint.linter


class FileNameGlobbingTest(unittest.TestCase):
    regions = ['eu-west-1']

    def test_should_find_all_files_matching_asterisk_suffix(self):
        filename = 'tests/test-data/*'

        matches, hasErrors = cflint.linter.getLintMatchesAndErrorState(filename, [], [], False, self.regions, None)

        self.assertGreater(len(matches), 0)

    def test_should_find_all_files_matching_asterisk_dot_yaml_suffix(self):
        filename = 'tests/test-data/*.yaml'

        matches, hasErrors = cflint.linter.getLintMatchesAndErrorState(filename, [], [], False, self.regions, None)

        self.assertGreater(len(matches), 0)

    def test_should_find_all_files_matching_exact_filename(self):
        filename = 'tests/test-data/cf.yaml'

        matches, hasErrors = cflint.linter.getLintMatchesAndErrorState(filename, [], [], False, self.regions, None)

        self.assertGreater(len(matches), 0)

    def test_should_ignore_swagger_files(self):
        filename = 'tests/test-data/swagger.yaml'

        matches, hasErrors = cflint.linter.getLintMatchesAndErrorState(filename, [], [], False, self.regions, None)

        self.assertEqual(len(matches), 0)


if __name__ == '__main__':
    unittest.main()
