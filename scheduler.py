import datetime

today = datetime.date.today()
last_day = datetime.date(today.year, today.month, 1) + datetime.timedelta(days=32)
last_day = last_day.replace(day=1) - datetime.timedelta(days=1)

def print_payment_alerts(mydb):

    for user_ in mydb.get_users_dict().values():
        print(f"welcome {mydb.get_users_dict()[user_.get_id()].get_username()}")
        # Check if today is the last day of the month
        if today == last_day:
            print("Today is the last day of the month!")
            if user_.get_payment().get_amount() > 0:
                print(f"you need to pay {user_.get_payment().get_amount()}!")
            else:
                print("Your balance has been cleared. you don't need to pay")

        # Check if today is the 10th, 15th, or 20th of the month
        elif today.day in [10, 15, 20] and user_.get_payment().get_amount() > 0:
            print("Today is the 10th, 15th, or 20th of the month!")
            print(f"this is a reminder you need to pay {user_.get_payment().get_amount()}!")

        else:
            print(f"the date today is {today.day}.{today.month}.{today.year}")
            print(f"you will be sent a payment at the end of the month ")
        print('')