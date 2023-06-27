import intialize
from user import User
import images
import reports
import payments
import os
import close_program
import helper_functions
import sql_functions
import scheduler

mydb = intialize.get_db()
cursor = mydb.get_mydb().cursor()


def add_user():

    email_input = input("Enter email address: ")
    if not helper_functions.is_valid_email(email_input):
        print("invalid email")
        return

    does_exist = sql_functions.check_if_user_exists(email_input)
    if does_exist:
        print("this user already exists, try a different email")
        return

    user_name = input("Enter username: ")
    does_exist = sql_functions.check_if_username_exists(user_name)
    if does_exist:
        print("this user name already exists, try a different user name")
        return
    password = input("Enter password: ")

    while not helper_functions.is_valid_password(password):
        password = input("try again...enter a password")

    insert_user_to_SQL_database(email_input, password, user_name)

    print("User added successfully.")
    sign_in(user_name,password)
    return


def insert_user_to_SQL_database(email_input, password, user_name):
    # insert user to SQL database
    user_id = sql_functions.insert_new_user(user_name, password, email_input)
    # insert payment to SQL database
    sql_functions.insert_new_payment(user_id)
    payment_ = payments.Payment(user_id)
    mydb.get_payments_dict()[payment_.get_payment_id()] = payment_
    user_ = sql_functions.retrieve_user_record(user_id)
    # create new user add to RAM
    created_at = user_[4]
    user = User(user_id, user_name, password, email_input, created_at, 'No', [], [], payment_)
    mydb.get_users_dict()[user_id] = user
    mydb.get_mydb().commit()


def sign_in(user_name=None, password=None):
    if user_name is None:
        user_name = input("Enter username: ")
    if password is None:
        password = input("Enter password: ")

    if sql_functions.is_user_connected(user_name):
        print(f"{user_name} is already connected")
        return

    result = sql_functions.check_user_credentials(cursor, user_name, password)
    if result is not None:
        print("Login successful!")
        print(f"user {user_name} has signed in")
        # update the is_connected field for all users to 'No'
        id_ = sql_functions.update_users_is_connected()
        if id_:
            mydb.get_users_dict()[id_].set_is_connected('No')
        # update the is_connected field for the current user to 'Yes' in the database
        sql_functions.update_is_connected(user_name)
        id_ = sql_functions.get_user_id(user_name)
        if id_:
            mydb.get_users_dict()[id_].set_is_connected('Yes')
    else:

        print("Incorrect username and/or password.")
    return


def upload_a_new_image():
    user_id = helper_functions.check_if_user_is_connected()
    if not user_id:
        return

    user_ = mydb.get_users_dict()[user_id]
    # get a list of all images that haven't been uploaded yet, and add the images that the user has already uploaded
    new_list = [elem for elem in list(mydb.get_all_initial_available_images().keys()) if elem not in mydb.get_uploaded_images_list()]
    if len(new_list) == 0:
        print("all available images have been uploaded already")
        return

    display_list = get_file_name_by_id(new_list)
    print("available images id: ", display_list)
    image_id = int(input("enter the id of the image you want to upload: "))
    if image_id not in mydb.get_all_initial_available_images().keys():
        print("no image with that id")
        return

    elif image_id in mydb.get_uploaded_images_list():
        img = mydb.get_images_dict()[image_id]
        print( f"that image was already uploaded by user {img.get_uploaded_user_name()}")
        return

    file_path, filename = get_image_filepath_and_name(image_id)
    name_ = user_.get_username()
    upload_and_update_image_to_SQL(file_path, filename, image_id, name_, user_id)
    update_amount(user_, user_id,intialize.cost_of_upload)
    #add payment due to the end of the current month
    helper_functions.add_payment_due(scheduler.last_day, user_)
    create_and_upload_image_to_RAM(file_path, filename, image_id, user_)
    print(f"{name_} has uploaded image {image_id} successfully!")


def get_file_name_by_id(new_list):
    file_names = [mydb.get_all_initial_available_images()[key] for key in new_list]
    zipped_list = list(zip(new_list, file_names))
    display_list = []
    for elem in zipped_list:
        display_list.append(str(elem[0]) + ' - ' + elem[1])
    print("enter the corresponding file name id")
    return display_list


def create_and_upload_image_to_RAM(file_path, filename, image_id, user_):
    user_.upload_image(image_id)
    mydb.get_uploaded_images_list().append(image_id)
    img = images.My_Image(image_id, filename, file_path, helper_functions.get_current_time(), user_.get_username(),
                          helper_functions.get_current_time(),
                          [], [])
    mydb.get_images_dict()[image_id] = img


def update_amount(user_, user_id,upload_or_download):
    amount_ = sql_functions.get_amount_from_db(user_id)
    amount_ += upload_or_download
    user_.get_payment().set_amount(amount_)
    sql_functions.update_user_payment(amount_, scheduler.last_day, user_id)


