import os
import speech_recognition as sr

# Function to recognize speech from a .wav audio file and convert it to text
def recognize_speech_from_wav(audio_path):
    # Check if the audio file exists
    if not os.path.exists(audio_path):
        print("Error: The file does not exist.")
        return
    
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Open the .wav audio file
    try:
        with sr.AudioFile(audio_path) as source:
            print("Listening to the audio file...")
            # Adjust for ambient noise if needed
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source)  # Record the entire audio file
    except Exception as e:
        print(f"Error processing the audio file: {e}")
        return

    try:
        # Use Google Speech API to recognize speech and convert it to text
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print(f"Transcription: {text}")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio. It might be unclear or noisy.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Function to record speech from the microphone and convert to text
def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    
    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Please say something...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen to the first phrase
        
    try:
        # Use Google's speech recognition API to recognize speech
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        print(f"Transcription: {text}")
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the speech. It might be unclear.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Main function to choose between file and microphone input
def main():
    print("Welcome to the Speech-to-Text Program.")
    choice = input("Do you want to process a file (f) or record from the microphone (m)? (f/m): ").strip().lower()

    if choice == 'f':
        # Ask for the .wav file path
        audio_file = input("Please enter the path to your .wav file: ").strip()
        recognize_speech_from_wav(audio_file)
    
    elif choice == 'm':
        # Record and recognize speech from the microphone
        recognize_speech_from_mic()
    
    else:
        print("Invalid choice! Please select 'f' for file or 'm' for microphone.")

if __name__ == "__main__":
    main()

