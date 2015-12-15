# Voices
def get_voice_input():
# obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone(sample_rate = 48000, chunk_size = 8192) as source:
        r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
        print("Say something!")
	audio = r.listen(source)

	# recognize speech using Google Speech Recognition
    try:
# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
# instead of `r.recognize_google(audio)`
	print 'recognizing speech'
	speech = r.recognize_google(audio) # returns voice recording as unicode characters (use str(speech) to convert to string)
	print speech
	return speech
    except sr.UnknownValueError:
	print("Google Speech Recognition could not understand audio")
        return 'Boston'
    except sr.RequestError as e:
	print("Could not request results from Google Speech Recognition service; {0}".format(e))
	return 'Boston'
