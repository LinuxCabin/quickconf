import pathlib

import core.info
import core.pkg
import core.resolver


SYSTEM = core.info.get_info()

print("系统：", SYSTEM["distro"])
print("变体：", SYSTEM["distro_variant"])
print("版本：", SYSTEM["distro_ver"])
print("基于：", SYSTEM["distro_like"])


def _select_optional_steps(step_names):
    if len(step_names) <= 1:
        return step_names

    print("请选择要执行的步骤：")
    print(f"0. 不执行")
    for index, name in enumerate(step_names, 1):
        print(f"{index}. {name}")
    
    while True:
        choice = input("输入序号: ").strip()
        if not choice:
            return []

        try:
            selected = int(choice)
        except ValueError:
            print("输入无效，请重新输入")
            continue

        if selected == 0:
            return []

        if 1 <= selected <= len(step_names):
            return [step_names[selected - 1]]

        print("输入超出范围，请重新输入")


def run_task(path):
    with open(path, encoding="utf-8") as handle:
        parsed_conf = core.resolver.load_steps_from_yaml(handle.read())

    conf = parsed_conf["steps"]
    optional = parsed_conf["optional"]

    matching_steps = []
    for step_name, step in conf.items():
        if not step.get("target"):
            continue

        matched = any(
            core.info.distro_match(target, SYSTEM["distro"], SYSTEM["distro_like"])
            for target in step["target"]
        )
        if matched:
            matching_steps.append((step_name, step))

    if optional and len(matching_steps) > 1:
        selected_names = set(_select_optional_steps([name for name, _ in matching_steps]))
        matching_steps = [(name, step) for name, step in matching_steps if name in selected_names]

    for step_name, step in matching_steps:
        print(f"执行任务：{step_name}")

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

