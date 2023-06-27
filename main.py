
import main_functions
import intialize
import scheduler




# Initialize the database
intialize.init()
mydb = intialize.get_db()
scheduler.print_payment_alerts(mydb)
running = True


def menu():
    print("1. add user")
    print("2. Sign in")
    print("3. upload a new image")
    print("4. download an image")
    print("5. print all payment details")
    print("6. print all uploaded images details")
    print("7. print all image details")
    print("8. print all downloaded images details")
    print("9. print all user details")
    print("10. display report")
    print("11. display image")
    print("12. Quit and rest all changeable details")


def choice():
    choice = input("Enter your choice: ")
    if choice == "1":
        main_functions.add_user()
    elif choice == "2":
        main_functions.sign_in()
    elif choice == "3":
        main_functions.upload_a_new_image()
    elif choice == "4":
        main_functions.download_an_image()
    elif choice == "5":
        main_functions.print_all_payment_details()
    elif choice == "6":
        main_functions.print_all_uploaded_images_details()
    elif choice == "7":
        main_functions.print_all_image_details()
    elif choice == "8":
        main_functions.print_all_downloaded_images_details()
    elif choice == "9":
        main_functions.print_all_user_details()
    elif choice == "10":
        main_functions.display_report()
    elif choice == "11":
        main_functions.display_image()
    elif choice == "12":
        main_functions.close_program_main()
        global running
        running= False
    else:
        print("Invalid choice. Please enter a valid option.")


while running:
    menu()
    choice()









