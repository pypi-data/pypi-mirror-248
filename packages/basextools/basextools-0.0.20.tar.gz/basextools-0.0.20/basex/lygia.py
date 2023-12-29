### Lygia - Library for Graphics, Images and Art
### A tribute to Lygia Clark, a Brazillian "non-artist"
### BASEX module for basic plots and graphics in EX context


# Imports
import pandas as pd
from matplotlib_venn import venn2
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.graph_objects as go


# Lista de todas as funções implementadas que podem ser
# importadas  com "from lygia import *"
_all = ['', '', '']


def grafico_barras(detalhamento, bar_color='#93c47d', benchmark=None, min_percentage=0, n_decimal_places=1,
                   text_fit=True, orientacao='horizontal', title='Título', keep_sorting=False):
    """
    Generates a bar chart based on the provided data.

    Parameters
    ----------
        detalhamento (pd.DataFrame): DataFrame containing the detailed data to generate the chart.
        bar_color (str, optional): Color of the bars in the chart. Default is '#93c47d'.
        benchmark (list, optional): List of alternatives to be highlighted with a different color. Default is None.
        min_percentage (float, optional): Minimum percentage to display an alternative in the legend. Default is 0.
        n_decimal_places (int, optional): Number of decimal places to display in the bar values. Default is 1.
        text_fit (bool, optional): Defines whether the text on the bars should fit the bar size. Default is True.
        orientacao (str, optional): Orientation of the chart. Can be 'vertical' (default) or 'horizontal'.
        keep_sorting (bool, optional): If True, keeps the original sorting from detalhamento.

    Returns
    -------
        matplotlib.pyplot: Object containing the generated bar chart.
    """

    # Filtrar as alternativas com percentual menor que min_percentage
    filtrado = detalhamento[(detalhamento['Percentual'] > min_percentage) |
                            (detalhamento['Alternativa'].isin(benchmark)) |
                            (detalhamento['Alternativa'].str.contains('\*'))]
    # Ordenar as alternativas em ordem decrescente de percentual
    if keep_sorting:
        df = filtrado.copy()
    else:
        df = filtrado.sort_values(by='Percentual', ascending=True)

    if benchmark is not None:
        # Verificar se os valores da coluna "Alternativa" estão presentes na lista "benchmark"
        condicao = df['Alternativa'].isin(benchmark)
        # Filtrar as linhas que correspondem aos valores da lista
        novo_df = df[condicao]
        # Remover as linhas do DataFrame original
        filt = df[~condicao]
        df = pd.concat([novo_df, filt], ignore_index=True)

    # Filtrar as alternativas com percentual menor que min_percentage para a legenda
    legenda = detalhamento[~detalhamento['Alternativa'].isin(filtrado['Alternativa'])]

    # Gerar as barras do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    if text_fit:
        n = 90
        df['Alternativa'] = df['Alternativa'].apply(lambda x: _add_line_breaks(x, n))
        legenda['Alternativa'] = legenda['Alternativa'].apply(lambda x: _add_line_breaks(x, n))
        if benchmark is not None:
            benchmark = [_add_line_breaks(i, n) for i in benchmark]

    # Definir eixo Y e eixo X conforme a orientação
    if orientacao == 'horizontal':
        y_pos = range(len(df))
        ax.barh(y_pos, df['Percentual'], color=bar_color)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(df['Alternativa'], fontsize=18)
        ax.set_xticks([])  # Remover os valores no eixo X
    else:
        x_pos = range(len(df))
        ax.bar(x_pos, df['Percentual'], color=bar_color)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(df['Alternativa'], fontsize=18, rotation=0, ha='center')
        ax.set_yticks([])  # Remover os valores no eixo Y

    # Definir cor cinza para as alternativas presentes na lista de benchmark
    if benchmark is not None:
        for index, row in df.iterrows():
            if row['Alternativa'] in benchmark:
                if orientacao == 'horizontal':
                    ax.get_children()[index].set_color('#acacac')
                else:
                    ax.get_children()[index].set_color('#acacac')

    # Adicionar o valor da porcentagem no final de cada barra
    for i, v in enumerate(df['Percentual']):
        if orientacao == 'horizontal':
            ax.text(v, i, f'{v:.{n_decimal_places}f}%', color='black', ha='left', va='center', fontsize=15)
            # Adicionar a legenda das alternativas com percentual menor que min_percentage
            if legenda.shape[0] > 0:
                legenda_text = f'*Detalhamento:\n'
                for index, row in legenda.iterrows():
                    legenda_text += f'- {row["Alternativa"]}: {row["Percentual"]:.{n_decimal_places}f}%\n'

                plt.text(0, -0.1, legenda_text, transform=ax.transAxes, verticalalignment='top',
                         horizontalalignment='left',
                         fontsize=15, bbox=dict(facecolor='none', edgecolor='none'))
        else:
            ax.text(i, v, f'{v:.{n_decimal_places}f}%', color='black', ha='center', va='bottom', fontsize=15)
            if legenda.shape[0] > 0:
                legenda_text = f'*Detalhamento:\n'
                for index, row in legenda.iterrows():
                    legenda_text += f'- {row["Alternativa"]}: {row["Percentual"]:.{n_decimal_places}f}%\n'

                plt.text(1.2, -0.1, legenda_text, transform=ax.transAxes, verticalalignment='top',
                         horizontalalignment='center',
                         fontsize=15, bbox=dict(facecolor='none', edgecolor='none'))

    # Configurar os rótulos e o título
    ax.set_title(title, fontsize=20)

    # Remover as bordas do gráfico
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    return plt


