# generate_data.py
# $ python3 generate_data.py dt_ratio num_files
# Alex Hergenhan 2024
# generate data files for the project

import os
import numpy as np
import subprocess
import sys

PATH = os.getcwd() + "/../DarkTridentGen/"
NUM_DARK_SCALARS = 10_000


def test_path():
    """Test paths using os.path.exists

    Returns:
        bool: if the path exists true, else false
    """
    if os.path.exists(PATH):
        return True
    else:
        return False
    
def gen_mass_points(dt_ratio, num_files):
    """
     * We want to generate files at sensible mass points.
     * But limits are effected by dt ratio
     * This is limited too the mass of an eta > 2 * m_chi
     * dt_ratio = m_chi / m_A'
     * so m_A'_max = m_chi / dt_ratio


    Returns:
        list : generated mass points
    """
    m_eta_meson = 0.547 # GeV (actually 0.547862, round slightly down to be safe)
    m_chi_max = m_eta_meson / 2.0 # GeV, this is the max we can have for m_chi
    m_A_max = m_chi_max / float(dt_ratio) # GeV, this is the max we can have for m_A'

    min_ma = 0.01 # GeV so 10 MeV
    mass_points = np.linspace(0.01, 0.1, 10)
    mass_points = mass_points.tolist()
    mass_point = 0.2
    while mass_point < m_A_max and len(mass_points) < num_files:
        mass_points.append(mass_point)
        mass_point += 0.1
    mass_point = 0.11
    while len(mass_points) < num_files and mass_point < m_A_max:
        mass_points.append(mass_point)
        mass_point += 0.01

    # round each mass point to 2 decimal places
    
    mass_points = [round(ma, 2) for ma in mass_points]
    
    #order numbers in ascending order
    mass_points.sort()
    
    return mass_points

def generate_paramater_card(dt_ratio, ma, chi_type, dm_mass):
    """Generate a parameter card for this ma and dt_ratio

    Args:
        dt_ratio (str): dt_ratio
        ma (str): mass of the dark photon
        chi_type (str): "scalar" or "fermion"
        dm_mass (str): mass of the dark matter particle (chi)
    Returns:

    """

    new_param_card = ""
    with open(PATH + "BdNMC/parameter_fermion_test_pi0.dat", "r") as f:
        for line in f:
            if "#" in line:
                # skip comments but include them in the new file
                # (there may be the word "run" in comments?)
                new_param_card += line
            elif "samplesize" in line[0:15]: 
                new_line = "samplesize " + str(NUM_DARK_SCALARS) + "\n"
                new_param_card += new_line
            elif "dark_matter_mass" in line[0:16]:
                new_line = "dark_matter_mass " + dm_mass + "\n"
                new_param_card += new_line
            elif "dark_photon_mass" in line[0:20]:
                new_line = "dark_photon_mass " + str(ma) + "\n"
                new_param_card += new_line
            elif "root_file" == line[0:9]:
                new_line = "root_file " + f"{os.getcwd()}/data/root/BdNMC/{chi_type}/pi0_{chi_type}_ma_{ma}_dt_{dt_ratio}.root\n"
                new_param_card += new_line
            elif "decay_type" in line[0:12]:
                new_line = "decay_type " + chi_type + "\n"
                new_param_card += new_line
            else:
                new_param_card += line
    
    # write the new_parameter_card to a .dat file
    param_card_id = os.getcwd()+f"/parameter_cards/parameter_pi0_{chi_type}_ma_{ma}_dt_{dt_ratio}.dat"
    with open(param_card_id, "w") as f:
        f.write(new_param_card)
    
    return param_card_id



def run_shell_script(chi_type, ma, dt_ratio):
    process = subprocess.Popen([PATH+"/BdNMC/bin/BDNMC", f"/parameter_cards/parameter_pi0_{chi_type}_ma_{ma}_dt_{dt_ratio}.dat"])
    output, error = process.communicate()

    if error:
        print(f"Error: {error}")
    else:
        print(output)



def main(dt_ratio, num_files, chi_type="scalar"):

    # test the paths
    if test_path():
        print("Found path to DarkTridentGen ...")
    else:
        print(f"Path {PATH} does not exist! Exiting ...")
        return -1
    
    # generate the mass points
    mass_points = gen_mass_points(dt_ratio, num_files)
    print(f"Generated mass points: {mass_points}")

    for ma in mass_points:
        # figure out the dark chi mass
        # dt_ratio = m_chi / m_A'
        # m_chi = dt_ratio * m_A'

        if dt_ratio == "0.33": # cannot get 1/3 exactly obviously
            dm_mass = str(float(ma) / 3.0)
        else:
            # dt_ratio = 2.0 or 0.6
            dm_mass = str(float(ma) / float(dt_ratio))

        # generate the parameter card
        param_card_id = generate_paramater_card(dt_ratio, ma, chi_type, dm_mass)
        print(f"Generated parameter card: {param_card_id}")

        # run the DarkTridentGen
        run_shell_script(chi_type, ma, dt_ratio)
        

    


if __name__ == "__main__":
    print("Warning: Usage: python3 generate_data.py dt_ratio num_files chi_type")
    #main(sys.argv[1], sys.argv[2], sys.argv[3])
    main("0.33", 15, "scalar") # move to kwargs?
