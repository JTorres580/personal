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
SESSION_FILE = "session.json"

def login_user():
    """
    Manages Instagram login using a session file or credentials with a custom User-Agent.
    """
    cl = Client()
    
    # Set a custom User-Agent to mimic an iPhone device
    #cl.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    if os.path.exists(SESSION_FILE):
        try:
            cl.load_settings(SESSION_FILE)
            cl.login(config.username, config.password)
            cl.get_timeline_feed()  # Validate session
            print(f"{Fore.GREEN}Login successful using session!")
            return cl
        except (LoginRequired, Exception) as e:
            print(f"{Fore.YELLOW}Session expired, logging in again...")
    
    # New login and session save
    try:
        cl.login(config.username, config.password)
        cl.dump_settings(SESSION_FILE)
        print(f"{Fore.GREEN}Login successful and session saved!")
        return cl
    except Exception as e:
        print(f"{Fore.RED}Login failed: {e}")
        input("Press Enter to exit...")
        exit()

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
