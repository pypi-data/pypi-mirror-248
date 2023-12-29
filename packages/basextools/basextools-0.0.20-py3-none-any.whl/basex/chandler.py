### Chandler - Creation of Heatmaps AND Large Extensions of Rows
### A tribute to Matthew Perry, interpreter of Chandler Bing
### BASEX module for heatmaps and tables creation


# Imports
import pandas as pd
import numpy as np
import warnings

from . import ada
from . import bender

# Lista de todas as funções implementadas que podem ser
# importadas  com "from tables import *"
_all = ['', '', '']


def hierarchical_heatmap(df: pd.DataFrame, column_indexes: list, target_variables: list,
                         variables_type: str, min_conf: int = 5, min_conf_value=np.nan,
                         add_heatmap: bool = False, decimal_places: int = 1, **kwargs):
    """
    Descrição da função, contendo objetivo, explicações de condicionais,
    corner cases e o que mais for relevante para que o usuário saiba como
    ulitizar a função.

    Parameters
    ----------
    df : tipo_do_parametro
        Explicação do parâmetro
    df : tipo_do_parametro
        Explicação do parâmetro
    mode : str, default = 'valor_especifico'


    Returns
    -------
    tipo_do_retorno
        Explicação do retorno

    Raises
    ------
    Erros levantados, se houver

    Notes (opcional)
    -----
    Outras informações que possam ser relevantes, opcional.

    Examples
    --------
    >>> nome_da_função(par1)
    retorno
    >>> nome_da_função(par1, par2)
    retorno
    """

    # Defines max_value
    if variables_type == 'nps':
        max_value = 10
    elif variables_type == 'favorability':
        max_value = 5

    # Take columns of interest from the original df
    heat = df[target_variables + column_indexes].copy()
    heat = heat.replace('-', np.nan)

    # Adds count for further filter
    final = heat.groupby(column_indexes)[target_variables[0]].count() \
        .reset_index().rename(columns={target_variables[0]: 'values'})
    final[f'level_{str(len(column_indexes))}'] = 'count'

    # Adds total metric, either nps or favorability
    if kwargs.get('total'):
        metric = heat.groupby(column_indexes)[target_variables] \
            .apply(lambda x: ada.favorability_nps_calculation_df(x, max_value)) \
            .reset_index().rename(columns={target_variables[0]: 'values'})
        metric[f'level_{str(len(column_indexes))}'] = 'total'
        final = pd.concat([final, metric]).round(decimal_places)

    # Adds percentages of promoters, neutrals and detractors
    if kwargs.get('percentages'):
        perc = heat.groupby(column_indexes)[target_variables] \
            .apply(lambda x: ada.favorability_nps_percentages_df(x, max_value)) \
            .rename(columns={0: 'values'}).reset_index()
        final = pd.concat([final, perc])

    # Adds conversion
    if kwargs.get('conversion'):
        conv = (heat.groupby(column_indexes)[target_variables[0]].count() * 100 / len(heat)) \
            .reset_index().rename(columns={target_variables[0]: 'values'}).round(decimal_places)

        conv[f'level_{str(len(column_indexes))}'] = 'conversion'
        final = pd.concat([final, conv]).round(decimal_places)

        # Transform df format into pivot table
    final = final.pivot_table(index=column_indexes, values='values',
                              columns=f'level_{str(len(column_indexes))}',
                              aggfunc='first').reset_index().round(decimal_places)

    # Parse dicts
    if kwargs.get('percentages'):
        for i in target_variables:
            data = pd.json_normalize(final[i])
            if len(target_variables) > 1:
                data.columns = [f"{i} - {col}" for col in data.columns]
            final = pd.concat([final, data], axis=1)
        final = final[final.columns.drop(target_variables).tolist()]

    # Hide values if the group does not meet the confidentiality minimum
    keep = column_indexes + ['count', 'conversion']
    final.loc[final['count'] < min_conf, [c for c in final.columns if c not in keep]] = min_conf_value

    # Keep or drop count column
    if not kwargs.get('count'):
        final.drop('count', axis=1, inplace=True)

    # Send conversion to bottom
    if kwargs.get('conversion'):
        final = final[[c for c in final.columns if c != 'conversion'] + ['conversion']]

    # Rename columns
    if variables_type == 'favorability':
        name_dict = {'perc_favorable': 'Favoráveis',
                     'perc_neutral': 'Neutros',
                     'perc_non_favorable': 'Não favoráveis'}
    else:
        name_dict = {'perc_favorable': 'Promotores',
                     'perc_neutral': 'Neutros',
                     'perc_non_favorable': 'Detratores'}
    name_dict.update({'count': 'Respostas'})
    name_dict.update({'total': 'Total'})
    name_dict.update({'conversion': 'Representatividade'})

    final = final.rename(columns=lambda x: bender.rename_columns(x, name_dict))
    original_columns = final.columns

    # Round values and transpose df
    pivo = final.pivot_table(index=column_indexes, aggfunc='first', dropna=False)
    pivo = pivo.reindex(columns=[c for c in original_columns if c not in pivo.index.names])
    pivo = pivo.round(decimal_places).transpose()

    return pivo


