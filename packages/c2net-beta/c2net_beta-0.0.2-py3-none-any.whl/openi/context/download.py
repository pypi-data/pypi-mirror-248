import os
import glob
from .env_check import dataset_to_env, pretrain_to_env, obs_copy_folder, unzip_dataset
from ..utils import constants

def prepare_dataset():
    moxing_required = os.getenv(constants.MOXING_REQUIRED)
    if moxing_required is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the {constants.MOXING_REQUIRED} environment variables.')
    if moxing_required == constants.MOXING_REQUIRED_TRUE:
            return prepare_dataset_for_obs()
    else:
        return prepare_dataset_for_minio()

def prepare_pretrain_model():
    moxing_required = os.getenv(constants.MOXING_REQUIRED)
    pretrain_model_path = os.getenv(constants.PRETRAIN_MODEL_PATH)
    if moxing_required is None or pretrain_model_path is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the {constants.MOXING_REQUIRED} and {constants.PRETRAIN_MODEL_PATH} environment variables.')
    else:
        if not os.path.exists(pretrain_model_path):
            os.makedirs(pretrain_model_path) 
    if moxing_required == constants.MOXING_REQUIRED_TRUE:
            return prepare_pretrain_model_for_obs()
    return pretrain_model_path

def prepare_output_path():
    output_path = os.getenv(constants.OUTPUT_PATH)
    if output_path is None:
            raise ValueError(f'Failed to obtain environment variables. Please set the {constants.OUTPUT_PATH} environment variables.')
    else:	
        if not os.path.exists(output_path):	
            os.makedirs(output_path)   
    print(f'please set openi_context.output_path as the output location')
    return output_path

def prepare_dataset_for_obs():
    dataset_url = os.getenv(constants.DATASET_URL)
    dataset_path = os.getenv(constants.DATASET_PATH)
    unzip_required = os.getenv(constants.UNZIP_REQUIRED, constants.UNZIP_REQUIRED_FALSE)

    if dataset_url is None or dataset_path is None:
        raise ValueError(f'Failed to obtain environment variables.Please set the {constants.PRETRAIN_MODEL_URL} and {constants.DATASET_PATH} environment variables')
    else:
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)

    if dataset_url != "":
        dataset_to_env(dataset_url, dataset_path, unzip_required)
    else:
        print(f'No dataset selected')       
    return dataset_path

def prepare_pretrain_model_for_obs():
    pretrain_model_url = os.getenv(constants.PRETRAIN_MODEL_URL)
    pretrain_model_path= os.getenv(constants.PRETRAIN_MODEL_PATH)
    if pretrain_model_url is None or pretrain_model_path is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the {constants.PRETRAIN_MODEL_URL} and {constants.PRETRAIN_MODEL_PATH} environment variables.')
    else:
        if not os.path.exists(pretrain_model_path):
            os.makedirs(pretrain_model_path) 
    if pretrain_model_url != "":             
        pretrain_to_env(pretrain_model_url, pretrain_model_path)
    else:
        print(f'No pretrainmodel selected')           
    return pretrain_model_path   

def prepare_output_path_for_obs():	
    output_path = os.getenv(constants.OUTPUT_PATH)	
    if output_path is None:	
        raise ValueError(f'Failed to obtain environment variables. Please set the {constants.OUTPUT_PATH} environment variables.')  
    print(f'please set openi_context.output_path as the output location')
    return output_path 	

def prepare_dataset_for_minio():
    dataset_path = os.getenv(constants.DATASET_PATH)
    unzip_required = os.getenv(constants.UNZIP_REQUIRED, constants.UNZIP_REQUIRED_FALSE)
    if dataset_path is None or unzip_required is None:
        raise ValueError(f'Failed to obtain environment variables. Please set the {constants.DATASET_PATH} and thr {constants.UNZIP_REQUIRED}environment variables.')
    else:
        if not os.path.exists(dataset_path):
            os.makedirs(dataset_path)
    if unzip_required == constants.UNZIP_REQUIRED_TRUE:
        path = os.path.join(dataset_path, "*")
        for filename in glob.glob(path):
            if filename.endswith('.zip') or filename.endswith('.tar.gz'):
                base = os.path.basename(filename)
                dirname = os.path.splitext(base)[0]
                target_path = os.path.join(dataset_path, dirname)
                unzip_dataset(filename, target_path)
    return dataset_path    

