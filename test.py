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
print(f"{Fore.YELLOW}Now Running Version 0.5V")
print(f"{Fore.RED}EXCLUSIVE MORTGAGE VERSION")

# Display the welcome message with the username from config (Blue)
print(f"{Fore.BLUE}Welcome! {Fore.WHITE}{config.username}")

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
        self.tags = [
            'Happyhomeowner', 'Firsthomeowner', 
            'dreamhome', 'womenwholead', 'bwofgod', 'womanofgod', 'jesuslovesyou', 'AVwomen', 
            'exprealty', 'Avrealty', 'palmdalerealestate', 'lancasterrealestate', 'palmdale', 
            'lancaster', 'firsttimebuyer', 'Realbrokerage', 'openhouse', 'coldwellbankerhartwig', 
            'santaclaritahomes', 'AVseller', 'homesweethome', 'realestategoals', 'kellerwilliams', 
            'Rosamond', '661realestate', 'azrealtor', 'downpaymentassistance', 'AntelopeValleyRealtor', 
            'PalmdaleRealtor', 'LancasterCARealtor', 'AVRealtors', 'PalmdaleHomesForSale', 
            'LancasterHomesForSale', 'AntelopeValleyRealEstate', 'PalmdaleRealEstate', 'LancasterCARealEstate', 
            'AntelopeValleyLiving', 'PalmdaleLiving', 'LancasterCALiving', 'AVLuxuryHomes', 'AVNewHomes', 
            'AVHomeLoans', 'AntelopeValleyMortgage', 'PalmdaleMortgageLender', 'LancasterCAMortgage', 
            'HomeBuyingMadeEasy', 'RealtorNetworking', 'RealtorMarketing', 'RealEstateGrowth', 'AVInvestors', 
            'FirstTimeHomeBuyerAV', 'HomeBuyersPalmdale', 'BuySellInvestAV', 'RealtorsOfInstagram', 
            'CaliforniaRealtors', 'RealEstateLife', 'RealtorGoals', 'RealtorSuccess', 'RealEstateMarketing', 
            'RealEstateInvesting', 'HouseHunting', 'JustListed', 'HomeOwnerLife', 'MyFirstHome', 
            'ForeverHome', 'DreamHomeGoals', 'HomeSweetHome', 'HouseToHome', 'NewHomeJourney', 'HomeOwnersUnite', 
            'FirstTimeBuyerTips', 'HomeBuying101', 'MortgageMadeEasy', 'HomeLoanExperts', 'HomeBuyingProcess', 
            'HomeLoanHelp', 'HomeFinance', 'SellingYourHome', 'ReadyToSell', 'TimeToMove', 'HouseForSaleNow', 
            'ListYourHome', 'SellYourHomeFast', 'BestTimeToSell', 'AntelopeValleyHomes', 'PalmdaleLiving', 
            'LancasterLiving', 'MoveToAV', 'AVHomesForSale', 'LiveInPalmdale', 'LiveInLancaster', 
            'BuyAHomeInAV', 'LuxuryHomesAV', 'AVInvestmentProperties', 'CaliforniaLuxuryHomes', 'RealEstateInvestorAV', 
            'RealtorLife', 'HomeBuyingMadeSimple', 'DreamHomeLoading', 'RealtorSuccessStories', 'HelpingHomeowners', 
            'HouseHunters'
        ]
        self.liked_medias = []
        self.elapsed_time = 0

    def wait_time(self, delay):
        # Countdown timer that updates on the same line
        for i in range(delay, 0, -1):
            print(f"{Fore.YELLOW}Waiting... {i}s", end="\r")
            time.sleep(1)
        print(f"{Fore.GREEN}Waiting complete!              ")  # Clear the line

    def wait_for_api(self, delay):
        # Countdown timer for API rate limit delay when fetching posts from followed users
        for i in range(delay, 0, -1):
            print(f"{Fore.YELLOW}Searching for posts... {i}s", end="\r")
            time.sleep(1)
        print(f"{Fore.GREEN}Search delay complete!              ")  # Clear the line

    def get_post_id_from_following(self):
        try:
            # Use the new method for fetching following users
            following = self.cl.user_following_v1(self.cl.user_id)  # Use user_following_v1
            
            # Select a random followed user
            random_user_id = random.choice(following).pk  # Ensure we use the correct object to get user ID
            print(f"{Fore.YELLOW}Searching for posts from followed user...")

            # Delay before attempting to fetch posts to avoid spamming the API
            self.wait_for_api(random.randint(10, 30))  # Adjust the delay as needed (30 to 60 seconds)

            # Get the media from that followed user
            user_posts = self.cl.user_medias(random_user_id, amount=1)  # Fetch 1 post from the followed user

            if user_posts:
                media_dict = user_posts[0].model_dump()  # Get media info
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
            # Display message when searching for a post via hashtags
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
            print(f"Error fetching post via hashtags: {e}")
            return None

    def like_post(self, amount):
        for _ in range(amount):
            # 70% chance to get a post from followed users, 30% chance from hashtags
            if random.random() < 0.7:
                random_post = self.get_post_id_from_following()
            else:
                random_post = self.get_post_id_from_hashtags()

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
