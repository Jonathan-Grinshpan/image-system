
class User:
    def __init__(self, id,username, password,email,created_at,is_connected,images_uploaded,images_downlaoded,payment):
        self.username = username
        self.password = password
        self.email = email
        self.id = id
        self.created_at = created_at
        self.is_connected = is_connected
        self.images_uploaded = images_uploaded
        self.images_downloaded = images_downlaoded
        self.payment = payment

    def get_pricing(self,cost_of_upload,cost_of_download):
        if self.payment.get_amount() >0:

            print(f"amount reasoning: number of uploaded images * price of upload({cost_of_upload}) + "
                  f"number of downloaded images * price of download({cost_of_download}) = {len(self.get_uploaded_images())}*3 + {len(self.get_downloaded_images())}*5 = "
                  f"{len(self.get_uploaded_images()) *cost_of_upload + len(self.get_downloaded_images())*cost_of_download}")
        return ''

    def get_payment(self):
        return self.payment

    def set_payment(self,payment_):
        self.payment = payment_

    def upload_image(self,img):
        self.images_uploaded.append(img)

    def download_image(self,img):
        self.images_downloaded.append(img)

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_uploaded_images(self):
        return self.images_uploaded

    def get_downloaded_images(self):
        return self.images_downloaded

    def get_email(self):
        return self.email

    def get_id(self):
        return self.id

    def get_created_at(self):
        return self.created_at

    def set_is_connected(self,connect):
        self.is_connected = connect

    def print_user_details(self):
        print(f"User ID: {self.id}")
        print(f"Username: {self.username}")
        print(f"Password: {self.password}")
        print(f"Email: {self.email}")
        print(f"Is Connected: {self.is_connected}")
        print(f"created at : {self.created_at}")
        images_uploaded_ = self.images_uploaded if len(self.images_uploaded) > 0 else "No images uploaded"
        print(f"uploaded images id : {images_uploaded_}")

        images_downloaded_ = self.images_downloaded if len(self.images_downloaded) > 0 else "No images downloaded"
        print(f"downloaded images id : {images_downloaded_}")

        payment_ = self.get_payment()
        print("No payment information found" if payment_ is None else f"has payment been paid? {payment_.get_has_been_paid()}")



