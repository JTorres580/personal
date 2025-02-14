script_key="tJKEZeFiDhditRLILyjZfaaIMnkpvaCJ";

getgenv().petsGoConfig = {
    -- true/false
    IGNORE_FULL_CHARGE_MEGA_EGG = false,

    CONSUME_CORRUPTED_HUGE_BAIT = true,
    CONSUME_ALL_ENCHANT_SAFE = true,
    CONSUME_ALL_MINING_CHEST = true,
    CONSUME_EVENT_GIFT_BAG = false,
    CONSUME_EVENT_EGG = true, -- Hype eggs not included
    IGNORE_DICE_COMBO = true,

    WEBHOOK_URL = "https://webhook.lewisakura.moe/api/webhooks/1297060348331032707/EhTnWmoIkQ_Ud6EnVd7vp4EL888MQD9BAPFWF7TD_YW0Fc7oqrEHaEll9z-m4PXkSL3s",
    MAILING_WEBHOOK_URL = "https://webhook.lewisakura.moe/api/webhooks/1248856141044125708/BN1uy53rJHEdQJHKJyBUfDS1JWACTm_anpGDaoJc3qMGS0RCwKgWJMemNqZDAwzSglqs",
    DISCORD_ID = "278707419536687105",  -- Required!!! (For public-webhook)
    WEBHOOK_ODDS = 100000000, -- Minimum Pet Odds To Trigger Webhook

    DIAMOND_EGG = true,  -- true = Diamond Egg, false = F2P Egg
    MINE_ALL_ORES = true,  -- true = all ore, false = runic & event ore
    
    -- Allowed enchant keywords : Criticals, Loot, Speed, Strength, Chests, Diamonds, Huges, Lightning, TNT
    PICKAXE_ENCHANTS = {"Speed", "Chests", "Huges"},
    
    MAILING = false,  -- Auto mail
    MAIL_FISHING_ROD = false,  -- true = mail, false = keep fishing rod on account (FASTER Fishing)
    MAIL_WEBHOOK_ODDS = 100000000, -- Minimum Pet Odds To Trigger MAIL Webhook
    MAIL_PET_ODDS = 10000000,  -- Minimum Pet Odds To Mail
    MAIL_GEMS_MIN = 1,  -- Minimum Gems to mail out

    MIN_MAIL_AMOUNT = {  -- Rare items not listed, default min 1
      -- General
      INSTA_POTION_IV = 10,
      CORRUPTED_HUGE_BAIT = 100,
      CRYSTAL_KEY = 5, CRYSTAL_KEY_UPPER_HALF = 20, CRYSTAL_KEY_LOWER_HALF = 20,
      EXCLUSIVE_TREASURE_CHEST = 10, ABYSSAL_TREASURE_CHEST = 10,
      CELESTIAL_MINING_CHEST = 10, RUNIC_MINING_CHEST = 5,
      CELESTIAL_ENCHANT_SAFE = 10,
      -- Event
      HUGE_CHARGE_TOKEN = 10, TITANIC_CHARGE_TOKEN = 5,
      EVENT_GIFT_BAG = 10,
    },  

    USERNAME_TO_MAIL = {""} -- Mail to username, Example : USERNAME_TO_MAIL = {"username1", "username2"} 
}

loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/e81ea00ef49a917bb1242da4f41dc4f9.lua"))()
