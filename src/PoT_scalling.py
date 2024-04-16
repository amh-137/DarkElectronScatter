
def calculate_pot(POT_g4numi : float, ntrials : float, Nm : float, BR : float, omega_int : list) -> float:
    """
    Calculate the POT
    Args:
        POT_g4numi (float): pot of g4numi
        ntrials (float): number of trials
        Nm (float): i dont know
        BR (float): branching ratio
        omega_int (list): ??

    Returns:
        float: POT
    """
    return (POT_g4numi * ntrials) / (Nm * BR * max(omega_int))


def pot_scale(number_of_events : float, PoT : float, pot_run1_microboone : float) -> float:
    """PoT scale the number of electrons scattered

    Args:
        number_of_events (float): number of electron events
        PoT (float): PoT to generate this many electrons
        pot_g4numi (float): PoT of the numi run 1

    Returns:
        float: pot scaled number of events
    """
    return number_of_events * (pot_run1_microboone / PoT)