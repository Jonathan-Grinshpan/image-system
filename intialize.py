import user
import databases
import os
import images
import payments
import close_program


db = databases.Databases()
mycurser = db.get_mydb().cursor()

path_to_images = 'C:/Users/User/PycharmProjects/test/images'
# Setting the directory where downloaded images will be saved
directory = "C:/Users/User/PycharmProjects/test/downloaded_images"

cost_of_upload = 3
cost_of_download = 5


def init():
    init_payments_from_SQL_to_RAM()
    init_users_to_RAM()
    load_images_to_db_obj()
    init_images_fromSQL_to_RAM()
    init_downlaods_directory()


def get_db():
    return db


def init_downlaods_directory():
    # Check if the downloaded images directory exists
    if not os.path.exists(directory):
        # Create the directory if it does not exist
        os.makedirs(directory)


def init_images_fromSQL_to_RAM():
    # Initialize all images to RAM
    mycurser.execute("SELECT * FROM IMAGES")
    all_images = mycurser.fetchall()
    for image_ in all_images:
        # Store the list of users who downloaded the image and the corresponding timestamps
        downloaders = image_[6].split(',') if image_[6] is not '' else []
        downloaded_at = image_[7].split(',') if image_[7] is not '' else []
        # Create a new My_Image object and store it in a dictionary
        new_image = images.My_Image(image_[0], image_[1], image_[2], image_[3], image_[4], image_[5], downloaders,
                                    downloaded_at)
        db.get_images_dict()[image_[0]] = new_image
        # if downloaders is not []:
        #     new_image.copy_image_to_new_directory(new_image.get_file_path(), directory)

def load_images_to_db_obj():
    image_files = os.listdir(path_to_images)
    for i, file in enumerate(image_files):
        # Store the image file names in a dictionary
        db.all_initial_available_images[i + 1] = file



def init_users_to_RAM():
    mycurser.execute("SELECT * FROM USERS")
    users = mycurser.fetchall()
    for user_ in users:
        # Store the list of uploaded images ids for the user
        images_uploaded_id = user_[6].split(',') if user_[6] is not None else []
        images_uploaded_id = [int(x) for x in images_uploaded_id if x]
        # Store the list of downloaded images ids for the user
        images_downloaded_id = user_[7].split(',') if user_[7] is not None else []
        images_downloaded_id = [int(x) for x in images_downloaded_id if x]
        # Get the payment information for the user
        payment_info = db.get_payments_dict().get(user_[0], None)
        # Create a new User object and store it in a dictionary
        new_user = user.User(user_[0], user_[1], user_[2], user_[3], user_[4], user_[5], images_uploaded_id,
                             images_downloaded_id, payment_info)
        db.get_users_dict()[user_[0]] = new_user
        # Add the list of uploaded and downloaded image ids to corresponding lists
        db.get_uploaded_images_list().extend(images_uploaded_id)
        db.get_downloaded_images_list().extend(images_downloaded_id)


def init_payments_from_SQL_to_RAM():
    mycurser.execute("SELECT * FROM PAYMENTS")
    payments_ = mycurser.fetchall()
    for payment_ in payments_:
        pay = payments.Payment(payment_[0], payment_[1], payment_[2], payment_[3])
        # Store the payment information in a dictionary
        db.get_payments_dict()[payment_[0]] = pay

