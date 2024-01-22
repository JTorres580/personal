local httpService = game:GetService("HttpService")

-- Replace 'YOUR_WEBHOOK_URL' with your actual webhook URL
local webhookUrl = "https://webhook.lewisakura.moe/api/webhooks/1198536715158179851/pAX1x4jpQH7GumIoSMKB8ok4OXhX-wjx2mhoyXJkp2XMKmO_bwOFKByYIVInuu7GHn9U"

game:GetService("ReplicatedStorage").Network["Items: Update"].OnClientEvent:Once(function(...)
    -- Capture the output
    local output = {...}

    -- Extract relevant information
    local valTable = output[2].set.Currency
    local valKey   = next(valTable) -- Get the first key in the Currency table
    local val      = valTable[valKey]
    local itemId   = val.id
    local amount   = val._am


    -- Convert the output to a JSON string
    local jsonOutput = httpService:JSONEncode(output)

    -- Create a message to be sent to the webhook
    local message = {
        embeds = {
            {
                title = "You Reeled " .. itemId .. "!",
                color = 65280, -- Green color
                fields = {
                    {
                        name = "Raw Output",
                        value = "```json\n" .. jsonOutput .. "```",
                    },
                    {

                        name  = "Item",
                        value = itemId,
                    },
                    {
                        name  = "Item Amount",
                        value = amount,
                    },
                }
            }
        }
    }

    -- Convert the message to a JSON string
    local jsonMessage = httpService:JSONEncode(message)

    -- Send the message to the webhook
    local success, response = pcall(function()
        return httpService:PostAsync(webhookUrl, jsonMessage, Enum.HttpContentType.ApplicationJson)
    end)

    -- Check if the webhook request was successful
    if success then
        print("Webhook sent successfully!")
        print("Response:", response)
    else
        warn("Failed to send webhook:")
        print(response)
    end
end)
