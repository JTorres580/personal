--getgenv().Config = {
--    ["AutoMailUser"] = "JSK_Streams",
--}
--loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/ea0ab6ccca282c76c23a12244973ad4e.lua"))()

getgenv().ps99Config = {
    -- General Config
    WEBHOOK_URL = "",
    DISCORD_ID = "",

    -- Mail Config
    USERNAME_TO_MAIL = "",
    MAILING_WEBHOOK_URL = "",

    loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/e1bd7cc383131e1bc6313c712409ee7d.lua"))()
}