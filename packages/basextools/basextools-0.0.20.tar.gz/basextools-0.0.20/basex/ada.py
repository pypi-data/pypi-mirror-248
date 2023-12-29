### ADA - Algorithms for Data Arithmetics
### A tribute to Ada Lovelace, the first programmer
### BASEX module for basic calculations in EX context


# Imports
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import median_abs_deviation
from datetime import date


# Lista de todas as funções implementadas que podem ser
# importadas  com "from ada import *"
_all = ['', '', '']


def favorability_nps_calculation(values, max_value=5):
    """
    Calculate the favorability or NPS of an array of scores
    according to the maximum value in `max_value`.
    If ``max_value = 5`` or 7, it'll treat `values` as favorability values;
    if ``max_value = 10``, it'll treat `values` as nPS values.
    Return NaN for an empty array

    Parameters
    ----------
    values : array-like (np.array or pd.Series)
        The numerical array os scores
    max_value : int (5, 7 or 10)
        The maximum value in the chosen Likert scale
        (5 or 7 for favorability arrays and 10 for NPS arrays)

    Returns
    -------
    Float
        Favorability or NPS score
    """

    n_answers = values.size
    if n_answers == 0:
        return np.nan

    assert (max_value == 5 or max_value == 7 or max_value == 10)

    if max_value == 5:
        assert (max(values) <= 5)
        favorable_values = values[values >= 4]
        perc_favorability = 100 * len(favorable_values) / n_answers
    elif max_value == 7:
        assert (max(values) <= 7)
        favorable_values = values[values >= 6]
        perc_favorability = 100 * len(favorable_values) / n_answers
    elif max_value == 10:  # NPS
        favorable_values = len(values[values >= 9]) - len(values[values <= 6])
        perc_favorability = 100 * favorable_values / n_answers

    return perc_favorability


def favorability_nps_calculation_df(df_values, max_value=5):
    """
    Calculate the favorability or the NPS for all columns
    of a DataFrame. Favorability and NPS variables are discriminated
    according to the maximum value in `max_value`.
    All columns must have only favorability questions or only NPS questions, not both.

    Parameters
    ----------
    df_values : pd.DataFrame
        DataFrame with all numeric columns
    max_value : int (5, 7 or 10)
        The maximum value in the chosen Likert scale
        (5 or 7 for favorability arrays and 10 for NPS arrays)

    Returns
    -------
    pd.Series
        Favorability or NPS score for each column of `df_values`
    """

    df_favorabilities = df_values.apply(lambda x: favorability_nps_calculation(x.dropna(), max_value=max_value), axis=0)

    return df_favorabilities


def favorability_nps_percentages(values, max_value=5):
    """
    Calculate the percentage of promoters (or favorables),
    neutrals and detractors (or non favorables) of an array of scores
    according to the maximum value in `max_value`.
    If ``max_value = 5`` or 7, it'll treat `values` as favorability values;
    if ``max_value = 10``, it'll treat `values` as nPS values.
    Return NaN for an empty array

    Parameters
    ----------
    values : array-like (np.array or pd.Series)
        The numerical array os scores
    max_value : int (5, 7 or 10)
        The maximum value in the chosen Likert scale
        (5 or 7 for favorability arrays and 10 for NPS arrays)

    Returns
    -------
    Dict
        Percentages of promoters (or favorables),
        neutrals and detractors (or non favorables)
    """

    n_answers = values.size
    if n_answers == 0:
        return np.nan

    assert (max_value == 5 or max_value == 7 or max_value == 10)

    if max_value == 5:
        assert (max(values) <= 5)
        favorable_values = values[values >= 4]
        neutral_values = values[values == 3]
        non_favorable_values = values[values <= 2]
        perc_favorable = 100 * len(favorable_values) / n_answers
        perc_neutral = 100 * len(neutral_values) / n_answers
        perc_non_favorable = 100 * len(non_favorable_values) / n_answers
    elif max_value == 7:
        favorable_values = values[values >= 6]
        neutral_values = values[values == 5]
        non_favorable_values = values[values <= 4]
        perc_favorable = 100 * len(favorable_values) / n_answers
        perc_neutral = 100 * len(neutral_values) / n_answers
        perc_non_favorable = 100 * len(non_favorable_values) / n_answers
    elif max_value == 10:  # NPS
        favorable_values = values[values >= 9]
        neutral_values = values[(values == 8) | (values == 7)]
        non_favorable_values = values[values <= 6]
        perc_favorable = 100 * len(favorable_values) / n_answers
        perc_neutral = 100 * len(neutral_values) / n_answers
        perc_non_favorable = 100 * len(non_favorable_values) / n_answers

    percentages = {'perc_favorable': perc_favorable,
                   'perc_neutral': perc_neutral,
                   'perc_non_favorable': perc_non_favorable}

    return percentages


