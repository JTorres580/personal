getgenv().Mailing = {
    ['Mail Items'] = {
        ['Hype Egg'] = { Class = "Lootbox", pt = nil, sh = nil, tn = nil},
        ['2024 Anniversary Gift'] = { Class = "Lootbox", pt = nil, sh = nil, tn = nil},
        ['Snowflake Gift'] = { Class = "Lootbox", pt = nil, sh = nil, tn = nil, MinAmount = 25},
        ['Huge Machine Egg 4'] = { Class = "Egg", pt = nil, sh = nil, tn = nil},
        ['Icy Phoenix'] = { Class = "Pet", pt = nil, sh = nil, tn = nil},
        ['Icy Phoenix'] = { Class = "Pet", pt = nil, sh = true, tn = nil},
        ['Icy Phoenix'] = { Class = "Pet", pt = 1, sh = nil, tn = nil},
        ['Icy Phoenix'] = { Class = "Pet", pt = 1, sh = true, tn = nil},
        ['Icy Phoenix'] = { Class = "Pet", pt = 2, sh = nil, tn = nil},
        ['Icy Phoenix'] = { Class = "Pet", pt = 2, sh = true, tn = nil},
        ['Lit Octopus'] = { Class = "Pet", pt = nil, sh = nil, tn = nil, MinAmount = 25},
        ['Lit Octopus'] = { Class = "Pet", pt = nil, sh = true, tn = nil, MinAmount = 25},
        ['Lit Octopus'] = { Class = "Pet", pt = 1, sh = nil, tn = nil, MinAmount = 25},
        ['Lit Octopus'] = { Class = "Pet", pt = 1, sh = true, tn = nil, MinAmount = 25},
        ['Lit Octopus'] = { Class = "Pet", pt = 2, sh = true, tn = nil, MinAmount = 25},
        ['Lit Octopus'] = { Class = "Pet", pt = 2, sh = true, tn = nil, MinAmount = 25},
    },
    ['Mail Users'] = {"JSK_Streams"}, -- Does random of one
}

repeat task.wait() until game:IsLoaded()
local LocalPlayer = game:GetService('Players').LocalPlayer
repeat task.wait() until not LocalPlayer.PlayerGui:FindFirstChild('__INTRO')

local Client = game:GetService('ReplicatedStorage').Library.Client
local PetDir = require(game.ReplicatedStorage.Library.Directory.Pets)

local Network = require(Client.Network)
local SaveMod = require(Client.Save)

task.spawn(function()
    local HypeEventCmd = require(Client.HypeEventCmds)
    if HypeEventCmd.IsActive() then
        if not HypeEventCmd.IsCompleted() then
            task.wait(HypeEventCmd.GetTimeRemaining())
        end
        Network.Invoke("Hype Wheel: Claim")
    end
end)

local Mail_Items = function()
    local MailQueue = {}
    for Class, Items in pairs(SaveMod.Get().Inventory) do
        for uid, Item in pairs(Items) do
            local IsSecret = (Class == "Pet") and PetDir[Item.id] and PetDir[Item.id].secret
            local IsHuge = (Class == "Pet") and string.find(Item.id, "Huge")
            local IsEgg = (Class == "Egg")

            local ValidConfig = false
            for ConfigName, ConfigTable in pairs(Mailing['Mail Items']) do
                if Item.id == ConfigName and Class == ConfigTable.Class and ConfigTable.pt == Item.pt and ConfigTable.sh == Item.sh and ConfigTable.tn == Item.tn and ((ConfigTable.MinAmount or 0) <= (Item._am or 1)) then
                    ValidConfig = true
                    break
                end
            end
            
            if ValidConfig or IsHuge or IsSecret or IsEgg and not MailQueue[uid] then
                MailQueue[uid] = { Item = Item, Class = Class }
            end
        end
    end

    for UID, Data in pairs(MailQueue) do
        local MailUser = Mailing['Mail Users'][math.random(1, #Mailing['Mail Users'])]
        local Item = Data.Item
        local Unlocked = false
        local Mailed = false
    
        if Item._lk then
            while not Unlocked do
                Unlocked = Network.Invoke("Locking_SetLocked", UID, false) task.wait(0.1)
            end
        end
    
        while not Mailed do
            Mailed = Network.Invoke("Mailbox: Send", MailUser, tostring(Random.new():NextInteger(9, 999999)), Data.Class, UID, (Item._am or 1)) task.wait(0.1)
        end
    end
end

while true do
    Mail_Items()
    task.wait(30)
end
