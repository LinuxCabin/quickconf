# QuickConf

QuickConf is a tool designed for executing commands and configuring the system on various distros.

## Usage

In QuickConf, transactions are broken down into steps. Each step has its targeting distro, requirements and commands (for diffrent distros). Also, steps can be recursively included, presenting tree-like structure.

QuickConf can be configured through .yaml files. Here is an example.

```yaml
optional: true
# When true, if multiple steps in this file match the current system,
# the user will be prompted to choose one to run.

step_a:
    target:
        - legacy
    requires:
        - legacy:
            git
    commands:
        - legacy:
            - echo "run step a"

step_b:
    target:
        - legacy
    commands:
        - legacy:
            - echo "run step b"
```