import re


def optimization_energy(filepath):
    with open(filepath, 'r') as file:
        content = file.read()

    matches = re.findall(r'^@\s*\d+\s*(-?\d+\.\d+)', content, re.MULTILINE)

    if matches:
        return float(matches[-1])

    return None

# Example usage
if __name__ == '__main__':
    energy = optimization_energy('9fcce1d9-8002-4243-90b6-78efc099f040')
    if energy is not None:
        print(f"The energy after the optimization converged is {energy}")
    else:
        print("Could not find the energy value in the file.")
