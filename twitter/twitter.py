from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        used_users = db_session.query(User.username)
        while True:
            username = input("What will your twitter handle be?\n")
            pw_1 = input("Enter a password:\n")
            pw_2 = input("Re-enter your password:\n")
            if username not in used_users:
                print("That username is already taken.")
            elif pw_1 != pw_2:   
                print("The passwords don't match. Try again.")
            else:
                break

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        while True:
            username = input("Username: ")
            username_user = db_session.query(User).where(User.username==username)
            password = input("Password: ")
            pw_user = db_session.query(User).where(User.password==password)
            if username_user == pw_user:
                print("Welcome " + username)
                break
            else:
                print("Invalid username or password.")
    
    def logout(self):
        pass

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        pass

    def follow(self):
        pass

    def unfollow(self):
        pass

    def tweet(self):
        pass
    
    def view_my_tweets(self):
        pass
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        pass

    def search_by_user(self):
        pass

    def search_by_tag(self):
        pass

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()

        self.print_menu()
        option = int(input(""))

        if option == 1:
            self.view_feed()
        elif option == 2:
            self.view_my_tweets()
        elif option == 3:
            self.search_by_tag()
        elif option == 4:
            self.search_by_user()
        elif option == 5:
            self.tweet()
        elif option == 6:
            self.follow()
        elif option == 7:
            self.unfollow()
        else:
            self.logout()
        
        self.end()