def heatmap_comparison(df, index_col, comparison_col, var_cols, max_value,
                       global_name='global', diff=True, significance=False):
    '''
    Cria um heatmap comparativo de favorabilidades ou nps a partir de colunas categóricas,
    indicando a diferença entre duas categorias e se a diferença é estatisticamente significativa.
    Parameters
    ----------
    df : Pandas Dataframe
        The dataframe containing the data.
    index_col : string
        Categorical column to be set as index.
    comparison_col : string
        Categorical column for the comparison, lower level of columns index.
    var_cols : array like
        Numerical columns for favorability/eNPS calculation, higher level of columns index.
    max_value : int, default = 10
        The maximum possible value in values.
    global_name : string, default = 'global'
        Label for the global results
    diff : bool, default = True
        If True, adds a difference column in the lower index column level for all the var_cols.
        Only works if the comparison_col contains only two distinct values.
    significance : bool, default = False
        If True, marks the statistically significant differences with a *. Only works if diff
        is also True.
    Returns
    -------
    pivo : Pandas DataFrame
        The generated heatmap.
    '''
    # Gera os dados do heatmap
    print('Generating heatmap comparison..')
    data = df[[index_col, comparison_col] + var_cols].copy()
    data[var_cols] = data[var_cols].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    data[[index_col, comparison_col]] = data[[index_col, comparison_col]].apply(lambda x: str(x))
    heat_geral = data.groupby(comparison_col)[var_cols] \
        .apply(lambda x: ada.favorability_nps_calculation_df(x, max_value=max_value))
    heat = data.groupby([index_col, comparison_col])[var_cols] \
        .apply(lambda x: ada.favorability_nps_calculation_df(x, max_value=max_value))
    # Junta os dados e formata o heatmap
    old_idx = heat_geral.index.to_frame()
    old_idx.insert(0, index_col, global_name)
    heat_geral.index = pd.MultiIndex.from_frame(old_idx)
    heat = pd.concat([heat, heat_geral])
    heat = heat.reset_index().round(1)
    pivo = heat.pivot_table(index=index_col, columns=[comparison_col])
    # Coloca linha de global no início
    idx = [global_name] + [i for i in pivo.index if i != global_name]
    pivo = pivo.reindex(idx)

    # Acrescenta coluna de diferença entre os valores de comparison_col
    if diff:
        try:
            assert (len(df[comparison_col].unique()) == 2)
            for n in reversed(var_cols):
                pivo[(n, 'diferença')] = pivo[n].diff(axis=1).iloc[:, -1]
            pivo = pivo.reindex(sorted(pivo.columns), axis=1)
        except AssertionError:
            warnings.warn(f'Só é possível calcular a diferença para 2 valores de comparação,\
                          {str(len(df[comparison_col].unique()))} foram passados')

    # Acrescenta um * como marcador de diferenças estatisticamente significantes
    # TODO generalizar o teste, atualmente é feito pelo intervalo de confiança
    # do eNPS, e só serve para comparações temporais.
    if significance:
        try:
            assert (diff == True)
            # Calcula e formata o heatmap de erro
            erro = data.groupby([index_col, comparison_col])[var_cols] \
                .apply(lambda x: ada.enps_confidence_interval_error_df(x, max_value=max_value))
            erro_geral = data.groupby(comparison_col)[var_cols] \
                .apply(lambda x: ada.enps_confidence_interval_error_df(x, max_value=max_value))
            erro_geral.index = pd.MultiIndex.from_frame(old_idx)
            erro = pd.concat([erro, erro_geral])
            pivo_erro = erro.pivot_table(index=index_col, columns=[comparison_col])
            # Coloca linha de global no início
            idx_erro = [global_name] + [i for i in pivo_erro.index if i != global_name]
            pivo_erro = pivo_erro.reindex(idx)
            # Marca o heatmap original
            for n in reversed(var_cols):
                sig = pivo[abs(pivo[(n, 'diferença')]) >= (pivo_erro[(n, pivo_erro.columns[0][1])])].index
                pivo[(n, 'diferença')].loc[sig] = pivo[(n, 'diferença')].loc[sig].apply(
                    lambda x: str(round(x, 1)) + '*')
        except AssertionError:
            warnings.warn(f'Só é possível calcular as diferenças significativas\
                            quando há diferenças calculadas')

    return pivo


