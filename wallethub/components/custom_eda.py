import os
import sys
import pandas as pd
import numpy as np
from scipy.stats import skew
from wallethub.exception import WallethubException
import plotly.express as px


class AutoEDA:
    def __init__(self, df:pd.DataFrame):
        try:
            self.df = df
        except Exception as e:
            raise WallethubException(e,sys) from e

    def sanity_check(self):
        try:          

            num_columns = [column for column in  self.df.columns if self.df[column].dtypes != object]
            cat_columns = [column for column in  self.df.columns if self.df[column].dtypes == object]
            output =f"""
            ------------------------------ Shape of Data ------------------

            Shape of data: {self.df.shape}

            ------------------------ Numerical Columns --------------------

            Numerical Columns: \n{[column for column in  self.df.columns if self.df[column].dtypes != object]}

            ------------------------- Catgorical Columns -------------------

            Categorical Columns: \n{[column for column in  self.df.columns if self.df[column].dtypes == object]}

            ------------------------- Columns Type Count -------------------
            Numerical : {len(num_columns)}

            Categorical: {len(cat_columns)}

            ------------------------- Missing Value -------------------

            Columns with missing values: \n{self.df.isnull().sum()[self.df.isnull().sum()> 0]}

                     """
            return output
        except Exception as e:
            raise WallethubException(e,sys) from e

    
    def custom_num_describe(self)->pd.DataFrame:
        try:
            num_columns = [column for column in  self.df.columns if self.df[column].dtypes != object]
            num_df = self.df[num_columns]
            count = []
            typ = []
            mean = []
            std = []
            minm = []
            q1 = []
            median = []
            q3 = []
            maxm = []
            iqr = []
            skewness = []
            skewness_comment = []
            outlier = []
            for name in num_df.columns:
                skew_score = round(skew(self.df[name],axis=0, bias=False ),2)
                skewness.append(skew_score)

                """
                If the skewness is between -0.5 & 0.5, the data are nearly symmetrical.

                If the skewness is between -1 & -0.5 (negative skewed) or between 0.5 & 1(positive skewed), the data are slightly skewed.

                If the skewness is lower than -1 (negative skewed) or greater than 1 (positive skewed), the data are extremely skewed.
                """
                
                if skew_score == 0:
                    skewness_comment.append("Symmetrical")
                elif skew_score > -0.5 and skew_score < 0:
                    skewness_comment.append("Fairly Symmetrical (Left)")
                elif skew_score > 0 and skew_score < 0.5:
                    skewness_comment.append("Fairly Symmetrical (Right)")
                elif skew_score > -1 and skew_score < -0.5:
                    skewness_comment.append("Moderate Left Skewed")
                elif skew_score > 0.5 and skew_score < 1:
                    skewness_comment.append("Moderate Right Skewed")
                elif skew_score < -1 :
                    skewness_comment.append("Extreme Left Skewed")
                else:
                    skewness_comment.append("Extreme Right Skewed")

                count.append(self.df[name].count())
                typ.append(str(self.df[name].dtypes).replace("dtype('",'').replace("')",''))
                mean.append(self.df[name].mean())
                std.append(self.df[name].std())
                minm.append(min(self.df[name]))
                median.append(self.df[name].median())
                maxm.append(max(self.df[name]))
                Q1 = num_df[name].quantile(0.25)
                q1.append(Q1)
                Q3 = num_df[name].quantile(0.75) 
                q3.append(Q3)      
                
                IQR = Q3- Q1
                iqr.append(IQR)
                upperbound =  (num_df[name].quantile(0.75)) + (1.5*IQR)
                lowerbound =  (num_df[name].quantile(0.25)) - (1.5*IQR)

                if min(num_df[name]) < lowerbound or max(num_df[name]) > upperbound:
                    outlier.append("HasOutliers")
                else:
                    outlier.append("NoOutliers")
            data = list(zip(count, typ, mean, std, minm, q1, median, q3, maxm, iqr, skewness, skewness_comment, outlier))
            column_names = ["Count", "Type", "Mean", "Standard Deviation" , "Minimum", "Q1","Median","Q3","Maximum","IQR", "Skewness Score", "Skewness Comment", "Outliers"]
            describe_df = pd.DataFrame(data, index=num_columns, columns=column_names)
                
            return describe_df
        except Exception as e:
            raise WallethubException(e,sys) from e

    def custom_cat_describe(self)->pd.DataFrame:
        try:
            describe_df =self.df.describe(include=['object']).T.sort_values(by='unique')                
            return describe_df
        except Exception as e:
            raise WallethubException(e,sys) from e

    def cat_auto_univariate_analysis(self,unique_val_count:int = 3, min_val_count_pctg:float = 0.05):
        try:
            cat_columns = [column for column in  self.df.columns if self.df[column].dtypes == object]
            for column in cat_columns:
                counts = self.df[column].value_counts(normalize=True)
                if (len(counts)) > unique_val_count:
                    l = list(counts.loc[counts< min_val_count_pctg].index)
                    self.df.loc[self.df[column].isin(l), column] = 'Others'
                    print(f'{column} - List of values replaced as "Others":', l)
                    _ = self.df.groupby(column).size().sort_values(ascending = False).to_frame('count').reset_index()
                    _['Percentage'] = (np.round(_['count']/_['count'].sum(), 3))*100
                    _['Percentage'] = _['Percentage'].map('{:,.2f}%'.format)
                    fig = px.bar(_, x = column, y = 'count', color = column, text=_['Percentage'], height = 600, width = 500, 
                                title = 'Plot of Values in {}'.format(column))
                    fig.update_layout(template = 'simple_white')                    
                    fig.show()
        except Exception as e:
            raise WallethubException(e, sys) from e

    
    def cat_manual_univariate_analysis(self, cols:list, unique_val_count:int = 0, min_val_count_pctg:float = 0.05, graph:str = 'bar'):
        try:
            cat_columns = cols            
            for column_name in cat_columns:            
                counts = self.df[column_name].value_counts(normalize=True)
                l = list(counts.loc[counts<min_val_count_pctg].index)
                self.df.loc[self.df[column_name].isin(l), column_name] = 'Others'
                _ = self.df.groupby(column_name).size().sort_values(ascending = False).to_frame('count').reset_index()
                _['Percentage'] = (np.round(_['count']/_['count'].sum(), 3))*100
                _['Percentage'] = _['Percentage'].map('{:,.2f}%'.format)
                if graph == 'bar':
                    fig = px.bar(_, x = column_name, y = 'count', color = column_name, text=_['Percentage'], height = 600, width = 500, 
                                title = 'Plot of Values in {}'.format(column_name))
                elif graph == 'pie':
                    fig = px.pie(_, names = column_name, color = column_name, values = 'count', height = 600, width = 500, 
                                    color_discrete_sequence = px.colors.qualitative.D3)

                fig.update_layout(template = 'simple_white')                    
                fig.show()
        except Exception as e:
            raise WallethubException(e, sys) from e

    
    def cat_auto_bivariate_analysis(self, target_column_name:str, unique_val_count:int = 3,min_val_count_pctg:float = 0.05):
        try:
            
            cat_columns = [column for column in  self.df.columns if self.df[column].dtypes == object]
            
            for column in cat_columns:                
                counts = self.df[column].value_counts(normalize=True)
                if (len(counts)) > unique_val_count:
                    l = list(counts.loc[counts<min_val_count_pctg].index)
                    self.df.loc[self.df[column].isin(l), column] = 'Others'
                    _ = self.df.groupby([target_column_name,column]).size().reset_index()
                    _['Percentage'] = (self.df.groupby([target_column_name, column]).size()
                                            .groupby(level = 0).apply(lambda x:100 * x / float(x.sum())).values)
                    _.columns = [target_column_name, column, 'Count', 'Percentage']
                    _['Percentage'] = _['Percentage'].map('{:,.2f}%'.format)
                    fig = px.bar(_, x = target_column_name, y = 'Count', color = column, text= _['Percentage'], height = 600, width = 500,
                                color_discrete_sequence=px.colors.qualitative.Bold)
                    fig.update_layout(template = 'simple_white')                    
                    fig.show()
            
        except Exception as e:
            raise WallethubException(e, sys) from e    
    

    def cat_manual_bivariate_analysis(self, target_column_name:str, cols:list, unique_val_count:int = 0, min_val_count_pctg:float = 0.05):
        try:
            if all == True:
                cat_columns = [column for column in  self.df.columns if self.df[column].dtypes == object]
            else:
                cat_columns = cols
            for column in cat_columns:
                counts = self.df[column].value_counts(normalize=True)
                if (len(counts)) > unique_val_count:
                    l = list(counts.loc[counts<min_val_count_pctg].index)
                    self.df.loc[self.df[column].isin(l), column] = 'Others'
                    _ = self.df.groupby([target_column_name,column]).size().reset_index()
                    _['Percentage'] = (self.df.groupby([target_column_name, column]).size()
                                            .groupby(level = 0).apply(lambda x:100 * x / float(x.sum())).values)
                    _.columns = [target_column_name, column, 'Count', 'Percentage']
                    _['Percentage'] = _['Percentage'].map('{:,.2f}%'.format)
                    fig = px.bar(_, x = target_column_name, y = 'Count', color = column, text= _['Percentage'], height = 600, width = 500,
                                color_discrete_sequence=px.colors.qualitative.Bold)
                    fig.update_layout(template = 'simple_white')                    
                    fig.show()
            
        except Exception as e:
            raise WallethubException(e, sys) from e



    def num_manual_univariate_analysis(self, cols:list, title:str, graph:str = 'bar'):
            try:
                num_columns = cols            
                for column_name in num_columns:            
                    _ = self.df.groupby(column_name).size().to_frame('count').reset_index()
                    _['Percentage_dec'] = (np.round(_['count']/_['count'].sum(), 3))*100
                    _['Percentage'] = _['Percentage_dec'].map('{:,.2f}%'.format)
                    if graph == 'bar':
                        fig = px.bar(_, x = column_name, y = 'count', color = column_name, text=_['Percentage'], height = 500, width = 800, 
                                    title = 'Plot of Values in {}'.format(column_name))
                    elif graph == 'pie':
                        fig = px.pie(_, names = column_name, color = column_name, values = 'count', height = 500, width = 800, 
                                        color_discrete_sequence = px.colors.qualitative.D3)

                    fig.update_layout(template = 'simple_white', 
                                    title = title)                    
                    fig.show()
            except Exception as e:
                raise WallethubException(e, sys) from e


    
    def num_manual_bivariate_analysis(self, target_column_name:str, cols:list, title:str):
        try:
            num_columns = cols
            for column in num_columns:
                    _ = self.df.groupby([target_column_name,column]).size().reset_index()
                    _['Percentage'] = (self.df.groupby([target_column_name, column]).size()
                                            .groupby(level = 0).apply(lambda x:100 * x / float(x.sum())).values)
                    _.columns = [target_column_name, column, 'Count', 'Percentage']
                    _['Percentage'] = _['Percentage'].map('{:,.2f}%'.format)
                    fig = px.bar(_, x = target_column_name, y = 'Count', color = column, text= _['Percentage'], height = 600, width = 500,
                                color_discrete_sequence=px.colors.qualitative.Bold)
                    fig.update_layout(template = 'simple_white', 
                                        title = title)                    
                    fig.show()
            
        except Exception as e:
            raise WallethubException(e, sys) from e

