import pathlib

import core.info
import core.pkg
import core.resolver


SYSTEM = core.info.get_info()

print("系统：", SYSTEM["distro"])
print("变体：", SYSTEM["distro_variant"])
print("版本：", SYSTEM["distro_ver"])
print("基于：", SYSTEM["distro_like"])


def run_task(path):
    with open(path, encoding="utf-8") as handle:
        conf = core.resolver.load_steps_from_yaml(handle.read())

    for step_name, step in conf.items():
        if not step.get("target"):
            continue

        matched = any(
            core.info.distro_match(target, SYSTEM["distro"], SYSTEM["distro_like"])
            for target in step["target"]
        )
        if not matched:
            continue

        for item in step.get("requires", []):
            target = item.get("target", "legacy")
            if not core.info.distro_match(target, SYSTEM["distro"], SYSTEM["distro_like"]):
                continue
            core.pkg.install_deps(item.get("requires", []), SYSTEM["distro"], SYSTEM["distro_like"])

        for item in step.get("commands", []):
            target = item.get("target", "legacy")
            if not core.info.distro_match(target, SYSTEM["distro"], SYSTEM["distro_like"]):
                continue
            for command in item.get("commands", []):
                if command.startswith("="):
                    subpath = command[1:]
                    run_task(str(pathlib.Path(path).parent / subpath))
                else:
                    print(f"执行命令: {command}")


if __name__ == "__main__":
    run_task("./recipe.yaml")

