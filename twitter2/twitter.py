from models import *
from database import init_db, db_session
from datetime import datetime
from sqlalchemy import desc 

class Twitter:
    current_user = None
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
        while True:
            username = input("What will your twitter handle be?\n")
            pw_1 = input("Enter a password:\n")
            pw_2 = input("Re-enter your password:\n")
            if db_session.query(User).where(User.username==username).first() is not None:
                print("That username is already taken.")
            elif pw_1 != pw_2:   
                print("The passwords don't match. Try again.")
            else:
                break
        print("Welcome " + username + "!")
        new_user = User(username, pw_1)
        self.current_user = new_user
        db_session.add(new_user)
        db_session.commit()

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        while True:
            username = input("Username: ")
            username_user = db_session.query(User).where(User.username==username).first()
            password = input("Password: ")
            pw_user = db_session.query(User).where(User.password==password).first()
            if (username_user is None or pw_user is None or username_user != pw_user):
                print("Invalid username or password.")
            else:
                self.current_user = username_user
                print("Welcome " + username)
                break
    
    def logout(self):
        self.current_user = None

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        print("\nPlease select a menu option:")
        print("1. Login")
        print("2. Register User")
        print("3. Exit")
        option = int(input(""))
        if option == 1:
            self.login()
        elif option == 2:
            self.register_user()
        elif option == 3:
            self.end()

    def follow(self):
        person = input("Who would you like to follow? ")
        follow = db_session.query(User).where(User.username == person).first()
        if follow in self.current_user.following:
            print("You already follow " + str(follow))
        else:
            new_row = Follower(self.current_user.username, follow.username)
            db_session.add(new_row)
            db_session.commit()
            print("You are now following " + str(follow))

    def unfollow(self):
        person = input("Who would you like to unfollow? ")
        unfollow = db_session.query(User).where(User.username==person).first()
        if unfollow not in self.current_user.following:
            print("You don't follow " + str(unfollow))
        else:
            delete_row = db_session.query(Follower).where((Follower.follower_id==self.current_user.username) & (Follower.following_id==unfollow.username)).first()
            db_session.delete(delete_row)
            db_session.commit()
            print("You no longer follow " + str(unfollow))

    def tweet(self):
        txt = input("Create tweet: ")
        tgs = input("Enter your tags separated by spaces: ")
        tweet = Tweet(txt, datetime.now(), self.current_user.username)
        db_session.add(tweet)
        db_session.commit()
        tags = tgs.split()
        for tag in tags:
            db_tag = db_session.query(Tag).where(Tag.content==tag).first()
            if db_tag is None:
                new_tag = Tag(tag)
                db_session.add(new_tag)
                db_session.commit()
                db_session.add(TweetTag(tweet.id, new_tag.id))
                db_session.commit()
            else:
                db_session.add(TweetTag(tweet.id, db_tag.id))
                db_session.commit()

    def view_my_tweets(self):
        lst = db_session.query(Tweet).where(Tweet.username==self.current_user.username)
        self.print_tweets(lst)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        following = db_session.query(Follower).where(self.current_user.username==Follower.follower_id).all()
        for person in following:
            self.print_tweets(db_session.query(Tweet).where(person.following_id==Tweet.username).order_by(desc(Tweet.timestamp)).limit(5))

    def search_by_user(self):
        user = input("Search user: ")
        person = db_session.query(User).where(user==User.username).first()
        if person is not None:
            self.print_tweets(db_session.query(Tweet).where(Tweet.username==person.username))
        else:
            print("There is no user by that name.")

    def search_by_tag(self):
        inp = input("Search tag: ")
        tag = db_session.query(Tag).where(inp==Tag.content).first()
        if tag is not None:
            tweettags = db_session.query(TweetTag).where(TweetTag.tag_id==tag.id).all()
            for tweettag in tweettags:
                tweet = db_session.query(Tweet).where(tweettag.tweet_id==Tweet.id).all()
                self.print_tweets(tweet)
        else:
            print("There are no tweets with that tag.")


    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()
        while True:
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
                break
        
        self.end()
