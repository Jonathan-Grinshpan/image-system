
import mysql.connector

try:
    mydb_connector = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        port='3306',
        database='user_administration',

    )
except Exception as e:
    print(f"error connecting to mysql database {e}")
    exit(1)


cursor =mydb_connector.cursor()


def close_program():
    try:
        cursor.execute("DELETE FROM users")
        mydb_connector.commit()
        cursor.execute("DELETE FROM images")
        mydb_connector.commit()
        cursor.execute("DELETE FROM payments")
        mydb_connector.commit()
    except Exception as e:
        print("An error occurred while closing the program: ", e)


def check_if_user_exists(email_input):
    try:
        cursor.execute("SELECT * FROM users WHERE BINARY email = %s", (email_input,))
        check_if_email_exists = cursor.fetchone()
        return check_if_email_exists
    except Exception as e:
        print("An error occurred while checking if user exists: ", e)
        return None


def check_if_username_exists(user_name):
    try:
        cursor.execute("SELECT * FROM users WHERE BINARY user_name = %s", (user_name,))
        check_if_user_name_exists = cursor.fetchone()
        return check_if_user_name_exists
    except Exception as e:
        print("An error occurred while checking if username exists: ", e)
        return None


def insert_new_user(user_name, password, email_input):
    try:
        cursor.execute("INSERT INTO users (user_name, password, email, created_at) VALUES (%s, %s, %s, NOW())", (user_name, password, email_input))
        mydb_connector.commit()
        # Get the ID of the newly inserted user
        return cursor.lastrowid
    except Exception as e:
        print("An error occurred while inserting new user: ", e)
        return None


def retrieve_user_record(user_id):
    try:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_record = cursor.fetchone()
        return user_record
    except Exception as e:
        print("An error occurred while retrieving user record: ", e)
        return None


def insert_new_payment(user_id):
    try:
        cursor.execute("INSERT INTO payments (payment_id, payment_due, amount, has_been_paid) VALUES (%s, %s, %s, %s)", (user_id, None, 0, 'Yes'))
        mydb_connector.commit()
    except Exception as e:
        print("An error occurred while inserting new payment: ", e)
        return None


def check_user_credentials(cursor, user_name, password):
    try:
        cursor.execute("SELECT * FROM users WHERE user_name = %s AND password = %s", (user_name, password))
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Error in check_user_credentials: {e}")
        return None


def is_user_connected(user_name):
    try:
        sql = "SELECT id FROM users WHERE user_name = %s AND is_connected = 'Yes'"
        cursor.execute(sql, (user_name,))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        print(f"Error in is_user_connected: {e}")
        return False


def get_id_from_connected_user():
    try:
        sql = "SELECT id FROM users WHERE is_connected = 'Yes'"
        cursor.execute(sql)
        result = cursor.fetchone()
        id_ = result[0] if result is not None else None
        return id_
    except Exception as e:
        print(f"Error in get_id_from_connected_user: {e}")
        return None


def update_users_is_connected():
    try:
        id_ = get_id_from_connected_user()
        if id_:
            cursor.execute(f"UPDATE users SET is_connected = 'No' WHERE id = '{id_}'")
            mydb_connector.commit()
            return id_
        return None
    except Exception as e:
        print(f"Error in update_users_is_connected: {e}")
        return None


def update_is_connected(user_name):
    try:
        sql = "UPDATE users SET is_connected = 'Yes' WHERE user_name = %s"
        cursor.execute(sql, (user_name,))
        mydb_connector.commit()
    except Exception as e:
        print(f"Error in update_is_connected: {e}")


def get_user_id(user_name):
    try:
        sql = "SELECT id FROM users WHERE user_name = %s"
        cursor.execute(sql, (user_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error in get_user_id: {e}")
        return None


def update_user_uploaded_downloaded_images(image_id, user_id, upload_or_download):
    try:
        sql = "UPDATE users SET {} = CONCAT(IF(LENGTH({}) > 0, CONCAT({}, ','), ''), %s) WHERE id = %s".format(upload_or_download, upload_or_download, upload_or_download)
        cursor.execute(sql, (image_id, user_id,))
        mydb_connector.commit()
    except Exception as e:
        print(f"Error in update_user_uploaded_downloaded_images: {e}")


def upload_image_to_sql(image_id,user_id,filename,file_path,user_name):
    try:
        query = "INSERT INTO images (id,filename, file_path, created_at,uploader,downloaders,downloaded_at) VALUES (%s, %s, %s,NOW(),%s,%s,%s)"
        values = (image_id, filename, file_path,user_name ,'', '')
        cursor.execute(query, values)
        mydb_connector.commit()
    except Exception as e:
        print(f"Error in upload_image_to_sql: {e}")


def set_uploader(name_,user_id):
    try:
        sql = "UPDATE images SET uploader = %s WHERE id = %s"
        cursor.execute(sql, (name_, user_id))
        mydb_connector.commit()
    except Exception as e:
        print(f"Error in set_uploader: {e}")


def set_uploaded_at(image_id):
    try:
        sql = "UPDATE images SET uploaded_at = NOW() WHERE id = %s"
        cursor.execute(sql, (image_id,))
        mydb_connector.commit()
    except Exception as e:
        print("An error occurred while setting uploaded_at:", e)


def get_amount_from_db(user_id):
    try:
        sql = "SELECT amount FROM payments WHERE payment_id = %s"
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()
        amount_ = 0 if result is None else result[0]
        return amount_
    except Exception as e:
        print("An error occurred while getting amount from db:", e)
        return 0


def update_user_payment(amount_,last_day,user_id):
    try:
        sql = "UPDATE payments SET has_been_paid = %s, amount = %s, payment_due = CASE WHEN payment_due IS NULL THEN %s ELSE payment_due END WHERE payment_id = %s"
        cursor.execute(sql, ('No', amount_, last_day, user_id))
        mydb_connector.commit()
    except Exception as e:
        print("An error occurred while updating user payment:", e)


def set_image_downloaders(name_,image_id):
    try:
        sql = "UPDATE images SET downloaders = CONCAT(downloaders, IF(LENGTH(downloaders) > 0, ',', ''), %s) WHERE id = %s"
        cursor.execute(sql, (name_, image_id,))
        mydb_connector.commit()
    except Exception as e:
        print("An error occurred while setting image downloaders:", e)


def set_image_download_time(image_id):
    try:
        sql = "UPDATE images SET downloaded_at = CONCAT(IF(LENGTH(downloaded_at) > 0, CONCAT(downloaded_at, ','), ''), NOW()) WHERE id = %s"
        cursor.execute(sql, (image_id,))
        mydb_connector.commit()
    except Exception as e:
        print("An error occurred while setting image download time:", e)