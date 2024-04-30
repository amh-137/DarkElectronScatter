import numpy as np

def rotate_to_microboone(v : np.array) -> np.array:
    det_rot = np.array([[0.92103853804025682, 0.0000462540012621546684, -0.38947144863934974],
                        [0.0227135048039241207, 0.99829162468141475, 0.0538324139386641073],
                        [0.38880857519374290, -0.0584279894529063024, 0.91946400794392302]])
    # rotation
    #print(det_rot @ det_rot.T)
    v = np.dot(det_rot, v)
    return v

def translate_to_microboone(v : np.array):
    det_centre = np.array([55.02, 72.59,  672.70])
    return v + det_centre

def add_cos_theta_signal(df):
    px, py, pz = df["electron_px"], df["electron_py"], df["electron_pz"]
    px, py, pz = rotate_to_microboone(np.array([px, py, pz]))
    # get the direction vector
    v = np.array([px, py, pz])
    # normalize
    v = v / np.linalg.norm(v, axis=0)

    v_numi=np.array([0.462372, 0.0488541, 0.885339])
    v_shwr = np.array([v[0], v[1], v[2]])
    df["cos_theta_numi"] = np.dot(v_shwr.T, v_numi)
    return df