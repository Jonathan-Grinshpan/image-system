from PIL import Image
import shutil


class My_Image:
    def __init__(self, id, filename, file_path, created_at,uploader,uploaded_time,downloaders,download_at):
        self.id = id
        self.filename = filename
        self.file_path = file_path
        self.uploaded_user_name = uploader
        self.downloaded_user_name = downloaders
        self.uploaded_time = uploaded_time
        self.downloaded_time = download_at
        self.created_at = created_at

    def copy_image_to_new_directory(self, img_path,directory):
        img_path = img_path.replace('\\', '/')
        shutil.copy(img_path, directory)


    def display_image(self,path):
        img = Image.open((path))
        img.show()

    # Getters
    def get_id(self):
        return self.id

    def get_filename(self):
        return self.filename

    def get_file_path(self):
        return self.file_path

    def get_uploaded_user_name(self):
        return self.uploaded_user_name

    def get_downloaded_user_name(self):
        return self.downloaded_user_name

    def get_uploaded_time(self):
        return self.uploaded_time

    def get_downloaded_time(self):
        return self.downloaded_time

    def get_created_at(self):
        return self.created_at

    # Setters
    def set_id(self, id):
        self.id = id

    def set_filename(self, filename):
        self.filename = filename

    def set_file_path(self, file_path):
        self.file_path = file_path

    def set_uploaded_user_name(self, uploaded_user_name):
        self.uploaded_user_name = uploaded_user_name

    def set_downloaded_user_name(self, downloaded_user_name):
        self.downloaded_user_name.append(downloaded_user_name)

    def set_uploaded_time(self, uploaded_time):
        self.uploaded_time = uploaded_time

    def set_downloaded_time(self, downloaded_time):
        self.downloaded_time.append(downloaded_time)

    def set_created_at(self, created_at):
        self.created_at = created_at

    def print_image_details(self):
        print(f'ID: {self.id}')
        print(f'Filename: {self.get_filename()}')
        print(f'File path: {self.get_file_path()}')
        print(f'uploader: {self.get_uploaded_user_name()}')
        print(f'uploaded at: {self.get_uploaded_time()}')
        print(f'downloaders: {(self.get_downloaded_user_name())}')
        print(f'downloaded at: {self.get_downloaded_time()}')
        print(f'inserted into sql server at: {self.get_created_at()}')

    def print_id(self):
        print(self.id)