def generate_vertical_bar_chart(data, var_type, add_total=None, values_order=True, n_decimal_places=1, text_fit=True):
    """
       Generates a vertical bar chart based on the provided data.

       Parameters
       ----------
           data (list or pd.DataFrame): Data to be plotted on the bar chart.
           var_type (str): Type of variable to be plotted. Can be 'nps' (Net Promoter Score) or 'favorability'.
           add_total (str, optional): Alternative to be added as a totalizing bar. Default is None.
           values_order (bool or None, optional): Defines whether the values should be ordered. Default is True.
           n_decimal_places (int, optional): Number of decimal places to display in the bar values. Default is 1.
           text_fit (bool, optional): Defines whether the text on the bars should fit the bar size. Default is True.

       Returns
       -------
           matplotlib.pyplot: Object containing the generated vertical bar chart.
    """

    # Ordenar os valores, se necessário
    if values_order is not None:
        data = pd.DataFrame(data)
        data = data.sort_values(by='Percentual', ascending=False)

    # Paleta de cores
    colors = ['#93c47d', '#f1c232', '#0097a7', '#ee4c4a']

    # Verificar se há mais recortes do que cores disponíveis
    if len(data) > len(colors):
        repetitions = len(data) // len(colors) + 1
        colors = colors * repetitions

    # Adicionar barra para o total de respondentes, se necessário
    if add_total is not None:
        data = data.set_index('Alternativa').loc[[add_total]].append(data.set_index('Alternativa').drop([add_total]))
        data = data.reset_index()

    # Gerar o gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))
    x_pos = range(len(data))

    # Plotar as barras
    ax.bar(x_pos, data['Percentual'], color=colors[:len(data)])
    if add_total is not None:
        ax.patches[0].set_facecolor('#acacac')

    if text_fit:
        data['Alternativa'] = data['Alternativa'].apply(lambda x: _add_line_breaks(x, 10))

    # Remover os valores no eixo Y
    ax.set_yticks([])

    # Adicionar o nome de cada alternativa no eixo X
    ax.set_xticks(x_pos)
    ax.set_xticklabels(data['Alternativa'], fontsize=10, ha='center')

    # Titulo
    if var_type == 'nps':
        ax.set_title('Gráfico de Barras (NPS)')
        # Adicionar o valor da porcentagem acima de cada barra
        for i, v in enumerate(data['Percentual']):
            ax.text(i, v, f'{v:.{n_decimal_places}f}', color='black', ha='center', va='bottom', fontsize=18)
    elif var_type == 'favorability':
        ax.set_title('Gráfico de Barras (Favorabilidade)')
        # Adicionar o valor da porcentagem acima de cada barra
        for i, v in enumerate(data['Percentual']):
            ax.text(i, v, f'{v:.{n_decimal_places}f}%', color='black', ha='center', va='bottom', fontsize=18)
    # Remover as bordas do gráfico
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    return plt


