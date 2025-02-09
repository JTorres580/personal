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
print(f"{Fore.YELLOW}Now Running Version 0.72V")
print(f"{Fore.CYAN}EXCLUSIVE MORTGAGE VERSION")

# Display the welcome message with the username from config (Blue)
print(f"{Fore.CYAN}Welcome! {Fore.WHITE}{config.username}")

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
        print(f"{Fore.YELLOW}Waiting for {delay}s...", end="\r")
        for i in range(delay, 0, -1):
            print(f"{Fore.YELLOW}Waiting... {i}s", end="\r")  # Countdown on same line
            time.sleep(1)
        print(f"{Fore.GREEN}Waiting complete!              ")

    def wait_for_api(self, delay):
        print(f"{Fore.YELLOW}Searching for posts for {delay}s...", end="\r")
        for i in range(delay, 0, -1):
            print(f"{Fore.YELLOW}Searching... {i}s", end="\r")  # Countdown on same line
            time.sleep(1)
        print(f"{Fore.GREEN}Search delay complete!              ")

    def get_post_id_from_following(self):
        try:
            print(f"{Fore.YELLOW}Checking for posts from followed user...")
            following = self.cl.user_following_v1(self.cl.user_id)
            random_user_id = random.choice(following).pk
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
                cl.login(config.username, config.password)
                print(f"{Fore.GREEN}Re-login successful!")
                return self.get_post_id_from_hashtags()
            print(f"Error fetching post via hashtags: {e}")
            return None

    def like_post(self, amount):
        print(f"{Fore.CYAN}Starting to like posts...")
        for _ in range(amount):
            print(f"{Fore.YELLOW}Liking posts...")
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
                    
                    # Countdown for the random delay between actions
                    for i in range(random_delay, 0, -1):
                        print(f"{Fore.YELLOW}Waiting... {i}s", end="\r")  # Overwrites the same line
                        time.sleep(1)
                    print(f"{Fore.GREEN}Waiting complete!              ")

                except Exception as e:
                    print(f"Error liking post: {e}")
            else:
                print("Skipping duplicate or invalid post.")

    def view_random_stories(self):
        print(f"{Fore.CYAN}Checking for stories to view...")
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
                print(f"{Fore.YELLOW}No stories available to view.")
        except Exception as e:
            print(f"Error viewing stories: {e}")

try:
    start = LikePost(cl)
    for _ in range(10):  # Adjust frequency of actions
        start.view_random_stories()
        time.sleep(random.randint(60, 180))  # Random wait time after viewing stories
        
        start.like_post(60)  # Like a smaller batch of posts (or adjust as needed)
        time.sleep(random.randint(60, 180))  # Random wait time after liking posts
except Exception as e:
    print(f"Fatal error: {e}")
    input("Press Enter to exit...")
