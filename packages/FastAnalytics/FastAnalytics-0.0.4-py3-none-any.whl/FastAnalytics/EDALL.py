from IPython.display import HTML, display
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)  # Ignore DeprecationWarnings

class EDA_ALL():

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.read_csv() 

    def read_csv(self):
        try:
            df = pd.read_csv(self.file_path, index_col=False)
            return df
        except FileNotFoundError:
            print("File not found error. Check the file path.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return None

    def head(self, n=5):
        try:
            n = int(n)  
         
            # display(HTML(f"<h1> head() method  displays Top n Rows of the Dataset</h1>"))
            if n==0:
                display(HTML(f"<h1> head(0) method , an empty DataFrame/zero rows is returned.</h1>"))
            elif n<0:
                abs_n=abs(n)
                display(HTML(f"<h1> head({n}) attempts to display rows by removing top {abs_n} rows of the DataFrame,.</h1>"))
                display(self.df.head(n))
                
            else:   
                display(HTML(f"<h1>Top {n} Rows of the Dataset</h1>"))
                display(self.df.head(n))
            
        except (TypeError,ValueError):
            # Handle the case where a non-integer (e.g., a string) is provided as input
            display(HTML("<h1>Error: Invalid input. Please provide a valid integer for the number of rows.</h1>"))
        

    def tail(self, n=5):
        
        try:
            n = int(n)  
                
            # display(HTML(f"<h1> tail() method  displays Bottom n Rows of the Dataset</h1>"))
            if n==0:
                display(HTML(f"<h1> tail(0) method , an empty DataFrame/zero rows is returned.</h1>"))
                
            elif n<0:
                abs_n=abs(n)
                display(HTML(f"<h1> tail({n}) attempts to display rows by removing bottom {abs_n} rows of the DataFrame,.</h1>"))
                display(self.df.tail(n))
                
            else:   
                display(HTML(f"<h1>bottom {n} Rows of the Dataset</h1>"))
            display(self.df.tail(n))
            
        except (TypeError,ValueError):
            # Handle the case where a non-integer (e.g., a string) is provided as input
            display(HTML("<h1>Error: Invalid input. Please provide a valid integer for the number of rows.</h1>"))


    def sample(self, n=10):
        
        try:
            n = int(n)  
            if n<=self.df.shape[0]:
                display(HTML(f"<h1>Random {n} Rows of the Dataset</h1>"))
                if n==0:
                    display(HTML(f"<h1> sample(0) method , an empty DataFrame/zero rows is returned.</h1>"))
                elif n<0:
                    abs_n = abs(n)  
                    display(HTML(f"<h1> sample({n}) will return an error so taking absolute value and \n"
                             f"displaying random {abs_n} rows of the DataFrame.</h1>"))
                    display(self.df.sample(abs_n))

                else:
                    # display(HTML(f"<h1>display random {n} Rows of the Dataset</h1>"))           
                    display(self.df.sample(n))
                
            else:
                print(f"Random number should always be less than the number of rows in the dataset i.e, {self.df.shape[0]} in this case")
            
        except (TypeError,ValueError):
            # Handle the case where a non-integer (e.g., a string) is provided as input
            display(HTML("<h1>Error: Invalid input. Please provide a valid integer for the number of rows.</h1>"))


    def shape(self):
        # display(HTML(f"<h1>Printing the Total Numbers of Rows and Columns of the Dataset</h1>"))
        display(HTML(f"<h2>Total Number of Rows of the Dataset : {self.df.shape[0]}</h2>"))
        display(HTML(f"<h2>Total Number of Columns of the Dataset : {self.df.shape[1]}</h2>"))

    def col(self):
      # display(HTML("<h1>Printing the Columns Name of the Dataset</h1>"))
      display(HTML(f"<h3>Total Number of Columns of the Dataset : {self.df.columns}</h3>"))

    def info(self):
        display(HTML("<h1>Printing the information of the Dataset</h1>"))
        self.df.info()

    def describe(self):
        display(HTML("<h1>Printing the Statistical information of the Dataset</h1>"))
        display(self.df.describe())

    def corr(self):
        display(HTML("<h1>Printing the correlation matrix information of the Dataset</h1>"))
        display(self.df.corr())

    def isnull(self):
        display(HTML("<h1>Printing the Null Values of the Dataset</h1>"))
        display(self.df.isnull().sum())

    def perisnull(self):
        display(HTML("<h1>Printing the Percentage of the Null Values of the Dataset</h1>"))
        display(self.df.isnull().sum() / self.df.shape[0] * 100)

    def duplicated(self):
        display(HTML("<h1>Printing the Duplicated Values of the Dataset</h1>"))
        display(self.df.duplicated().sum())

    def perduplicated(self):
        display(HTML("<h1>Printing the Percentage of the Duplicated Values of the Dataset</h1>"))
        display(self.df.duplicated().sum() / self.df.shape[0] * 100)
        
        
    def unique_values(self):
        display(HTML("<h1>Unique Values in Each Column</h1>"))
        for column in self.df.columns:
            unique_vals = self.df[column].unique()
            display(HTML(f"<h2>{column}:</h2>"))
            display(unique_vals)
            
    def all(self):
        self.head()
        self.tail()
        self.sample()
        self.shape()
        self.col()
        self.info()
        self.describe()
        self.corr()
        self.isnull()
        self.perisnull()
        self.duplicated()
        self.perduplicated()
        self.unique_values()



























































# from IPython.display import HTML, display
# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt

# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)  # Ignore DeprecationWarnings

# class EDA_ALL():

#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.df = self.read_csv() 

#     def read_csv(self):
#         try:
#             df = pd.read_csv(self.file_path, index_col=False)
#             return df
#         except FileNotFoundError:
#             print("File not found error. Check the file path.")
#             return None
#         except Exception as e:
#             print(f"An unexpected error occurred: {str(e)}")
#             return None

#     def head(self, n=5):
#         try:
#             n = int(n)  
         
#             display(HTML(f"<h1> head() method  displays Top n Rows of the Dataset</h1>"))
#             if n==0:
#                 display(HTML(f"<h1> head(0) method , an empty DataFrame/zero rows is returned.</h1>"))
#             elif n<0:
#                 abs_n=abs(n)
#                 display(HTML(f"<h1> head({n}) attempts to display rows by removing top {abs_n} rows of the DataFrame,.</h1>"))
#                 display(self.df.head(n))
                
#             else:   
#                 display(HTML(f"<h1>Top {n} Rows of the Dataset</h1>"))
#                 display(self.df.head(n))
            
#         except (TypeError,ValueError):
#             # Handle the case where a non-integer (e.g., a string) is provided as input
#             display(HTML("<h1>Error: Invalid input. Please provide a valid integer for the number of rows.</h1>"))
        

#     def tail(self, n=5):
        
#         try:
#             n = int(n)  
                
#             display(HTML(f"<h1> tail() method  displays Bottom n Rows of the Dataset</h1>"))
#             if n==0:
#                 display(HTML(f"<h1> tail(0) method , an empty DataFrame/zero rows is returned.</h1>"))
                
#             elif n<0:
#                 abs_n=abs(n)
#                 display(HTML(f"<h1> tail({n}) attempts to display rows by removing bottom {abs_n} rows of the DataFrame,.</h1>"))
#                 display(self.df.tail(n))
                
#             else:   
#                 display(HTML(f"<h1>bottom {n} Rows of the Dataset</h1>"))
#             display(self.df.tail(n))
            
#         except (TypeError,ValueError):
#             # Handle the case where a non-integer (e.g., a string) is provided as input
#             display(HTML("<h1>Error: Invalid input. Please provide a valid integer for the number of rows.</h1>"))


#     def sample(self, n=10):
        
#         try:
#             n = int(n)  
#             if n<=self.df.shape[0]:
#                 display(HTML(f"<h1>Random {n} Rows of the Dataset</h1>"))
#                 if n==0:
#                     display(HTML(f"<h1> sample(0) method , an empty DataFrame/zero rows is returned.</h1>"))
#                 elif n<0:
#                     abs_n = abs(n)  
#                     display(HTML(f"<h1> sample({n}) will return an error so taking absolute value and \n"
#                              f"displaying random {abs_n} rows of the DataFrame.</h1>"))
#                     display(self.df.sample(abs_n))

#                 else:
#                     display(HTML(f"<h1>display random {n} Rows of the Dataset</h1>"))           
#                     display(self.df.sample(n))
                
#             else:
#                 print(f"Random number should always be less than the number of rows in the dataset i.e, {self.df.shape[0]} in this case")
            
#         except (TypeError,ValueError):
#             # Handle the case where a non-integer (e.g., a string) is provided as input
#             display(HTML("<h1>Error: Invalid input. Please provide a valid integer for the number of rows.</h1>"))


#     def shape(self):
#         display(HTML(f"<h1>Printing the Total Numbers of Rows and Columns of the Dataset</h1>"))
#         display(HTML(f"<h2>Total Number of Rows of the Dataset : {self.df.shape[0]}</h2>"))
#         display(HTML(f"<h2>Total Number of Columns of the Dataset : {self.df.shape[1]}</h2>"))

#     def col(self):
#       display(HTML("<h1>Printing the Columns Name of the Dataset</h1>"))
#       display(HTML(f"<h3>Total Number of Columns of the Dataset : {self.df.columns}</h3>"))

#     def info(self):
#         display(HTML("<h1>Printing the information of the Dataset</h1>"))
#         self.df.info()

#     def describe(self):
#         display(HTML("<h1>Printing the Statistical information of the Dataset</h1>"))
#         display(self.df.describe())

#     def corr(self):
#         display(HTML("<h1>Printing the correlation matrix information of the Dataset</h1>"))
#         display(self.df.corr())

#     def isnull(self):
#         display(HTML("<h1>Printing the Null Values of the Dataset</h1>"))
#         display(self.df.isnull().sum())

#     def perisnull(self):
#         display(HTML("<h1>Printing the Percentage of the Null Values of the Dataset</h1>"))
#         display(self.df.isnull().sum() / self.df.shape[0] * 100)

#     def duplicated(self):
#         display(HTML("<h1>Printing the Duplicated Values of the Dataset</h1>"))
#         display(self.df.duplicated().sum())

#     def perduplicated(self):
#         display(HTML("<h1>Printing the Percentage of the Duplicated Values of the Dataset</h1>"))
#         display(self.df.duplicated().sum() / self.df.shape[0] * 100)
        
        
#     def unique_values(self):
#         display(HTML("<h1>Unique Values in Each Column</h1>"))
#         for column in self.df.columns:
#             unique_vals = self.df[column].unique()
#             display(HTML(f"<h2>{column}:</h2>"))
#             display(unique_vals)
            
#     def univariate_analysis(self, columns=None):
#         if columns is None:
#             columns = self.df.columns
#         elif isinstance(columns, str):
#             columns = [columns]

#         for column in columns:
#             self.plot_univariate(column)

#     def plot_univariate(self, columns):
#         if isinstance(columns, list):
#             for col in columns:
#                 self.plot_univariate_col(col)
#         else:
#             self.plot_univariate_col(columns)

#     def plot_univariate_col(self, column):
#         if column in self.df.select_dtypes(include='number').columns:
#             self.kde_plot(column)
#             self.box_plot(column)
#             self.violin_plot(column)
#         else:
#             self.count_plot(column)

#     def kde_plot(self, column):
#         if column in self.df.select_dtypes(include='number').columns:
#             display(HTML(f"<h2>KDE Plot for {column}</h2>"))
#             sns.kdeplot(data=self.df, x=column, fill=True)
#             plt.title(f'KDE Plot for {column}')
#             plt.show()
#         else:
#             print(f"'{column}' is not a numerical variable.")

#     def box_plot(self, column):
#         if column in self.df.select_dtypes(include='number').columns:
#             display(HTML(f"<h2>Box Plot for {column}</h2>"))
#             sns.boxplot(data=self.df, y=column)
#             plt.title(f'Box Plot for {column}')
#             plt.show()
#         else:
#             print(f"'{column}' is not a numerical variable.")

#     def violin_plot(self, column):
#         if column in self.df.select_dtypes(include='number').columns:
#             display(HTML(f"<h2>Violin Plot for {column}</h2>"))
#             sns.violinplot(data=self.df, y=column)
#             plt.title(f'Violin Plot for {column}')
#             plt.show()
#         else:
#             print(f"'{column}' is not a numerical variable.")
            
#     def count_plot(self, column):
#         if column in self.df.columns:
#             if self.df[column].nunique() <= 5:  # Check if the number of unique values is reasonable for a count plot
#                 display(HTML(f"<h2>Count Plot for {column}</h2>"))
#                 sns.countplot(data=self.df, x=column)
#                 plt.title(f'Count Plot for {column}')
#                 plt.xticks(rotation=45)
#                 plt.show()
#             else:
#                 print(f"'{column}' is not a suitable column for a count plot.")
#         else:
#             print(f"'{column}' does not exist in the DataFrame.")


#     def scatter_plot(self, x, y):
#         if x in self.df.columns and y in self.df.columns:
#             display(HTML(f"<h2>Scatter Plot: {x} vs. {y}</h2>"))
#             sns.scatterplot(data=self.df, x=x, y=y)
#             plt.title(f'Scatter Plot: {x} vs. {y}')
#             plt.show()
#         else:
#             print("Invalid column names. Please provide valid column names.")

#     def pair_plot(self, columns):
#         valid_columns = [col for col in columns if col in self.df.columns]
#         if len(valid_columns) >= 2:
#             display(HTML(f"<h2>Pair Plot for columns: {', '.join(valid_columns)}</h2>"))
#             sns.pairplot(self.df[valid_columns])
#             plt.show()
#         else:
#             print("Not enough valid columns for a pair plot. Please provide at least two valid column names.")

#     def correlation_matrix(self, columns=None):
#         if columns:
#             valid_columns = [col for col in columns if col in self.df.columns]
#             if valid_columns:
#                 display(HTML(f"<h2>Correlation Matrix for selected columns: {', '.join(valid_columns)}</h2>"))
#                 correlation = self.df[valid_columns].corr()
#                 sns.heatmap(correlation, annot=True, cmap="coolwarm")
#                 plt.title("Correlation Matrix")
#                 plt.show()
#             else:
#                 print("No valid columns selected for correlation analysis.")
#         else:
#             display(HTML("<h2>Correlation Matrix for all columns</h2>"))
#             correlation = self.df.corr()
#             sns.heatmap(correlation, annot=True, cmap="coolwarm")
#             plt.title("Correlation Matrix")
#             plt.show()

            
            
#     def all(self):
#         self.head()
#         self.tail()
#         self.sample()
#         self.shape()
#         self.col()
#         self.info()
#         self.describe()
#         self.corr()
#         self.isnull()
#         self.perisnull()
#         self.duplicated()
#         self.perduplicated()
#         self.unique_values()
#         self.univariate_analysis()
#         self.kde_plot(columns)
#         self.box_plot(columns)
#         self.violin_plot(columns)
#         self.count_plot(columns)
#         self.pmf_plot(columns)
#         self.scatter_plot(col1,col2)
#         self.pair_plot(columns)
#         self.correlation_matrix(columns)


