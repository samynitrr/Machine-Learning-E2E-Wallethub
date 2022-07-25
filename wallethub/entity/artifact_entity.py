from collections import namedtuple


DataIngestionArtifact = namedtuple("DataIngestionArtifact",["train_file_path","test_file_path",
                                                            "is_ingested","message"])

DataValidationArtifact = namedtuple("DataValidationArtifact", ["schema_file_path",
                                                                "report_file_path",
                                                                "report_page_file_path",
                                                                "is_validated",
                                                                "is_data_drift_found",
                                                                 "message"])

DataTransformationArtifact = namedtuple("DataTransformationArtifact",["is_transformed","message",
                                                                "transformed_train_file_path",
                                                                "transformed_test_file_path",
                                                                "preprocessed_object_file_path"])

ModelTrainerArtifact = namedtuple("ModelTrainerArtifact", ["is_trained", "message", "trained_model_file_path","model_name",
                                                           "train_rmse", "test_rmse","train_mae", "test_mae","train_mape", "test_mape",
                                                           "train_accuracy", "test_accuracy", "model_rmse", "model_mae", "model_mape", "model_accuracy"])

ModelEvaluationArtifact = namedtuple("ModelEvaluationArtifact", ["is_model_accepted", "evaluated_model_path"])

ModelPusherArtifact = namedtuple("ModelPusherArtifact", ["is_model_pusher", "export_model_file_path"])

