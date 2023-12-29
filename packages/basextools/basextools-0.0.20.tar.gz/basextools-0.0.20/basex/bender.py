### Bender - Biblioteca de ENcapsulamento de Dados e Extrações Recorrentes
### A data bender, the unknown element
### BASEX module for ELT and data prep

# Imports
import pandas as pd
import re

# Lista de todas as funções implementadas que podem ser
# importadas  com "from bender import *"
_all = ['', '', '']


def preprocess_grouping(df: pd.DataFrame, grouping: dict):
    """
    *Created by ChatGPT on 01/09/2023.
    Groups data into new categories, creating new columns in the received
    DataFrame according to the info in the dict.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to be preprocessed.
    groupings : dict
        3 level dict containing the original columns to be considered,
        and the new values - original values mapping.

    Returns
    -------
    pd.DataFrame
        Received DataFrame with the new categorical columns

    Notes
    -----
    Dict example:
    {
    column_a:
        {new_column_name:
            {new_value_1:
                [old_value_1, old_value_2],
            new_value_2:
                [old_value_3, old_value_4]}
        },
    column_b:
        {new_column_name:
            {new_value_1:
                [old_value_1, old_value_2],
            new_value_2:
                [old_value_3, old_value_4]}
        }
    ...
    }
    """
    # Create a copy of the original DataFrame to avoid modifying it directly
    df_copy = df.copy()

    # Loop through the grouping dictionary
    for column, new_columns in grouping.items():
        for new_column_name, mapping in new_columns.items():
            # Create a new column and initialize it with the original values
            try:
                df_copy[new_column_name] = df_copy[column]
                for new_value, old_values in mapping.items():
                    # Update the new column based on the mapping
                    df_copy[new_column_name] = df_copy[new_column_name].replace(old_values, new_value)
            except:
                pass

    return df_copy


def clean_column(df: pd.DataFrame, column_to_clean: str, keep_values: list, replacement_value: str) -> pd.DataFrame:
    """
    *Created by ChatGPT on 01/09/2023.
    Clean a specific column in a DataFrame by keeping specified values and replacing others.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data.
    column_to_clean : str
        Name of the column to be cleaned.
    keep_values : list
        List of values to be kept in the specified column.
    replacement_value : str
        Value to replace any other value in the column.

    Returns
    -------
    pd.DataFrame
        DataFrame with the specified column cleaned.

    Examples
    --------
    >>> data = {'A': ['apple', 'banana', 'cherry', 'date', 'fig']}
    >>> df = pd.DataFrame(data)
    >>> df_cleaned = clean_column(df, 'A', ['apple', 'banana', 'cherry'], 'other')
    >>> print(df_cleaned)
          A
    0   apple
    1  banana
    2  cherry
    3   other
    4   other
    """
    # Create a copy of the DataFrame to avoid modifying it directly
    df_copy = df.copy()

    # Use the `replace` method to clean the specified column
    df_copy[column_to_clean] = df_copy[column_to_clean].apply(lambda x: x if x in keep_values else replacement_value)

    return df_copy

def rename_columns(column_name, name_dict):
    for pattern, replacement in name_dict.items():
        column_name = re.sub(pattern, replacement, column_name)
    return column_name

def get_column_types(sheets, verbose=False):
    '''
    Create a series that maps each column of the answer base to its type
    Possible types are: 'nps', 'favorability', 'dissertative', 'alternative',
    'filter' and 'comment'

    Parameters
    ----------
    sheets : dict of DataFrames
    verbose : bool, default True
        If `True`, print columns' type

    Returns
    -------
    ps.Series
        Dict that maps each column name into its type
    '''

    cols_type = {}

    # some columns don't have a type
    cols_type['id'] = None
    cols_type['user_id'] = None
    cols_type['Data da Resposta'] = None
    cols_type['Horário da Resposta'] = None

    df = sheets['Exportação']
    df = df[[col for col in df.columns if not col.startswith('Filtro -')]]

    # filters
    for col in df.columns:
        if col.startswith('Filtro - '):
            cols_type[col] = 'filter'

    # nps columns
    if 'NPS' in sheets:
        for col in sheets['NPS']['Variável'].values:
            cols_type[col] = 'nps'
            cols_type['[Aberta] ' + col] = 'dissertative'  # error prone way

    # fav columns
    for col in sheets['Favorabilidade']['Variável'].values:
        if (col != 'Questões sem dimensão') & (col != 'Favorabilidade Média'):  # these are never fav questions
            cols_type[col] = 'favorability'
            cols_type[
                'Comentários - ' + col] = 'comment'  # the question may not have comments (this will be handled below)

    # alternative columns
    if 'Alternativas' in sheets:
        for col in sheets['Alternativas'][sheets['Alternativas']['Respostas'].isna()]['Variável/Alternativas'].values:
            cols_type[col] = 'alternative'

    # any untagged column is tagged as dissertative
    untagged_cols = set(df.columns) - set(cols_type.keys())
    for col in untagged_cols:
        cols_type[col] = 'dissertative'

    # search for tagged columns that do not exist in the base (they will be removed)
    devoid_cols = set(cols_type.keys()) - set(df.columns)
    warnings.warn("Algumas colunas não foram encontradas na base:\n" + '\n'.join(devoid_cols))
    [cols_type.pop(col) for col in devoid_cols]

    if verbose:
        print(json.dumps(cols_type, indent=4, sort_keys=True, ensure_ascii=False))

    return pd.Series(cols_type)