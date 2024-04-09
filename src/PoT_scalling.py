
def pot(POT_g4numi : float, ntrials : float, Nm : float, BR : float, omega_int : list) -> float:
    return (POT_g4numi * ntrials) / (Nm * BR * max(omega_int))