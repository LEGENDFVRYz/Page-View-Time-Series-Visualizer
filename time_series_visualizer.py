import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col="date", parse_dates=['date'])

# Clean data
df = df[
    (df['value'] > df['value'].quantile(0.025)) &   # Should higher than the top 2.5 %
    (df['value'] < df['value'].quantile(0.975))     # Should lower than the top 97.5%
]
df.head()


def draw_line_plot():
    # Draw line plot
    fig = df.plot(
    title = 'Daily freeCodeCamp Forum Page Views 5/2016-12/2019',
    xlabel = 'Date',
    ylabel = 'Page Views',
    
    figsize=(15,8),     # making wide graph
    kind = 'line',      # deploy a line graph
    legend = False,     # don't show legend box
    color = 'red'       # red line color
    )

    fig = fig.figure

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = pd.DataFrame(
        data = {
            'value' : df['value'],              # getting the value from the df
            'year' : df.index.year,             # geting the year
            'month' : df.index.month_name(),    # used for getting the name representation of the month
        },
        index = df.index
    )

    df_bar = df_bar.pivot_table(        # Re-shaping the data in more appropriate way
        index='year',                          
        columns='month',                        # make the 'month' value become a column
        values='value',                         # make the value of corresponding month
        aggfunc='mean'                          # apply mean() function in every month
    )

    df_bar = df_bar[                    # Make it in ordered
        ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December']
    ]


    # Draw bar plot
    fig = df_bar.plot(
        kind = 'bar',
        xlabel='Years',
        ylabel='Average Page Views',

        figsize=(10,8),
        legend = True
    )
    plt.legend(title='Months')

    fig = fig.figure

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()                                                              # Copying the df
    df_box.reset_index(inplace=True)                                                # then, reset index
    df_box['year'] = [date.year for date in df_box['date']]                         # new column, has year of the df
    df_box['month'] = [date.strftime('%b') for date in df_box['date']]              # new column, has abb. month of the df

    order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']      # Order of the month in abb. format

    # Draw box plots (using Seaborn)
    fig, (plot1, plot2) = plt.subplots(1, 2, figsize=(20, 5))                       # Initialize plot 1 and plot 2
    plot1 = sns.boxplot(data=df_box, x='year', y='value', ax=plot1)                 # Create plot 1 (year)
    plot2 = sns.boxplot(data=df_box, x='month', y='value', ax=plot2, order=order);  # Create plot 2 (months)

    plot1.set_title('Year-wise Box Plot (Trend)')
    plot1.set_xlabel('Year')
    plot1.set_ylabel('Page Views')

    plot2.set_title('Month-wise Box Plot (Seasonality)')
    plot2.set_xlabel('Month')
    plot2.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
