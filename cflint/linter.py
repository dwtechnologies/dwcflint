import argparse
import os.path
import sys
import glob
import pkg_resources
import json

import cfnlint.core


def parseArgs():
    version = pkg_resources.require("dwcflint")[0].version
    parser = argparse.ArgumentParser(description='...')
    parser.add_argument('templatefile', type=str, help='The cloudformation yaml file(s) to be linted')
    parser.add_argument('--regions', type=str, default='eu-west-1', help='A comma-separated list of AWS regions')
    parser.add_argument('--includeexperimental', type=bool, default=False,
                        help='Include experimental rules from Amazon? (deprecated, use --include-experimental)')
    parser.add_argument('--include-experimental', type=bool, default=False,
                        help='Include experimental rules from Amazon?')
    parser.add_argument('--includedrules', type=str, default='',
                        help='A comma-separated list of rule ids to include (deprecated, use --included-rules)')
    parser.add_argument('--included-rules', type=str, default='',
                        help='A comma-separated list of rule ids to include')
    parser.add_argument('--ignoredrules', type=str, default='',
                        help='A comma-separated list of rule ids to exclude (deprecated, use --ignored-rules)')
    parser.add_argument('--ignored-rules', type=str, default='',
                        help='A comma-separated list of rule ids to exclude')
    parser.add_argument('--version', action='version', help='Print version and exit',
                        version=f'Amazon Cloudformation Linter with BEAM ruleset - version {version}')
    parser.add_argument('--json-output-file', type=str, default='', help='Output lint results to a json file')
    args = parser.parse_args()
    if args.ignoredrules or args.includedrules or args.includeexperimental:
        print('Warning: The --ignoredrules, --includedrules and --includeexperimental CLI flags are deprecated and '
              'will be removed in a future version.')
    return args.templatefile, (args.ignoredrules or args.ignored_rules).split(','), \
        (args.includedrules or args.included_rules).split(','), \
        args.includeexperimental or args.include_experimental, args.regions.split(','), args.json_output_file


def convertIdToType(ruleId):
    if ruleId[0] == 'E':
        return 'error'
    if ruleId[0] == 'W':
        return 'warning'
    if ruleId[0] == 'I':
        return 'info'


def printMatchesToFile(outputFilePath, matches):
    output = {'warnings': 0, 'errors': 0, 'info': 0, 'violations': []}
    idMappings = {'W': 'warnings', 'E': 'errors', 'I': 'info'}
    for match in matches:
        output[idMappings[match.rule.id[0]]] = output[idMappings[match.rule.id[0]]] + 1
        output['violations'].append({
            'id': match.rule.id,
            'type': convertIdToType(match.rule.id),
            'message': str(match)
        })
    with open(outputFilePath, 'wt') as fd:
        fd.write(json.dumps(output))


def getLintMatchesAndErrorState(filenameOrGlob, ignored, included, includeExperimental, regions, jsonOutputFilePath):
    fileNames = [filenameOrGlob]
    if '*' in filenameOrGlob:
        fileNames = glob.glob(filenameOrGlob)
    fileNames = [fileName for fileName in fileNames if 'swagger.yml' not in fileName and 'swagger.yaml' not in fileName]

    hasErrors = False
    cfnlint.core.configure_logging(None)
    currentFilePath = os.path.abspath(os.path.dirname(__file__))
    rulesDir = os.path.abspath(os.path.join(currentFilePath, "rules"))
    rules = cfnlint.core.get_rules([rulesDir], ignored, included, includeExperimental)

    allMatches = []
    for fileName in fileNames:
        template = cfnlint.decode.cfn_yaml.load(fileName)

        matches = cfnlint.core.run_checks(fileName, template, rules, regions)
        if not hasErrors:
            hasErrors = len([match for match in matches if match.rule.id[0] == 'E']) > 1
        allMatches += matches

    if jsonOutputFilePath:
        printMatchesToFile(jsonOutputFilePath, allMatches)

    return allMatches, hasErrors


def runLinter():
    filenameOrGlob, ignored, included, includeExperimental, regions, jsonOutputFile = parseArgs()
    matches, hasErrors = getLintMatchesAndErrorState(filenameOrGlob, ignored, included, includeExperimental, regions,
                                                     jsonOutputFile)

    for match in matches:
        print(match)

    if hasErrors:
        sys.exit(-1)
    sys.exit(0)
