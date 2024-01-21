]]
getgenv().autoFish = true

local plr = game.Players.LocalPlayer
local rootPart = plr.Character.HumanoidRootPart
local ws = game:GetService("Workspace")
local rStorage = game:GetService("ReplicatedStorage")
local remote = rStorage.Network.Instancing_FireCustomFromClient
local fishingGame = plr.PlayerGui._INSTANCES.FishingGame
local fishBar = fishingGame.GameBar.FishingBar
local fishingRod = ws[tostring(plr)].Model.Rod
local args = {
    [1] = "Fishing",
    [2] = "RequestCast",
    [3] = Vector3.new(1139.0439453125, 75.91415405273438, -3445.31982421875)
}

-- Fishing progress bar always goes up
require(game:GetService("Workspace")["__THINGS"]["__INSTANCE_CONTAINER"].Active.Fishing.ClientModule.FishingGame).IsFishInBar = function() return true end

-- Webhook function with item information
local function sendWebhook(withDiscord, itemName)
    local webhookUrl = "YOUR_DISCORD_WEBHOOK_URL"
    local message = "Fishing event detected!"

    -- Include item information in the message
    if itemName then
        message = message .. "\nReeled in: " .. itemName
    end

    -- Check if the event includes Discord
    if withDiscord then
        message = message .. " @discord"
    end

    -- Replace this with your actual webhook sending logic
    print("Sending webhook:", message, "to", webhookUrl)
end

spawn(function()
    while wait() do
        if not autoFish then break end
        if not fishingRod:FindFirstChild("FishingLine") then
            remote:FireServer(unpack(args))
            wait(0.5)
        end
        if fishingRod:FindFirstChild("FishingLine") then
            while fishingRod:FindFirstChild("FishingLine") do
                if not autoFish then break end
                local attachment1 = fishingRod:FindFirstChild("FishingLine").Attachment1
                local bobber = attachment1.Parent
                local height = tonumber(bobber.CFrame.Position.Y)
                if height > 75.91415405273438 then
                    print("too high, waiting")
                    wait(0.1)
                elseif height == 75.91415405273438 then
                    print("no fish, waiting")
                    wait(0.1)
                elseif height < 75.8 then
                    print("height detected")
                    wait(0.1)
                    remote:FireServer("Fishing", "RequestReel")

                    -- Check the drop condition and call the webhook function accordingly
                    local drop = "xxx"  -- Replace with the actual condition for drop
                    if drop == "xxx" then
                        -- Replace "ItemName" with the actual variable containing the item information
                        sendWebhook(true, "ItemName")  -- With Discord
                    else
                        sendWebhook(false)  -- Without Discord
                    end
                end
                wait(0.1)
            end
        end
        wait(0.1)
    end
end)
