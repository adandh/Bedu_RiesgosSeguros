

def primerP0(x):
    """
    Función que devuelve una matriz cuyas columnas contienen los primeros valores distintos de NaN
    que se encuentran (por columna) en una matriz x
    """

    n,m = x.shape
    nom_col = list(x.columns.values)
    for i in range(m):
        x[nom_col[i]] = [x.iloc[:,i].dropna()[0].item()]*n

    return x