def generate_venn_chart(payload, intersection, adjust_circle=False):
    """
    Generates a Venn diagram based on the provided data.

    Parameters
    ----------
        payload (list): List containing the data of the sets to be represented in the diagram.
            Each item in the list should be a dictionary with the keys 'label', 'value', and 'enps'.
            'label' is the label of the set, 'value' is the percentage of the set, and 'enps' is the eNPS value.
        intersection (dict): Dictionary containing the data of the intersection between the sets.
            It should have the keys 'value' and 'enps' representing the percentage and eNPS value of the intersection.
        adjust_circle (bool, optional): Defines whether the Venn diagram circle should be adjusted for the provided values.
            Default is False.

    Returns
    -------
        matplotlib.pyplot: Object containing the generated Venn diagram.
    """
    # Obter as chaves e valores do dicionário
    labels = [x['label'] for x in payload]
    values = [x['value'] for x in payload]
    enpss = [x['enps'] for x in payload]

    # Converter os valores para inteiros
    values = [int(v) for v in values]

    # Criar o gráfico de Venn
    fig, ax = plt.subplots(figsize=(6, 6))
    if adjust_circle:
        venn = venn2(subsets=(values[0], values[1], intersection['value']), set_labels=(labels[0], labels[1]), ax=ax)

    else:
        venn = venn2(subsets=(10, 10, 5), set_labels=(labels[0], labels[1]), ax=ax)

    # Adicionar os valores dentro dos subconjuntos
    subset_labels = [f'{value}%\neNPS{enps}' for value, enps in zip(values, enpss)]
    subset_labels.append(f'{intersection["value"]}%\neNPS{intersection["enps"]}')
    for text in venn.subset_labels:
        text.set_fontsize(12)
    for text, label in zip(venn.subset_labels, subset_labels):
        text.set_text(label)
    return plt


def grafico_sentimentos(dataframe, n_decimal_places=0):

    """
    Generate a sentiment analysis chart using horizontal bars.

    Parameters
    ----------
        dataframe (pd.DataFrame): DataFrame containing sentiment data.
        n_decimal_places (int, optional): Number of decimal places to round the percentages (default: 0).

    Returns
    -------
        plt: Matplotlib plot object.

    """
    # Arredondar os valores percentuais
    dataframe = dataframe.round(n_decimal_places)

    # Ordenar o DataFrame pelo percentual positivo, seguido pelo percentual neutro
    dataframe = dataframe.sort_values(by=['Positivo', 'Neutro'], ascending=False)

    # Gerar as barras do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    y_pos = range(len(dataframe))

    # Barra Positivo (verde)
    ax.barh(y_pos, dataframe['Positivo'], color='#93c47d')

    # Barra Neutro (cinza)
    ax.barh(y_pos, dataframe['Neutro'], left=dataframe['Positivo'], color='#acacac')

    # Barra Negativo (preto)
    ax.barh(y_pos, 100 - dataframe['Positivo'] - dataframe['Neutro'], left=dataframe['Positivo'] + dataframe['Neutro'],
            color='#000000')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(dataframe.index, fontsize=18)
    ax.set_xticks([])  # Remover os valores no eixo X

    # Adicionar o valor da porcentagem em cada barra
    for i, (positivo, neutro, negativo) in enumerate(
            zip(dataframe['Positivo'], dataframe['Neutro'], 100 - dataframe['Positivo'] - dataframe['Neutro'])):
        ax.text(positivo / 2, i, f'{positivo:.{n_decimal_places}f}%', color='white', ha='center', va='center',
                fontsize=15)
        ax.text(positivo + neutro / 2, i, f'{neutro:.{n_decimal_places}f}%', color='black', ha='center', va='center',
                fontsize=15)
        ax.text(positivo + neutro + negativo / 2, i, f'{negativo:.{n_decimal_places}f}%', color='white', ha='center',
                va='center', fontsize=15)

    # Configurar os rótulos e o título
    ax.set_title('Análise de Sentimentos', fontsize=18)

    # Adicionar a legenda das alternativas
    pos_patch = mpatches.Patch(color='#93c47d', label='Positivo')
    neu_patch = mpatches.Patch(color='#acacac', label='Neutro')
    neg_patch = mpatches.Patch(color='#000000', label='Negativo')

    # ax.legend(handles=[pos_patch, neu_patch, neg_patch], loc='lower right')
    ax.legend(handles=[pos_patch, neu_patch, neg_patch], loc='upper center', bbox_to_anchor=(0.5, 0), ncol=3)

    # Remover as bordas do gráfico
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    return plt


def _add_line_breaks(text, n):
    """
    Add line breaks to the input text at whitespace boundaries, ensuring each substring
    has a length as close to the specified number of characters (n) as possible.

    Parameters
    ----------
        text (str): The input text.
        n (int): The desired length of each substring.

    Returns
    -------
        str: The modified text with line breaks added.

    """
    words = text.split()  # Split the text into individual words
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) <= n:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return '\n'.join(lines)


