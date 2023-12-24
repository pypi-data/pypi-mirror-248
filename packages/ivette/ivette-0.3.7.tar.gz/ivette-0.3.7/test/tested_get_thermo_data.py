from ivette.types import ThermoData


def get_thermo_data(file_path):
    thermo_data = ThermoData()
    # flag to check if 'cv (constant volume heat capacity)' line has passed
    cv_passed = False
    with open(file_path, 'r') as file:
        for line in file:
            line = line.lower().strip()  # convert line to lower case and strip spaces
            if 'temperature' in line:
                thermo_data.temp = float(
                    line.split('=')[1].split('k')[0].strip())
            elif 'frequency scaling parameter' in line:
                thermo_data.freq_scale = float(line.split('=')[1].strip())
            elif 'zero-point correction to energy' in line:
                thermo_data.zpe = float(line.split(
                    '=')[1].split('kcal')[0].strip())
            elif 'thermal correction to energy' in line:
                thermo_data.te = float(line.split(
                    '=')[1].split('kcal')[0].strip())
            elif 'thermal correction to enthalpy' in line:
                thermo_data.th = float(line.split(
                    '=')[1].split('kcal')[0].strip())
            elif 'total entropy' in line:
                thermo_data.ts = float(line.split(
                    '=')[1].split('cal')[0].strip())
            elif '- translational' in line and not cv_passed:
                thermo_data.ts_trans = float(
                    line.split('=')[1].split('cal')[0].strip())
            elif '- rotational' in line and not cv_passed:
                thermo_data.ts_rot = float(
                    line.split('=')[1].split('cal')[0].strip())
            elif '- vibrational' in line and not cv_passed:
                thermo_data.ts_vib = float(
                    line.split('=')[1].split('cal')[0].strip())
            elif 'cv (constant volume heat capacity)' in line:
                thermo_data.cv = float(line.split(
                    '=')[1].split('cal')[0].strip())
                # set the flag to True after 'cv (constant volume heat capacity)' line
                cv_passed = True
            # only check for translational, rotational, and vibrational Cv values after 'cv (constant volume heat capacity)' line
            elif cv_passed:
                if '- translational' in line:
                    thermo_data.cv_trans = float(
                        line.split('=')[1].split('cal')[0].strip())
                elif '- rotational' in line:
                    thermo_data.cv_rot = float(
                        line.split('=')[1].split('cal')[0].strip())
                elif '- vibrational' in line:
                    thermo_data.cv_vib = float(
                        line.split('=')[1].split('cal')[0].strip())
    return thermo_data


# Example of how to use the above function
if __name__ == "__main__":
    thermo_data = get_thermo_data('public/7bd411bc-5c30-4758-a86f-34acce9fd9b8')
    for key, value in thermo_data.__dict__.items():
        print(key, value)