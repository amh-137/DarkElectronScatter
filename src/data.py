import uproot3 as up3
import pandas as pd


def load_root_file(fname: str, path: str, vars: list, chunk_size=10_000, structure="vertex_tree") -> pd.DataFrame:
    """Performant loading of a root file into a pandas dataframe. Loads by chunks of size chunk_size.
    Args:
        fname (str): filename
        path (str): path to file
        vars (list): variables you want as columns in the dataframe
        chunk_size (int, optional): Size of chunks that are loaded at a time. Defaults to 10_000.
        structure (str, optional): is root data under ["vertex_tree"] or ["singlephotonana"]["vertex_tree"]. Defaults to "vertex_tree".

    Returns:
        pd.DataFrame: Cleaned data with selection cuts applied.
    """

    if structure == "vertex_tree":
        root_data = up3.open(path+fname)["vertex_tree"]
    elif structure == "singlephotonana":
        root_data = up3.open(path+fname)["singlephotonana"]["vertex_tree"]
    else:
        root_data = up3.open(path+fname)

    df = pd.DataFrame(columns=vars)

    for data in root_data.iterate(vars, entrysteps=chunk_size, flatten=False):
        # dict -> df
        df_temp = pd.DataFrame(data)

        # make the columns strings
        df_temp.columns = df_temp.columns.map(lambda x: x.decode('utf-8'))
        df_temp = df_temp[vars]

        # append cleaned data to our df
        df = pd.concat((df, df_temp))
    return df.infer_objects()
