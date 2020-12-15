import json
import unittest

import cflint.linter
from tests.utils import getFileOrDefault


class JsonOutputFileTest(unittest.TestCase):
    regions = ['eu-west-1']

    def test_should_output_json_to_given_file_path(self):
        filename = getFileOrDefault('tests/test-data/cf.yaml', 'test-data/cf.yaml')
        out = 'output.json'

        matches, hasErrors = cflint.linter.getLintMatchesAndErrorState(filename, [], [], False, self.regions, out)

        self.assertGreater(len(matches), 0)
        with open(out, 'rt') as fd:
            jsonFileOutput = json.loads(fd.read())
        self.assertGreater(jsonFileOutput['errors'], 0)
        self.assertGreater(jsonFileOutput['warnings'], 0)
        self.assertGreaterEqual(jsonFileOutput['info'], 0)
        self.assertGreater(len(jsonFileOutput['violations']), 0)


if __name__ == '__main__':
    unittest.main()