def build_heatmaps(df, questions_type, comparison_types=[]):
    """
    Build the favorability and nps tables from the answer base
    for each comparison type inside `comparison_types`
    If `comparison_types` is empty, it'll do it for all comparison types (`filters` inside `question_type`)

    Parameters
    ----------
    df : pd.DataFrame
        The answer base
    questions_type : Dict
        Maps each question to its type
    comparison_types : list
        The subset of comparison types to build the heatmap
    save : bool, default False
        If `True`, save the resulting tables as .csv files and the corresponding heatmap .png image
    plot : bool, default False
        If `True`, plot the heatmap

    Returns
    -------
    heatmaps : Dict
        dict with both nps and favorability tables for each comparison type
    """

    # get filter names if not given
    if not comparison_types:
        comparison_types = [question for question, q_type in questions_type.items() if q_type == 'filter']

    # separate the questions by type
    fav_questions = [question for question, q_type in questions_type.items() if q_type == 'favorability']
    enps_questions = [question for question, q_type in questions_type.items() if q_type == 'nps']

    heatmaps = {}
    # build each heatmap individually
    for comparison_type in comparison_types:

        heatmaps[comparison_type] = {}

        fav_heatmap = build_heatmap(df, comparison_type, fav_questions, max_value=5)

        heatmaps[comparison_type]['fav'] = fav_heatmap

        if enps_questions:
            enps_heatmap = build_heatmap(df, comparison_type, enps_questions, max_value=10)
            heatmaps[comparison_type]['enps'] = enps_heatmap

    return heatmaps


def build_heatmap(df, comparison_type, questions, max_value, min_answers, agg=True):
    '''
    Build a DataFrame with favorability or nps scores as it appears on the platform

    Parameters
    ----------
    df : pd.DataFrame
        The answer base
    comparison_type : String
        The selected comparison type
    questions : list
        The set of favorability or NPS questions
    max_value : int
        The maximum value in the chosen Likert Scale (5 or 7
        indicate favorability questions and 10 indicate NPS questions)
    agg : bool, default True
        If True, includes the aggregated row and the aggregated column in the table

    Returns
    -------
    pd.DataFrame
        The resulting table
    '''

    agg_col_name = 'Total da Pesquisa'
    agg_row_name = 'FAVORABILIDADE MÉDIA'

    # apply a standard preprocessing step
    df_hm = df[questions + [comparison_type]]

    # evaluate the totals before dropping comparison_type's non respondents
    if agg:
        df_aux = df_hm.set_index(comparison_type).replace('-', np.nan).apply(pd.to_numeric)
        df_total = df_aux.apply(lambda x: ada.favorability_nps_calculation(x.dropna(), max_value=max_value))

    df_hm = df_hm.replace('-', np.nan).dropna(subset=[comparison_type], axis=0)
    df_hm = df_hm.set_index(comparison_type)
    df_hm = df_hm.apply(pd.to_numeric)
    if df_hm.groupby(comparison_type).count().empty:
        return pd.DataFrame({})

    if min_answers > 0:
        df_counts = df_hm.groupby(comparison_type).count()
        df_hm = df_hm.groupby(comparison_type).apply(
            lambda x: ada.favorability_nps_calculation_df(x, max_value=max_value))
        df_hm = df_hm[df_counts >= min_answers]
    else:
        df_hm = df_hm.groupby(comparison_type).apply(
            lambda x: ada.favorability_nps_calculation_df(x, max_value=max_value))

    df_hm = df_hm.T

    if agg:
        df_hm[agg_col_name] = df_total
        # put the aggregated column in the first position
        df_hm = df_hm[[agg_col_name] + list(df_hm.columns[:-1])]
        if max_value < 10:  # fav heatmap
            # put the aggregated row in the first position
            df_hm.loc[agg_row_name] = df_hm.mean(axis=0)
            df_hm = df_hm.reindex(np.roll(df_hm.index, shift=1))

    return df_hm