def plot_stacked_bar(df, columns_dict, add_total_fav, colors=['#a8a4a4', '#d8d4d4', '#669ec8'], save_path=None):
    """
    Plot horizontal stacked bar charts for the given dataframe.

    Parameters:
    - df: DataFrame containing values from 1 to 5
    - colors: Colors for the 3 categories
    """

    # Calculate the percentage of values in each category
    percs_12 = (df.isin([1, 2]).sum() / df.count()) * 100
    percs_3 = (df == 3).sum() / df.count() * 100
    percs_45 = (df.isin([4, 5]).sum() / df.count()) * 100

    # Create horizontal stacked bar chart
    fig, ax = plt.subplots(figsize=(12, len(df.columns) * 0.2))

    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)

    cols = list(df.columns)
    new_order = []
    if columns_dict:
        for new_col, orig_cols in columns_dict.items():
            cols.append(new_col)
            new_order.append(new_col)
            new_order = new_order + orig_cols

            dff = df[orig_cols].stack().copy()
            percs_12[new_col] = (dff.isin([1, 2]).sum() / dff.count()) * 100
            percs_3[new_col] = ((dff == 3).sum() / dff.count()) * 100
            percs_45[new_col] = (dff.isin([4, 5]).sum() / dff.count()) * 100
    else:
        new_order = cols

    # new_order = [total_col] + new_order
    percs_12 = percs_12[new_order][::-1]
    percs_3 = percs_3[new_order][::-1]
    percs_45 = percs_45[new_order][::-1]

    # add total col
    if add_total_fav:
        total_col = 'Macro Indicador (Média Geral)'
        new_order = [total_col] + new_order
        dff = df.stack()
        percs_12[total_col] = (dff.isin([1, 2]).sum() / dff.count()) * 100
        percs_3[total_col] = ((dff == 3).sum() / dff.count()) * 100
        percs_45[total_col] = (dff.isin([4, 5]).sum() / dff.count()) * 100
    else:
        total_col = ''

    new_order = new_order[::-1]

    ax.barh(new_order, percs_45, color=colors[2])
    ax.barh(new_order, percs_3, color=colors[1], left=percs_45)
    ax.barh(new_order, percs_12, color=colors[0], left=percs_45 + percs_3)

    # Annotate with percentage values
    for i, (p45, p3, p12) in enumerate(zip(percs_45, percs_3, percs_12)):
        if p45 > 0:
            ax.text(p45 / 2, i, f"{p45:.1f}%", ha='center', va='center', color='black')
        if p3 > 0:
            position = p45 + p3 / 2
            if (position > 92.5) and (p12 > 0):
                position = 92.5
            if (position > 95) and (p12 == 0):
                position = 95
            ax.text(position, i, f"{p3:.1f}%", ha='center', va='center', color='black')
        if p12 > 0:
            position = p45 + p3 + p12 / 2
            if (p45 + p3) > 95:
                position = 97.5
            ax.text(position, i, f"{p12:.1f}%", ha='center', va='center', color='black')

    # Set y-ticks and make certain labels bold
    labels = new_order
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels, fontsize=10)

    # Bold labels for columns that are keys in columns_dict
    for label in ax.get_yticklabels():
        if ((columns_dict is not None) and (label.get_text() in columns_dict.keys())) or (
                label.get_text() == total_col):
            label.set_weight('bold')

    # Remove the axis, xlabel and xticks
    # ax.axis('off')
    ax.set_xlabel('')
    ax.set_xticks([])
    # ax.legend(loc="upper right")
    plt.tight_layout()

    return fig

def stack_plot(name, n_coms, per_n, per_p, leg, file_path=None):
    '''
    Plota barra de sentimentos

    Parameters
    ----------
    name : String
        Título da barra de sentimentos. Por exemplo, nome do tópico
    n_coms : int
        Número de comentários (não é atualmente utilizado)
    perc_n: float
        Percentual de comentários negativos
    per_p: float
        Percentual de comentários positivos
    leg: bool
        Ajusta o aparecimento da legenda

    '''
    #     if n_coms > 0 and n_coms <= 99:
    #         n_coms = '  '+str(n_coms)
    #     elif n_coms >= 100 and n_coms <=999:
    #         n_coms = ' '+str(n_coms)
    name = name.replace(' ', '\n')
    d = {'Positivos': per_p, 'Negativos': per_n, 'Neutros': 100 - per_p - per_n}
    d = pd.DataFrame(pd.Series(d)).T
    # d = d.rename({0: f'{name}\n({str(n_coms)} comentários)'})
    d = d[['Negativos', 'Neutros', 'Positivos']]
    # color=['#ea9999', 'lightgrey', '#69c2cc']
    ax = d.plot.barh(stacked=True, color=['#a8a4a4', '#d8d4d4', '#669ec8'], fontsize=12, figsize=(12, 2), legend=leg)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_yticks([])

    counts = 0
    for i, bar in enumerate(ax.patches):
        vertical_move = 0 if (per_n <= 4) & (i == 1) else 1
        if bar.get_width() > 0:
            ax.annotate(f'{np.round(bar.get_width(), 1)}%',
                        (counts,
                         bar.get_y() + vertical_move * bar.get_height() / 3), ha='left', va='center',
                        size=14, xytext=(0, 8),
                        textcoords='offset points')
            counts = counts + bar.get_width()
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        left=False,
        top=False,  # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off
    if leg:
        ax.legend(ncol=3, loc='lower center')
    plt.title(name, size=16)
    # plt.ylabel(name, size=14)
    fig = ax.get_figure()

    return fig

