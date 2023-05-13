import telebot
import openai 
from pydub import AudioSegment

openai.api_key = "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"
proxy_url = "socks5://sockduser:f2%kE%.)as!S@46.101.118.222:6666"
telebot.apihelper.proxy = {
	'http': proxy_url,
	'https': proxy_url
}

bot = telebot.TeleBot("5999868700:AAFnUm53zFJMAAUTtuMUlz-gUifuLkdYu_U")

@bot.message_handler(commands=['start'])
def message_handler_start_main(message):
	msg = bot.send_message(message.chat.id, 'hey hi')
	return

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	response = openai.ChatCompletion.create(
	    model="gpt-3.5-turbo-0301",
	    messages=[
	            {"role": "system", "content": "You are a chatbot"},
	            {"role": "user", "content": message.text},
	        ]
	)
	result = ''
	for choice in response.choices:
	    result += choice.message.content
	bot.send_message(message.chat.id,result)

@bot.message_handler(content_types=['voice', 'audio'])
def get_audio_messages(message):
	file_info = bot.get_file(message.voice.file_id)
	print(file_info.file_path)
	downloaded_file = bot.download_file(file_info.file_path)
	print(downloaded_file)
	with open('user_voice.ogg', 'wb') as new_file:
		new_file.write(downloaded_file)
	AudioSegment.from_file("/Users/sepezho/Work/ai/user_voice.ogg", format="ogg").export("/Users/sepezho/Work/ai/audio.mp3", format="mp3")
	audio_file= open("audio.mp3", "rb")
	transcript = openai.Audio.transcribe("whisper-1",audio_file)
	print(transcript.text)
	response = openai.ChatCompletion.create(
	    model="gpt-3.5-turbo-0301",
	    messages=[
	            {"role": "system", "content": "You are a chatbot"},
	            {"role": "user", "content": transcript.text},
	        ]
	)
	result = ''
	for choice in response.choices:
	    result += choice.message.content
	bot.send_message(message.chat.id,result)

bot.polling()

