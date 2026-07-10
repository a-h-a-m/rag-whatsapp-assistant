from app.services.media import download_audio


def handle_audio_message(
    message,
    ai_provider,
    whatsapp_provider
):

    sender = message["sender"]

    audio_file = download_audio(
        message["audio_url"]
    )



    transcript = ai_provider.transcribe(
        audio_file
    )


    if not transcript:
        transcript = "Transcription failed"

    return transcript

    # whatsapp_provider.send_text(
    #     sender,
    #     transcript
    # )