# QuickConf

QuickConf is a tool designed for executing commands and configuring the system on various distros.

## Usage

In QuickConf, transactions are broken down into steps. Each step has its targeting distro, requirements and commands (for diffrent distros). Also, steps can be recursively included, presenting tree-like structure.

QuickConf can be configured through .yaml files. Here is an example.

```yaml
the_name_of_the_step:
    target:
        - legacy
        # or
        # - debian
        # - fedora>=44
        # ...
    requires:
        - legacy:
            - git
        # or
        # ...
    commands:
        - legacy: # All targets above
            - git clone https://github.com/LinuxCabin/quickconf
            - =subtasks/subtask1
```