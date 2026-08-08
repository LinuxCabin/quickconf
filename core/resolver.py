import yaml


def _parse_requires(requires):
    if not requires:
        return []

    if isinstance(requires, list):
        parsed = []
        for item in requires:
            if isinstance(item, dict):
                for target_name, pkg_list in item.items():
                    parsed.append({"target": target_name, "requires": list(pkg_list)})
            else:
                parsed.append({"target": "legacy", "requires": [item]})
        return parsed

    if isinstance(requires, dict):
        parsed = []
        for target_name, pkg_list in requires.items():
            parsed.append({"target": target_name, "requires": list(pkg_list)})
        return parsed

    return [{"target": "legacy", "requires": [requires]}]


def parse_steps(data):
    if not isinstance(data, dict):
        raise TypeError("step data must be a mapping")

    optional = bool(data.get("optional", False))
    steps = {}
    for name, config in data.items():
        if name == "optional":
            continue
        if not isinstance(config, dict):
            raise TypeError(f"step '{name}' must be a mapping")

        target = config.get("target", [])
        requires = config.get("requires", [])
        commands = config.get("commands", [])

        parsed_commands = []
        for item in commands:
            if isinstance(item, dict):
                for target_name, command_list in item.items():
                    parsed_commands.append(
                        {
                            "target": target_name,
                            "commands": list(command_list),
                        }
                    )
            else:
                parsed_commands.append({"target": "legacy", "commands": [item]})

        steps[name] = {
            "target": list(target),
            "requires": _parse_requires(requires),
            "commands": parsed_commands,
            "optional": bool(config.get("optional", False)),
        }

    return {"steps": steps, "optional": optional}


def load_steps_from_yaml(text):
    data = yaml.safe_load(text) or {}
    return parse_steps(data)

