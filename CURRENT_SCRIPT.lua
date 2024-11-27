script_key="BINLlfIdmintgxIxZMABRlNizTkMFesr";
-- Please Read FAQ channel for more info! Make sure you understand these parameters
-- If not sure ask info in channel
_G.GPROGRESS_MODE = "Hybrid"
_G.GRANK_TO = 1
_G.GWAIT_AT_GATES_TILL_RANK = 2 -- default value in script is 6. This means when in Hybrid mode, it will wait at the gates to gather coins for hatching-quests untill you are rank 6. Once you are rank 6 it will not wait at gates anymore & only start hatching again when you reach final area defined in ZONE_TO.
_G.GREBIRTH_TO = 10 -- number, limits the amount of rebirths
_G.GGFX_MODE = 1
_G.GZONE_TO = 999 -- ONLY increase above 99 to go to world2, only when 100% sure, there is no way back for the "best zone" quests etc. 
_G.GMAX_EGG_SLOTS = 99
_G.GMAX_EQUIP_SLOTS = 99
_G.GHOLD_GIFTS = false
_G.GHOLD_BUNDLES = false
_G.GMAX_ZONE_UPGRADE_COST = 20000
_G.GIGNORE_SLEDRACE = false
_G.GFRUITS = {"Apple","Banana","Orange","Rainbow"}
_G.GPOTIONS = {"Damage","Coins","The Cocktail","Treasure Hunter","Walkspeed","Diamonds"}
_G.GPOTIONS_MAX_TIER = 8
_G.GIGNORE_VIP = false
_G.GET_RNG_PETS = false
_G.GENCHANTS = {"Huge Hunter", "Coins", "Huge Hunter", "Strong Pets", "Criticals"}
_G.GWEBHOOK_USERID = "278707419536687105"
_G.GWEBHOOK_LINK = "https://webhook.lewisakura.moe/api/webhooks/1248856141044125708/BN1uy53rJHEdQJHKJyBUfDS1JWACTm_anpGDaoJc3qMGS0RCwKgWJMemNqZDAwzSglqs"
loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/34915da4ad87a5028e1fd64efbe3543f.lua"))()




--getgenv().Config = {
--    ["AutoMailUser"] = "JSK_Streams",
--    ["UserID"] = "278707419536687105",
--    ["Webhook"] = "https://webhook.lewisakura.moe/api/webhooks/1248523147507142656/Pk0BBjxWtIjx_1WtUaVFBzVqCg8mx3KNcNe4zMU3754EtaBOOLHc_bDb5rU46YU2a0g-"
--}
--loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/ea0ab6ccca282c76c23a12244973ad4e.lua"))()