def nps_gauge_plot(enps, ref=-101, perc=False, round=False):
    '''
    Plot an eNPS value using a gauge visualization

    Parameters
    ----------
    enps : float
        The enps value
    ref : float, default -101 (outside the enps range)
        A reference enps value
    group : String, default = ''
       An optional group name that refers to the eNPS being prompted
       Example: "Ativos" or "Diretoria de TI"
    perc : bool, default True
        If True, it prompts the relative difference to `ref` in percentage
    round : bool, default False
        If True, round the eNPS value to match the visualization of the platform
    file_path : String or None, default None
        The desired location of the image file. If it's not given a default location will be set up
    '''

    # round to match the platform
    if round:
        enps = int(np.round(enps))

    if ref >= -100:
        mode = "gauge+number+delta"
        threshold_thickness = .75
    else:
        mode = "gauge+number"
        threshold_thickness = 0

    fig = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=enps,
        mode=mode,
        # title={'text': f"eNPS {group}"},
        delta={'reference': ref, 'relative': perc},
        gauge={'axis': {'range': [-100, 100]},
               'bar': {'color': "#57bf3a", 'thickness': 1},
               'threshold': {'line': {'color': "gray", 'width': 4}, 'thickness': threshold_thickness, 'value': ref}}))

    fig.update_layout(height=380, width=700, margin={'t': 0, 'b': 0, 'l': 35, 'r': 35})

    return fig

def colors_from_values(values):
    '''
    Generate a divergent color palette with color hues proportional to each valuee in `values`
    Adapted from https://stackoverflow.com/questions/36271302/changing-color-scale-in-seaborn-bar-plot

    :param values: (Python iterator) a list of floats
    :param

    :return: palette (np.array) the color palette
    '''

    if len(values) > 1:  # general case
        # normalize the values to range [0, 1]
        normalized = (values - min(values)) / (max(values) - min(values))
        # convert to indices
        indices = np.round(normalized * (len(values) - 1)).astype(np.int32)
        # use the indices to get the colors
        palette = sns.diverging_palette(11, 186, s=99, l=60, sep=1, n=len(values))
        palette = np.array(palette).take(indices, axis=0)
    else:
        # only one bar
        palette = sns.diverging_palette(11, 186, s=99, l=60, sep=1, n=len(values))

    return palette

def plot_n_respondents(df, comparison_types, show=True):
    '''
    Plot a bar graph with number and ration of answers for each class of a comparison type
    Adapted from https://www.geeksforgeeks.org/how-to-annotate-bars-in-barplot-with-matplotlib-in-python/

    :param dfc: (pd.DataFrame) the answers' base
    :param comparison_type: (list) the comparison types
    :param save: (Boolean) if `True` saves the images
    :param show: (Boolean) if `True` plots the bar graph
    :return:
    '''

    output = {}
    for comparison_type in comparison_types:
        df[comparison_type] = df[comparison_type].replace('-', np.nan).dropna()
        dfc = df[comparison_type].value_counts()
        output[comparison_type] = dfc.to_dict()

        # Defining the plot size
        fig = plt.figure(figsize=(6, len(dfc) / 2))

        # Add axes object to our figure that takes up entire figure
        ax = fig.add_axes([0, 0, 1, 1])

        # Hide the top and right spines of the axis
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # plot
        plots = sns.barplot(x=dfc.values, y=dfc.index, palette=colors_from_values(dfc.values), orient='h')

        percentages = (100 * dfc.values / dfc.sum()).round(1)
        cumsum = percentages.cumsum().round(1)
        # Iterrating over the bars one-by-one
        for i, bar in enumerate(plots.patches):
            # Using Matplotlib's annotate function and
            # passing the coordinates where the annotation shall be done
            # x-coordinate: bar.get_x() + bar.get_width() / 2
            # y-coordinate: bar.get_height()
            # free space to be left to make graph pleasing: (0, 8)
            # ha and va stand for the horizontal and vertical alignment
            plots.annotate(f'{int(bar.get_width())} ({percentages[i]}%, {cumsum[i]}%)',
                           (bar.get_width() + 1,
                            bar.get_y() + bar.get_height() / 2 + bar.get_height()/3), ha='left', va='center',
                           size=12, xytext=(0, 8),
                           textcoords='offset points')

        plt.ylabel("Quantidade de respondentes", size=16)
        plt.xlabel(comparison_type, size=16)
        plt.xticks(rotation=0)
        # plt.grid(axis='x')
        if show:
            plt.show()

    return output


