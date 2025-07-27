# Standard library imports
import os
import sys
import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

# Custom exception and logging (from your own project structure)
from src.exception import CustomException
from src.logger import logging

# Importing data transformation and model trainer components
from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_trainer import ModelTrainer, ModelTrainerConfig

# Configuration class to store paths for data files using @dataclass
@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")  # Path to save training data
    test_data_path: str = os.path.join('artifacts', "test.csv")    # Path to save testing data
    raw_data_path: str = os.path.join('artifacts', "data.csv")     # Path to save raw data

# Main class that handles data ingestion process
class DataIngestion:
    def __init__(self):
        # Initialize with configuration for paths
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # Read the input dataset
            df = pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the dataset as dataframe')

            # Create the artifacts directory if it doesn't exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Save the raw data to file
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # Perform train-test split
            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save the train and test datasets to file
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            # Return paths of the generated train and test files
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            # Raise a custom exception if any error occurs
            raise CustomException(e, sys)

# Main script execution block
if __name__ == "__main__":
    # STEP 1: Data Ingestion
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    # STEP 2: Data Transformation (scaling, encoding, etc.)
    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)

    # STEP 3: Model Training and Evaluation
    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))
