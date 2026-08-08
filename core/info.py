import os


def _get_os_release():
    release_path = "/etc/os-release"
    if not os.path.exists(release_path):
        return {}

    data = {}
    with open(release_path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            data[key] = value.strip().strip('"')

    return data


def get_info():
    os_release = _get_os_release()

    return {
        "distro": os_release.get("ID", "unknown"),
        "distro_like": os_release.get("ID_LIKE", "unknown"),
        "distro_ver": os_release.get("VERSION_ID", "unknown"),
        "distro_variant": os_release.get("VARIANT_ID", "unknown"),
        "display": os.environ.get("DISPLAY", "unknown"),
    }
    
def distro_match(target,distro,distro_like):
    if target == "legacy":
        return True
    if target=="ubuntu":
        if distro=="ubuntu" or distro_like=="ubuntu":
            return True
        return False
    if target=="debian":
        if distro=="ubuntu":
            return False
        return True
    return distro == target or distro_like == target