def bar_plot_distribution_given_group(scores, group, show,
                                      highlight_outliers=False,
                                      avg=None,
                                      highlight_variable=None):
    '''
    Plot a bar graph with the distributions of the favorability scores for each variable from a `group` of people
    Adapted from https://www.geeksforgeeks.org/how-to-annotate-bars-in-barplot-with-matplotlib-in-python/

    :param scores_new: (pd.Series) the favorability scores of a given group of people
    :param group: (String) a class of a comparison type or `Total da Pesquisa`
    :param save: (Boolean) if `True` save the plot
    :param show: (Boolean) if `True` plot the distributions
    :param highlight_outliers (Boolean) if `True` highlight outliers regions
    :param avg (int) if available displays de avg. favorability
    :param highlight_variable (String) A valid variable name to be highlighted in the plot
    :return:
    '''

    # scores = scores.sort_values(ascending=True)

    # later, we can think about displaying NaN variables
    scores = scores.dropna()
    scores_new = scores.copy()
    scores_new.index = [f'{v} ({i + 1})' for i, v in enumerate(list(scores_new.index)[::-1])][::-1]

    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plots = sns.barplot(x=scores_new.index, y=scores_new.values, palette=colors_from_values(scores_new.values))  # color=COMPANY_COLOR)

    # Iterrating over the bars one-by-one
    for bar in plots.patches:
        plots.annotate(str(int(np.round(bar.get_height()))),
                       (bar.get_x() + bar.get_width() / 2,
                        bar.get_height()+1), ha='center', va='center',
                       size=14, xytext=(0, 8), rotation=0,
                       textcoords='offset points')

    if highlight_outliers:
        outliers = utils.get_reject_outliers(scores_new.values, method='mapping')
        neg_outliers_size = (outliers == -1).sum()
        if neg_outliers_size > 0:
            plt.axvline(neg_outliers_size - 0.5, c='r', linestyle='--', alpha=0.7, label='Limite inferior')
            # plt.legend()
        pos_outliers_size = (outliers == 1).sum()
        if pos_outliers_size > 0:
            plt.axvline(scores_new.size - pos_outliers_size - 0.5, c='g', linestyle='--', alpha=0.7, label='Limite superior')
            # plt.legend()

    if avg:
        slack = 0.5
        if (scores_new[scores_new == avg]).size > 0:
            slack = 0
        num_bars_below = (scores_new[scores_new < avg]).size
        plt.axvline(num_bars_below - slack, c='k', linestyle='--', alpha=0.7, label=f'Favorabilidade média: {int(avg)}')

    if highlight_variable:
        plt.gca().get_xticklabels()[list(scores.index).index(highlight_variable)].set_weight("bold") # https://stackoverflow.com/questions/41924963/formatting-only-selected-tick-labels

    plt.xlabel(group, size=14)
    plt.xticks(rotation=90, size=12)
    plt.yticks(rotation=0, size=12)
    plt.ylabel("% de favorabilidade", size=14)
    plt.legend()
    # plt.grid()
    if show:
        plt.show()

    return fig

def strip_plot_distribution_given_var(scores, var, comparison_type, show, highlight_outliers=False):
    '''
    Plot a strip plot of favorability scores for each class in a comparison type for a given variable

    :param scores: (pd.Series) the favorability scores of a given variable
    :param var: (String) a question/variable or `FAVORABILIDADE MÉDIA`
    :param comparison_type: (String)
    :param highlight_outliers (Boolean) if `True` highlight outliers regions
    '''
    fig = plt.figure(figsize=(12, scores.shape[0] / 2))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    sns.stripplot(x=scores, y=scores.index, size=12, linewidth=1, palette=colors_from_values(scores.values), marker='o')
    plt.ylabel('', size=14)
    plt.xlabel(var, size=14)
    plt.xticks(rotation=0, size=14)
    plt.yticks(rotation=0, size=14)
    plt.grid()

    if highlight_outliers and scores.size > 5:
        outliers = utils.get_reject_outliers(scores.values, method='mapping')
        limits = utils.get_reject_outliers(scores.values, method='limits')

        neg_outliers_size = (outliers == -1).sum()
        if neg_outliers_size > 0:
            plt.axvline(limits[0], c='r', linestyle='--', alpha=0.7, label='Limite inferior')
            plt.legend()
        pos_outliers_size = (outliers == 1).sum()
        if pos_outliers_size > 0:
            plt.axvline(limits[1], c='g', linestyle='--', alpha=0.7, label='Limite superior')
            plt.legend()

    if show:
        plt.show()

    return