def upload_and_update_image_to_SQL(file_path, filename, image_id, name_, user_id):
    sql_functions.upload_image_to_sql(image_id, user_id, filename, file_path, name_)
    sql_functions.update_user_uploaded_downloaded_images(image_id, user_id, 'images_uploaded_ids')
    sql_functions.set_uploaded_at(image_id)


def get_image_filepath_and_name(image_id):
    filename = mydb.get_all_initial_available_images()[image_id]
    # Get the path to the images directory from the `initialize` module.
    path_to_images = intialize.path_to_images
    # Join the path to the images directory and the filename to get the full file path.
    file_path = os.path.join(path_to_images, filename)
    file_path = file_path.replace('\\', '/')
    return file_path, filename


def download_an_image():

    user_id = helper_functions.check_if_user_is_connected()
    if not user_id:
        return

    user_ = mydb.get_users_dict()[user_id]
    if len(mydb.get_uploaded_images_list()) == 0:
        print("no images to download, images need to be uploaded first")
        return

    display_list = get_file_name_by_id(mydb.get_uploaded_images_list())
    print(f"choose an image to download: {display_list}")
    image_id = int(input("enter the id of the image you want to download: "))
    if image_id not in mydb.get_uploaded_images_list():
        print("no image with that id")
        return

    name_ = user_.get_username()
    download_and_update_image(image_id, name_, user_id)
    update_amount(user_, user_id, intialize.cost_of_download)
    # add payment due to the end of the current month
    helper_functions.add_payment_due(scheduler.last_day, user_)
    # add user's downloaded image
    user_.download_image(image_id)
    update_image_details_to_RAM(image_id, name_)
    print(f"{name_} has downloaded image {image_id} successfully!")


def update_image_details_to_RAM(image_id, name_):
    img = mydb.get_images_dict()[image_id]
    img.set_downloaded_user_name(name_)
    img.set_downloaded_time(helper_functions.get_current_time())
    if not image_id in mydb.get_downloaded_images_list():
        img.copy_image_to_new_directory(img.get_file_path(), intialize.directory)
    mydb.get_downloaded_images_list().append(image_id)


def download_and_update_image(image_id, name_, user_id):
    sql_functions.update_user_uploaded_downloaded_images(image_id, user_id, 'images_downloaded_ids')
    sql_functions.set_image_downloaders(name_, image_id)
    sql_functions.set_image_download_time(image_id)


def print_all_payment_details():
    if len(mydb.get_payments_dict())==0:
        print("there are no payments for any user")
    for payment_ in mydb.get_payments_dict().values():
        print(payment_.print_payment_details(mydb.get_users_dict()[payment_.get_payment_id()].get_username()))
        print(mydb.get_users_dict()[payment_.get_payment_id()].get_pricing(intialize.cost_of_upload,intialize.cost_of_download))
    return


def print_all_uploaded_images_details():
    if len(mydb.get_uploaded_images_list()) == 0:
        print("no images have been uploaded yet")
    else:
        for uploaded_image_id in set(mydb.get_uploaded_images_list()):
            print(f"image id: {uploaded_image_id}, uploaded by user {mydb.get_images_dict()[uploaded_image_id].get_uploaded_user_name()}, at {mydb.get_images_dict()[uploaded_image_id].get_uploaded_time()}")
    return


def print_all_image_details():
    if len(mydb.get_images_dict())==0:
        print("no images uploaded yet")
    for image_ in mydb.get_images_dict().values():
        image_.print_image_details()
    return


def print_all_downloaded_images_details():
    if len(mydb.get_downloaded_images_list()) == 0:
        print("no images have been downloaded yet")
    else:
        for image_ in mydb.get_images_dict().values():
            print(f"image id: {image_.get_id()}")
            for i,user_ in enumerate(image_.get_downloaded_user_name()):
                print(f"downloaded by {user_} at:  {image_.get_downloaded_time()[i]}")
    return


def print_all_user_details():
    if len(mydb.get_users_dict()) == 0:
        print("no users added yet")
    for user in mydb.get_users_dict().values():
        user.print_user_details()
        print('')


def display_report():
    reports.Report(mydb)
    return


def display_image():
    user_id = helper_functions.check_if_user_is_connected()
    if not user_id:
        return

    user_ = mydb.get_users_dict()[user_id]
    new_list = list(set(user_.get_downloaded_images() + user_.get_uploaded_images()))
    if len(new_list) == 0:
        print(f"{user_.get_username()} has no images to display, please upload or download images")
        return

    display_list = get_file_name_by_id(new_list)
    print(f"choose an image to disply: {display_list}")
    image_id = int(input("enter the id of the image you want to display: "))
    if image_id not in new_list:
        print("no image with that id, upload it or download it to display it")
        return

    print("displaying image....this may take a moment")
    img = mydb.get_images_dict()[image_id]
    try:
        path = img.get_file_path()
        img.display_image(path)
    except Exception as e:
        print(f"An error occurred while trying to display image in path:  {e}")


def close_program_main():
    sql_functions.close_program()
    close_program.delete_download_images_directory()
    print("Goodbye!")


