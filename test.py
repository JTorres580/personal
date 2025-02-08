from instagrapi import Client
import config
import time
import random
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

cl = Client()

# Display a loading message when starting the bot (Blue)
print(f"{Fore.BLUE}Loading Instagram Bot...")
print(f"{Fore.YELLOW}Now Running Version 0.5V")

# Display the welcome message with the username from config (Blue)
print(f"{Fore.BLUE}Welcome! {config.username}")

try:
    cl.login(config.username, config.password)
    # Login successful message (Green)
    print(f"{Fore.GREEN}Login successful!")
except Exception as e:
    print(f"Login failed: {e}")
    input("Press Enter to exit...")  # Prevents the script from closing immediately
    exit()

class LikePost:
    def __init__(self, client):
        self.cl = client
        self.tags = ['pokemon', 'toys', 'gaming', 'programming']
        self.liked_medias = []
        self.elapsed_time = 0

    def wait_time(self, delay):
        time.sleep(delay)

    def get_post_id(self):
        # Display message when searching for a post (Yellow)
        print(f"{Fore.YELLOW}Searching for a post...")
        try:
            medias = self.cl.hashtag_medias_recent(random.choice(self.tags), amount=1)
            if medias:
                media_dict = medias[0].model_dump()  # Fixed: Replaced dict() with model_dump()
                print(f"{Fore.GREEN}Post Found!")  # Message after finding a post
                return str(media_dict['id'])
            else:
                print("No media found, retrying...")
                return None
        except Exception as e:
            print(f"Error fetching post: {e}")
            return None

    def like_post(self, amount):
        for _ in range(amount):
            random_post = self.get_post_id()
            if random_post and random_post not in self.liked_medias:
                try:
                    self.cl.media_like(media_id=random_post)
                    self.liked_medias.append(random_post)
                    random_delay = random.randint(20, 60)  # Adjust delay if needed
                    self.elapsed_time += random_delay
                    print(f"Liked {len(self.liked_medias)} posts, time elapsed {self.elapsed_time / 60:.2f} minutes, now waiting {random_delay} seconds")
                    self.wait_time(random_delay)
                except Exception as e:
                    print(f"Error liking post: {e}")
            else:
                print("Skipping duplicate or invalid post.")

try:
    start = LikePost(cl)
    start.like_post(600)
except Exception as e:
    print(f"Fatal error: {e}")
    input("Press Enter to exit...")  # Keeps the window open after an error
