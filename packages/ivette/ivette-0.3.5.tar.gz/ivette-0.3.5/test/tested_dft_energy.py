def get_total_dft_energy(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if 'Total DFT energy' in line:  # replace 'energy' with the actual keyword
                # assumes the energy value is after an '=' sign
                energy = float(line.split('=')[-1].strip())
                return energy

# Example usage
if __name__ == '__main__':
    energy = get_total_dft_energy('9656218b-1dff-4bc5-b1e3-e6f46bd1e52d')
    print(energy)
