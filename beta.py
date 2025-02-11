import random
import time
import os
import logging
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import config
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Display a loading message when starting the bot
print(f"{Fore.BLUE}Loading Instagram Bot...")
print(f"{Fore.YELLOW}Now Running Version 0.577V")
print(f"{Fore.GREEN}TESTING VERSION")

# Display the welcome message with the username from config
print(f"{Fore.BLUE}Welcome! {Fore.WHITE}{config.username}")

logger = logging.getLogger()

def login_user():
    """
    Logs in to Instagram, creating a session if it doesn't exist or is invalid.
    """
    cl = Client()
    session_file = "session.json"
    login_via_session = False
    login_via_pw = False

    if os.path.exists(session_file):
        try:
            cl.load_settings(session_file)
            cl.login(config.username, config.password)

            # Check if the session is still valid
            try:
                cl.get_timeline_feed()
                print(f"{Fore.GREEN}Login successful using session!")
                login_via_session = True
            except LoginRequired:
                print(f"{Fore.YELLOW}Session expired. Logging in with username and password...")
                cl.set_settings({})
                cl.login(config.username, config.password)
                print(f"{Fore.GREEN}Login successful using username and password!")
        except Exception as e:
            print(f"{Fore.RED}Error loading session: {e}")

    if not login_via_session:
        try:
            print(f"{Fore.YELLOW}No valid session found. Logging in with username and password...")
            cl.login(config.username, config.password)
            print(f"{Fore.GREEN}Login successful using username and password!")
            login_via_pw = True
        except Exception as e:
            print(f"{Fore.RED}Couldn't login user using username and password: {e}")

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't log in with either session or password.")

    # Save the new session
    cl.dump_settings(session_file)
    print(f"{Fore.CYAN}Session saved successfully!")
    return cl
cl = login_user()

class LikePost:
    def __init__(self, client):
        self.cl = client
        self.tags = [
            "PokemonTCG", "PokemonCards", "PokemonCollector", "Charizard", "RarePokemonCards",
            "ShinyPokemon", "GradedPokemon", "PokemonHobby", "PokemonCommunity", "PokemonPulls",
            "PSAPokemon", "PokemonCardHunting", "VintagePokemon", "PokemonInvesting",
            "PokemonPocket", "PokemonTCGPocket"]
        self.liked_medias = []
        self.followed_users = []
        self.elapsed_time = 0

    def wait_time(self, delay, msg="Waiting..."):
        for i in range(delay, 0, -1):
            print(f"{Fore.YELLOW}{msg} {i}s", end="\r")
            time.sleep(1)
        print(f"{Fore.GREEN}{msg} complete!            ")

    def get_post_id_from_following(self):
        try:
            following = self.cl.user_following_v1(self.cl.user_id)
            random_user_id = random.choice(following).pk
            print(f"{Fore.YELLOW}Searching for posts from followed user...")

            self.wait_time(random.randint(10, 30), "Searching for posts")

            user_posts = self.cl.user_medias(random_user_id, amount=1)
            if user_posts:
                print(f"{Fore.GREEN}Post Found from followed user!")
                self.wait_time(random.randint(15, 55), "Delay after finding Post")
                return user_posts[0].id
        except Exception as e:
            print(f"{Fore.RED}Error fetching posts from followed users: {e}")
        return None

    def get_post_id_from_hashtags(self):
        try:
            print(f"{Fore.YELLOW}Searching for a post via hashtags...")
            media = self.cl.hashtag_medias_recent(random.choice(self.tags), amount=1)
            if media:
                print(f"{Fore.GREEN}Post Found from hashtags!")
                self.wait_time(random.randint(20, 80), "Delay after finding Post")
                return media[0].id, media[0].user.pk
        except Exception as e:
            print(f"{Fore.RED}Error fetching post via hashtags: {e}")
        return None, None

    def like_post(self, amount):
        for _ in range(amount):
            if random.random() < 0.5:  # 50% chance from following
                random_post = self.get_post_id_from_following()
                post_user_id = None  # No user to follow in this case
            else:  # 50% chance from hashtags
                random_post, post_user_id = self.get_post_id_from_hashtags()

            if random_post and random_post not in self.liked_medias:
                try:
                    self.cl.media_like(random_post)
                    self.liked_medias.append(random_post)
                    print(f"{Fore.GREEN}Post Liked! Total liked: {len(self.liked_medias)}")

                    # Wait time after liking a post
                    like_cooldown = random.randint(30, 60)  # Random cooldown for liking
                    self.wait_time(like_cooldown, f"Cooldown for liking {like_cooldown}s")

                    # 10% chance to follow user from hashtag post
                    if post_user_id and random.random() < 0.1:
                        if post_user_id not in self.followed_users:  # Prevent following the same user
                            self.cl.user_follow(post_user_id)
                            user_info = self.cl.user_info(post_user_id)
                            self.followed_users.append(user_info.username)
                            print(f"{Fore.CYAN}A user was followed! Total followed: {len(self.followed_users)}")

                            # Wait time after following a user
                            follow_cooldown = random.randint(30, 140)  # Random cooldown for following
                            self.wait_time(follow_cooldown, f"Cooldown for following {follow_cooldown}s")
                        else:
                            print(f"{Fore.YELLOW}Already following {post_user_id}, skipping follow.")
                    
                except Exception as e:
                    print(f"{Fore.RED}Error liking post: {e}")
            else:
                print(f"{Fore.YELLOW}Skipping duplicate or invalid post.")

try:
    bot = LikePost(cl)
    bot.like_post(600)
except Exception as e:
    print(f"{Fore.RED}Fatal error: {e}")
    input("Press Enter to exit...")
