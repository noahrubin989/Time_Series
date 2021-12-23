import matplotlib.pyplot as plt
from statsmodels.tsa.filters.hp_filter import hpfilter


def filter_relevant_countries(data, column='GDP Per Capita'):
    """
    To ensure that we don't have any missing values for certain dates, we will only consider countries where all values
    for GDP per capita are present
    :param data: The dataset to make the adjustments to
    :param column: The series (column) to ensure no missing values for
    :return: A modified dataset with only the countries where all values were present
    """
    for country in data['Country Name'].unique():
        particular_country = data[data['Country Name'] == country].copy()
        if particular_country[column].isna().sum() > 0:
            data.drop(particular_country.index, axis='index', inplace=True)
    return data


def apply_hp_filter(data, country, column='GDP Per Capita', lamb=6.25, style='seaborn-white'):
    """
    Applies the HP Filter to a particular country, plotting the results
    :param data: The dataset being used to filter out a particular country
    :param country: The country to consider
    :param column: The series to apply the HP filter too
    :param lamb: The lambda value to (depends on annual, quarterly, monthly data)
    :param style: matplotlib plotting style to use ('seaborn-white' by default)
    :return: Shows two graphs; the first being the data (with the HP filter applied) as well as the estimated cyclical
    component of the time series
    """
    plt.style.use(style)

    # Grab the country of interest and set the index column to the date
    chosen_country = data.loc[data['Country Name'] == country].copy()
    chosen_country.rename(columns={'Year': 'Date'}, inplace=True)
    chosen_country.set_index('Date', inplace=True)

    # Extract estimated trend and estimated cyclical component
    chosen_country['Estimated Cycle'], chosen_country['Smoothed Trend Estimate'] = hpfilter(chosen_country[column],
                                                                                            lamb=lamb)

    # Set up figure and axes to plot on
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    if style == 'dark_background':
        colours = ['#33cc33', '#33ccff']
    else:
        colours = ['black', 'blue']

    # Plot the result
    chosen_country[[column, 'Smoothed Trend Estimate']].plot(ax=ax1, color=colours)
    chosen_country['Estimated Cycle'].plot(ax=ax2, color='violet')

    # Titles and labels etc.
    fig.suptitle(f'Hodrick-Prescott Filter ($\lambda = {{{lamb}}}$): {country}', fontsize='xx-large')
    ax1.set(title='GDP Per Capita ($USD)', ylabel='GDP Per Capita ($USD)')
    ax2.set(title=r'Estimated Cyclical Component $\hat{c}_t = y_t - \hat{\tau}_t$',
            ylabel='Estimated Cyclical Component')

    # Remove grid
    for ax in fig.get_axes():
        ax.grid(False)
