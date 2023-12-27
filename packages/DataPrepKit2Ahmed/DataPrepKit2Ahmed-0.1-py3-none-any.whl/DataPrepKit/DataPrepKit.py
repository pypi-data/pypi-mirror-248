"""
DataPrepKit Capstone Project

In the DataPrepKit capstone project, students will create a Python package that serves as a comprehensive toolkit for preprocessing datasets. Leveraging their knowledge of NumPy and Pandas, students will design functions to seamlessly read data from various file formats, provide a data summary, handle missing values, and encode categorical data. The final deliverable will be a published package on PyPI under the name "DataPrepKit."

Key Features:
1. Data Reading: Implement functions to read data from different file formats such as CSV, Excel, and JSON, using Pandas.
2. Data Summary: Develop functions that print key statistical summaries of the data, including the average and most frequent values, utilizing NumPy and Pandas.
3. Handling Missing Values: Create functions to handle missing values by either removing or imputing them based on predefined strategies.
4. Categorical Data Encoding: Implement encoding functions for categorical variables, enabling users to convert them into numerical representations.
5. Package Deployment: Publish the DataPrepKit package on PyPI to make it easily accessible to the broader Python community.

Project Requirements:
1. Efficient utilization of NumPy and Pandas for data manipulation and analysis.
2. Implementation of robust functions for data reading, summary generation, missing value handling, and categorical data encoding.
3. Successful registration and deployment of the package on PyPI.

Evaluation Criteria:
* Functionality and correctness of the implemented data preprocessing features.
* Quality and completeness of the documentation.
* Effectiveness of the test suite in ensuring the reliability of the package.
* Successful deployment of the package on PyPI.
* Adherence to best practices in coding, packaging, and testing.
* Creativity and efficiency in addressing different file formats and data preprocessing challenges.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder,OrdinalEncoder,OneHotEncoder , StandardScaler,MinMaxScaler,RobustScaler,Normalizer
from sklearn.impute import SimpleImputer,KNNImputer

class DataPrepKit:

        def __init__(self, data=None, file_path=None, file_type='csv'):
            if data is not None:
                self.data = data
            elif file_path is not None:
                self.read_data(file_path, file_type)

        def read_data(self, file_path, file_type):
            if file_type == "csv":
                self.data = pd.read_csv(file_path)
            elif file_type == "excel":
                self.data = pd.read_excel(file_path)
            elif file_type == "json":
                self.data = pd.read_json(file_path)
            else:
                raise ValueError("Invalid file type. Please enter a valid file type.")

        def data_summary(self):
            print("Data Summary")
            print("============")
            print("Shape: {}".format(self.data.shape))
            print("Head:")
            print(self.data.head())
            print("Tail:")
            print(self.data.tail())
            print("Data Info:")
            print(self.data.info())
            print("Missing Values:")
            print(self.data.isnull().sum())
            print("Unique Values:")
            print(self.data.nunique())
            for col in self.data.columns:
                if pd.api.types.is_numeric_dtype(self.data[col]):
                    print(f"Column: {col}")
                    print("Mean:", np.mean(self.data[col]))
                    print("Median:", np.median(self.data[col]))
                    print("Mode:", self.data[col].mode()[0])
                    print("Standard Deviation:", np.std(self.data[col]))
                    print("Minimum Value:", np.min(self.data[col]))
                    print("Maximum Value:", np.max(self.data[col]))
                else:
                    print(f"Column: {col}")
                    print("Most Frequent Value:", self.data[col].mode()[0])
                    print("Value Counts:", self.data[col].value_counts())

        def drop_duplicates(self):
            self.data.drop_duplicates(inplace=True)

        def encode_categorical(self, columns, method):
            if not set(columns).issubset(self.data.columns):
                raise KeyError(f"One or more columns {columns} are not present in the DataFrame.")
            
            if method == "label":
                encoder = LabelEncoder()
            elif method == "ordinal":
                encoder = OrdinalEncoder()
            elif method == "one-hot":
                encoder = OneHotEncoder()
            else:
                raise ValueError("Invalid encoding method. Please enter a valid encoding method.")

            self.data[columns] = encoder.fit_transform(self.data[columns])

        def scale_data(self, columns, method):
            if method == "standard":
                scaler = StandardScaler()
            elif method == "min-max":
                scaler = MinMaxScaler()
                
            elif method == "robust":
                scaler = RobustScaler()
            elif method == "normalizer":
                scaler = Normalizer()
            else:
                raise ValueError("Invalid scaling method. Please enter a valid scaling method.")
            
            self.data[columns] = scaler.fit_transform(self.data[columns])
            
        def impute_data(self, columns=None, method='mean'):
            imputer = None
            if columns is None:
                columns = self.data.select_dtypes(include=[np.number]).columns
            if method == "dropna":
                self.data.dropna(subset=columns, inplace=True)
            elif method == "mean":
                imputer = SimpleImputer(strategy="mean")
            elif method == "median":
                imputer = SimpleImputer(strategy="median")
            elif method == "most-frequent":
                imputer = SimpleImputer(strategy="most_frequent")
            elif method == "knn":
                imputer = KNNImputer()
            else:
                raise ValueError("Invalid imputation method. Please enter a valid imputation method.")
            if imputer is None:
                return self.data
            else:
                for col in columns:
                    if pd.api.types.is_numeric_dtype(self.data[col]):
                        self.data[col] = imputer.fit_transform(self.data[[col]])
                    else:
                        self.data[col] = imputer.fit_transform(self.data[[col]])


        def drop(self, rows=None, columns=None):
            if rows is not None:
                self.data.drop(rows, inplace=True)
            if columns is not None:
                self.data.drop(columns, axis=1, inplace=True)
