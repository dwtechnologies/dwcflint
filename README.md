# dwcflint - Custom rules and wrapper for Amazon's cfnlint
[![PyPI version](https://badge.fury.io/py/dwcflint.svg)](https://badge.fury.io/py/dwcflint)

This Python module is a runnable module and wrapper around Amazons cfn-lint tool for Cloudformation file linting that
adds a few extra rules. It is written in Python 3, lightweight (only a single dependency) and fast.

## Background

This module was created at Daniel Wellington during early 2019 as we were
gradually running into various gotchas and corner cases with Cloudformation.
Some of these gotchas caused issues during testing and production of our
projects, and we started thinking about how we could automatically detect
these Cloudformation patterns and warn about them before they made it into
AWS stack deployments. This led to the discovery of AWS' cfn-lint and we
decided to create a wrapper around this tool so that we could easily bundle
custom rules for the corner cases we discovered and distribute them among
the development teams. Eventually we made the decision to open source this
module as it can be useful to other developers and organizations as well.

## How to run in a pipeline

    # assuming you have Python 3 installed
    pip3 install dwcflint
    dwcflint cloudformation/cf.yaml
    
    # or for multiple files
    dwcflint 'cloudformation/*.yaml'

For an even simpler setup, you can add the installation line to your custom pipeline images and then just call `dwcflint` in your project-specific pipeline step(s).

## How to add new rules

To add a new rule, create a new class in the `cflint/rules` folder that
extends the `CloudFormationLintRule` class. Then add a public method named `match`
that takes the `self` and `cfn` parameters. The match method should return
an array of `RuleMatch` objects or an empty array if no matches for the rule
logic were found in the Cloudformation file. Then add public string fields named
id, shortdesc and description. The id field must be prefixed with a 'W' or
an 'E' representing whether it's an error or a warning, followed by a
positive integer representing it's id.

## How to run locally

    pip3 install dwcflint
    dwcflint cloudformation/cf.yaml
    # or for multiple files
    dwcflint 'cloudformation/*.yaml'

## How to run tests

    python3 -m unittest discover -s tests/ -t tests/

## List of rules

- No mismatched log groups and subscription filters
- No missing endpoint types
- No missing log retention period
- No use of deprecated lambda runtimes
- No use of full access policies
- No use of leading zeroes in numbers or strings
- No missing/implicit log groups for lambdas
- No use of old style subscription filters
- No use of provisioned throughput
- No use of reserved environment variable names
- No use of reserved words for Dynamodb column names
- No malformed subscription filters

## Dependencies

- cfnlint (https://pypi.org/project/cfn-lint/)

## Sample output

    E1338 Error: The mapping with the key dev.examplemall-locationA.machineid and value 0600586 will have its value's leading zero(es) stripped by aws-cli. It is highly recommended that you add a leading non-numeric character and convert it back in your code or use a number without a leading zero to avoid incorrect values.
    test-data/cf.yaml:24:7
    
    W1337 The policies of DailySalesPollerExampleMall01Role contain overly broad policies: AmazonSQSFullAccess, AmazonDynamoDBFullAccess
    test-data/cf.yaml:74:1
    
    W1337 The policies of SftpUploaderRole contain overly broad policies: AmazonDynamoDBFullAccess, AmazonSSMFullAccess
    test-data/cf.yaml:74:1
    
    W1337 The policies of PutItemShipmentsLambdaRole contain too broad policy actions: s3:*
    test-data/cf.yaml:342:9
    
    E1338 Error: The resource property with the value 01 will have its value's leading zero(es) stripped by aws-cli. It is highly recommended that you add a leading non-numeric character and convert it back in your code or use a number without a leading zero to avoid incorrect values.
    test-data/cf.yaml:376:7

## Commandline usage

    usage: beamcflint [-h] [--regions REGIONS]
                      [--include-experimental INCLUDEEXPERIMENTAL]
                      [--included-rules INCLUDEDRULES]
                      [--ignored-rules IGNOREDRULES]
                      templatefile

    ...

    positional arguments:
      templatefile          The cloudformation yaml file to be linted

    optional arguments:
      -h, --help            show this help message and exit
      --regions REGIONS     A comma-separated list of AWS regions
      --include-experimental INCLUDEEXPERIMENTAL
                            Include experimental rules from Amazon?
      --included-rules INCLUDEDRULES
                            A comma-separated list of rule ids to include
      --ignored-rules IGNOREDRULES
                            A comma-separated list of rule ids to exclude
