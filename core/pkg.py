import shutil
import subprocess


def install_deps(deps, distro, distro_like):
    if distro == "debian" or distro_like == "debian" or distro_like == "ubuntu":
        subprocess.run(["sudo", "apt", "install", "-y", *deps], check=True)
    elif distro == "fedora":
        subprocess.run(["sudo", "dnf", "install", "-y", *deps], check=True)
    elif distro == "arch":
        for pkg in deps:
            repo_check = subprocess.run(
                ["pacman", "-Si", pkg],
                capture_output=True,
                text=True,
                check=False,
            )

            if repo_check.returncode == 0 and "Repository" in repo_check.stdout:
                subprocess.run(["sudo", "pacman", "-S", "--noconfirm", pkg], check=True)
            else:
                if shutil.which("yay") is not None:
                    subprocess.run(["yay", "-S", "--noconfirm", pkg], check=True)
                elif shutil.which("paru") is not None:
                    subprocess.run(["paru", "-S", "--noconfirm", pkg], check=True)
                else:
                    raise RuntimeError(f"Package '{pkg}' not found in Arch repo and no AUR helper installed")