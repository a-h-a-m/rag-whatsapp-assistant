def extract_message(data):

    message_data = data.get("messageData", {})

    sender = data.get("senderData", {}).get("chatId")

    message_type = message_data.get("typeMessage")

    result = {
        "sender": sender,
        "type": message_type,
        "text": None,
        "audio_url": None
    }

    if message_type == "textMessage":

        result["text"] = (
            message_data
            .get("textMessageData", {})
            .get("textMessage")
        )

    elif message_type == "extendedTextMessage":
        result["text"] = (
            message_data
            .get("extendedTextMessageData", {})
            .get("text")
        )


    elif message_type == "audioMessage":

        result["audio_url"] = (
            message_data
            .get("fileMessageData", {})
            .get("downloadUrl")
        )

    return result