# fermion_cross_section.py
# test the differential cross section equation that we derived is correct.
# Alex Hergenhan 2024

import numpy as np

EPSILON = 1e-3
ALPHA_EM = 1./137.
ALPHA_D = 0.06
mA = 0.05
mx = 0.6*mA
me = 511e-3

# minkwski metric
g = np.diag([1., -1., -1., -1.])

# test
#print((Ek1*Ek2)-(kx1*kx2)-(ky1*ky2)-(kz1*kz2))
#print(k1@g@k2)

def Asq_fermion(p1, p2, k1, k2):
    t = (k1 - p1) @ g @ (k1 - p1)
    prefactor = (128. * np.pi**2 * EPSILON**2 * ALPHA_D * ALPHA_EM) / (t-mA**2)**2
    A = ((k1@g@k2)*(p1@g@p2) + (k2@g@p1)*(p2@g@k1) - mx**2 * (k2@g@p2) - me**2 * (p1@g@k1) + 2.*mx**2 * me**2)
    return A * prefactor

def p_star_sq(s):
    numerator = (s - me**2 - mx**2)**2 - 4.*me**2 * mx**2
    denominator = 4. * s
    return numerator / denominator

def dsigma_fermion(p1, p2, k1, k2):
    s = mx**2 + me**2 + 2.*me*p1[0] # p1[0] is Ep1
    pstarsq = p_star_sq(s)

    num = me * Asq_fermion(p1, p2, k1, k2)
    den = 32. * np.pi * s * pstarsq

    return num / den


def dsigma_fermion2(Ep1, Ek2):
    prefactor = 4. * np.pi * EPSILON**2 * ALPHA_D * ALPHA_EM
    num = ( (Ep1**2 *me) + Ep1*(Ep1*me + 2*me*(-Ek2 + me)) + (Ek2 - me)*((Ek2 - 2*me)*me - mx**2))
    den = ((mA**2 + 2*(Ek2 - me)*me)**2 * (Ep1 - mx)*(Ep1 + mx))

    return prefactor * (num / den)


def gen_three_floats():
    random_floats = np.random.random(3)
    sum_of_floats = np.sum(random_floats)
    normalized_floats = random_floats / sum_of_floats
    return normalized_floats

def main():
    for i in range(1000):

        # Use conservation of energy to get Es
        Ep1 = np.random.uniform(low=0.5, high=40, size=(1,))[0]
        # Ep1 + me = Ek1 + Ek2
        Ek2 = np.random.uniform(low=0.4, high=Ep1, size=(1,))[0]
        Ek1 = Ep1 + me - Ek2


        # E^2 - m^2 = p^2
        mag_p1_sq = Ep1**2 - mx**2 # magnitude of the momentum from E1 squared
        mag_p2_sq = Ek1**2 - me**2
        mag_k2_sq = Ek2**2 - me**2

        # okay so now need 3 random numbers that sum up to 1
        px1, py1, pz1 = np.sqrt(np.array([mag_p1_sq, mag_p1_sq, mag_p1_sq]) * gen_three_floats())
        kx1, ky1, kz1 = np.sqrt(np.array([mag_p2_sq, mag_p2_sq, mag_p2_sq]) * gen_three_floats())
        kx2, ky2 ,kz2 = np.sqrt(np.array([mag_k2_sq, mag_k2_sq, mag_k2_sq]) * gen_three_floats())

        # setup 4-vectors
        p1 = np.array([Ep1, px1, py1, pz1])
        p2 = np.array([511e-3, 0, 0, 0])
        k1 = np.array([Ek1, kx1, ky1, kz1])
        k2 = np.array([Ek2, kx2, ky2, kz2])
        print(dsigma_fermion(p1, p2, k1, k2), dsigma_fermion2(Ep1, Ek2))

        if np.abs(dsigma_fermion(p1, p2, k1, k2) - dsigma_fermion2(Ep1, Ek2)) > 1e-6:
            print("Error! ", i)
            print(dsigma_fermion(p1, p2, k1, k2))
            print(dsigma_fermion2(Ep1, Ek2))
            return -1



    return 0

if __name__ == "__main__":
    main()