def plot_hm(df, kind, comparison_type=''):
    '''
    Save a .png heatmap as it appears in the platform

    :param df (pd.DataFrame): the table of scores
    :param kind (String): `fav` for favorability and `enps` for eNPS questions
    :param comparison_type (String): tipo de comparação
    :param save (Boolean): if `True`, save the heatmap
    :param show (Boolean): if `True`, show the heatmap
    '''

    plt.rcParams['font.size'] = 11
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['axes.linewidth'] = 2

    plt.figure(figsize=(max(16, df.shape[1] / 2), 1 + df.shape[0] / 2))  # 16, 32

    if len(df.columns) == 1:
        rot = 0
    else:
        rot = 90

    name = ''
    if kind == 'fav':
        df = np.round(df, 1)
        vmin = 0
        center = 70
        vmax = 100
        name = '% de favorabilidade'
    elif kind == 'enps':
        df = np.round(df)
        vmin = -100
        center = 0
        vmax = 100
        name = 'escores NPS'
    elif kind == 'fav_diff_score' or kind == 'enps_diff_score':
        df = np.round(df, 1)
        vmin = -50
        center = 0
        vmax = 50
        plt.title('Signed Importance Score', size=16)

    cmap = sns.diverging_palette(10, 186, as_cmap=True)
    ax = sns.heatmap(df, annot=True, cmap=cmap, fmt='g', center=center, vmin=vmin, vmax=vmax,
                     annot_kws={'rotation': 0})
    ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    ax.set_xticklabels(labels=df.columns, rotation=rot, size=12)
    ax.set_yticklabels(labels=df.index, rotation=0, size=12)
    ax.set_facecolor('lightgray')  # color of NaN values

    ax.set_ylabel('')
    if name:
        ax.set_xlabel(f'{comparison_type} ({name})', size=14)
    else:
        ax.set_xlabel(f'{comparison_type}', size=14)

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=12)

    return ax

def plot_horizontal_alternative_bars(dff, color, file_path=None):
    dff = dff.sort_values('% respostas', ascending=False)
    print(dff.shape)
    dff = dff.iloc[:10]

    fig = plt.figure(figsize=(4, 2))
    ax = fig.add_axes([0, 0, 1, 1])

    if '% referência' in dff.columns:
        df1 = dff.copy()
        df1['Valor'] = '% referência'
        df1['% respostas'] = df1['% respostas']
        df2 = dff.copy()
        df2['Valor'] = '% respostas'
        df1['% respostas'] = df1['% referência']
        dff = pd.concat([df1, df2], axis=0)
        p = sns.barplot(ax=ax, x='% respostas', y='Alternativa', hue='Valor', data=dff, color=color)

        for i, p in enumerate(ax.patches):
            plt.text(p.get_width() - 5, p.get_y() + 0.55 * p.get_height(),
                     '{:1.1f}'.format(p.get_width()),
                     ha='center', va='center', size=10)

    else:
        p = sns.barplot(ax=ax, x=dff['% respostas'], y=dff['Alternativa'], color=color, label='% alternativa')

        # # Iterating over the bars one-by-one
        # Source: https://stackoverflow.com/questions/42861049/horizontal-barplot-with-annotations
        # Annotate every single Bar with its value, based on it's width
        for i, p in enumerate(ax.patches):
            width = p.get_width()
            if '% referência' in dff.columns:
                ref = dff.iloc[i]['% referência']
                plt.text(p.get_width() - 5, p.get_y() + 0.55 * p.get_height(),
                         '{:1.1f} ({:1.1f})'.format(width, ref),
                         ha='center', va='center', size=10)
            else:
                plt.text(p.get_width() - 5, p.get_y() + 0.55 * p.get_height(),
                         '{:1.1f}'.format(width),
                         ha='center', va='center', size=10)
        # if '% referência' in dff.columns:
        #     sns.barplot(ax=ax, x=dff['% referência'], y=dff['Alternativa'], color='#f1c23235', alpha=0.4, label='% referência')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    plt.xlim([0, 105])  # space for 100 legend
    # ax.spines['bottom'].set_visible(False)
    #ax.set_yticks(ticks= list(dff['Alternativa']), size=10)
    ax.set_axisbelow(True)
    ax.set_xlabel('')
    # ax.grid()
    ax.set_xlabel("Percentual de respostas", size=10)
    # ax.set_yticklabels(labels=dff['Alternativa'], rotation=0, size=7)
    ax.set_ylabel("", size=12)
    # sns.barplot(ax=ax, y=dff['% referência'], x=dff['Alternativa'], color='#fff2cc6e', alpha=0.4, label='% referência')
