import uproot3 as up3
import pandas as pd
import numpy as np


def identity_func(df: pd.DataFrame) -> pd.DataFrame:
    """Identity function. Returns the dataframe as is.
    Args:
        df (pd.DataFrame): Input dataframe

    Returns:
        pd.DataFrame: Output dataframe
    """
    return df

def load_root_file(fname: str, path: str, vars: list, cut_function=identity_func, chunk_size=10_000, structure="vertex_tree") -> pd.DataFrame:
    """Performant loading of a root file into a pandas dataframe. Loads by chunks of size chunk_size.
    Args:
        fname (str): filename
        path (str): path to file
        vars (list): variables you want as columns in the dataframe
        chunk_size (int, optional): Size of chunks that are loaded at a time. Defaults to 10_000.
        cut_function (function, optional): Function that takes a dataframe and applies cuts. Must return a dataframe. Defaults to identity_func that does nothing.
        structure (str, optional): is root data under ["vertex_tree"] or ["singlephotonana"]["vertex_tree"]. Defaults to "vertex_tree". Also allows ["vertex_tree;x"] if specified.

    Returns:
        pd.DataFrame: Cleaned data with selection cuts applied.
    """

    if structure == "vertex_tree":
        root_data = up3.open(path+fname)["vertex_tree"]
    elif structure == "singlephotonana":
        root_data = up3.open(path+fname)["singlephotonana"]["vertex_tree"]
    else:
        root_data = up3.open(path+fname)[structure]

    df = pd.DataFrame(columns=vars)

    for data in root_data.iterate(vars, entrysteps=chunk_size, flatten=False):
        # dict -> df
        df_temp = pd.DataFrame(data)

        # make the columns strings
        df_temp.columns = df_temp.columns.map(lambda x: x.decode('utf-8'))
        df_temp = df_temp[vars]

        # make cuts
        df_temp = cut_function(df_temp)
        df_temp = clean_data(df_temp)
        df_temp = add_cos_theta_col(df_temp)

        # append cleaned data to our df
        df = pd.concat((df, df_temp))
    return df.infer_objects()


def add_cos_theta_col(df, v_numi=np.array([0.462372, 0.0488541, 0.885339])):
    """Add a column with cos(theta) of the shower with respect to the neutrino beam direction

    Args:
        df (pandas.dataframe): df
        v_numi (np.array, len=3, optional): The vector from numi target to uboone detector. Defaults to np.array([0.462372, 0.0488541, 0.885339]).

    Returns:
        pandas.dataframe: return df with new column
    """
    v_shwr = np.array(
        [df.reco_shower_dirx, df.reco_shower_diry, df.reco_shower_dirz])

    df["cos_theta_numi"] = np.dot(v_shwr.T, v_numi)
    return df



def clean_data(df):
    """Sum Energy of showers, take max of other variables

    Args:
        df (pandas.dataframe): the df you want to clean

    Returns:
        pandas.dataframe: cleaned df
    """

    df["reco_shower_energy_max"] = df["reco_shower_energy_max"].apply(lambda x: [
                                                                      sum(x)])
    df = df.map(lambda x: x[0] if (isinstance(
        x, np.ndarray) or isinstance(x, list)) else x)
    return df