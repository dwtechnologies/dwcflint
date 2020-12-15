# dwcflint - Custom rules and wrapper for Amazon's cfnlint

This Python module is a runnable module and wrapper around Amazons cfn-lint tool for Cloudformation file linting that
adds a few extra rules. It is written in Python 3, lightweight (only a single dependency) and fast.

## How to run in a pipeline:

    # assuming you have Python 3 installed
    pip3 install dwcflint
    dwcflint cloudformation/cf.yaml
    
    # or for multiple files
    dwcflint 'cloudformation/*.yaml'

For an even simpler setup, you can add the installation line to your custom pipeline images and then just call `beamcflint` in your project-specific pipeline step(s).

## How to run locally:

    pip3 install dwcflint
    dwcflint cloudformation/cf.yaml
    # or for multiple files
    dwcflint 'cloudformation/*.yaml'

## How to run tests:

    python3 -m unittest discover -s tests/ -t tests/

## List of rules:

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

## Sample output:

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
