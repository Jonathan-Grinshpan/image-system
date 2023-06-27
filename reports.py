import pandas as pd
import os
import helper_functions
import csv

class Report:
    def __init__(self,mydb):
        num_of_rows = 7
        data = {}
        users_df = pd.DataFrame(data)
        images_df = pd.DataFrame(data)
        numbers_df = pd.DataFrame(data)
        payment_df = pd.DataFrame(data)

        calnder_df = pd.DataFrame({
            'JAN': [[] for _ in range(num_of_rows)],'FEB': [[] for _ in range(num_of_rows)],'MAR': [[] for _ in range(num_of_rows)],
            'APR': [[] for _ in range(num_of_rows)],'MAY': [[] for _ in range(num_of_rows)], 'JUN': [[] for _ in range(num_of_rows)],
            'JUL': [[] for _ in range(num_of_rows)], 'AUG': [[] for _ in range(num_of_rows)],'SEP': [[] for _ in range(num_of_rows)],
            'OCT': [[] for _ in range(num_of_rows)],'NOV': [[] for _ in range(num_of_rows)],'DEC': [[] for _ in range(num_of_rows)]
        }, index=['uploaded imgs', 'downloaded imgs','user creation','percent of uploads','percent of downloads','num of uploads','num of downloads'])

        for user_ in mydb.get_users_dict().values():
            new_row = {'user_ID': int(float(user_.get_id())), 'user_name': user_.get_username(),'password': user_.get_password(), 'email': user_.get_email(), 'creation_date': user_.get_created_at(),
                       'uploaded_img_id':user_.get_uploaded_images(), 'downloaded_img_id': user_.get_downloaded_images(),'payment date': user_.get_payment().get_payment_due()}
            users_df = users_df.append(new_row, ignore_index=True)

            month_name = helper_functions.extract_month(user_.get_created_at())
            calnder_df.loc['user creation', month_name].append(user_.get_username())

        for image_ in mydb.get_images_dict().values():
            # add a new row
            download_by_ = set(image_.get_downloaded_user_name()) if image_.get_downloaded_user_name() else ''
            new_row = {
                'img_id': image_.get_id(),
                'uploaded by': image_.get_uploaded_user_name(),
                'downloaded by': download_by_,
                'uploaded_time': image_.get_uploaded_time(),


            }
            if image_.get_uploaded_time() is not None:
                month_name = helper_functions.extract_month(image_.get_uploaded_time())
                calnder_df.loc['uploaded imgs', month_name].append( image_.get_id())

            if len(image_.get_downloaded_time())!=0:
                for date_ in image_.get_downloaded_time():
                    month_name = helper_functions.extract_month(date_)
                    calnder_df.loc['downloaded imgs', month_name].append(image_.get_id())

            images_df = images_df.append(new_row, ignore_index=True)

        numbers_df.at[0, 'number_of_users'] = len(mydb.get_users_dict())
        numbers_df.at[0, 'number_of_images_uploaded'] = len(mydb.get_uploaded_images_list())
        numbers_df.at[0, 'number_of_images_downloaded'] = len(mydb.get_downloaded_images_list())

        total_uploads = len(mydb.get_uploaded_images_list())
        total_downloads = len(mydb.get_downloaded_images_list())
        months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        for month in months:
            if total_uploads>0:
                uploaded_imgs_by_month = (len(calnder_df.loc['uploaded imgs',month]))
                res = (uploaded_imgs_by_month/total_uploads)
                res = '{:.2f}%'.format(res*100) if res > 0 else 0
                calnder_df.loc['percent of uploads', month].append(res)
            if total_downloads>0:
                downloaded_imgs_by_month = (len(calnder_df.loc['downloaded imgs',month]))
                res = (downloaded_imgs_by_month/total_downloads)
                res = '{:.2f}%'.format(res * 100) if res > 0 else 0
                calnder_df.loc['percent of downloads', month].append(res)

            calnder_df.loc['num of uploads', month].append(len(calnder_df.loc['uploaded imgs', month]))
            calnder_df.loc['num of downloads', month].append(len(calnder_df.loc['downloaded imgs', month]))
        for payment_ in mydb.get_payments_dict().values():
            new_row = {'payment id': payment_.get_payment_id(),
                       'user': mydb.get_users_dict()[payment_.get_payment_id()].get_username(),
                       'payment due': payment_.get_payment_due(),
                       'amount': payment_.get_amount(),
                       'has been paid': payment_.get_has_been_paid()}

            payment_df = payment_df.append(new_row, ignore_index=True)

        try:
            separator = pd.DataFrame({'': ['']})
            separator = pd.concat([separator] * 3, ignore_index=True)
            users_df.to_csv('report.csv', index=False)
            separator.to_csv('report.csv',index=False,mode='a')

            images_df.to_csv('report.csv', index=False, mode='a')
            separator.to_csv('report.csv',index=False,mode='a')

            payment_df.to_csv('report.csv', index=False, mode='a')
            separator.to_csv('report.csv',index=False,mode='a')

            with open('report.csv', mode='a', newline='') as file:

                # Create a writer object
                writer = csv.writer(file)
                for image_ in mydb.get_images_dict().values():
                    if len(image_.get_downloaded_user_name())==0:
                        continue
                    new_row = [f"image id: {image_.get_id()}"]
                    writer.writerow(new_row)
                    for i, user_ in enumerate(image_.get_downloaded_user_name()):
                        new_row = [f"downloaded by {user_} at:  {image_.get_downloaded_time()[i]}"]
                        writer.writerow(new_row)

            separator.to_csv('report.csv', index=False, mode='a')
            calnder_df.to_csv('report.csv', index=True, mode='a')
            separator.to_csv('report.csv',index=False,mode='a')

            numbers_df.to_csv('report.csv', index=False, mode='a')

            os.startfile('report.csv')
            print("opening excel sheet......this may take a moment")
        except PermissionError as e:
            print('try closing report.csv and then try to open it again')
