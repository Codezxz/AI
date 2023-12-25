import os
import openai
import os
import openai
import speech_recognition as sr
import requests
import json
import os, json
import os
import wave
import json
# import vosk
from flask import Flask, request, jsonify
import requests
import PyPDF2

ENV_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = ENV_PATH + r'/.env'
token = os.getenv('OPENAI_API_KEY')
json_string = os.getenv('JSON')
PDATA = os.getenv('PDATA')

app = Flask(__name__)

# @app.route('/gmailNotes', methods = ['GET','POST'])
# def gmn():
#     # Google Speech Recognizer
# 	#------------------------------------
# 	# data = request.files['file']
# 	# r = sr.Recognizer()
# 	# # prompt = "Worlds fastest man alive"
# 	# with sr.AudioFile(data) as source:
# 	# 	audio_text = r.listen(source)
# 	# 	text = r.recognize_google(audio_text)
# 	# 	print(text)
# 	# return text
# 	#-------------------------------------
# 	data = request.files['file']
# 	model = vosk.Model("/home/urbano-infotech/Documents/FlaskAPI/AI/Flask API/vosk-model-small-en-us-0.15")
# 	# print(model)

# 	# Recieve the WAV file
# 	filename = data
#     # filename = "C:/Users/Administrator/Documents/imagineWave.wav"
# 	wf = wave.open(filename, "rb")
# 	a = []
# 	final_result = ""
# 	rec = vosk.KaldiRecognizer(model, wf.getframerate())
# 	# pdb.set_trace()
# 	# pdb.set_trace()
# 	while True:
# 		data = wf.readframes(4000)
# 		if len(data) == 0:
# 			break
# 		if rec.AcceptWaveform(data):
# 			result = json.loads(rec.Result())
# 			# print(result)
# 			final_result = final_result + " " + ((result)['text'])
# 			# print(final_result)
# 			# a.append(final_result.values())
# 			# final_result += (" " + str(((result)['text'])))
# 	final_result = " ".join(final_result.split())
# 	with open('output.txt', 'w') as f:
# 		f.write(final_result)
	
	
# 	print(final_result)
# 	# result['text'] = final_result
# 	# pdb.set_trace()
# 	# return jsonify((result)["text"])
# 	return jsonify(final_result)


@app.route('/chat', methods=['POST','GET'])
def chat():
	# with open('C:/Users/Administrator/Documents/text.txt', 'r') as f:
	# 	lines = f.readlines()
	# 	lines = ' '.join([str(elem) for elem in lines])
	# 	f.close()
		data = request.form
		# data = str(data)
		print("Received data :", data)
		prompt = f"Q: {data}\nA:"
		# Make a request to the OpenAI API
		response = requests.post(
			'https://api.openai.com/v1/engines/text-davinci-002/completions',
			headers={
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + token
			},
			json={'prompt':prompt,'temperature':0.7,'max_tokens':100,'n':1,'stop':None})

		# Extract the response text from the OpenAI API response
		response_data = response.json()
		choices = response_data.get('choices')
		if choices and len(choices) > 0:
			# response_text = choices[0].get('text', '').st rip()  
			response_text = response['choices'][0]['text']
		else:
			response_text = "Sorry, I could not generate a response for your query."

		return jsonify({"response": response_text})



@app.route('/textSummarize', methods=['POST','GET'])
def smt():
	# with open('C:/Users/Administrator/Documents/text.txt', 'r') as f:
	# 	lines = f.readlines()
	# 	lines = ' '.join([str(elem) for elem in lines])
	# 	f.close()
		data = request.files['file']
		for line in data:
			# print(line)
			lines = " "	
			lines += str(line)

		print("Received data :", lines)
		data = "Please summarize this: "
		prompt = f"Q: {data + lines}\nA:"
		# Make a request to the OpenAI API
		response = requests.post(
			'https://api.openai.com/v1/engines/text-davinci-002/completions',
			headers={
				'Content-Type': 'application/json',
				'Authorization': 'Bearer ' + token
			},
			json={'prompt':prompt,'temperature':0.7,'max_tokens':100,'n':1,'stop':None})

		# Extract the response text from the OpenAI API response
		response_data = response.json()
		choices = response_data.get('choices')
		if choices and len(choices) > 0:
			response_text = choices[0].get('text', '').strip()
		else:
			response_text = "Sorry, I could not generate a response for your query."

		return jsonify({"response": response_text})


@app.route('/audioToImage', methods=['POST','GET'])
def ati():
	data = request.files['file']
	r = sr.Recognizer()
	# prompt = "Worlds fastest man alive"
	with sr.AudioFile(data) as source:
		audio_text = r.listen(source)
		text = r.recognize_google(audio_text)
		# print(text)
		
		response = openai.Image.create(
		prompt=text,
		n=1,
		size="1024x1024"
		)
		image_url = response['data'][0]['url']

		print(image_url)

	return jsonify({"response": image_url})


#Code to ACCEPT PDF AND Output it's Summary
@app.route('/pdfsummarize', methods=['GET','POST'])
def api():
	# pdb.set_trace()
	data = request.files['file']
	print('Received data:', data)

	reader = PyPDF2.PdfReader(data)
	# page1 = reader.pages[44]
	all_pages = ""
	lenPage = len(reader.pages)
	for i in range(lenPage):
		pages = reader.pages[i]
		# pdfData = pages.extract_text()
		
	# print(len(reader.pages))
	all_pages += pages.extract_text()
	n = len(all_pages)
	if n < 400000000:
		print(all_pages)
		data = all_pages
	# Define the prompt for the OpenAI API
		prompt = f"Q: {PDATA+data}\nA:"

		# Make a request to the OpenAI API
		response = requests.post(
			'https://api.openai.com/v1/engines/text-davinci-002/completions',
			headers={
				'Content-Type': 'application/json',
				'Authorization': 'Bearer '+token
			},
			json={'prompt':prompt,'temperature':0.1,'max_tokens':100,'n':1,'stop':None})

		# Extract the response text from the OpenAI API response
		response_data = response.json()
		choices = response_data.get('choices')
		if choices and len(choices) > 0:
			# response_text = choices[0].get('text', '').strip()
			response_text = response['choices'][0]['text']
		else:
			response_text = "Sorry, I could not generate a response for your query."

		return jsonify({"response": response_text})
	else:
		return jsonify({"response": "Please upload a PDF with characters < 100."})