def favorability_nps_percentages_df(df_values, max_value=5):
    """
    Calculate the percentage of promoters (or favorables),
    neutrals and detractors (or non favorables) for all columns
    of a DataFrame. Favorability and NPS variables are discriminated
    according to the maximum value in `max_value`.
    All columns must have only favorability questions or only NPS questions, not both.

    Parameters
    ----------
    df_values : pd.DataFrame
        DataFrame with all numeric columns
    max_value : int (5, 7 or 10)
        The maximum value in the chosen Likert scale
        (5 or 7 for favorability arrays and 10 for NPS arrays)

    Returns
    -------
    pd.Series
        Percentage of promoters (or favorables),
        neutrals and detractors (or non favorables)
        for each column of `df_values`
    """
    df_percentages = df_values.apply(lambda x: favorability_nps_percentages(x.dropna(), max_value=max_value))
    df_percentages = pd.DataFrame(df_percentages)

    return df_percentages


def enps_confidence_interval(values, c_level=.95, percent=True, max_value=10):
    '''
    Evalute the NPS confidence interval according to https://measuringu.com/nps-confidence-intervals/.
    Method: adjusted-wald (3,T).

    Parameters
    ----------
    values : array-like
        The eNPS values.
    c_level : float, default = 0.95
        The confidence level.
    percent : bool, default = True
        If True, returns the values multiplied by 100, already in eNPS typical scale.
    max_value : int, default = 10
        The maximum possible value in values.
    Returns
    -------
    l_bound : float
        The lower bound of the confidence level.
    u_bound : float
        The upper bound of the confidence level.
    enps : float
        The eNPS.
    moe : float
        The error of the confidence interval.
    '''
    if max_value == 10:
        det_upper = 6
        pro_lower = 9
    if max_value == 5:
        det_upper = 2
        pro_lower = 4

    # values = pd.Series(values)
    n = len(values)  # sample size
    n_detractors = values[values <= det_upper].count()
    n_promoters = values[values >= pro_lower].count()
    # n_passives = n_detractors = values[(values>6) & (values<9)].count()
    enps = (n_promoters - n_detractors) / n

    adj_n = n + 3
    adj_n_detractors = n_detractors + 3 / 4
    adj_n_promoters = n_promoters + 3 / 4

    adj_prop_promoters = adj_n_promoters / adj_n
    adj_prop_detractors = adj_n_detractors / adj_n
    adj_enps = adj_prop_promoters - adj_prop_detractors

    adj_var = adj_prop_promoters + adj_prop_detractors - (adj_prop_promoters - adj_prop_detractors) ** 2
    adj_se = np.sqrt(adj_var / adj_n)
    z_value = stats.norm.ppf(c_level)
    moe = z_value * adj_se

    l_bound = adj_enps - moe
    u_bound = adj_enps + moe

    if percent:
        l_bound *= 100
        u_bound *= 100
        enps *= 100
        moe *= 100

    return l_bound, u_bound, enps, moe

def enps_confidence_interval_error_df(df_values, c_level=.95, percent=True, max_value=10):
    '''
    Evalute the NPS confidence interval according to https://measuringu.com/nps-confidence-intervals/
    for all columns of a dataframe. Returns the calculated error for the confidence interval.
    Method: adjusted-wald (3,T).

    Parameters
    ----------
    df_values : Pandas DataFrame
        The dataframe containing the eNPS values.
    c_level : float, default = 0.95
        The confidence level.
    percent : bool, default = True
        If True, returns the values multiplied by 100, already in eNPS typical scale.
    max_value : int, default = 10
        The maximum possible value in values.
    Returns
    -------
    df_error : Pandas DataFrame
        The error dataframe.
    '''
    df_error = df_values.apply(lambda x: enps_confidence_interval(x,\
                                                                  c_level=c_level, percent=percent,
                                                                  max_value=max_value)[3], axis=0)

    return df_error


def enps_confidence_interval2(values, delta):
    n = len(values)  # sample size
    n_detractors = values[values <= 6].count()
    n_promoters = values[values >= 9].count()
    # n_passives = n_detractors = values[(values>6) & (values<9)].count()
    enps = (n_promoters - n_detractors) / n
    print(enps)
    adj_n = n + 3
    adj_n_detractors = n_detractors + 3 / 4
    adj_n_promoters = n_promoters + 3 / 4

    adj_prop_promoters = adj_n_promoters / adj_n
    adj_prop_detractors = adj_n_detractors / adj_n
    # adj_enps = adj_prop_promoters - adj_prop_detractors

    adj_var = adj_prop_promoters + adj_prop_detractors - (adj_prop_promoters - adj_prop_detractors) ** 2
    adj_se = np.sqrt(adj_var / adj_n)

    # l_bound = adj_enps - delta
    # u_bound = adj_enps + delta

    # code

    # stat.norm.cdf(1.64)
    z_value = delta / adj_se
    c_level = stats.norm.cdf(z_value)

    return c_level

