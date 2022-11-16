#########################
# GLOBAL VARIABLES USED 主程式區
#########################

ai_name = 'Jarvis'.lower() # 介面最上面的名稱
EXIT_COMMANDS = ['bye','exit','quit','shut down', 'shutdown'] # 結束詞


ownerName = "User" # 使用者名稱 (Settings 介面)
ownerDesignation = "Felix" # 稱呼
ownerPhoto = "1" # 選擇照片一
rec_email, rec_phoneno = "", "" # Email + 手機號碼
WAEMEntry = None

avatarChoosen = 0 # 頭像的選擇
choosedAvtrImage = None # 選擇圖像

botChatTextBg = "#007cc7" 
botChatText = "white" 
userChatTextBg = "#4da8da"

chatBgColor = '#12232e'
background = '#203647'
textColor = 'white'
AITaskStatusLblBG = '#203647'

KCS_IMG = 1 # 0 是 light, 1 是 dark (初始)
voice_id = 1 # 0 是 female, 1 是 male (初始)
ass_volume = 1 # volume (100 為初始)
ass_voiceRate = 200 # Voice rate (200 為 Normal 初始)
startup = 0 # 0 啟動, 1 暫停
stage = 0 # 0: Listening, 1: Adding
buffer = None
####################################### IMPORTING MODULES 導入模組 ########################################### 
""" User Created Modules 與用戶創建相關的py匯入 """
try:
	import normalChat # 基本問答
	import math_function # 數學功能
	import appControl # 程序的控制
	import webScrapping
	import game # 遊戲功能
	from userHandler import UserData # 使用者
	import timer
	import dictionary # 字典功能
	import ToDo # 代辦清單功能
	import fileHandler
	from translates import * # 和語言切換相關的
	from newspaper import article

except Exception as e: # 異常處理
	raise e

""" System Modules 與系統相關的py匯入 """
try:
	import os
	import speech_recognition as sr # 語音辨識模組 (語音轉文字)
	import pyttsx3 # 文字轉語音
	# tkinter 視窗設計
	import playsound
	from tkinter import *
	from tkinter import ttk
	from tkinter import messagebox
	from tkinter import colorchooser
	from PIL import Image, ImageTk # 影像處理套件 (處理和圖片相關的)
	from time import sleep # 時間模組 (sleep 休眠)
	from threading import Thread # 多執行序模組平行化
	
	# word2vec
	from gensim.models.keyedvectors import KeyedVectors

except Exception as e: # 異常處理
	print(e)

if os.path.exists('userData')==False:
	os.mkdir('userData')
############################################ SET UP VOICE ###########################################
try:
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[voice_id].id) # male
	engine.setProperty('volume', ass_volume)
except Exception as e:
	print(e)

t = 0 # 次數
name = []
for voice in voices:
	t += 1
	n1 = voice.name
	n2 = n1.split("- ")
	n3 = n2[1]
	n = re.sub(u"\\(.*?\\)", "", n3)
	name.append(n)
########################################## BOOT UP WINDOW 啟動視窗 ###########################################
def ChangeSettings(write=False):
	import pickle
	global background, textColor, chatBgColor, voice_id, ass_volume, ass_voiceRate, AITaskStatusLblBG, startup, KCS_IMG, botChatTextBg, botChatText, userChatTextBg
	setting = {'background': background,
				'textColor': textColor,
				'chatBgColor': chatBgColor,
				'AITaskStatusLblBG': AITaskStatusLblBG,
				'KCS_IMG': KCS_IMG,
				'botChatText': botChatText,
				'botChatTextBg': botChatTextBg,
				'userChatTextBg': userChatTextBg,
				'voice_id': voice_id,
				'ass_volume': ass_volume,
				'ass_voiceRate': ass_voiceRate,
				'startup' : startup
			}
	if write:
		with open('userData/settings.pck', 'wb') as file:
			pickle.dump(setting, file)
		return
	try:
		with open('userData/settings.pck', 'rb') as file:
			loadSettings = pickle.load(file)
			background = loadSettings['background']
			textColor = loadSettings['textColor']
			chatBgColor = loadSettings['chatBgColor']
			AITaskStatusLblBG = loadSettings['AITaskStatusLblBG']
			KCS_IMG = loadSettings['KCS_IMG']
			botChatText = loadSettings['botChatText']
			botChatTextBg = loadSettings['botChatTextBg']
			userChatTextBg = loadSettings['userChatTextBg']
			voice_id = loadSettings['voice_id']
			ass_volume = loadSettings['ass_volume']
			ass_voiceRate = loadSettings['ass_voiceRate']
			startup = loadSettings['startup']
	except Exception as e:
		pass

if os.path.exists('userData/settings.pck')==False:
	ChangeSettings(True)
	
def getChatColor():
	global chatBgColor
	#chatBgColor = myColor[1]
	colorbar['bg'] = chatBgColor
	chat_frame['bg'] = chatBgColor
	root1['bg'] = chatBgColor

