import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display, HTML

class UnivariateAnalysis():

    def __init__(self, df):
        self.df = df

    def analyze_numerical_columns(self, columns=None):
        if columns is None:
            columns = self.df.select_dtypes(include='number').columns.tolist()
        for column in columns:
            self.plot_numeric_column(column)

    def analyze_categorical_columns(self, columns=None):
        if columns is None:
            columns = self.df.select_dtypes(include='object').columns.tolist()
        for column in columns:
            self.plot_categorical_column(column)

    def analyze_timeseries_columns(self, columns=None):
        if columns is None:
            columns = self.df.select_dtypes(include='datetime64').columns.tolist()
        for column in columns:
            self.plot_timeseries(column)

    def plot_numeric_column(self, column):
        display(HTML(f'<div style="text-align: center;"><h1> Plot for {column}<h1>'))
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        self.plot_histogram(column, axes[0])
        self.plot_box_plot(column, axes[1])
        self.plot_violin_plot(column, axes[2])

        plt.show()

    def plot_histogram(self, column,ax):
        sns.histplot(data=self.df, x=column, ax=ax, kde=True, color='#FF5733')
        ax.set_title(f'Histogram and KDE for {column}', fontsize=16, fontweight='bold')

    def plot_box_plot(self, column, ax):
        sns.boxplot(data=self.df, y=column, ax=ax, color='#FF5733')
        ax.set_title(f'Boxplot for {column}', fontsize=16, fontweight='bold')

    def plot_violin_plot(self, column, ax):
        sns.violinplot(data=self.df, y=column, ax=ax, color='#FF5733')
        ax.set_title(f'Violin plot for {column}', fontsize=16, fontweight='bold')

    def plot_categorical_column(self, column):
        categories = self.df[column].unique()
        value_counts = self.df[column].value_counts()
        display(HTML(f'<div style="text-align: center;"><h1> Plot for {column}<h1>'))

        self.plot_count_plot(column)
        self.plot_doughnut_plot(column)

    def plot_count_plot(self, column):
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        sns.set(style="darkgrid")

        # Extract categories and value_counts from the DataFrame
        categories = self.df[column].unique()
        value_counts = self.df[column].value_counts()

        n_colors = len(categories)
        color_palette = sns.color_palette("husl", n_colors)

        counts = value_counts.tolist()
        bars = axes[0].bar(categories, counts, color=color_palette)
        axes[0].set_title(f'Count Plot for {column}', fontsize=16, fontweight='bold')
        axes[0].set_xlabel('Categories')
        axes[0].set_ylabel('Counts')

        for bar, count in zip(bars, counts):
            axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(count), ha='center', va='bottom')

        wedges, texts, autotexts = axes[1].pie(counts, labels=categories, autopct='%1.1f%%',
                                               startangle=140, wedgeprops={'width': 0.5})
        axes[1].set_title(f'Doughnut Plot for {column}', fontsize=16, fontweight='bold')

        plt.tight_layout()
        plt.show()

    def plot_doughnut_plot(self, column):
        categories = self.df[column].unique()
        value_counts = self.df[column].value_counts()

        wedges, texts, autotexts = plt.pie(value_counts.tolist(), labels=categories, autopct='%1.1f%%',
                                           startangle=140, wedgeprops={'width': 0.5})
        plt.title(f'Doughnut Plot for {column}', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()

    def plot_timeseries(self, column):
        plt.figure(figsize=(14, 6))
        display(HTML(f'<div style="text-align: center;"><h1> Plot for {column}<h1>'))
        df_resampled = self.df.set_index(column).resample('D').size()
        df_resampled.plot(marker='o', linestyle='-')
        plt.title(f'Time Series Plot for {column}', fontsize=16, fontweight='bold')
        plt.xlabel(column)
        plt.ylabel('Count')
        plt.show()
