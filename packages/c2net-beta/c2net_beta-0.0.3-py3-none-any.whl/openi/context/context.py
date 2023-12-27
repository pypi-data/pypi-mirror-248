from .download import prepare_dataset, prepare_pretrain_model, prepare_output_path
from .upload import upload_output

class OpeniContext:
    """
    Args:
        dataset_path:           The storage path of the dataset
        pretrain_model_path:    The storage path of the pretrain model
        output_path:            The storage path of the output
    """
    def __init__(self, dataset_path, pretrain_model_path, output_path):
        self.dataset_path = dataset_path
        self.pretrain_model_path = pretrain_model_path
        self.output_path = output_path
        
def prepare():
    """
    Prepare the dataset, pretrain model and output path
    """
    dataset_path = prepare_dataset()
    pretrain_model_path = prepare_pretrain_model()
    output_path = prepare_output_path()
    t = OpeniContext(dataset_path, pretrain_model_path, output_path)
    return t

def upload_openi():
    """
    Upload the output to openi
    """
    return upload_output()    
