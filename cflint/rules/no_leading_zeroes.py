from cfnlint.rules import CloudFormationLintRule, RuleMatch
from datetime import date


class NoLeadingZeroes(CloudFormationLintRule):
    """Fails if using strings containing numbers with leading zeroes"""
    id = 'E1338'
    shortdesc = 'Throws error if numbers with leading zeroes are found'
    description = 'Detects occurrences of strings containing numbers with leading zeroes, since the PyYAML lib will ' \
                  'automatically convert these to numbers without leading zeroes, which can be catastrophic. '
    source_url = 'https://bitbucket.com/keycomponent/cfn-python-lint-dw'
    tags = ['numbers', 'strings', 'yaml', 'quirks']

    @staticmethod
    def check_value(value):
        if value.isnumeric() and value[0] == '0':
            return True
        return False

    def match(self, cfn):
        matches = []

        mappings = cfn.get_mappings()
        for key0 in mappings.keys():
            for key1 in mappings[key0].keys():
                for key2 in mappings[key0][key1].keys():
                    value = mappings[key0][key1][key2]
                    if not (isinstance(value, int) or isinstance(value, float)):
                        if self.check_value(value):
                            path = ['Mappings', key0, key1, key2]
                            key = '.'.join(path[1:])
                            message = f"Error: The mapping with the key {key} and value {value} will have its " \
                                f"value's leading zero(es) stripped by aws-cli. It is highly recommended that you " \
                                f"add a leading non-numeric character and convert it back in your code or use a " \
                                f"number without a leading zero to avoid incorrect values."
                            matches.append(RuleMatch(path, message))

        extractedValues = []
        for key, value in cfn.get_resources().items():
            self._extractValues(value['Properties'], extractedValues, ['Resources', key, 'Properties'])
        if len(extractedValues):
            for match in extractedValues:
                matches.append(match)

        return matches

    def _extractValues(self, node, extractedValues, path):
        if callable(getattr(node, "values", None)):
            for key, value in node.items():
                self._extractValues(value, extractedValues, path + [key])
        elif 'cfnlint.decode.node.create_dict_list_class.<locals>.node_class' in str(type(node)):
            for i in range(0, len(node)):
                self._extractValues(node[i], extractedValues, path)
        elif type(node) is str or 'cfnlint.decode.node.create_str_node_class.<locals>.node_class' in str(type(node)):
            strValue = str(node)
            if strValue.isnumeric() and strValue[0] == '0':
                extractedValues.append(RuleMatch(path, self.createRuleMatchMessage(strValue, path)))
        elif type(node) is int:
            strValue = str(node)
            if strValue.isnumeric() and strValue[0] == '0':
                extractedValues.append(RuleMatch(path, self.createRuleMatchMessage(strValue, path)))
        elif type(node) is date:
            pass
        else:
            print('Found unknown node type: ', type(node), node)

    @staticmethod
    def createRuleMatchMessage(strValue, path):
        return f"Error: The property {'.'.join(path)} with the value {strValue} will have its value's leading " \
            f"zero(es) stripped by aws-cli. It is highly recommended that you add a leading non-numeric " \
            f"character and convert it back in your code or use a number without a leading zero to avoid " \
            f"incorrect values."
