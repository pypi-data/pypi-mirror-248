import platform
import uuid

from ivette.types import SystemInfo


def system_info():
    info = SystemInfo(
        system_id=str(uuid.getnode()),
        system=platform.system(),
        node=platform.node(),
        release=platform.release(),
        version=platform.version(),
        machine=platform.machine(),
        processor=platform.processor()
    )
    return info

# Example usage
if __name__ == "__main__":
    print(system_info())
