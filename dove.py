import random
import time
from instagrapi import Client
import config
from colorama import Fore, init
import logging

# Initialize colorama
init(autoreset=True)

logger = logging.getLogger()

cl = Client()

def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """
    session = cl.load_settings("session.json")
    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(config.username, config.password)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(config.username, config.password)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password.")
            if cl.login(config.username, config.password):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

    # Save session for future use
    cl.dump_settings("session.json")

# Display a loading message when starting the bot (Blue)
print(f"{Fore.BLUE}Loading Instagram Bot...")
print(f"{Fore.YELLOW}Now Running Version 0.73V")
print(f"{Fore.CYAN}TCGDOVES VERSION")

# Display the welcome message with the username from config (Blue)
print(f"{Fore.CYAN}Welcome! {Fore.WHITE}{config.username}")

try:
    login_user()
    # Login successful message (Green)
    print(f"{Fore.GREEN}Login successful!")
except Exception as e:
    print(f"Login failed: {e}")
    input("Press Enter to exit...")  # Prevents the script from closing immediately
    exit()

class LikePost:
    def __init__(self, client):
        self.cl = client
        self.tags = [
            "PokemonTCG", "PokemonCards", "PokemonCollector", "Charizard", "RarePokemonCards",
            "ShinyPokemon", "GradedPokemon", "PokemonHobby", "PokemonCommunity", "PokemonPulls",
            "PSAPokemon", "PokemonCardHunting", "VintagePokemon", "PokemonInvesting",
            "PokemonPocket", "PokemonTCGPocket"
        ]
        self.liked_medias = []
        self.elapsed_time = 0

    def wait_time(self, delay):
        for i in range(delay, 0, -1):
            print(f"{Fore.YELLOW}Waiting... {i}s", end="\r")
            time.sleep(1)
        print(f"{Fore.GREEN}Waiting complete!              ")

    def wait_for_api(self, delay):
        for i in range(delay, 0, -1):
            print(f"{Fore.YELLOW}Searching for posts for {i}s...", end="\r")
            time.sleep(1)
        print(f"{Fore.GREEN}Search delay complete!              ")

    def get_post_id_from_following(self):
        try:
            following = self.cl.user_following_v1(self.cl.user_id)
            random_user_id = random.choice(following).pk
            print(f"{Fore.YELLOW}Searching for posts from followed user...")
            self.wait_for_api(random.randint(20, 30))
            user_posts = self.cl.user_medias(random_user_id, amount=1)
            if user_posts:
                media_dict = user_posts[0].model_dump()
                print(f"{Fore.GREEN}Post Found from followed user!")
                return str(media_dict['id'])
            else:
                print("No posts found from followed user.")
                return None
        except Exception as e:
            print(f"Error fetching posts from followed users: {e}")
            return None

    def get_post_id_from_hashtags(self):
        try:
            print(f"{Fore.YELLOW}Simulating scrolling before searching for a post via hashtags...")
            time.sleep(random.randint(5, 10))
            print(f"{Fore.YELLOW}Searching for a post via hashtags...")
            medias = self.cl.hashtag_medias_recent(random.choice(self.tags), amount=1)
            if medias:
                media_dict = medias[0].model_dump()
                print(f"{Fore.GREEN}Post Found from hashtags!")
                return str(media_dict['id'])
            else:
                print("No media found, retrying...")
                return None
        except Exception as e:
            if "login_required" in str(e):
                print(f"{Fore.RED}Session expired, re-logging in after 60 seconds...")
                time.sleep(60)
                login_user()
                print(f"{Fore.GREEN}Re-login successful!")
                return self.get_post_id_from_hashtags()
            print(f"Error fetching post via hashtags: {e}")
            return None

    def like_post(self, amount):
        for _ in range(amount):
            if random.random() < 0.1:
                random_post = self.get_post_id_from_following()
            else:
                random_post = self.get_post_id_from_hashtags()

            if random_post and random_post not in self.liked_medias:
                try:
                    self.cl.media_like(media_id=random_post)
                    self.liked_medias.append(random_post)
                    random_delay = random.randint(30, 120)
                    self.elapsed_time += random_delay
                    print(f"Liked {len(self.liked_medias)} posts, time elapsed {self.elapsed_time / 60:.2f} minutes, now waiting {random_delay} seconds")
                    self.wait_time(random_delay)
                except Exception as e:
                    print(f"Error liking post: {e}")
            else:
                print("Skipping duplicate or invalid post.")

    def view_random_stories(self):
        try:
            following = self.cl.user_following_v1(self.cl.user_id)
            random_user_id = random.choice(following).pk
            stories = self.cl.user_stories(random_user_id, amount=random.randint(1, 3))
            if stories:
                story_pks = [story.id for story in stories]
                self.cl.story_seen(story_pks, skipped_story_pks=[])
                if random.random() < 0.2:
                    self.cl.story_like(story_pks[0])
                print(f"{Fore.GREEN}Viewed {len(stories)} stories and liked one!")
            else:
                print("No stories available to view.")
        except Exception as e:
            print(f"Error viewing stories: {e}")

try:
    start = LikePost(cl)
    # Viewing stories
    for _ in range(10):  # Adjust frequency of story views
        start.view_random_stories()
        print(f"{Fore.YELLOW}Waiting for next story view...")
        for i in range(random.randint(60, 180), 0, -1):
            print(f"{Fore.YELLOW}Waiting... {i}s", end="\r")
            time.sleep(1)

    # Liking posts
    print(f"{Fore.YELLOW}Liking posts...")
    start.like_post(60)  # Like a smaller batch of posts (or adjust as needed)
    for i in range(random.randint(60, 180), 0, -1):
        print(f"{Fore.YELLOW}Waiting for next like... {i}s", end="\r")
        time.sleep(1)

except Exception as e:
    print(f"Fatal error: {e}")
    input("Press Enter to exit...")