def changeTheme():
	global background, textColor, AITaskStatusLblBG, KCS_IMG, botChatText, botChatTextBg, userChatTextBg, chatBgColor
	if themeValue.get()==1:
		background, textColor, AITaskStatusLblBG, KCS_IMG = "#203647", "white", "#203647",1
		cbl['image'] = cblDarkImg
		kbBtn['image'] = kbphDark
		settingBtn['image'] = sphDark
		AITaskStatusLbl['bg'] = AITaskStatusLblBG
		botChatText, botChatTextBg, userChatTextBg = "white", "#007cc7", "#4da8da"
		chatBgColor = "#12232e"
		colorbar['bg'] = chatBgColor
	else:
		background, textColor, AITaskStatusLblBG, KCS_IMG = "#F6FAFB", "#303E54", "#14A769", 0
		cbl['image'] = cblLightImg
		kbBtn['image'] = kbphLight
		settingBtn['image'] = sphLight
		AITaskStatusLbl['bg'] = AITaskStatusLblBG
		botChatText, botChatTextBg, userChatTextBg = "#494949", "#EAEAEA", "#23AE79"
		chatBgColor = "#F6FAFB"
		colorbar['bg'] = '#E8EBEF'

	root['bg'], root2['bg'] = background, background
	settingsFrame['bg'] = background
	settingsLbl['fg'], userPhoto['fg'], userName['fg'], assLbl['fg'], voiceRateLbl['fg'], volumeLbl['fg'], themeLbl['fg'], chooseChatLbl['fg'],  startupbl['fg'] = textColor, textColor, textColor, textColor, textColor, textColor, textColor, textColor, textColor
	settingsLbl['bg'], userPhoto['bg'], userName['bg'], assLbl['bg'], voiceRateLbl['bg'], volumeLbl['bg'], themeLbl['bg'], chooseChatLbl['bg'],  startupbl['bg'] = background, background, background, background, background, background, background, background, background
	s.configure('Wild.TRadiobutton', background=background, foreground=textColor)
	volumeBar['bg'], volumeBar['fg'], volumeBar['highlightbackground'] = background, textColor, background
	chat_frame['bg'], root1['bg'] = chatBgColor, chatBgColor
	userPhoto['activebackground'] = background
	ChangeSettings(True)

def changeVoice(e):
	global voice_id
	voice_id = 0
	voice_id = name.index(assVoiceOption.get(),0,t)
	engine.setProperty('voice', voices[voice_id].id)
	ChangeSettings(True)

def changeVolume(e):
	global ass_volume
	ass_volume = volumeBar.get() / 100
	engine.setProperty('volume', ass_volume)
	ChangeSettings(True)

def changeVoiceRate(e):
	global ass_voiceRate
	temp = voiceOption.get()
	if temp=='Very Low': ass_voiceRate = 100
	elif temp=='Low': ass_voiceRate = 150
	elif temp=='Fast': ass_voiceRate = 250
	elif temp=='Very Fast': ass_voiceRate = 300
	else: ass_voiceRate = 200
	#print(ass_voiceRate)
	engine.setProperty('rate', ass_voiceRate)
	ChangeSettings(True)

