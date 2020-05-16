import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
pd.plotting.register_matplotlib_converters()


if __name__ == "__main__":
    world = pd.read_csv('../data/time_series_covid19_confirmed_global.csv')
    sweden = world[world['Country/Region'].isin(['Sweden'])]
    sweden = sweden.drop(['Province/State', 'Lat', 'Long'], axis=1)
    # Change format from wide to long for plotting
    sweden_long = pd.melt(sweden, id_vars=['Country/Region'], var_name='ds', value_name='y')
    # Change data column for time series
    sweden_long['ds'] = pd.to_datetime(sweden_long['ds'], infer_datetime_format=True)
    sweden_long.to_csv('../data/prognosis_cumulative.csv')

    sweden_cases = pd.read_excel('../data/Folkhalsomyndigheten_Covid19.xlsx', 'Antal per dag region')
    sweden_cases = sweden_cases.iloc[:, 0:2]
    sweden_cases = sweden_cases.rename(columns={'Statistikdatum': 'ds', 'Totalt_antal_fall': 'y'})
    sweden_cases.to_csv('../data/prognosis_daily.csv')

    fig = plt.figure(figsize=(5, 3))
    ax = fig.add_axes([0, 0, 1, 1])
    fit1 = sm.tsa.statespace.SARIMAX(sweden_long.y, order=(2, 1, 4)).fit()
    plt.plot(sweden_long['y'], label='Train')
    plt.plot(fit1.forecast(93), label='SARIMA_forecast')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=12)

    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: f'{int(x*1e-3)}'))
    plt.xlabel('Day', fontsize=12)
    plt.ylabel('Cumulative number of cases [K]', fontsize=10)
    plt.title('3 months forecast', fontsize=18)
    plt.legend(loc='best', prop={'size': 12})
    plt.grid()
    # plt.show()
    fig.savefig('../figures_static/prognosis_cumulative.png', bbox_inches='tight', dpi=96)

    fig = plt.figure(figsize=(5, 3))
    ax = fig.add_axes([0, 0, 1, 1])
    fit1 = sm.tsa.statespace.SARIMAX(sweden_cases.y, order=(2, 1, 4)).fit()
    plt.plot(sweden_cases['y'], label='Train')
    plt.plot(fit1.forecast(14), label='SARIMA_forecast')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=12)
    plt.xlabel('Day', fontsize=12)
    plt.ylabel('Daily number of cases', fontsize=12)
    plt.title('14 day forecast', fontsize=18)
    plt.legend(loc='best', prop={'size': 12})
    plt.grid()
    # plt.show()
    fig.savefig('../figures_static/prognosis_daily.png', bbox_inches='tight', dpi=96)
