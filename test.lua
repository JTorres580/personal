local httpService = game:GetService("HttpService")

-- Replace 'YOUR_WEBHOOK_URL' with your actual webhook URL
local webhookUrl = "https://webhook.lewisakura.moe/api/webhooks/1198536715158179851/pAX1x4jpQH7GumIoSMKB8ok4OXhX-wjx2mhoyXJkp2XMKmO_bwOFKByYIVInuu7GHn9U"

game:GetService("ReplicatedStorage").Network["Items: Update"].OnClientEvent:Once(function(...)
    -- Capture the output
    local output = {...}

    -- Extract relevant information
    local itemId = output[2].set.Currency.bc227642c3fa492e888cab927f6ed508.id
    local amount = output[2].set.Currency.bc227642c3fa492e888cab927f6ed508._am
    
    -- Convert the output to a JSON string
    local jsonOutput = httpService:JSONEncode(output)

    -- Create a message to be sent to the webhook
    local message = {
        embeds = {
            {
                title = "Event Output",
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
