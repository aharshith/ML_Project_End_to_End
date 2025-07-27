# Standard imports
import sys
import os
from dataclasses import dataclass

# Data manipulation and preprocessing
import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Custom modules for error handling and logging
from src.exception import CustomException
from src.logger import logging

# Utility to save objects as pickle files
from src.utils import save_object

# Configuration class to store file path for the preprocessor object
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', "proprocessor.pkl")  # Where to save preprocessor

# Main class for handling data transformation
class DataTransformation:
    def __init__(self):
        # Load the path config for the preprocessor
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function builds and returns a ColumnTransformer,
        which applies preprocessing steps to both numerical and categorical columns.
        '''
        try:
            # Define which columns are numerical and which are categorical
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # Pipeline for numerical features: median imputation + standard scaling
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            # Pipeline for categorical features: most frequent imputation + one-hot + scaling
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))  # with_mean=False required for sparse data
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            # Combine numerical and categorical pipelines into a single preprocessor
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor
        
        except Exception as e:
            # Raise custom exception for error tracing
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        '''
        Reads the train and test CSV files, applies the preprocessing pipeline,
        and returns transformed arrays along with the path to the saved preprocessor object.
        '''
        try:
            # Load training and testing data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("Obtaining preprocessing object")

            # Get the preprocessor object
            preprocessing_obj = self.get_data_transformer_object()

            # Define target column
            target_column_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]

            # Split input and target features
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on training and testing dataframes.")

            # Apply preprocessing: fit on train, transform both train and test
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combine processed features with target variable
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info("Saving preprocessing object as a pickle file")

            # Save the preprocessing object for later use (e.g., during prediction)
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            # Return transformed arrays and the preprocessor path
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
