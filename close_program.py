import intialize
import shutil


def delete_download_images_directory():
    try:
        directory = intialize.directory
        shutil.rmtree(directory)
    except Exception as e:
        print("An error occurred while removing the directory: ", e)