#     counts = 0
#     for i, (bar, alt) in enumerate(zip(ax.patches, list(dff['Alternativa']))):
#         ax.annotate(str(alt),
#                         (bar.get_x(),
#                          0), size=10, xytext=(3, 2), rotation=90,
#                         textcoords='offset points')
#         counts = counts + bar.get_width()
    # plt.legend(loc='upper right', prop={'size': 8})
    # plt.legend(bbox_to_anchor=(1, 1.25), loc='upper right', borderaxespad=0)
    # ax.legend(ncol=1, loc='upper right')
    # plt.show()

    if file_path is None:
        fig.savefig(f"./outputs/_temp/img_gen_alternative_comp.png", dpi=300, bbox_inches='tight')
    else:
        fig.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close('all')

    return

def plot_alternative_bars(dff, color, file_path=None):
    dff = dff.sort_values('% respostas', ascending=False)
    dff = dff.iloc[:10]

    if '% referência' in dff.columns:
        dff['% respostas'] = dff['% respostas'].round(0).astype(int)
        dff['% referência'] = dff['% referência'].round(0).astype(int)
        dff['values'] = dff['% respostas'].astype(str) + '\n' + dff['% referência'].astype(str)
        values = list(dff['values'].values)

    fig = plt.figure(figsize=(2, 2))
    ax = fig.add_axes([0, 0, 1, 1])

    p = sns.barplot(ax=ax, y=dff['% respostas'], x=dff['Alternativa'], color=color, label='% alternativa')

    if '% referência' in dff.columns:
        # Iterating over the bars one-by-one
        # for bar, v in zip(p.patches, values):
        #     p.annotate(v,
        #                (bar.get_x() + bar.get_width() / 2,
        #                 bar.get_height() + 1), ha='center', va='center',
        #                size=10, xytext=(0, 8), rotation=0,
        #                textcoords='offset points')
        sns.barplot(ax=ax, y=dff['% referência'], x=dff['Alternativa'], color='#f1c23235', alpha=0.4, label='% referência')
    else:
        # Iterating over the bars one-by-one
        for bar in p.patches:
            p.annotate(str(int(np.round(bar.get_height()))),
                       (bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 1), ha='center', va='center',
                       size=10, xytext=(0, 8), rotation=0,
                       textcoords='offset points')


    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(False)
    plt.ylim([0, 105])  # space for 100 legend
    # ax.spines['bottom'].set_visible(False)
    #ax.set_yticks(ticks= list(dff['Alternativa']), size=10)
    ax.set_axisbelow(True)
    ax.set_ylabel('')
    # ax.grid()
    ax.set_ylabel("Percentual de respostas", size=12)
    ax.set_xticklabels(labels=dff['Alternativa'], rotation=90, size=8)
    ax.set_xlabel("", size=12)
    # sns.barplot(ax=ax, y=dff['% referência'], x=dff['Alternativa'], color='#fff2cc6e', alpha=0.4, label='% referência')
#     counts = 0
#     for i, (bar, alt) in enumerate(zip(ax.patches, list(dff['Alternativa']))):
#         ax.annotate(str(alt),
#                         (bar.get_x(),
#                          0), size=10, xytext=(3, 2), rotation=90,
#                         textcoords='offset points')
#         counts = counts + bar.get_width()
    # plt.legend(loc='upper right', prop={'size': 8})
    if '% referência' in dff.columns:
        plt.legend(bbox_to_anchor=(1, 1.25), loc='upper right', borderaxespad=0)
        ax.set_axisbelow(True)
        ax.grid()
    # ax.legend(ncol=1, loc='upper right')
    # plt.show()

    if file_path is None:
        fig.savefig(f"./outputs/_temp/img_gen_alternative_comp.png", dpi=300, bbox_inches='tight')
    else:
        fig.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close('all')

    return