def run_date(numbered_month=False):
    """
    Returns the current date in a specific format.

    Parameters
    ----------
        numbered_month (bool): if True, returns month as numeral

    Returns
    -------
        str: Current date in the specified format.
    """
    data_atual = date.today()
    ano = data_atual.year
    mes = data_atual.month
    meses = {1: 'Janeiro',
             2: 'Favereiro',
             3: 'Março',
             4: 'Abril',
             5: 'Maio',
             6: 'Junho',
             7: 'Julho',
             8: 'Agosto',
             9: 'Setembro',
             10: 'Outubro',
             11: 'Novembro',
             12: 'Dezembro'}

    if numbered_month:
        return f'{mes}/{ano}'

    return f'{meses[mes]}, {ano}'

def enps_groups(enps_series, perc=False):
    ''' UNIFICAR COM favorability_nps_percentages

    :param enps_series:
    :param perc:
    :return:
    '''
    enps_series = enps_series.dropna()
    n_answers = enps_series.size
    promoters = enps_series[enps_series >= 9].size
    neutrals = enps_series[(enps_series > 6) & (enps_series < 9)].size
    detractors = enps_series[enps_series <= 6].size

    enps = 100*(promoters - detractors) / n_answers

    if perc:
        promoters = 100 * promoters / n_answers
        neutrals = 100 * neutrals / n_answers
        detractors = 100 * detractors / n_answers

    return promoters, neutrals, detractors, enps

def get_reject_outliers(data, m=2.0, method='get', technique='standard'):
    """
    Get or reject the outliers from an array of data using median absolute deviation around the median.
    Source: Benjamin's answer from https://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list

    Parameters
    ----------
    data : np.array
        The sample data.
    m : float, default = 2.5
        How many deviations around the median to consider as threshold.
        The value of 2.5 is suggested by the following work
        https://www.sciencedirect.com/science/article/abs/pii/S0022103113000668
    method : String, default = 'get'
        if 'get', identified outliers will be returned.
        if 'reject', outliers are removed from 'data'.
        if 'mapping', each entry of 'data' is mapped to 1 (if it's a positive outlier),\
            -1 (neg. outlier) and 0 otherwise.
        if 'score', each entry is mapped to its score on numbers
            of absolute deviations around the median.
            'm' is irrelevant in this method. NaNs are mapped to NaNs.
    technique : String, default = 'standard'
        The MAD technique applied to data.
        If 'single', standard MAB is applied; ideal for normal or symmetric distributions.
        For skewed distributions use 'double', which will define different
        thresholds for right and left tails.

    Returns
    -------
    np.array:
        The filtered data. Returns an array NaNs if both mean and median are zero.
    """

    data_size = data.size
    nan_pos = list(np.where(np.isnan(data))[0])  # getting nans indices
    data = data[~np.isnan(data)]  # dropping nan for analysis
    if not list(data):
        return np.nan * np.ones(data_size)

    def compute_mad(data):
        '''
        Computes the median absolute deviation around the median of every element of an array.

        Parameters
        ----------
        data (numpy.ndarray): the data.

        Returns
        -------
        (numpy.ndarray): MAD values. Returns 0 if both mean and median are zero.
        '''

        d = np.abs(data - np.median(data))
        scale = 'normal'  # b = 1.4826; consistency constant suggested by Leys' if distribution is normal.
        # for general symmetric distributions, we should use the code below:
        # standarized_data = (data - np.mean(data))/(np.std(data))
        # scale = 1/np.percentile(standarized_data, 75))
        mdev = median_abs_deviation(data, scale=scale)
        # or explicitly:
        # mdev = b*np.median(d)
        # mad = d/mdev if mdev else 0

        if mdev:
            mad = d / mdev
        else:  # triggered if more than 50% of scores are the same
            # solution suggested by https://www.ibm.com/support/knowledgecenter/SSEP7J_11.1.0/com.ibm.swg.ba.cognos.ug_ca_dshb.doc/modified_z.html
            d = np.abs(data - np.median(data))
            mdev = 1.253314 * np.mean(d)  # a mean absolute deviaiton
            mad = d / mdev if mdev else 0
        return mad

        if technique == 'standard':
            mad = compute_mad(data)
            if type(mad) == int:
                return np.nan * np.ones(data_size)

        elif technique == 'double':  # for asymmetric distributions (the general case)
            left_data = data[data <= np.median(data)]
            right_data = data[data > np.median(data)]
            l_mad = compute_mad(left_data)
            r_mad = compute_mad(right_data)
            if (type(r_mad) == int) or (type(l_mad) == int):
                return np.nan * np.ones(data_size)
            else:
                mad = np.concatenate((l_mad, r_mad))

        s = mad
        if method == 'get':
            return data[s >= m]  # get outliers
        elif method == 'reject':
            return data[s < m]  # reject outliers
        elif method == 'mapping':
            result = ((s >= m) & (data > np.median(data))).astype(float) + -1 * (
                    (s >= m) & (data < np.median(data))).astype(float)
            for pos in nan_pos:  # putting nans back
                result = np.insert(result, pos, np.nan)
            return result
        elif method == 'score':
            result = (1 * (data >= np.median(data)) + -1 * (data <= np.median(data))) * s
            for pos in nan_pos:  # putting nans back
                result = np.insert(result, pos, np.nan)
            return result
        elif method == 'limits':
            return [np.median(data) - median_abs_deviation(data, scale="normal") * m,
                    np.median(data) + median_abs_deviation(data, scale="normal") * m]
        else:
            print('Error: no available method.')

    return None