def startupTheme():
	global startup
	if startupValue.get() == 0: 
		startup = 0
		engine.setProperty('start', startup)
		Button(settingsFrame, image=cimg, relief=FLAT, command=getChatColor).place(x=261, y=180)
		backBtn = Button(settingsFrame, text='   Back   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=setChatModeToSpeach)
		backBtn.place(x=5, y=275)
	if startupValue.get() == 1: 
		startup = 1
		engine.setProperty('pause', startup)
		raise_frame(root2)
		clearChatScreen()
		Button(settingsFrame, image=cimg, relief=FLAT, command=getChatColor).place(x=261, y=180)
		backBtn = Button(settingsFrame, text='   Back   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=None)
		backBtn.place(x=5, y=275)
	ChangeSettings(True)
ChangeSettings()
####################################### SET UP TEXT TO SPEECH #######################################
def speak(text, display=False, icon=False):
	from googletrans import Translator # Google 翻譯 裡面有的語言：LANGUAGES
	translator = Translator() # 創造翻譯物件
	lan = googletrans(assVoiceOption.get())
	if text != '':
		text = translator.translate(text,lan).text
	text = trans(text)
	AITaskStatusLbl['text'] = 'Speaking...'
	if icon: Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w',pady=0)
	if display: attachTOframe(text, True)
	print('\n'+ai_name.upper()+': '+text)
	try:
		engine.say(text)
		engine.runAndWait()
	except:
		print("Try not to type more...")
####################################### SET UP SPEECH TO TEXT #######################################
def record(clearChat=True, iconDisplay=True):
	from googletrans import Translator # Google 翻譯 裡面有的語言：LANGUAGES
	translator = Translator() # 創造翻譯物件
	lan = googletrans(assVoiceOption.get())
	print('\nListening...')
	AITaskStatusLbl['text'] = 'Listening...'
	r = sr.Recognizer()

	r.dynamic_energy_threshold = False
	r.energy_threshold = 4000
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
		said = ""
		try:
			if chatMode == 1:
				return ''
			else:
				AITaskStatusLbl['text'] = 'Processing...'
				said = r.recognize_google(audio, language=lan) # 選擇辨識的語言
				print(f"\nUser said: {said}")
				if clearChat:
					clearChatScreen()
				if iconDisplay: Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
				attachTOframe(said)
		except Exception as e:
			print(e)
			# speak("I didn't get it, Say that again please...")
			if "connection failed" in str(e):
				speak("Your System is Offline...", True, True)
			return 'None'
	print(trans_e(translator.translate(said,'en').text).lower())	
	return trans_e(translator.translate(said,'en').text).lower()
def voiceMedium():
	global chatMode, speachThread, startup
	while True:
		if chatMode != 0:
			print("stopping speach thread inside function")
			speachThread = None
			return
		
		startupTheme()
		query = record()
		if query == 'None': continue

		if isContain(query, EXIT_COMMANDS):
			speak("Shutting down the System. Good Bye "+ownerDesignation+"!", True, True)
			break
		elif chatMode == 0: main(query.lower())
	appControl.Win_Opt('close')

def keyboardInput(e):
	from googletrans import Translator # Google 翻譯 裡面有的語言：LANGUAGES
	translator = Translator() # 創造翻譯物件
	global startup
	user_input = UserField.get().lower()
	if user_input != "":
		clearChatScreen()
		print(user_input)
		user_input_en = trans_e(translator.translate(user_input,'en').text)
		print(user_input_en)

		if isContain(user_input_en, 'pause'):
			startup = 1
			engine.setProperty('pause', startup)
			startupValue.set(1)

		if isContain(user_input_en, EXIT_COMMANDS):
			speak("Shutting down the System. Good Bye "+ownerDesignation+"!", True, True)
		else:
			Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
			attachTOframe(user_input.capitalize())
			Thread(target=main, args=(user_input_en,)).start() #Every time you type, it starts a new Thread, Thread can't easily communicate with eachother, so you neeed to store a stage, the listening stage, an Creating a List stage,
		UserField.delete(0, END)


###################################### LOAD WORD2VEC MODEL  #########################################

print("Loading Word2Vec model, please wait.")
w2v_model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
print("Word2Vec loading complete!")
w2v_vocab = list(w2v_model.index_to_key)

def determineYesNo(sentence):
   splited = re.split('\W', sentence)
   splited = list(filter(None, splited))
   yes_score = 0
   no_score = 0
   for word in splited:
      if word in w2v_vocab:
         yes_score += w2v_model.similarity('yes', word)
         no_score += w2v_model.similarity('no', word)
   print("Similarities: yes: " + str(yes_score) + ", no: " + str(no_score))
   if yes_score == 0 and no_score == 0:
      return False
   return yes_score > no_score

###################################### TASK/COMMAND HANDLER #########################################
def isContain(txt, lst):
	for word in lst:
		if word in txt:
			return True
	return False

buffer = None

def main(text):
		global stage, buffer

		if stage == 1:
			ToDo.toDoList(text)
			speak("Alright, I added to your list", True)
			stage = 0
			return
		elif stage == 2:
			projectName = text
			speak(fileHandler.CreateHTMLProject(projectName.capitalize()), True)
			stage = 0
		elif stage == 3:
			buffer = text
			speak("Which language to translate ?", True)
			stage = 4
			return
		elif stage == 4:
			sentence = buffer
			language = translate(text)
			print(language)
			result = normalChat.lang_translate(sentence, language)
			print(result)
			if result=="None": speak("This language doesn't exists")
			else:
					speak(f"In {language.capitalize()} you would say:", True)
					attachTOframe(result.text, True)
					engine.say(result.pronunciation)
					engine.runAndWait()
			stage = 0
			return
		elif stage == 5: 
			if not determineYesNo(text):
				speak("No Problem "+ownerDesignation, True)
			else:
				speak("Ok "+ownerDesignation+", Opening browser...", True)
				webScrapping.openWebsite('https://www.taiwannews.com.tw/en/index')
				speak("You can now read the full news from this website.")
			stage = 0
			return
		elif stage == 6:
			buffer = text
			speak("Ok "+ownerDesignation+", Where you want to go?", True)
			stage = 7
			return
		elif stage == 7:
			startingPoint = buffer
			destinationPoint = text
			speak("Ok "+ownerDesignation+", Getting Directions...", True)
			try:
				distance = webScrapping.giveDirections(startingPoint, destinationPoint)
				speak('You have to cover a distance of '+ distance, True)
			except:
				speak("I think location is not proper, Try Again!")
			stage = 0
			return
		elif stage == 8:
			buffer = text
			speak('What message you want to send ?', True)
			stage = 9
			return
		elif stage == 9:
			message = text
			subject = buffer
			Thread(target=webScrapping.email, args=(rec_email,message,subject,) ).start()
			speak('Email has been Sent', True)
			return
		elif stage == 10:
			buffer = text
			if text=="None":
				speak("Didn't understand what you say?", True, True)
				return
			if 'online' in text:
				speak("Ok "+ownerDesignation+", Let's play some online games", True, True)
				webScrapping.openWebsite('https://www.agame.com/games/mini-games/')
				return
			if not determineYesNo(text):
				speak("No Problem "+ownerDesignation+", We'll play next time.", True, True)
			else:
				speak("Ok "+ownerDesignation+", Let's Play " + text, True, True)
				os.system(f"python -c \"import game; game.play('{text}')\"")
			stage = 0
			return
			

		if "project" in text:
			if isContain(text, ['make', 'create']):
				speak("What do you want to give the project name ?", True, True)
				stage = 2
				return

		if "create" in text and "file" in text:
			speak(fileHandler.createFile(text), True, True)
			return

		if "translate" in text:
			speak("What do you want to translate?", True, True)
			stage = 3
			return

		if 'list' in text:
			if isContain(text, ['add', 'create', 'make']):
				speak("What do you want to add?", True, True)
				# Set Stage to Adding stuff to a list, and then return, let the next Thread handles the adding part
				stage = 1
				return
			if isContain(text, ['show', 'my list']):
				items = ToDo.showtoDoList()
				if len(items)==1:
					speak(items[0], True, True)
					return
				attachTOframe('\n'.join(items), True)
				speak(items[0])
				return

		if isContain(text, ['battery', 'system info']):
			result = appControl.OSHandler(text)
			if len(result)==2:
				speak(result[0], True, True)
				attachTOframe(result[1], True)
			else:
				speak(result, True, True)
			return
			
		if isContain(text, ['meaning', 'dictionary', 'definition', 'define']):
			result = dictionary.translate(text)
			speak(result[0], True, True)
			if result[1]=='': return
			speak(result[1], True)
			return

		if 'volume' in text:
			appControl.volumeControl(text)
			Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w',pady=0)		
			attachTOframe('Volume Settings Changed', True)
			return
			
		if isContain(text, ['timer', 'countdown']):
			Thread(target=timer.startTimer, args=(text,)).start()
			speak('Ok, Timer Started!', True, True)
			return

		if 'email' in text:
			speak('Whom do you want to send the email?', True, True)
			WAEMPOPUP("Email", "E-mail Address")
			attachTOframe(rec_email)
			speak('What is the Subject?', True)
			stage = 8
			return

		if isContain(text, ['covid','virus']):
			result = webScrapping.covid(text)
			if 'str' in str(type(result)):
				speak(result, True, True)
				return
			speak(result[0], True, True)
			result = '\n'.join(result[1])
			attachTOframe(result, True)
			return

		if isContain(text, ['youtube','video']):
			speak("Ok "+ownerDesignation+", here a video for you...", True, True)
			try:
				speak(webScrapping.youtube(text), True)
			except Exception as e:
				speak("Video Result Not Found", True)
			return

		if isContain(text, ['search', 'image']):
			if 'image' in text and 'show' in text:
				Thread(target=showImages, args=(text,)).start()
				speak('Here are the images...', True, True)
				return
			speak(webScrapping.googleSearch(text), True, True)
			return
			
		if isContain(text, ['map', 'direction']):
			if "direction" in text:
				speak('What is your starting location?', True, True)
				stage = 6
				return
			else:
				webScrapping.maps(text)
				speak('Here you go...', True, True)
			return

		if isContain(text, ['factorial','log','value of','math',' + ',' - ',' x ','multiply','divided by','binary','hexadecimal','octal','shift','sin ','cos ','tan ']):
			try:
				speak(('Result is: ' + math_function.perform(text)), True, True)
			except Exception as e:
				return
			return

		if "joke" in text:
			speak('Here is a joke...', True, True)
			speak(webScrapping.jokes(), True)
			return

		if isContain(text, ['news']):
			speak('Getting the latest news...', True, True)
			headlines,headlineLinks = webScrapping.latestNews(2)
			for head in headlines: speak(head, True)
			speak('Do you want to read the full news?', True)
			stage = 5
			return

		if isContain(text, ['weather']):
			data = webScrapping.weather()
			speak('', False, True)
			showSingleImage("weather", data[:-1])
			speak(data[-1])
			return

		if isContain(text, ['screenshot']):
			Thread(target=appControl.Win_Opt, args=('screenshot',)).start()
			speak("Screen Shot Taken", True, True)
			return

		if isContain(text, ['window','close that']):
			appControl.Win_Opt(text)
			return

		if isContain(text, ['settings']):
			raise_frame(root2)
			clearChatScreen()
			return

		if isContain(text, ['open','type','save','delete','select','press enter']):
			appControl.System_Opt(text)
			return

		if isContain(text, ['wiki', 'who is']):
			Thread(target=webScrapping.downloadImage, args=(text, 1,)).start()
			speak('Searching...', True, True)
			result = webScrapping.wikiResult(text)
			showSingleImage('wiki')
			speak(result, True)
			return
		
		if isContain(text, ['game']):
			speak("Which game do you want to play?", True, True)
			attachTOframe(game.showGames(), True)
			stage = 10
			return

		if isContain(text, ['coin','dice','die']):
			if "toss" in text or "roll" in text or "flip" in text:
				speak("Ok "+ownerDesignation, True, True)
				result = game.play(text)
				if "Head" in result: showSingleImage('head')
				elif "Tail" in result: showSingleImage('tail')
				else: showSingleImage(result[-1])
				speak(result)
				return

		if isContain(text, ['time','date']):
			speak(normalChat.chat(text), True, True)
			return

		if 'my name' in text:
			speak('Your name is, ' + ownerName, True, True)
			return

		if isContain(text, ['morning','evening','noon']) and 'good' in text:
			speak(normalChat.chat("good"), True, True)
			return
		
		if isContain(text, ['pause']):
			startup = 1
			engine.setProperty('pause', startup)
			startupValue.set(1)
			raise_frame(root2)
			clearChatScreen()
			return

		result = normalChat.reply(text)
		if result != "None": speak(result, True, True)
		else:
			speak("Sorry, I couldn't understand. Please try again.", True, True)
			#speak("Here's what I found on the web... ", True, True)
			#webScrapping.googleSearch(text) #uncomment this if you want to show the result on web, means if nothing found
		
##################################### DELETE USER ACCOUNT #########################################
def deleteUserData():
	result = messagebox.askquestion('Alert', 'Are you sure you want to exit ?')
	if result=='no': return
	root.destroy()
						#####################
						####### GUI #########
						#####################

############ ATTACHING BOT/USER CHAT ON CHAT SCREEN ###########
def attachTOframe(text,bot=False):
	if bot:
		botchat = Label(chat_frame,text=text, bg=botChatTextBg, fg=botChatText, justify=LEFT, wraplength=250, font=('Montserrat',12, 'bold'))
		botchat.pack(anchor='w',ipadx=5,ipady=5,pady=5)
	else:
		userchat = Label(chat_frame, text=text, bg=userChatTextBg, fg='white', justify=RIGHT, wraplength=250, font=('Montserrat',12, 'bold'))
		userchat.pack(anchor='e',ipadx=2,ipady=2,pady=5)

def clearChatScreen():
	for wid in chat_frame.winfo_children():
		wid.destroy()

### SWITCHING BETWEEN FRAMES ###
def raise_frame(frame):
	frame.tkraise()
	clearChatScreen()

################# SHOWING DOWNLOADED IMAGES ###############
img0, img1, img2, img3, img4 = None, None, None, None, None
def showSingleImage(type, data=None):
	global img0, img1, img2, img3, img4
	try:
		img0 = ImageTk.PhotoImage(Image.open('Downloads/0.jpg').resize((90,110), Image.ANTIALIAS))
	except:
		pass
	img1 = ImageTk.PhotoImage(Image.open('extrafiles/images/heads.jpg').resize((220,200), Image.ANTIALIAS))
	img2 = ImageTk.PhotoImage(Image.open('extrafiles/images/tails.jpg').resize((220,200), Image.ANTIALIAS))
	img4 = ImageTk.PhotoImage(Image.open('extrafiles/images/WeatherImage.png'))

	if type=="weather":
		weather = Frame(chat_frame)
		weather.pack(anchor='w')
		Label(weather, image=img4, bg=chatBgColor).pack()
		Label(weather, text=data[0], font=('Arial Bold', 45), fg='white', bg='#3F48CC').place(x=65,y=45)
		Label(weather, text=data[1], font=('Montserrat', 15), fg='white', bg='#3F48CC').place(x=78,y=110)
		Label(weather, text=data[2], font=('Montserrat', 10), fg='white', bg='#3F48CC').place(x=78,y=140)
		Label(weather, text=data[3], font=('Arial Bold', 12), fg='white', bg='#3F48CC').place(x=60,y=160)

	elif type=="wiki":
		Label(chat_frame, image=img0, bg='#EAEAEA').pack(anchor='w')
	elif type=="head":
		Label(chat_frame, image=img1, bg='#EAEAEA').pack(anchor='w')
	elif type=="tail":
		Label(chat_frame, image=img2, bg='#EAEAEA').pack(anchor='w')
	else:
		img3 = ImageTk.PhotoImage(Image.open('extrafiles/images/dice/'+type+'.jpg').resize((200,200), Image.ANTIALIAS))
		Label(chat_frame, image=img3, bg='#EAEAEA').pack(anchor='w')
	
def showImages(query):
	global img0, img1, img2, img3
	webScrapping.downloadImage(query)
	w, h = 150, 110
	#Showing Images
	imageContainer = Frame(chat_frame, bg='#EAEAEA')
	imageContainer.pack(anchor='w')
	#loading images
	img0 = ImageTk.PhotoImage(Image.open('Downloads/0.jpg').resize((w,h), Image.ANTIALIAS))
	img1 = ImageTk.PhotoImage(Image.open('Downloads/1.jpg').resize((w,h), Image.ANTIALIAS))
	img2 = ImageTk.PhotoImage(Image.open('Downloads/2.jpg').resize((w,h), Image.ANTIALIAS))
	img3 = ImageTk.PhotoImage(Image.open('Downloads/3.jpg').resize((w,h), Image.ANTIALIAS))
	#Displaying
	Label(imageContainer, image=img0, bg='#EAEAEA').grid(row=0, column=0)
	Label(imageContainer, image=img1, bg='#EAEAEA').grid(row=0, column=1)
	Label(imageContainer, image=img2, bg='#EAEAEA').grid(row=1, column=0)
	Label(imageContainer, image=img3, bg='#EAEAEA').grid(row=1, column=1)


############################# WAEM - WhatsApp Email ##################################
def sendWAEM():
	global rec_phoneno, rec_email
	data = WAEMEntry.get()
	rec_email, rec_phoneno = data, data
	WAEMEntry.delete(0, END)
	appControl.Win_Opt('close') # 關閉程序
def send(e):
	sendWAEM()

def WAEMPOPUP(Service='None', rec='Reciever'):
	global WAEMEntry
	PopUProot = Tk()
	PopUProot.title(f'{Service} Service')
	PopUProot.configure(bg='white')

	if Service=="WhatsApp": PopUProot.iconbitmap("extrafiles/images/whatsapp.ico")
	else: PopUProot.iconbitmap("extrafiles/images/email.ico")
	w_width, w_height = 410, 200
	s_width, s_height = PopUProot.winfo_screenwidth(), PopUProot.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	PopUProot.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	Label(PopUProot, text=f'Reciever {rec}', font=('Arial', 16), bg='white').pack(pady=(20, 10))
	WAEMEntry = Entry(PopUProot, bd=10, relief=FLAT, font=('Arial', 12), justify='center', bg='#DCDCDC', width=30)
	WAEMEntry.pack()
	WAEMEntry.focus()

	SendBtn = Button(PopUProot, text='Send', font=('Arial', 12), relief=FLAT, bg='#14A769', fg='white', command=sendWAEM)
	SendBtn.pack(pady=20, ipadx=10)
	PopUProot.bind('<Return>', send)
	PopUProot.mainloop()

######################## CHANGING CHAT BACKGROUND COLOR #########################
def getChatColor():
	global chatBgColor
	myColor = colorchooser.askcolor()
	if myColor[1] is None: return
	chatBgColor = myColor[1]
	colorbar['bg'] = chatBgColor
	chat_frame['bg'] = chatBgColor
	root1['bg'] = chatBgColor
	ChangeSettings(True)

chatMode = 0
def setChatMode(newChatMode):
	global chatMode
	chatMode = newChatMode
	if chatMode == 1:
		#print("Setting chatmode to 1")
		VoiceModeFrame.pack_forget()
		TextModeFrame.pack(fill=BOTH)
		UserField.focus()
	elif chatMode == 2:
		#print("Setting chatmode to 2")
		VoiceModeFrame.pack_forget()
		TextModeFrame.pack(fill=BOTH)
		raise_frame(root2)
		clearChatScreen()
	elif chatMode == 0:
		#print("Setting chatmode to 0")
		startSpeachThread()
		TextModeFrame.pack_forget()
		VoiceModeFrame.pack(fill=BOTH)
		raise_frame(root1)
		root.focus()

def setChatModeToSpeach():
	setChatMode(0)

def setChatModeToText():
	setChatMode(1)

def setChatModeToSettings():
	setChatMode(2)
#####################################  MAIN GUI ####################################################

#### SPLASH/LOADING SCREEN ####

def destroySplash():
	splash_root.destroy()

speachThread = None
def startSpeachThread():
	global speachThread
	if speachThread == None:
		print("Starting speach process")
		speachThread = Thread(target=voiceMedium, args=())
		speachThread.start()

#print("Process: ", __name__)

if __name__ == '__main__':
	splash_root = Tk()
	splash_root.configure(bg='#3895d3')
	splash_root.overrideredirect(True)
	splash_label = Label(splash_root, text="Processing...", font=('montserrat',15),bg='#3895d3',fg='white')
	splash_label.pack(pady=40)
	# splash_percentage_label = Label(splash_root, text="0 %", font=('montserrat',15),bg='#3895d3',fg='white')
	# splash_percentage_label.pack(pady=(0,10))

	w_width, w_height = 400, 200
	s_width, s_height = splash_root.winfo_screenwidth(), splash_root.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	splash_root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30))

	splash_root.after(10, destroySplash)
	splash_root.mainloop()

	root = Tk()
	root.title('Jarvis')
	w_width, w_height = 400, 650
	s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	root.configure(bg=background)
	# root.resizable(width=False, height=False)
	root.pack_propagate(0)

	root1 = Frame(root, bg=chatBgColor)
	root2 = Frame(root, bg=background)
	root3 = Frame(root, bg=background)

	for f in (root1, root2, root3):
		f.grid(row=0, column=0, sticky='news')	
	
	################################
	########  CHAT SCREEN  #########
	################################

	#Chat Frame
	chat_frame = Frame(root1, width=380,height=551,bg=chatBgColor)
	chat_frame.pack(padx=10)
	chat_frame.pack_propagate(0)

	bottomFrame1 = Frame(root1, bg='#dfdfdf', height=100)
	bottomFrame1.pack(fill=X, side=BOTTOM)
	VoiceModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
	VoiceModeFrame.pack(fill=BOTH)
	TextModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
	TextModeFrame.pack(fill=BOTH)

	# VoiceModeFrame.pack_forget()
	TextModeFrame.pack_forget()

	cblLightImg = PhotoImage(file='extrafiles/images/centralButton.png')
	cblDarkImg = PhotoImage(file='extrafiles/images/centralButton1.png')
	if KCS_IMG==1: cblimage=cblDarkImg
	else: cblimage=cblLightImg
	cbl = Label(VoiceModeFrame, fg='white', image=cblimage, bg='#dfdfdf')
	cbl.pack(pady=17)
	AITaskStatusLbl = Label(VoiceModeFrame, text='    Offline', fg='white', bg=AITaskStatusLblBG, font=('montserrat', 16))
	AITaskStatusLbl.place(x=140,y=32)
	
	#Settings Button
	sphLight = PhotoImage(file = "extrafiles/images/setting.png")
	sphLight = sphLight.subsample(2,2)
	sphDark = PhotoImage(file = "extrafiles/images/setting1.png")
	sphDark = sphDark.subsample(2,2)
	if KCS_IMG==1: sphimage=sphDark
	else: sphimage=sphLight
	settingBtn = Button(VoiceModeFrame,image=sphimage,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf",command=setChatModeToSettings)
	settingBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
	
	#Keyboard Button
	kbphLight = PhotoImage(file = "extrafiles/images/keyboard.png")
	kbphLight = kbphLight.subsample(2,2)
	kbphDark = PhotoImage(file = "extrafiles/images/keyboard1.png")
	kbphDark = kbphDark.subsample(2,2)
	if KCS_IMG==1: kbphimage=kbphDark
	else: kbphimage=kbphLight
	kbBtn = Button(VoiceModeFrame,image=kbphimage,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf", command=setChatModeToText)
	kbBtn.place(x=25, y=30)

	#Mic
	micImg = PhotoImage(file = "extrafiles/images/mic.png")
	micImg = micImg.subsample(2,2)
	micBtn = Button(TextModeFrame,image=micImg,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf", command=setChatModeToSpeach)
	micBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
	
	#Text Field
	TextFieldImg = PhotoImage(file='extrafiles/images/textField.png')
	UserFieldLBL = Label(TextModeFrame, fg='white', image=TextFieldImg, bg='#dfdfdf')
	UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
	UserField = Entry(TextModeFrame, fg='white', bg='#203647', font=('Montserrat', 16), bd=6, width=22, relief=FLAT)
	UserField.place(x=20, y=30)
	UserField.insert(0, "Ask me anything...")
	UserField.bind('<Return>', keyboardInput)
	
	#User and Bot Icon
	userIcon = PhotoImage(file="extrafiles/images/avatars/ChatIcons/a"+str(ownerPhoto)+".png")
	botIcon = PhotoImage(file="extrafiles/images/assistant2.png")
	botIcon = botIcon.subsample(2,2)
	

	###########################
	########  SETTINGS  #######
	###########################

	settingsLbl = Label(root2, text='Settings', font=('Arial Bold', 15), bg=background, fg=textColor)
	settingsLbl.pack(pady=10)
	separator = ttk.Separator(root2, orient='horizontal')
	separator.pack(fill=X)
	#User Photo
	userProfileImg = Image.open("extrafiles/images/avatars/a"+str(ownerPhoto)+".png")
	userProfileImg = ImageTk.PhotoImage(userProfileImg.resize((120, 120)))
	userPhoto = Button(root2, image=userProfileImg, bg=background, bd=0, relief=FLAT, activebackground=background)
	userPhoto.pack(pady=(20, 5))

	#Username
	userName = Label(root2, text=ownerName, font=('Arial Bold', 15), fg=textColor, bg=background)
	userName.pack()

	#Settings Frame
	settingsFrame = Frame(root2, width=350, height=350, bg=background)
	settingsFrame.pack(pady=20)

	assLbl = Label(settingsFrame, text='Language', font=('Arial', 13), fg=textColor, bg=background)
	assLbl.place(x=0, y=20)
	n = StringVar()

	assVoiceOption = ttk.Combobox(settingsFrame, values=(name), font=('Arial', 13), width=13, textvariable=n)
	assVoiceOption.current(voice_id)
	assVoiceOption.place(x=150, y=20)
	assVoiceOption.bind('<<ComboboxSelected>>', changeVoice)

	voiceRateLbl = Label(settingsFrame, text='Voice Rate', font=('Arial', 13), fg=textColor, bg=background)
	voiceRateLbl.place(x=0, y=60)
	n2 = StringVar()
	voiceOption = ttk.Combobox(settingsFrame, font=('Arial', 13), width=13, textvariable=n2)
	voiceOption['values'] = ('Very Low', 'Low', 'Normal', 'Fast', 'Very Fast')
	voiceOption.current(ass_voiceRate//50-2) #100 150 200 250 300
	voiceOption.place(x=150, y=60)
	voiceOption.bind('<<ComboboxSelected>>', changeVoiceRate)
	
	volumeLbl = Label(settingsFrame, text='Volume', font=('Arial', 13), fg=textColor, bg=background)
	volumeLbl.place(x=0, y=105)
	volumeBar = Scale(settingsFrame, bg=background, fg=textColor, sliderlength=30, length=135, width=16, highlightbackground=background, orient='horizontal', from_=0, to=100, command=changeVolume)
	volumeBar.set(int(ass_volume*100))
	volumeBar.place(x=150, y=85)

	startupbl = Label(settingsFrame, text='Start up', font=('Arial', 13), fg=textColor, bg=background)
	startupbl.place(x=0,y=225)
	startupValue = IntVar()
	s1 = ttk.Style()
	s1.configure('Wild.TRadiobutton', font=('Arial Bold', 10), background=background, foreground=textColor, focuscolor=s1.configure(".")["background"])
	startBtn = ttk.Radiobutton(settingsFrame, text='Start', value=0, variable=startupValue, style='Wild.TRadiobutton', command=startupTheme, takefocus=False)
	startBtn.place(x=150,y=225)
	pauseBtn = ttk.Radiobutton(settingsFrame, text='Pause', value=1, variable=startupValue, style='Wild.TRadiobutton', command=startupTheme, takefocus=False)
	pauseBtn.place(x=230,y=225)
	startupValue.set(1)
	if startup == 0: startupValue.set(0)

	themeLbl = Label(settingsFrame, text='Theme', font=('Arial', 13), fg=textColor, bg=background)
	themeLbl.place(x=0,y=143)
	themeValue = IntVar()
	s = ttk.Style()
	s.configure('Wild.TRadiobutton', font=('Arial Bold', 10), background=background, foreground=textColor, focuscolor=s.configure(".")["background"])
	darkBtn = ttk.Radiobutton(settingsFrame, text='Dark', value=1, variable=themeValue, style='Wild.TRadiobutton', command=changeTheme, takefocus=False)
	darkBtn.place(x=150,y=145)
	lightBtn = ttk.Radiobutton(settingsFrame, text='Light', value=2, variable=themeValue, style='Wild.TRadiobutton', command=changeTheme, takefocus=False)
	lightBtn.place(x=230,y=145)
	themeValue.set(1)
	if KCS_IMG==0: themeValue.set(2)

	chooseChatLbl = Label(settingsFrame, text='Chat Background', font=('Arial', 13), fg=textColor, bg=background)
	chooseChatLbl.place(x=0,y=180)
	cimg = PhotoImage(file = "extrafiles/images/colorchooser.png")
	cimg = cimg.subsample(3,3)
	colorbar = Label(settingsFrame, bd=3, width=18, height=1, bg=chatBgColor)
	colorbar.place(x=150, y=180)
	if KCS_IMG==0: colorbar['bg'] = '#E8EBEF'
	Button(settingsFrame, image=cimg, relief=FLAT, command=getChatColor).place(x=261, y=180)
	backBtn = Button(settingsFrame, text='   Back   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=setChatModeToSpeach)
	clearFaceBtn = Button(settingsFrame, text='   Close the ChatBot   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=deleteUserData)
	backBtn.place(x=5, y=275)
	clearFaceBtn.place(x=150, y=275)

	try:
		# pass
		Thread(target=webScrapping.dataUpdate).start()
	except Exception as e:
		print('System is Offline...')

	setChatMode(chatMode)
	
	root.iconbitmap('extrafiles/images/assistant2.ico')
	raise_frame(root1)
	root.mainloop()