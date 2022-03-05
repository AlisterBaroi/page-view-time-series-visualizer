import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
from datetime import datetime

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
def parse_date(x):
    return datetime.strptime(x, "%Y-%m-%d")

df = pd.read_csv('fcc-forum-pageviews.csv',
                 parse_dates=['date'],
                 date_parser=parse_date)
df = df.set_index('date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025))
        & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(16, 5))
    ax = sns.lineplot(data=df, x='date', y='value', color='red')
    ax.set(xlabel='Date', ylabel='Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = pd.DatetimeIndex(df_bar.index).year
    df_bar['month'] = pd.DatetimeIndex(df_bar.index).month
  
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean()
    df_bar = df_bar.unstack()

    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]

    # Draw bar plot
    fig = df_bar.plot(kind='bar', figsize=(7,6)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', labels=months)
  
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
  
    sns.boxplot(data=df_box,ax=ax1,x=df_box["year"],y=df_box["value"])
    ax1.set(xlabel="Year",ylabel="Page Views", title="Year-wise Box Plot (Trend)")
  
    sns.boxplot(
        ax=ax2,
        data=df_box,
        x=df_box["month"],
        y=df_box["value"],
        order=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
    )
    ax2.set(xlabel="Month", ylabel="Page Views")
    ax2.set_title("Month-wise Box Plot (Seasonality)")

    y_ticks = [
        "0",
        "20000",
        "40000",
        "60000",
        "80000",
        "100000",
        "120000",
        "140000",
        "160000",
        "180000",
        "200000",
    ]
        
    ax1.yaxis.set_major_locator(mticker.FixedLocator([int(s) for s in y_ticks]))
    ax1.set_yticklabels(y_ticks)

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