def compare_two_favs(p1_fav, p1_n, p2_fav, p2_n):
    '''
    Quantifying user experience: chapter 5 (Comparing completion rates)

    :return:
    '''

    # for testing
    # p1_fav = 11
    # p1_n = 12
    # p2_fav = 4  # p2: bench
    # p2_n = 9

    # evaluation
    p1_prop = p1_fav / p1_n
    p2_prop = p2_fav / p2_n
    N = p1_n + p2_n
    P = (p1_fav + p2_fav) / N
    Q = 1 - P

    z_score = ((p1_prop - p2_prop) * np.sqrt((N - 1) / N)) / (np.sqrt(P * Q * ((1 / p1_n) + (1 / p2_n))))

    return z_score

def compare_favorability_with_bench(fav, n_answers, bench_fav):
    '''
    This function is designed to apply proportions tests
    following the theory and examples from Chapter 4 of
    the book: Quantifying the User Experience.


    Parameters
    ----------
    p: float
        The observed proportion; must be a value between 0 and 1
    n: int
        Number of observations (samples)
    benchmark: float
        The benchmark proportion; must be a value between 0 and 1

    Returns
    -------

    '''
    n = n_answers
    p = fav
    benchmark = bench_fav

    n_success = np.round(n * p)
    q = 1.0 - p

    # check the small sample size condition
    if (p * n < 15) | (q * n < 15):
        # print('small sample size')

        # source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binom.html
        prob1 = stats.binom.pmf(k=np.arange(n_success, n_success + 1), n=n, p=benchmark).sum() / 2 # mid probability
        prob2 = stats.binom.pmf(k=np.arange(n_success + 1, n + 1), n=n, p=benchmark).sum()
        prob = prob1 + prob2
    else:
        # print('large sample size')
        z_score = (p - benchmark) / np.sqrt(benchmark * (1 - benchmark) / n)
        prob = 1 - stats.norm.cdf(z_score)

    if (p * n < 15) | (q * n < 15):
        z_score = stats.norm.ppf(1 - prob)
    if p < benchmark:
        prob = 1 - prob

    return z_score

def compare_enps_with_bench(values, bench, c_level=0.95):
    '''
    UNIFICAR COM INTERVALO DE CONFIANÇA
    Evalutes the enps confidence interval according to https://measuringu.com/nps-confidence-intervals/
    Method: adjusted-wald (3,T)
    '''
    # for testing
    #     n = 107
    #     n_detractors = 16
    #     n_promoters = 61

    n = len(values)  # sample size
    n_detractors = values[values <= 6].count()
    n_promoters = values[values >= 9].count()
    # n_passives = n_detractors = values[(values>6) & (values<9)].count()
    enps = (n_promoters - n_detractors) / n

    adj_n = n + 3
    adj_n_detractors = n_detractors + 3 / 4
    adj_n_promoters = n_promoters + 3 / 4

    adj_prop_promoters = adj_n_promoters / adj_n
    adj_prop_detractors = adj_n_detractors / adj_n
    adj_enps = adj_prop_promoters - adj_prop_detractors

    adj_var = adj_prop_promoters + adj_prop_detractors - (adj_prop_promoters - adj_prop_detractors) ** 2
    adj_se = np.sqrt(adj_var / adj_n)

    enps_diff = adj_enps - bench
    z_score = enps_diff / adj_se
    # p_value = 1 - stats.norm.cdf(z_score)

    return z_score