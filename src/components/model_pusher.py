import sys
import os
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from src.entity.config_entity import ModelPusherConfig
import dagshub

class ModelPusher:
    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact,
                 model_pusher_config: ModelPusherConfig):
        """
        :param model_evaluation_artifact: Output reference of data evaluation artifact stage
        :param model_pusher_config: Configuration for model pusher
        """
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Method Name :   initiate_model_evaluation
        Description :   This function is used to initiate all steps of the model pusher
        
        Output      :   Returns model evaluation artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered initiate_model_pusher method of ModelPusher class")

        try:
            print("------------------------------------------------------------------------------------------------")
            logging.info("Pushing trained model to Dagshub...")
            
            trained_model_path = self.model_evaluation_artifact.trained_model_path
            destination_path = self.model_pusher_config.model_deploy_path

            # Create the necessary directory structure if it doesn't exist
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

            # Copy the model file to the destination path
            dagshub.dagshub_fs.upload(local_path=trained_model_path, remote_path=destination_path)

            model_pusher_artifact = ModelPusherArtifact(model_deploy_path=destination_path)

            logging.info("Model pushed to Dagshub.")
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logging.info("Exited initiate_model_pusher method of ModelPusher class")
            
            return model_pusher_artifact
        except Exception as e:
            raise MyException(e, sys) from e