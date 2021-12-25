import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# SES here will be referring to Simple Exponential Smoothing


def simple_exponential_smoothing(data, col, span):
    """
    Simple/Single Exponential Smoothing

    Parameters
    ----------
    data : a pandas dataframe
    col : a string
        The series to consider
    span : an integer (accepts float too)
        N-day exponentially weighted moving average. Alpha is then 2/(span+1)

    Returns
    -------
    A series with the exponentially weighted moving average for when alpha = 2/(span+1)
    """
    alpha = 2 / (span + 1)
    new_series = data[col].ewm(alpha=alpha, adjust=False).mean()
    return new_series


def create_new_columns(data, span_values):
    """
    Adds new columns with the estimates for SES based on the different span values

    Parameters
    ----------
    data : a pandas dataframe
    span_values : an array-like object with span values to consider
    """

    for val in span_values:
        print(f"If span = {val} then alpha = {2 / (val + 1)}")
        # Create the new columns
        data[f'High Price: Simple Exponential Smoothing (span={val})'] = simple_exponential_smoothing(data,
                                                                                                      col='High',
                                                                                                      span=val)

    print("\nAll columns with the specified span values have now been created and added to your dataframe")


def plot_results(data,
                 col_with_estimated_vals,
                 time_period_from='December 4 2015',
                 time_period_to='December 24 2021'):
    """
    Plots results of simple exponential smoothing for all specified span values

    Parameters
    ----------
    data : a pandas dataframe

   time_period_from: str
        Start from this point in time
        -  default is 'December 4 2015', the earliest value in the series
        e.g. '09-2018' would start at September 2018
        Note: Can pass in the date like f{month_name} {day_number} {year_number}'
        ...or like f'{month_number}-{day_number}-{year_number}'

   time_period_to: str
        End at this point in time
        - default is 'December 24 2021', the latest value in the series
        e.g. '07-14-2019' would imply July 14 2019 is the last value in our slice
        Note: Can pass in the date like f{month_name} {day_number} {year_number}'
        ...or like f'{month_number}-{day_number}-{year_number}'

    col_with_estimated_vals: str
        The column containing the estimates
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.set(title=f'Exponential Smoothing: IHHY Prices for {time_period_from} - {time_period_to}', ylabel='IHHY Prices')

    # Plot actual values
    data.loc[time_period_from:time_period_to, ['High']].plot(ax=ax, color='black')

    # Plot exponentially weighted moving average estimates
    data.loc[time_period_from:time_period_to, [col_with_estimated_vals]].plot(ax=ax, color='green')

    ax.legend(loc='lower right', prop={'size': 'medium'})

