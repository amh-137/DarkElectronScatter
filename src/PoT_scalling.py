
def pot(POT_g4numi : float, ntrials : float, Nm : float, BR : float, omega_int : list) -> float:
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
