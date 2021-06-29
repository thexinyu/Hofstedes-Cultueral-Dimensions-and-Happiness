import pandas as pd
import matplotlib.pyplot as plt
import random as rand
import numpy as np


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)


def keep_country_duplicates(filename1, filename2):
    """
    read data from csv file and return dataframe with same country between two datafiles
    :param filename1: datafile 1
    :param filename2: datafile 2
    :return: dataframe with same country between two datafiles
    """
    country_df1 = pd.read_csv(filename1)
    country_df1.dropna() # drop invalid row data
    country_df2 = pd.read_csv(filename2, sep=';', na_values='#NULL!')
    country_df2.dropna()

    # filter dataframe row, keep the duplicates's country data row only
    output_df1 = country_df1[country_df1['Country'].isin(country_df2['country'])].sort_values('Country').reset_index()
    output_df1.drop_duplicates() # drop duplicate row data
    output_df2 = country_df2[country_df2['country'].isin(country_df1['Country'])].sort_values('country').reset_index()
    output_df2.drop_duplicates()

    return output_df1, output_df2

def merge_with_freedom_column(source_df, freedom_df):
    """
    merge freedom column into dataframe
    :param freedom_df:
    :param source_df:
    """
    return pd.merge(source_df, freedom_df, left_index=True, right_index=True, how='inner')


def fetch_rows_with_valid_columns(dataframe, columns=None):
    """
    fetch dataframe rows with valid columns
    :param dataframe:
    :param columns:
    """
    six_culture_dimensions = ['pdi', 'idv', 'mas', 'uai', 'ltowvs', 'ivr']
    if columns is None:
        columns = []
    valid_rows_df =  dataframe[columns].dropna(thresh=len(columns))
    data = pd.merge(dataframe[list(set(dataframe.columns) - set(six_culture_dimensions))], valid_rows_df, left_index=True, right_index=True, how='inner')
    return data

def graph_one(data, xdata, xlabel, ydata, ylabel, title):
    """
    creates a scatter plot and corresponding best fit line
    data: entire dataset
    xdata: variables to graph on x-axis
    xlabel: x-axis label
    ylabel: variables to graph on y-axis
    title: graph title
    """

    # create scatter plot for data
    plt.figure()
    color = '#565c5e'
    plt.scatter(data[xdata], data[ydata], c=color, marker='.')
    plt.title(str(title))
    plt.xlabel(str(xlabel))
    plt.ylabel(str(ylabel))

    # create best fit line
    x = np.array(data[xdata])
    y = np.array(data[ydata])
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x + b, color = '#a9665a')

def graph_all(data, xdata, xlabel, ydata, ylabel, title):
    """
    creates a scatter plot with legend of multiple variables in a single dataset
    data: entire dataset
    xdata: variables to graph on x-axis
    xlabel: x-axis label
    ylabel: variables to graph on y-axis
    title: graph title
    """
    plt.figure()
    colors = ['#a9665a','#bdcbc4','#3e4c40','#565c5e','#9d7643','#4f6e92']

    # create scatter plot for each variable in xdata
    for i in xdata:
        color = rand.sample(colors,1)
        plt.scatter(data[i], data[ydata], c=color, marker='.')
        plt.legend(xdata, title='Cultural Dimensions', loc='upper right', bbox_to_anchor=(1.36, 1))
    plt.title(str(title))
    plt.xlabel(str(xlabel))
    plt.ylabel(str(ylabel))


def main():
    print('"""\n')

    # process data and print processed data
    dp_country_df1, dp_country_df2 = keep_country_duplicates('happiness.csv', '6dimensions.csv')
    step2_data_process_df = merge_with_freedom_column(dp_country_df2, dp_country_df1['Freedom'])
    all_six = ['pdi', 'idv', 'mas', 'uai', 'ltowvs', 'ivr']
    processed_data = fetch_rows_with_valid_columns(step2_data_process_df, all_six)
    print(processed_data)

    # create labels and title
    xlabel = "Hofstede's Cultural Dimensions"
    ydata = 'Freedom'
    ylabel = "Freedom-Happiness Index"
    title = "Freedom-Happiness Index and Hofstede's Six Cultural Dimensions"

    # graph data for six dimensions simultaneously
    graph_all(processed_data, all_six, xlabel, ydata, ylabel, title)

    # create separate graph for each of the six dimensions
    graph_one(processed_data, 'pdi', 'Power Distance', ydata, ylabel, title)
    graph_one(processed_data, 'idv', 'Individualism', ydata, ylabel, title)
    graph_one(processed_data, 'mas', 'Masculinity', ydata, ylabel, title)
    graph_one(processed_data, 'uai', 'Uncertainty Avoidance', ydata, ylabel, title)
    graph_one(processed_data, 'ltowvs', 'Long-term Orientation', ydata, ylabel, title)
    graph_one(processed_data, 'ivr', 'Indulgence', ydata, ylabel, title)

if __name__ == "__main__":
    main()
