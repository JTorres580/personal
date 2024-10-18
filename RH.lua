local Workspace = game:GetService("Workspace")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local Players = game:GetService("Players")
local TeleportService = game:GetService("TeleportService")
local HttpService = game:GetService("HttpService")

local PlaceId = game.PlaceId
local JobId = game.JobId
local Player = Players.LocalPlayer

if not Player.Character then
    Player.CharacterAdded:Wait()
end

local getChar = function()
    return Player.Character
end

local getHRP = function()
    return Player.Character.HumanoidRootPart
end

local Hop = function(low:boolean)
    local ServersLink = "https://games.roblox.com/v1/games/"..tostring(game.PlaceId).."/servers/Public?sortOrder="..(low and "Asc" or "Des").."&limit=100"
    local ServersReturn = game:HttpGet(ServersLink)
    if ServersReturn then
        local Servers = HttpService:JSONDecode(ServersReturn)

        if Servers and Servers.data then
            for i,v in pairs(Servers.data) do
                if v.playing and v.playing < v.maxPlayers - 1 and v.id ~= game.JobId then
                    TeleportService:TeleportToPlaceInstance(game.PlaceId, v.id, game.Players.LocalPlayer)
                    return
                end
            end
        end
    end
end

for _,part in Workspace:GetChildren() do
    if part:IsA("Part") and part:GetAttribute("DormTemplateId") then
        getHRP().CFrame = part.OuterDorm.Colorable.DormDoor.TeleportOut.CFrame

        local Furniture = part:WaitForChild("DormFurniture", 5)
        if Furniture then
            for i,v in Furniture:GetChildren() do
                if v:IsA("Model") and v:GetAttribute("Interactable") and v:FindFirstChild("CandyBowl") then
                    -- Interact with the CandyBowl
                    local candyBowl = v:FindFirstChild("CandyBowl")
                    while candyBowl do
                        -- If it has a ClickDetector, simulate clicking it to claim candy
                        if candyBowl:FindFirstChild("ClickDetector") then
                            fireclickdetector(candyBowl.ClickDetector)
                        end
                        task.wait() -- Wait a bit before checking again
                        candyBowl = v:FindFirstChild("CandyBowl") -- Recheck if the bowl is still there
                    end
                end
            end
        end
    end
end

Hop()
