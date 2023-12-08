
import os
import wget
import zipfile


def download_file(path_dir):

    """
    Download model form huggingface
    
    """

    model_url = "https://huggingface.co/saiful9379/BanglaNER/resolve/main/bangla_ner_model.zip?download=true"

    os.makedirs(path_dir, exist_ok=True)

    model_path = os.path.join(path_dir, "bangla_ner_model.zip")

    model_dir = ""

    if os.path.exists(model_path):
       print("Model already exits, if you download again delete the bangla_ner_model.zip file from models folder\n")
       model_dir = os.path.join(path_dir, "bangla_ner_model")
    else:
        try:
            wget.download(model_url, out=path_dir)
            zip_file_path = os.path.join(path_dir, "bangla_ner_model.zip")

            print("\n Unzip model file processing ..... ", end="", flush=True)
            if os.path.exists(zip_file_path):
                try:
                    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                        zip_ref.extractall(path_dir)
                        model_dir = os.path.join(path_dir, "bangla_ner_model")
                    print("Done")
                except Exception as e:
                    print("Please delete the corrupted zip file and download again")
                    print("Or manually download bangla_ner_model.zip model form the url: https://huggingface.co/saiful9379/BanglaNER/tree/main")
                    print("And put into models directory and unzip")
            else:
                print("Model zip file not found")
        except Exception as e:
            print("Please delete the corrupted zip file and download again")
            print("Or manually download bangla_ner_model.zip model form the url: https://huggingface.co/saiful9379/BanglaNER/tree/main")
            print("And put into models directory and unzip")

    if model_dir:
        os.remove(model_path)        
    return model_dir


if __name__ == "__main__":
  path_dir = "models"
  model_dir = download_file(path_dir)
