import random
import time
from instagrapi import Client
import config
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

cl = Client()

# Display a loading message when starting the bot (Blue)
print(f"{Fore.BLUE}Loading Instagram Bot...")
print(f"{Fore.YELLOW}Now Running Version 0.67V")
print(f"{Fore.CYAN}TCGDOVES VERSION")

# Display the welcome message with the username from config (Blue)
print(f"{Fore.CYAN}Welcome! {Fore.WHITE}{config.username}")

def login():
    """Logs into Instagram using the provided credentials."""
    global cl
    try:
        cl.login(config.username, config.password)
        print(f"{Fore.GREEN}Login successful!")
    except Exception as e:
        print(f"{Fore.RED}Login failed: {e}")
        input("Press Enter to exit...")
        exit()

# Perform initial login
login()

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
        """Displays a countdown timer."""
        for i in range(delay, 0, -1):
            print(f"{Fore.YELLOW}Waiting... {i}s", end="\r")
            time.sleep(1)
        print(f"{Fore.GREEN}Waiting complete!              ")

    def wait_for_api(self, delay):
        """Wait time for API rate limits."""
        for i in range(delay, 0, -1):
            print(f"{Fore.YELLOW}Searching for posts... {i}s", end="\r")
            time.sleep(1)
        print(f"{Fore.GREEN}Search delay complete!              ")

    def get_post_id_from_following(self):
        """Fetches a post from a random followed user."""
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
        """Fetches a post using a random hashtag."""
        global cl
        try:
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
            print(f"{Fore.RED}Error fetching post via hashtags: {e}")

            if "login_required" in str(e):
                print(f"{Fore.RED}Login required! Waiting 1 minute before re-logging in...")
                self.wait_time(60)  # Wait 1 minute
                login()  # Re-login
                return self.get_post_id_from_hashtags()  # Retry after login
            
            return None

    def like_post(self, amount):
        """Likes a specified number of posts."""
        for _ in range(amount):
            # 70% chance to get a post from followed users, 30% chance from hashtags
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

try:
    start = LikePost(cl)
    start.like_post(600)
except Exception as e:
    print(f"{Fore.RED}Fatal error: {e}")
    input("Press Enter to exit...")
