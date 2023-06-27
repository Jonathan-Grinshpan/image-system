
import sql_functions

class Databases:
    def __init__(self):

        self.mydb = sql_functions.mydb_connector
        self.users_dict = {}
        self.images_dict = {}
        self.uploaded_images_list = []
        self.downloaded_images_list = []
        self.all_initial_available_images = {}
        self.payments_dict = {}



    def get_all_initial_available_images(self):
        return  self.all_initial_available_images

    def get_payments_dict(self):
        return self.payments_dict

    def get_mydb(self):
        return self.mydb

    def get_users_dict(self):
        return self.users_dict

    def get_images_dict(self):
        return self.images_dict

    def get_uploaded_images_list(self):
        return self.uploaded_images_list

    def get_downloaded_images_list(self):
        return self.downloaded_images_list