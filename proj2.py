import speech_recognition as sr

def transcribe_audio(audio_path):
    """
    Transcribe audio to text using Google's Speech Recognition API.
    """
    recognizer = sr.Recognizer()
    
    try:
        # Load the audio file
        with sr.AudioFile(audio_path) as source:
            print("Listening to audio...")
            audio_data = recognizer.record(source)

        # Transcribe the audio
        print("Transcribing audio...")
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand the audio."
    except sr.RequestError:
        return "Could not request results from Google Speech Recognition service."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Main function to run the transcription
if __name__ == "__main__":
    audio_file = "padma.wav"  # Update with the correct path to your audio file
    
    # Transcribe the audio file and print the result
    transcribed_text = transcribe_audio(audio_file)
    
    print("\nTranscription Result:")
    print(transcribed_text)
