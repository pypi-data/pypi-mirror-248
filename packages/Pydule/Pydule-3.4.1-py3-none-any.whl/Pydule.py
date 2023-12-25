import datetime
import os
import tkinter as tk
import pyttsx3 
from tkinter import *

engine = pyttsx3.init() 

facemoji='\U0001F605'
err='\U0000274C'

def underdevelopment(wifiname):
	if isinstance(wifiname,str):
		import subprocess
		command = f"netsh wlan show profile name={wifiname} key=clear"
		output = subprocess.check_output(command, shell=True)
		output = output.decode("utf-8")
		password_index = output.find("Key Content")
		password = output[password_index+17:password_index+49]
		return f"Wifi-Name : {wifiname}\nWifi Password : {password}"
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str and str and int {err}')

def DesktopNotification(title:str,sub:str,t:int):
	if isinstance(title,str) and isinstance(sub,str) and isinstance(t,int):
		from win10toast import ToastNotifier
	
		root = ToastNotifier()
	
		root.show_toast(title,sub, duration = t)

	else:
		print(f'{err} Arguments Must {facemoji} Be in str and str and int {err}')

def openapp(appname:str) -> str:
	if isinstance(appname,str):
		from AppOpener import open
		open(appname)
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')	

def RemoveBG(ipath:str):
	if isinstance(ipath,str):
		from rembg import remove
		from PIL import Image
		import datetime

		filename = "Pydule Removed BG -" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".png"
		
		i = Image.open(ipath)
		
		o = remove(i)
		
		o.save(filename)
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str and str {err}')	 

def SepRowCsv(filehandler,clm:str,find:str) -> list:
	if str(type(filehandler))=="<class '_io.TextIOWrapper'>" and isinstance(find,str) and isinstance(clm,str):
		import csv

		index = 0

		c=csv.reader(filehandler)
	
		for i in c:
			if clm in i:
				index=i.index(clm)
				continue

			else:
				if i[index]==find:
					return i


	else:
		print(f'{err} Arguments Must {facemoji} Be in _io.TextIOWrapper and str and str {err}')	 

def SepColumnCsv(filehandler,find:str) -> list:
	if str(type(filehandler))=="<class '_io.TextIOWrapper'>" and isinstance(find,str):
		import csv

		c,l=csv.reader(filehandler),[]
	
		for i in c:
			if find in i:
				index=i.index(find)
				continue
			else:
				l+=[i[index]]

		return l

	else:
		print(f'{err} Arguments Must {facemoji} Be in _io.TextIOWrapper and str {err}')		

def inputpassword(st:str='') -> str:
	if isinstance(st,str):
		from getpass import getpass

		return getpass(st)
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')   

def sepednumtoint(st:str) -> int:
	if isinstance(st,str):
		sep,new=st,''
		
		for i in sep:
			if i!=',':
				new+=i
			
		return int(new)
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')

def sepnum(num:int) -> str:
	if isinstance(num,int):

		return f'{num:,}'
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in int {err}') 

def shufflelist(l) -> list:
	if isinstance(l,list):
		import random as r

		ind,n=[],[]
		
		while True:
			ran=r.randint(0,len(l)-1)
			
			if len(ind)==len(l):
				break
			
			if ran not in ind:
				ind+=[ran]
		
		for i in ind:
			n+=[l[i]] 
		
		return n

	else:
		print(f'{err} Arguments Must {facemoji} Be in list {err}')

def shuffledict(d:dict) -> dict:
	if isinstance(d,dict):
		import random as r

		nd,l={},[]

		for i in d:
			l+=[i]

		while True:
			ran=r.randint(0,len(l)-1)

			if len(l)==len(nd):
				break

			if l[ran] not in nd:
				nd[l[ran]]=d[l[ran]]

		return nd
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in dict {err}')	

def FIGlet(string:str) -> str:
	if isinstance(string,str):
		import pyfiglet

		FIGlet = pyfiglet.figlet_format(string)

		return FIGlet
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')	

def internetspeed() -> list:
	import speedtest
	
	st = speedtest.Speedtest()

	download = st.download() / 10**6

	upload = st.upload() / 10**6

	return [f"{download:.2f} Mbps",f"{upload:.2f} Mbps"]

def pytoexe(filename:str,windowed:bool=False,noconsole:bool=True):
	if isinstance(filename,str) and isinstance(windowed,bool) and isinstance(noconsole,bool):
		if filename.endswith('.py'):
			import os

			files,cmd=os.listdir(),''

			if noconsole==True:
				cmd+=f'cmd /k pyinstaller {filename} --onefile --noconsole'
			else:
				cmd+=f'cmd /k pyinstaller {filename} --onefile'

			if windowed==True:
				cmd+=f' --windowed'		

			if filename in files:
				os.system(cmd)	
	
			else:
				print(err)
	
		else:
			print(f'{err} File Must {facemoji} Be a Python File {err}')				
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str and bool and bool {err}')		

def Calendar(yr,month):
	if isinstance(yr,int) and isinstance(month,int):
		import calendar as C
		
		return C.month(yr,month)
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in int and int {err}')		

class AI:
	def GenerateImage(self,prompt:str,size:str='1024x1024') -> str:
		if isinstance(prompt,str):
			import openai

			openai.api_key = self.api

			response=openai.Image.create(model="image-alpha-001",prompt=prompt,n=1,size=size)

			return response['data'][0]['url']

		else:
			print(f'{err} Arguments Must {facemoji} Be in str and str {err}')	

	def ChatGPT(self,prompt:str,engine:str="text-davinci-003",max_tokens:int=1024,temperature:float=0.7) -> str:
		if isinstance(prompt,str) and isinstance(self.api,str):	
			import openai

			openai.api_key = self.api

			completions = openai.Completion.create(engine=engine,prompt=prompt,max_tokens=max_tokens,n=1,stop=None,temperature=temperature)

			return completions.choices[0].text.strip()
	
		else:
			print(f'{err} Arguments Must {facemoji} Be in str and str and str and int and float {err}')

def aboutbattery(string:str) -> str:
	if isinstance(string,str):
		if string=='percentage':
			import psutil

			battery = psutil.sensors_battery()

			percent = str(battery.percent)+'%'

			return percent

		elif string=='charging?':
			import psutil

			battery = psutil.sensors_battery()

			plugged = battery.power_plugged

			return plugged

		else:
			print(err)   
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')		   

def percent(string:str) -> float:
	if isinstance(string,str):
		percent,number='',''

		for i in string:
			if i=='%':
				break
			else:
				percent+=i	

		string=string[::-1]

		for i in string:
			if i==' ':
				break
			else:
				number+=i

		number=number[::-1]

		return (eval(number) * eval(percent))/100
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')	

def resizeimg(size:tuple,path:str):
	if isinstance(size,tuple) and isinstance(path,str):
		from PIL import Image

		img = Image.open(path)

		img_resized = img.resize(size)

		fname="Pydule Resize Image -" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".png"

		img_resized.save(fname)
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in tuple and str {err}')	

def GetWebHTML(url:str) -> str:
	if isinstance(url,str):
		import requests

		page = requests.get(url)

		return page.text
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')	

def screenshot(sec:int=0):
	if isinstance(sec,int) or isinstance(sec,float):
		import pyautogui
		import time as t
		import datetime

		t.sleep(sec)

		myScreenshot = pyautogui.screenshot()

		fname="Pydule Screen Shot -" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".png"

		myScreenshot.save(fname)
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in int {err}')	

def SpeechtoText(string:str=''):
	if isinstance(string,str):
		import speech_recognition as sr

		r = sr.Recognizer()

		mic = sr.Microphone()

		with mic as source:
			print(string,end='')
			audio = r.listen(source)

		try:
			return r.recognize_google(audio)
	
		except:
			print(err)
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')	    

def recintaudio(sec:int):
	if isinstance(sec,int):
		if sec>0:
			import soundcard as sc
			import soundfile as sf
			import datetime

			out = "Pydule Recorded Internel Audio -" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".wav"
			rate=48000

			with sc.get_microphone(id=str(sc.default_speaker().name),include_loopback=True).recorder(samplerate=rate) as mic:
				data=mic.record(numframes=rate*sec)
				sf.write(file=out,data=data[:,0],samplerate=rate)
	
		else:
			print(err)
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in int {err}')		

def recscreen():
	import pyautogui
	import cv2
	import numpy as np
	import datetime

	screen_size = pyautogui.size()

	filename = "Pydule Recorded Screen -" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".avi"

	fourcc = cv2.VideoWriter_fourcc(*"XVID")

	out = cv2.VideoWriter(filename, fourcc, 20.0, screen_size)

	cv2.namedWindow("Recording", cv2.WINDOW_NORMAL)

	cv2.resizeWindow("Recording", 480, 270)

	while True:
		img = pyautogui.screenshot()

		frame = np.array(img)

		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		out.write(frame)

		cv2.imshow('Live', frame)

		if cv2.waitKey(1) == ord('q'):
			break

	out.release()
	cv2.destroyAllWindows()

def DetectEmoji(st:str) -> dict:
	if isinstance(st,str):
		import demoji as d

		return d.findall(st)

	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')	

def Emoji(n:int or str) -> str:
	emoji={1: '😀', 2: '😁', 3: '😂', 4: '😃', 5: '😄', 6: '😅', 7: '😆', 8: '😇', 9: '😈', 10: '😉', 11: '😊', 12: '😋', 13: '😌', 14: '😍', 15: '😎', 16: '😏', 17: '😐', 18: '😑', 19: '😒', 20: '😓', 21: '😔',
	 22: '😕', 23: '😖', 24: '😗', 25: '😘', 26: '😙', 27: '😚', 28: '😛', 29: '😜', 30: '😝', 31: '😞', 32: '😟', 33: '😠', 34: '😡', 35: '😢', 36: '😣', 37: '😤', 38: '😥', 39: '😦', 40: '😧', 41: '😨', 42: '😩', 
	 43: '😪', 44: '😫', 45: '😬', 46: '😭', 47: '😮', 48: '😯', 49: '😰', 50: '😱', 51: '😲', 52: '😳', 53: '😴', 54: '😵', 55: '😶', 56: '😷', 57: '😸', 58: '😹', 59: '😺', 60: '😻', 61: '😼', 62: '😽', 63: '😾', 
	 64: '😿', 65: '🙀', 66: '🙁', 67: '🙂', 68: '🙃', 69: '🙄', 70: '🙅', 71: '🙆', 72: '🙇', 73: '🙈', 74: '🙉', 75: '🙊', 76: '🙋', 77: '🙌', 78: '🙍', 79: '🙎', 80: '🙏', 81: '🌀', 82: '🌁', 83: '🌂', 84: '🌃', 
	 85: '🌄', 86: '🌅', 87: '🌆', 88: '🌇', 89: '🌈', 90: '🌉', 91: '🌊', 92: '🌋', 93: '🌌', 94: '🌍', 95: '🌎', 96: '🌏', 97: '🌐', 98: '🌑', 99: '🌒', 100: '🌓', 101: '🌔', 102: '🌕', 103: '🌖', 104: '🌗', 105: 
	 '🌘', 106: '🌙', 107: '🌚', 108: '🌛', 109: '🌜', 110: '🌝', 111: '🌞', 112: '🌟', 113: '🌠', 114: '🌡', 115: '🌢', 116: '🌣', 117: '🌤', 118: '🌥', 119: '🌦', 120: '🌧', 121: '🌨', 122: '🌩', 123: '🌪', 124: 
	 '🌫', 125: '🌬', 126: '🌭', 127: '🌮', 128: '🌯', 129: '🌰', 130: '🌱', 131: '🌲', 132: '🌳', 133: '🌴', 134: '🌵', 135: '🌶', 136: '🌷', 137: '🌸', 138: '🌹', 139: '🌺', 140: '🌻', 141: '🌼', 142: '🌽', 143: 
	 '🌾', 144: '🌿', 145: '🍀', 146: '🍁', 147: '🍂', 148: '🍃', 149: '🍄', 150: '🍅', 151: '🍆', 152: '🍇', 153: '🍈', 154: '🍉', 155: '🍊', 156: '🍋', 157: '🍌', 158: '🍍', 159: '🍎', 160: '🍏', 161: '🍐', 162: 
	 '🍑', 163: '🍒', 164: '🍓', 165: '🍔', 166: '🍕', 167: '🍖', 168: '🍗', 169: '🍘', 170: '🍙', 171: '🍚', 172: '🍛', 173: '🍜', 174: '🍝', 175: '🍞', 176: '🍟', 177: '🍠', 178: '🍡', 179: '🍢', 180: '🍣', 181: 
	 '🍤', 182: '🍥', 183: '🍦', 184: '🍧', 185: '🍨', 186: '🍩', 187: '🍪', 188: '🍫', 189: '🍬', 190: '🍭', 191: '🍮', 192: '🍯', 193: '🍰', 194: '🍱', 195: '🍲', 196: '🍳', 197: '🍴', 198: '🍵', 199: '🍶', 200: 
	 '🍷', 201: '🍸', 202: '🍹', 203: '🍺', 204: '🍻', 205: '🍼', 206: '🍽', 207: '🍾', 208: '🍿', 209: '🎀', 210: '🎁', 211: '🎂', 212: '🎃', 213: '🎄', 214: '🎅', 215: '🎆', 216: '🎇', 217: '🎈', 218: '🎉', 219: 
	 '🎊', 220: '🎋', 221: '🎌', 222: '🎍', 223: '🎎', 224: '🎏', 225: '🎐', 226: '🎑', 227: '🎒', 228: '🎓', 229: '🎔', 230: '🎕', 231: '🎖', 232: '🎗', 233: '🎘', 234: '🎙', 235: '🎚', 236: '🎛', 237: '🎜', 238: 
	 '🎝', 239: '🎞', 240: '🎟', 241: '🎠', 242: '🎡', 243: '🎢', 244: '🎣', 245: '🎤', 246: '🎥', 247: '🎦', 248: '🎧', 249: '🎨', 250: '🎩', 251: '🎪', 252: '🎫', 253: '🎬', 254: '🎭', 255: '🎮', 256: '🎯', 257: 
	 '🎰', 258: '🎱', 259: '🎲', 260: '🎳', 261: '🎴', 262: '🎵', 263: '🎶', 264: '🎷', 265: '🎸', 266: '🎹', 267: '🎺', 268: '🎻', 269: '🎼', 270: '🎽', 271: '🎾', 272: '🎿', 273: '🏀', 274: '🏁', 275: '🏂', 276: 
	 '🏃', 277: '🏄', 278: '🏅', 279: '🏆', 280: '🏇', 281: '🏈', 282: '🏉', 283: '🏊', 284: '🏋', 285: '🏌', 286: '🏍', 287: '🏎', 288: '🏏', 289: '🏐', 290: '🏑', 291: '🏒', 292: '🏓', 293: '🏔', 294: '🏕', 295: 
	 '🏖', 296: '🏗', 297: '🏘', 298: '🏙', 299: '🏚', 300: '🏛', 301: '🏜', 302: '🏝', 303: '🏞', 304: '🏟', 305: '🏠', 306: '🏡', 307: '🏢', 308: '🏣', 309: '🏤', 310: '🏥', 311: '🏦', 312: '🏧', 313: '🏨', 314: 
	 '🏩', 315: '🏪', 316: '🏫', 317: '🏬', 318: '🏭', 319: '🏮', 320: '🏯', 321: '🏰', 322: '🏱', 323: '🏲', 324: '🏳', 325: '🏴', 326: '🏵', 327: '🏶', 328: '🏷', 329: '🏸', 330: '🏹', 331: '🏺', 332: '🏻', 333: 
	 '🏼', 334: '🏽', 335: '🏾', 336: '🏿', 337: '🐀', 338: '🐁', 339: '🐂', 340: '🐃', 341: '🐄', 342: '🐅', 343: '🐆', 344: '🐇', 345: '🐈', 346: '🐉', 347: '🐊', 348: '🐋', 349: '🐌', 350: '🐍', 351: '🐎', 352: 
	 '🐏', 353: '🐐', 354: '🐑', 355: '🐒', 356: '🐓', 357: '🐔', 358: '🐕', 359: '🐖', 360: '🐗', 361: '🐘', 362: '🐙', 363: '🐚', 364: '🐛', 365: '🐜', 366: '🐝', 367: '🐞', 368: '🐟', 369: '🐠', 370: '🐡', 371: 
	 '🐢', 372: '🐣', 373: '🐤', 374: '🐥', 375: '🐦', 376: '🐧', 377: '🐨', 378: '🐩', 379: '🐪', 380: '🐫', 381: '🐬', 382: '🐭', 383: '🐮', 384: '🐯', 385: '🐰', 386: '🐱', 387: '🐲', 388: '🐳', 389: '🐴', 390: 
	 '🐵', 391: '🐶', 392: '🐷', 393: '🐸', 394: '🐹', 395: '🐺', 396: '🐻', 397: '🐼', 398: '🐽', 399: '🐾', 400: '🐿', 401: '👀', 402: '👁', 403: '👂', 404: '👃', 405: '👄', 406: '👅', 407: '👆', 408: '👇', 409: 
	 '👈', 410: '👉', 411: '👊', 412: '👋', 413: '👌', 414: '👍', 415: '👎', 416: '👏', 417: '👐', 418: '👑', 419: '👒', 420: '👓', 421: '👔', 422: '👕', 423: '👖', 424: '👗', 425: '👘', 426: '👙', 427: '👚', 428: 
	 '👛', 429: '👜', 430: '👝', 431: '👞', 432: '👟', 433: '👠', 434: '👡', 435: '👢', 436: '👣', 437: '👤', 438: '👥', 439: '👦', 440: '👧', 441: '👨', 442: '👩', 443: '👪', 444: '👫', 445: '👬', 446: '👭', 447: 
	 '👮', 448: '👯', 449: '👰', 450: '👱', 451: '👲', 452: '👳', 453: '👴', 454: '👵', 455: '👶', 456: '👷', 457: '👸', 458: '👹', 459: '👺', 460: '👻', 461: '👼', 462: '👽', 463: '👾', 464: '👿', 465: '💀', 466: 
	 '💁', 467: '💂', 468: '💃', 469: '💄', 470: '💅', 471: '💆', 472: '💇', 473: '💈', 474: '💉', 475: '💊', 476: '💋', 477: '💌', 478: '💍', 479: '💎', 480: '💏', 481: '💐', 482: '💑', 483: '💒', 484: '💓', 485: 
	 '💔', 486: '💕', 487: '💖', 488: '💗', 489: '💘', 490: '💙', 491: '💚', 492: '💛', 493: '💜', 494: '💝', 495: '💞', 496: '💟', 497: '💠', 498: '💡', 499: '💢', 500: '💣', 501: '💤', 502: '💥', 503: '💦', 504: 
	 '💧', 505: '💨', 506: '💩', 507: '💪', 508: '💫', 509: '💬', 510: '💭', 511: '💮', 512: '💯', 513: '💰', 514: '💱', 515: '💲', 516: '💳', 517: '💴', 518: '💵', 519: '💶', 520: '💷', 521: '💸', 522: '💹', 523: 
	 '💺', 524: '💻', 525: '💼', 526: '💽', 527: '💾', 528: '💿', 529: '📀', 530: '📁', 531: '📂', 532: '📃', 533: '📄', 534: '📅', 535: '📆', 536: '📇', 537: '📈', 538: '📉', 539: '📊', 540: '📋', 541: '📌', 542: 
	 '📍', 543: '📎', 544: '📏', 545: '📐', 546: '📑', 547: '📒', 548: '📓', 549: '📔', 550: '📕', 551: '📖', 552: '📗', 553: '📘', 554: '📙', 555: '📚', 556: '📛', 557: '📜', 558: '📝', 559: '📞', 560: '📟', 561: 
	 '📠', 562: '📡', 563: '📢', 564: '📣', 565: '📤', 566: '📥', 567: '📦', 568: '📧', 569: '📨', 570: '📩', 571: '📪', 572: '📫', 573: '📬', 574: '📭', 575: '📮', 576: '📯', 577: '📰', 578: '📱', 579: '📲', 580: 
	 '📳', 581: '📴', 582: '📵', 583: '📶', 584: '📷', 585: '📸', 586: '📹', 587: '📺', 588: '📻', 589: '📼', 590: '📽', 591: '📾', 592: '📿', 593: '🔀', 594: '🔁', 595: '🔂', 596: '🔃', 597: '🔄', 598: '🔅', 599: 
	 '🔆', 600: '🔇', 601: '🔈', 602: '🔉', 603: '🔊', 604: '🔋', 605: '🔌', 606: '🔍', 607: '🔎', 608: '🔏', 609: '🔐', 610: '🔑', 611: '🔒', 612: '🔓', 613: '🔔', 614: '🔕', 615: '🔖', 616: '🔗', 617: '🔘', 618: 
	 '🔙', 619: '🔚', 620: '🔛', 621: '🔜', 622: '🔝', 623: '🔞', 624: '🔟', 625: '🔠', 626: '🔡', 627: '🔢', 628: '🔣', 629: '🔤', 630: '🔥', 631: '🔦', 632: '🔧', 633: '🔨', 634: '🔩', 635: '🔪', 636: '🔫', 637: 
	 '🔬', 638: '🔭', 639: '🔮', 640: '🔯', 641: '🔰', 642: '🔱', 643: '🔲', 644: '🔳', 645: '🔴', 646: '🔵', 647: '🔶', 648: '🔷', 649: '🔸', 650: '🔹', 651: '🔺', 652: '🔻', 653: '🔼', 654: '🔽', 655: '🔾', 656: 
	 '🔿', 657: '🕀', 658: '🕁', 659: '🕂', 660: '🕃', 661: '🕄', 662: '🕅', 663: '🕆', 664: '🕇', 665: '🕈', 666: '🕉', 667: '🕊', 668: '🕋', 669: '🕌', 670: '🕍', 671: '🕎', 672: '🕏', 673: '🕐', 674: '🕑', 675: 
	 '🕒', 676: '🕓', 677: '🕔', 678: '🕕', 679: '🕖', 680: '🕗', 681: '🕘', 682: '🕙', 683: '🕚', 684: '🕛', 685: '🕜', 686: '🕝', 687: '🕞', 688: '🕟', 689: '🕠', 690: '🕡', 691: '🕢', 692: '🕣', 693: '🕤', 694: 
	 '🕥', 695: '🕦', 696: '🕧', 697: '🕨', 698: '🕩', 699: '🕪', 700: '🕫', 701: '🕬', 702: '🕭', 703: '🕮', 704: '🕯', 705: '🕰', 706: '🕱', 707: '🕲', 708: '🕳', 709: '🕴', 710: '🕵', 711: '🕶', 712: '🕷', 713: 
	 '🕸', 714: '🕹', 715: '🕺', 716: '🕻', 717: '🕼', 718: '🕽', 719: '🕾', 720: '🕿', 721: '🖀', 722: '🖁', 723: '🖂', 724: '🖃', 725: '🖄', 726: '🖅', 727: '🖆', 728: '🖇', 729: '🖈', 730: '🖉', 731: '🖊', 732: 
	 '🖋', 733: '🖌', 734: '🖍', 735: '🖎', 736: '🖏', 737: '🖐', 738: '🖑', 739: '🖒', 740: '🖓', 741: '🖔', 742: '🖕', 743: '🖖', 744: '🖗', 745: '🖘', 746: '🖙', 747: '🖚', 748: '🖛', 749: '🖜', 750: '🖝', 751: 
	 '🖞', 752: '🖟', 753: '🖠', 754: '🖡', 755: '🖢', 756: '🖣', 757: '🖤', 758: '🖥', 759: '🖦', 760: '🖧', 761: '🖨', 762: '🖩', 763: '🖪', 764: '🖫', 765: '🖬', 766: '🖭', 767: '🖮', 768: '🖯', 769: '🖰', 770: 
	 '🖱', 771: '🖲', 772: '🖳', 773: '🖴', 774: '🖵', 775: '🖶', 776: '🖷', 777: '🖸', 778: '🖹', 779: '🖺', 780: '🖻', 781: '🖼', 782: '🖽', 783: '🖾', 784: '🖿', 785: '🗀', 786: '🗁', 787: '🗂', 788: '🗃', 789: 
	 '🗄', 790: '🗅', 791: '🗆', 792: '🗇', 793: '🗈', 794: '🗉', 795: '🗊', 796: '🗋', 797: '🗌', 798: '🗍', 799: '🗎', 800: '🗏', 801: '🗐', 802: '🗑', 803: '🗒', 804: '🗓', 805: '🗔', 806: '🗕', 807: '🗖', 808: 
	 '🗗', 809: '🗘', 810: '🗙', 811: '🗚', 812: '🗛', 813: '🗜', 814: '🗝', 815: '🗞', 816: '🗟', 817: '🗠', 818: '🗡', 819: '🗢', 820: '🗣', 821: '🗤', 822: '🗥', 823: '🗦', 824: '🗧', 825: '🗨', 826: '🗩', 827: 
	 '🗪', 828: '🗫', 829: '🗬', 830: '🗭', 831: '🗮', 832: '🗯', 833: '🗰', 834: '🗱', 835: '🗲', 836: '🗳', 837: '🗴', 838: '🗵', 839: '🗶', 840: '🗷', 841: '🗸', 842: '🗹', 843: '🗺', 844: '🗻', 845: '🗼', 846: 
	 '🗽', 847: '🗾', 848: '🗿', 849: '🚀', 850: '🚁', 851: '🚂', 852: '🚃', 853: '🚄', 854: '🚅', 855: '🚆', 856: '🚇', 857: '🚈', 858: '🚉', 859: '🚊', 860: '🚋', 861: '🚌', 862: '🚍', 863: '🚎', 864: '🚏', 865: 
	 '🚐', 866: '🚑', 867: '🚒', 868: '🚓', 869: '🚔', 870: '🚕', 871: '🚖', 872: '🚗', 873: '🚘', 874: '🚙', 875: '🚚', 876: '🚛', 877: '🚜', 878: '🚝', 879: '🚞', 880: '🚟', 881: '🚠', 882: '🚡', 883: '🚢', 884: 
	 '🚣', 885: '🚤', 886: '🚥', 887: '🚦', 888: '🚧', 889: '🚨', 890: '🚩', 891: '🚪', 892: '🚫', 893: '🚬', 894: '🚭', 895: '🚮', 896: '🚯', 897: '🚰', 898: '🚱', 899: '🚲', 900: '🚳', 901: '🚴', 902: '🚵', 903: 
	 '🚶', 904: '🚷', 905: '🚸', 906: '🚹', 907: '🚺', 908: '🚻', 909: '🚼', 910: '🚽', 911: '🚾', 912: '🚿', 913: '🛀', 914: '🛁', 915: '🛂', 916: '🛃', 917: '🛄', 918: '🛅', 919: '🛆', 920: '🛇', 921: '🛈', 922: 
	 '🛉', 923: '🛊', 924: '🛋', 925: '🛌', 926: '🛍', 927: '🛎', 928: '🛏', 929: '🛐', 930: '🛑', 931: '🛒', 932: '🛓', 933: '🛔', 934: '🛕', 935: '🛖', 936: '🛗', 937: '\U0001f6d8', 938: '\U0001f6d9', 939: 
	 '\U0001f6da', 940: '\U0001f6db', 941: '\U0001f6dc', 942: '🛝', 943: '🛞', 944: '🛟', 945: '🛠', 946: '🛡', 947: '🛢', 948: '🛣', 949: '🛤', 950: '🛥', 951: '🛦', 952: '🛧', 953: '🛨', 954: '🛩', 955: '🛪', 
	 956: '🛫', 957: '🛬', 958: '\U0001f6ed', 959: '\U0001f6ee', 960: '\U0001f6ef', 961: '🛰', 962: '🛱', 963: '🛲', 964: '🛳', 965: '🛴', 966: '🛵', 967: '🛶', 968: '🛷', 969: '🛸', 970: '🛹', 971: '🛺', 972: 
	 '🛻', 973: '🛼', 974: '\U0001f6fd', 975: '\U0001f6fe', 976: '\U0001f6ff', 977: '☀', 978: '☁', 979: '☂', 980: '☃', 981: '☄', 982: '★', 983: '☆', 984: '☇', 985: '☈', 986: '☉', 987: '☊', 988: '☋', 989: '☌', 990: 
	 '☍', 991: '☎', 992: '☏', 993: '☐', 994: '☑', 995: '☒', 996: '☓', 997: '☔', 998: '☕', 999: '☖', 1000: '☗', 1001: '☘', 1002: '☙', 1003: '☚', 1004: '☛', 1005: '☜', 1006: '☝', 1007: '☞', 1008: '☟', 1009: '☠', 
	 1010: '☡', 1011: '☢', 1012: '☣', 1013: '☤', 1014: '☥', 1015: '☦', 1016: '☧', 1017: '☨', 1018: '☩', 1019: '☪', 1020: '☫', 1021: '☬', 1022: '☭', 1023: '☮', 1024: '☯', 1025: '☰', 1026: '☱', 1027: '☲', 1028: '☳', 
	 1029: '☴', 1030: '☵', 1031: '☶', 1032: '☷', 1033: '☸', 1034: '☹', 1035: '☺', 1036: '☻', 1037: '☼', 1038: '☽', 1039: '☾', 1040: '☿', 1041: '♀', 1042: '♁', 1043: '♂', 1044: '♃', 1045: '♄', 1046: '♅', 1047: '♆', 
	 1048: '♇', 1049: '♈', 1050: '♉', 1051: '♊', 1052: '♋', 1053: '♌', 1054: '♍', 1055: '♎', 1056: '♏', 1057: '♐', 1058: '♑', 1059: '♒', 1060: '♓', 1061: '♔', 1062: '♕', 1063: '♖', 1064: '♗', 1065: '♘', 1066: '♙', 
	 1067: '♚', 1068: '♛', 1069: '♜', 1070: '♝', 1071: '♞', 1072: '♟', 1073: '♠', 1074: '♡', 1075: '♢', 1076: '♣', 1077: '♤', 1078: '♥', 1079: '♦', 1080: '♧', 1081: '♨', 1082: '♩', 1083: '♪', 1084: '♫', 1085: '♬', 
	 1086: '♭', 1087: '♮', 1088: '♯', 1089: '♰', 1090: '♱', 1091: '♲', 1092: '♳', 1093: '♴', 1094: '♵', 1095: '♶', 1096: '♷', 1097: '♸', 1098: '♹', 1099: '♺', 1100: '♻', 1101: '♼', 1102: '♽', 1103: '♾', 1104: '♿', 
	 1105: '⚀', 1106: '⚁', 1107: '⚂', 1108: '⚃', 1109: '⚄', 1110: '⚅', 1111: '⚆', 1112: '⚇', 1113: '⚈', 1114: '⚉', 1115: '⚊', 1116: '⚋', 1117: '⚌', 1118: '⚍', 1119: '⚎', 1120: '⚏', 1121: '⚐', 1122: '⚑', 1123: '⚒', 
	 1124: '⚓', 1125: '⚔', 1126: '⚕', 1127: '⚖', 1128: '⚗', 1129: '⚘', 1130: '⚙', 1131: '⚚', 1132: '⚛', 1133: '⚜', 1134: '⚝', 1135: '⚞', 1136: '⚟', 1137: '⚠', 1138: '⚡', 1139: '⚢', 1140: '⚣', 1141: '⚤', 1142: '⚥', 
	 1143: '⚦', 1144: '⚧', 1145: '⚨', 1146: '⚩', 1147: '⚪', 1148: '⚫', 1149: '⚬', 1150: '⚭', 1151: '⚮', 1152: '⚯', 1153: '⚰', 1154: '⚱', 1155: '⚲', 1156: '⚳', 1157: '⚴', 1158: '⚵', 1159: '⚶', 1160: '⚷', 1161: '⚸', 
	 1162: '⚹', 1163: '⚺', 1164: '⚻', 1165: '⚼', 1166: '⚽', 1167: '⚾', 1168: '⚿', 1169: '⛀', 1170: '⛁', 1171: '⛂', 1172: '⛃', 1173: '⛄', 1174: '⛅', 1175: '⛆', 1176: '⛇', 1177: '⛈', 1178: '⛉', 1179: '⛊', 1180: '⛋', 
	 1181: '⛌', 1182: '⛍', 1183: '⛎', 1184: '⛏', 1185: '⛐', 1186: '⛑', 1187: '⛒', 1188: '⛓', 1189: '⛔', 1190: '⛕', 1191: '⛖', 1192: '⛗', 1193: '⛘', 1194: '⛙', 1195: '⛚', 1196: '⛛', 1197: '⛜', 1198: '⛝', 1199: '⛞', 
	 1200: '⛟', 1201: '⛠', 1202: '⛡', 1203: '⛢', 1204: '⛣', 1205: '⛤', 1206: '⛥', 1207: '⛦', 1208: '⛧', 1209: '⛨', 1210: '⛩', 1211: '⛪', 1212: '⛫', 1213: '⛬', 1214: '⛭', 1215: '⛮', 1216: '⛯', 1217: '⛰', 1218: '⛱', 
	 1219: '⛲', 1220: '⛳', 1221: '⛴', 1222: '⛵', 1223: '⛶', 1224: '⛷', 1225: '⛸', 1226: '⛹', 1227: '⛺', 1228: '⛻', 1229: '⛼', 1230: '⛽', 1231: '⛾', 1232: '⛿', 1233: '✀', 1234: '✁', 1235: '✂', 1236: '✃', 1237: '✄', 
	 1238: '✅', 1239: '✆', 1240: '✇', 1241: '✈', 1242: '✉', 1243: '✊', 1244: '✋', 1245: '✌', 1246: '✍', 1247: '✎', 1248: '✏', 1249: '✐', 1250: '✑', 1251: '✒', 1252: '✓', 1253: '✔', 1254: '✕', 1255: '✖', 1256: '✗', 
	 1257: '✘', 1258: '✙', 1259: '✚', 1260: '✛', 1261: '✜', 1262: '✝', 1263: '✞', 1264: '✟', 1265: '✠', 1266: '✡', 1267: '✢', 1268: '✣', 1269: '✤', 1270: '✥', 1271: '✦', 1272: '✧', 1273: '✨', 1274: '✩', 1275: '✪', 
	 1276: '✫', 1277: '✬', 1278: '✭', 1279: '✮', 1280: '✯', 1281: '✰', 1282: '✱', 1283: '✲', 1284: '✳', 1285: '✴', 1286: '✵', 1287: '✶', 1288: '✷', 1289: '✸', 1290: '✹', 1291: '✺', 1292: '✻', 1293: '✼', 1294: '✽', 
	 1295: '✾', 1296: '✿', 1297: '❀', 1298: '❁', 1299: '❂', 1300: '❃', 1301: '❄', 1302: '❅', 1303: '❆', 1304: '❇', 1305: '❈', 1306: '❉', 1307: '❊', 1308: '❋', 1309: '❌', 1310: '❍', 1311: '❎', 1312: '❏', 1313: '❐', 
	 1314: '❑', 1315: '❒', 1316: '❓', 1317: '❔', 1318: '❕', 1319: '❖', 1320: '❗', 1321: '❘', 1322: '❙', 1323: '❚', 1324: '❛', 1325: '❜', 1326: '❝', 1327: '❞', 1328: '❟', 1329: '❠', 1330: '❡', 1331: '❢', 1332: '❣', 
	 1333: '❤', 1334: '❥', 1335: '❦', 1336: '❧', 1337: '❨', 1338: '❩', 1339: '❪', 1340: '❫', 1341: '❬', 1342: '❭', 1343: '❮', 1344: '❯', 1345: '❰', 1346: '❱', 1347: '❲', 1348: '❳', 1349: '❴', 1350: '❵', 1351: '❶', 
	 1352: '❷', 1353: '❸', 1354: '❹', 1355: '❺', 1356: '❻', 1357: '❼', 1358: '❽', 1359: '❾', 1360: '❿', 1361: '➀', 1362: '➁', 1363: '➂', 1364: '➃', 1365: '➄', 1366: '➅', 1367: '➆', 1368: '➇', 1369: '➈', 1370: '➉', 
	 1371: '➊', 1372: '➋', 1373: '➌', 1374: '➍', 1375: '➎', 1376: '➏', 1377: '➐', 1378: '➑', 1379: '➒', 1380: '➓', 1381: '➔', 1382: '➕', 1383: '➖', 1384: '➗', 1385: '➘', 1386: '➙', 1387: '➚', 1388: '➛', 1389: '➜', 
	 1390: '➝', 1391: '➞', 1392: '➟', 1393: '➠', 1394: '➡', 1395: '➢', 1396: '➣', 1397: '➤', 1398: '➥', 1399: '➦', 1400: '➧', 1401: '➨', 1402: '➩', 1403: '➪', 1404: '➫', 1405: '➬', 1406: '➭', 1407: '➮', 1408: '➯', 
	 1409: '➰', 1410: '➱', 1411: '➲', 1412: '➳', 1413: '➴', 1414: '➵', 1415: '➶', 1416: '➷', 1417: '➸', 1418: '➹', 1419: '➺', 1420: '➻', 1421: '➼', 1422: '➽', 1423: '➾', 1424: '➿', 1425: '🤀', 1426: '🤁', 1427: 
	 '🤂', 1428: '🤃', 1429: '🤄', 1430: '🤅', 1431: '🤆', 1432: '🤇', 1433: '🤈', 1434: '🤉', 1435: '🤊', 1436: '🤋', 1437: '🤌', 1438: '🤍', 1439: '🤎', 1440: '🤏', 1441: '🤐', 1442: '🤑', 1443: '🤒', 1444: '🤓', 
	 1445: '🤔', 1446: '🤕', 1447: '🤖', 1448: '🤗', 1449: '🤘', 1450: '🤙', 1451: '🤚', 1452: '🤛', 1453: '🤜', 1454: '🤝', 1455: '🤞', 1456: '🤟', 1457: '🤠', 1458: '🤡', 1459: '🤢', 1460: '🤣', 1461: '🤤', 1462: 
	 '🤥', 1463: '🤦', 1464: '🤧', 1465: '🤨', 1466: '🤩', 1467: '🤪', 1468: '🤫', 1469: '🤬', 1470: '🤭', 1471: '🤮', 1472: '🤯', 1473: '🤰', 1474: '🤱', 1475: '🤲', 1476: '🤳', 1477: '🤴', 1478: '🤵', 1479: '🤶', 
	 1480: '🤷', 1481: '🤸', 1482: '🤹', 1483: '🤺', 1484: '🤻', 1485: '🤼', 1486: '🤽', 1487: '🤾', 1488: '🤿', 1489: '🥀', 1490: '🥁', 1491: '🥂', 1492: '🥃', 1493: '🥄', 1494: '🥅', 1495: '🥆', 1496: '🥇', 1497: 
	 '🥈', 1498: '🥉', 1499: '🥊', 1500: '🥋', 1501: '🥌', 1502: '🥍', 1503: '🥎', 1504: '🥏', 1505: '🥐', 1506: '🥑', 1507: '🥒', 1508: '🥓', 1509: '🥔', 1510: '🥕', 1511: '🥖', 1512: '🥗', 1513: '🥘', 1514: '🥙', 
	 1515: '🥚', 1516: '🥛', 1517: '🥜', 1518: '🥝', 1519: '🥞', 1520: '🥟', 1521: '🥠', 1522: '🥡', 1523: '🥢', 1524: '🥣', 1525: '🥤', 1526: '🥥', 1527: '🥦', 1528: '🥧', 1529: '🥨', 1530: '🥩', 1531: '🥪', 1532: 
	 '🥫', 1533: '🥬', 1534: '🥭', 1535: '🥮', 1536: '🥯', 1537: '🥰', 1538: '🥱', 1539: '🥲', 1540: '🥳', 1541: '🥴', 1542: '🥵', 1543: '🥶', 1544: '🥷', 1545: '🥸', 1546: '🥹', 1547: '🥺', 1548: '🥻', 1549: '🥼', 
	 1550: '🥽', 1551: '🥾', 1552: '🥿', 1553: '🦀', 1554: '🦁', 1555: '🦂', 1556: '🦃', 1557: '🦄', 1558: '🦅', 1559: '🦆', 1560: '🦇', 1561: '🦈', 1562: '🦉', 1563: '🦊', 1564: '🦋', 1565: '🦌', 1566: '🦍', 1567: 
	 '🦎', 1568: '🦏', 1569: '🦐', 1570: '🦑', 1571: '🦒', 1572: '🦓', 1573: '🦔', 1574: '🦕', 1575: '🦖', 1576: '🦗', 1577: '🦘', 1578: '🦙', 1579: '🦚', 1580: '🦛', 1581: '🦜', 1582: '🦝', 1583: '🦞', 1584: '🦟', 
	 1585: '🦠', 1586: '🦡', 1587: '🦢', 1588: '🦣', 1589: '🦤', 1590: '🦥', 1591: '🦦', 1592: '🦧', 1593: '🦨', 1594: '🦩', 1595: '🦪', 1596: '🦫', 1597: '🦬', 1598: '🦭', 1599: '🦮', 1600: '🦯', 1601: '🦰', 1602: 
	 '🦱', 1603: '🦲', 1604: '🦳', 1605: '🦴', 1606: '🦵', 1607: '🦶', 1608: '🦷', 1609: '🦸', 1610: '🦹', 1611: '🦺', 1612: '🦻', 1613: '🦼', 1614: '🦽', 1615: '🦾', 1616: '🦿', 1617: '🧀', 1618: '🧁', 1619: '🧂', 
	 1620: '🧃', 1621: '🧄', 1622: '🧅', 1623: '🧆', 1624: '🧇', 1625: '🧈', 1626: '🧉', 1627: '🧊', 1628: '🧋', 1629: '🧌', 1630: '🧍', 1631: '🧎', 1632: '🧏', 1633: '🧐', 1634: '🧑', 1635: '🧒', 1636: '🧓', 1637: 
	 '🧔', 1638: '🧕', 1639: '🧖', 1640: '🧗', 1641: '🧘', 1642: '🧙', 1643: '🧚', 1644: '🧛', 1645: '🧜', 1646: '🧝', 1647: '🧞', 1648: '🧟', 1649: '🧠', 1650: '🧡', 1651: '🧢', 1652: '🧣', 1653: '🧤', 1654: '🧥', 
	 1655: '🧦', 1656: '🧧', 1657: '🧨', 1658: '🧩', 1659: '🧪', 1660: '🧫', 1661: '🧬', 1662: '🧭', 1663: '🧮', 1664: '🧯', 1665: '🧰', 1666: '🧱', 1667: '🧲', 1668: '🧳', 1669: '🧴', 1670: '🧵', 1671: '🧶', 1672: 
	 '🧷', 1673: '🧸', 1674: '🧹', 1675: '🧺', 1676: '🧻', 1677: '🧼', 1678: '🧽', 1679: '🧾', 1680: '🧿', 1681: '🇦', 1682: '🇧', 1683: '🇨', 1684: '🇩', 1685: '🇪', 1686: '🇫', 1687: '🇬', 1688: '🇭', 1689: '🇮', 
	 1690: '🇯', 1691: '🇰', 1692: '🇱', 1693: '🇲', 1694: '🇳', 1695: '🇴', 1696: '🇵', 1697: '🇶', 1698: '🇷', 1699: '🇸', 1700: '🇹', 1701: '🇺', 1702: '🇻', 1703: '🇼', 1704: '🇽', 1705: '🇾', 1706: '🇿'}
	
	emoji2={'bullseye': '🎯', 'skis': '🎿', 'cat with wry smile': '😼', 'rice cracker': '🍘', 'tangerine': '🍊', 'zebra': '🦓', 'alien': '👽', 'ledger': '📒', 'owl': '🦉', 'hiking boot': '🥾', 'leaf fluttering in wind': '🍃',
	'foggy': '🌁', 'woman and man holding hands': '👫', 'briefcase': '💼', 'family': '👪', 'pie': '🥧', 'yen banknote': '💴', 'check mark button': '✅', 'grinning cat with smiling eyes': '😸', 'star and crescent': '☪',
	'goal net': '🥅', 'flexed biceps': '💪', 'flat shoe': '🥿', 'ferry': '⛴', 'diamond suit': '♦', 'tanabata tree': '🎋', 'no littering': '🚯', 'panda': '🐼', 'muted speaker': '🔇', 'yellow heart': '💛', 'moon cake': '🥮',
	'dollar banknote': '💵', 'hundred points': '💯', 'onion': '🧅', 'repeat button': '🔁', 'performing arts': '🎭', 'motor boat': '🛥', 'racing car': '🏎', 'Statue of Liberty': '🗽', 'bell with slash': '🔕',
	'lying face': '🤥', 'four-thirty': '🕟', 'computer disk': '💽', 'hut': '🛖', 'stadium': '🏟', 'rolled-up newspaper': '🗞', 'musical notes': '🎶', 'skateboard': '🛹', 'pound banknote': '💷',
	'globe with meridians': '🌐', 'man’s shoe': '👞', 'atom symbol': '⚛', 'thumbs up': '👍', 'dvd': '📀', 'thermometer': '🌡', 'studio microphone': '🎙', 'flushed face': '😳', 'circus tent': '🎪',
	'Cancer': '♋', 'admission tickets': '🎟', 'envelope': '✉', 'motor scooter': '🛵', 'eight-spoked asterisk': '✳', 'Aquarius': '♒', 'red hair': '🦰', 'person playing water polo': '🤽',
	'electric plug': '🔌', 'railway car': '🚃', 'angry face with horns': '👿', 'cherry blossom': '🌸', 'moon viewing ceremony': '🎑', 'horse face': '🐴', 'printer': '🖨', 'Libra': '♎', 'pile of poo': '💩',
	'locked with pen': '🔏', 'construction': '🚧', 'person raising hand': '🙋', 'camera': '📷', 'pick': '⛏', 'microbe': '🦠', 'face with steam from nose': '😤', 'oncoming automobile': '🚘',
	 'transgender symbol': '⚧', 'palms up together': '🤲', 'sleepy face': '😪', 'palm tree': '🌴', 'ice cream': '🍨', 'goat': '🐐', 'heart decoration': '💟', 'alembic': '⚗', 'hospital': '🏥',
	'flying saucer': '🛸', 'dango': '🍡', 'tropical fish': '🐠', 'mechanical arm': '🦾', 'convenience store': '🏪', 'lion': '🦁', 'nine o’clock': '🕘', 'hotel': '🏨', 'person walking': '🚶',
	'woman’s clothes': '👚', 'desert': '🏜', 'loudly crying face': '😭', 'eyes': '👀', 'e-mail': '📧', 'person taking bath': '🛀', 'red paper lantern': '🏮', '1st place medal': '🥇', 'cross mark': '❌',
	'elevator': '🛗', 'shopping bags': '🛍', 'T-Rex': '🦖', '2nd place medal': '🥈', 'man dancing': '🕺', 'smiling face with sunglasses': '😎', 'ant': '🐜', 'confetti ball': '🎊', 'bank': '🏦',
	'blowfish': '🐡', 'one-thirty': '🕜', '3rd place medal': '🥉', 'first quarter moon face': '🌛', 'baby angel': '👼', 'unicorn': '🦄', 'leafy green': '🥬', 'running shoe': '👟',
	'place of worship': '🛐', 'sandwich': '🥪', 'avocado': '🥑', 'green heart': '💚', 'wheel of dharma': '☸', 'scissors': '✂', 'full moon': '🌕', 'umbrella on ground': '⛱', 'trophy': '🏆',
	'glasses': '👓', 'ogre': '👹', 'national park': '🏞', 'smiling face with heart-eyes': '😍', 'kissing face': '😗', 'sunrise over mountains': '🌄', 'books': '📚', 'person in suit levitating': '🕴',
	'face with open mouth': '😮', 'grinning cat': '😺', 'heavy dollar sign': '💲', 'bagel': '🥯', 'zombie': '🧟', 'broom': '🧹', 'expressionless face': '😑', 'sleeping face': '😴',
	'person with veil': '👰', 'grinning face with sweat': '😅', 'umbrella with rain drops': '☔', 'rescue worker’s helmet': '⛑', 'input latin lowercase': '🔡', 'lipstick': '💄',
	'right arrow': '➡', 'loudspeaker': '📢', 'megaphone': '📣', 'SOON arrow': '🔜', 'Pisces': '♓', 'spade suit': '♠', 'six-thirty': '🕡', 'manual wheelchair': '🦽', 'elf': '🧝',
	'radioactive': '☢', 'Ophiuchus': '⛎', 'genie': '🧞', 'chess pawn': '♟', 'scorpion': '🦂', 'ping pong': '🏓', 'light bulb': '💡', 'magnifying glass tilted left': '🔍', 'trolleybus': '🚎',
	'peace symbol': '☮', 'kimono': '👘', 'yawning face': '🥱', 'triangular ruler': '📐', 'guitar': '🎸', 'compass': '🧭', 'syringe': '💉', 'toolbox': '🧰', 'snowboarder': '🏂', 'sun behind large cloud': '🌥',
	'scarf': '🧣', 'double curly loop': '➿', 'pouting cat': '😾', 'ghost': '👻', 'moai': '🗿', 'glass of milk': '🥛', 'evergreen tree': '🌲', 'person cartwheeling': '🤸', 'beating heart': '💓',
	'five o’clock': '🕔', 'lizard': '🦎', 'basket': '🧺', 'black square button': '🔲', 'passenger ship': '🛳', 'two-hump camel': '🐫', 'glowing star': '🌟', 'money bag': '💰', 't-shirt': '👕',
	'growing heart': '💗', 'monkey': '🐒', 'BACK arrow': '🔙', 'railway track': '🛤', 'shooting star': '🌠', 'balloon': '🎈', 'baseball': '⚾', 'grinning face with smiling eyes': '😄', 'face vomiting': '🤮',
	'pot of food': '🍲', 'blue heart': '💙', 'mango': '🥭', 'raised hand': '✋', 'potato': '🥔', 'slightly frowning face': '🙁', 'musical score': '🎼', 'speak-no-evil monkey': '🙊', 'lollipop': '🍭',
	'orangutan': '🦧', 'diamond with a dot': '💠', 'notebook with decorative cover': '📔', 'thread': '🧵', 'necktie': '👔', 'fire engine': '🚒', 'saxophone': '🎷', 'open mailbox with lowered flag': '📭',
	'oyster': '🦪', 'supervillain': '🦹', 'badger': '🦡', 'princess': '👸', 'penguin': '🐧', 'face blowing a kiss': '😘', 'bird': '🐦', 'person standing': '🧍', 'outbox tray': '📤', 'eggplant': '🍆',
	'crossed swords': '⚔', 'neutral face': '😐', 'waxing gibbous moon': '🌔', 'robot': '🤖', 'cat with tears of joy': '😹', 'coconut': '🥥', 'poodle': '🐩', 'flag: Ghana': '🇬🇭', 'gem stone': '💎',
	'microscope': '🔬', 'sparkle': '❇', 'pretzel': '🥨', 'deaf person': '🧏', 'green book': '📗', 'breast-feeding': '🤱', 'aerial tramway': '🚡', 'notebook': '📓', 'triangular flag': '🚩', 'fox': '🦊',
	'horse': '🐎', 'suspension railway': '🚟', 'petri dish': '🧫', 'person frowning': '🙍', 'people wrestling': '🤼', 'beaming face with smiling eyes': '😁', 'bust in silhouette': '👤', 'snail': '🐌',
	'smiling face with horns': '😈', 'canned food': '🥫', 'black heart': '🖤', 'lotion bottle': '🧴', 'fortune cookie': '🥠', 'bone': '🦴', 'cold face': '🥶', 'person getting haircut': '💇',
	'tired face': '😫', 'steaming bowl': '🍜', 'sunrise': '🌅', 'sushi': '🍣', 'globe showing Asia-Australia': '🌏', 'tornado': '🌪', 'Japanese post office': '🏣', 'wind chime': '🎐', 'old woman': '👵',
	'kitchen knife': '🔪', 'fountain pen': '🖋', 'peach': '🍑', 'carp streamer': '🎏', 'wolf': '🐺', 'camera with flash': '📸', 'merperson': '🧜', 'radio': '📻', 'link': '🔗', 'cucumber': '🥒',
	'mount fuji': '🗻', 'teacup without handle': '🍵', 'crocodile': '🐊', 'turtle': '🐢', 'soap': '🧼', 'chicken': '🐔', 'mage': '🧙', 'litter in bin sign': '🚮', 'biohazard': '☣', 'sponge': '🧽',
	'house with garden': '🏡', 'clapping hands': '👏', 'euro banknote': '💶', 'pear': '🍐', 'downcast face with sweat': '😓', 'fog': '🌫', 'card file box': '🗃', 'clinking glasses': '🥂', 
	'Mrs. Claus': '🤶', 'yarn': '🧶', 'heart with ribbon': '💝', 'latin cross': '✝', 'people with bunny ears': '👯', 'giraffe': '🦒', 'bowling': '🎳', 'face with rolling eyes': '🙄',
	'cricket game': '🏏', 'partying face': '🥳', 'customs': '🛃', 'light rail': '🚈', 'field hockey': '🏑', 'snowman': '☃', 'flying disc': '🥏', 'tractor': '🚜', 'mushroom': '🍄', 
	'clinking beer mugs': '🍻', 'mouse face': '🐭', 'skull and crossbones': '☠', 'waffle': '🧇', 'mate': '🧉', 'three o’clock': '🕒', 'bus': '🚌', 'prince': '🤴', 'chopsticks': '🥢',
	'flag: Congo - Kinshasa': '🇨🇩', 'Santa Claus': '🎅', 'black nib': '✒', 'anger symbol': '💢', 'leg': '🦵', 'incoming envelope': '📨', 'handshake': '🤝', 'reminder ribbon': '🎗', 'socks': '🧦', 
	'frowning face with open mouth': '😦', 'new moon face': '🌚', 'bikini': '👙', 'tumbler glass': '🥃', 'flamingo': '🦩', 'guide dog': '🦮', 'speaking head': '🗣', 'cat face': '🐱', 'motorcycle': '🏍',
	'closed mailbox with raised flag': '📫', 'wrench': '🔧', 'winking face': '😉', 'orange heart': '🧡', 'large blue diamond': '🔷', 'high-speed train': '🚄', 'clipboard': '📋', 'Taurus': '♉',
	'three-thirty': '🕞', 'artist palette': '🎨', 'mouth': '👄', 'red apple': '🍎', 'zzz': '💤', 'lobster': '🦞', 'mobile phone with arrow': '📲', 'cup with straw': '🥤', 'sign of the horns': '🤘',
	'shinto shrine': '⛩', 'nose': '👃', 'mechanical leg': '🦿', 'weary face': '😩', 'egg': '🥚', 'backhand index pointing down': '👇', 'burrito': '🌯', 'rice ball': '🍙', 'waning gibbous moon': '🌖',
	'sun behind small cloud': '🌤', 'paw prints': '🐾', 'film frames': '🎞', 'crayon': '🖍', 'om': '🕉', 'Scorpio': '♏', 'skunk': '🦨', 'night with stars': '🌃', 'rose': '🌹', 'red triangle pointed down': '🔻',
	'END arrow': '🔚', 'Virgo': '♍', 'medium skin tone': '🏽', 'bear': '🐻', 'hot dog': '🌭', 'seven-thirty': '🕢', 'chart increasing': '📈', 'world map': '🗺', 'cactus': '🌵', 'crossed fingers': '🤞',
	'spaghetti': '🍝', 'dolphin': '🐬', 'building construction': '🏗', 'purse': '👛', 'turkey': '🦃', 'couple with heart': '💑', 'pushpin': '📌', 'toilet': '🚽', 'flashlight': '🔦', 'nazar amulet': '🧿',
	'raised back of hand': '🤚', 'downwards button': '🔽', 'one o’clock': '🕐', 'women’s room': '🚺', 'comet': '☄', 'blue book': '📘', 'thumbs down': '👎', 'balance scale': '⚖', 'sneezing face': '🤧', 
	'relieved face': '😌', 'bread': '🍞', 'ATM sign': '🏧', 'ear': '👂', 'no mobile phones': '📵', 'school': '🏫', 'mantelpiece clock': '🕰', 'croissant': '🥐', 'open book': '📖', 'angry face': '😠', 
	'fallen leaf': '🍂', 'herb': '🌿', 'revolving hearts': '💞', 'headphone': '🎧', 'left-facing fist': '🤛', 'Gemini': '♊', 'sad but relieved face': '😥', 'ferris wheel': '🎡', 'wedding': '💒', 
	'koala': '🐨', 'funeral urn': '⚱', 'input numbers': '🔢', 'magnet': '🧲', 'minus': '➖', 'anchor': '⚓', 'level slider': '🎚', 'footprints': '👣', 'sloth': '🦥', 'shrimp': '🦐', 'desktop computer': '🖥',
	'busts in silhouette': '👥', 'right-facing fist': '🤜', 'repeat single button': '🔂', 'joystick': '🕹', 'green salad': '🥗', 'chart increasing with yen': '💹', 'hamster': '🐹', 'roll of paper': '🧻', 
	'person facepalming': '🤦', 'lacrosse': '🥍', 'middle finger': '🖕', 'kissing cat': '😽', 'laptop': '💻', 'face with monocle': '🧐', 'beach with umbrella': '🏖', 'curling stone': '🥌', 
	'pregnant woman': '🤰', 'deer': '🦌', 'cut of meat': '🥩', 'divide': '➗', 'hindu temple': '🛕', 'roasted sweet potato': '🍠', 'water buffalo': '🐃', 'snowman without snow': '⛄', 'hammer and pick': '⚒',
	'face with tongue': '😛', 'passport control': '🛂', 'dodo': '🦤', 'video camera': '📹', 'waxing crescent moon': '🌒', 'input latin uppercase': '🔠', 'water wave': '🌊', 'floppy disk': '💾', 
	'candy': '🍬', 'slot machine': '🎰', 'maple leaf': '🍁', 'unlocked': '🔓', 'face with head-bandage': '🤕', 'synagogue': '🕍', 'Aries': '♈', 'cricket': '🦗', 'hippopotamus': '🦛', 'person': '🧑', 
	'speaker low volume': '🔈', 'frog': '🐸', 'bright button': '🔆', 'person kneeling': '🧎', 'crab': '🦀', 'water pistol': '🔫', 'person biking': '🚴', 'classical building': '🏛', 'seal': '🦭', 
	'party popper': '🎉', 'face screaming in fear': '😱', 'winking face with tongue': '😜', 'person mountain biking': '🚵', 'white flag': '🏳', 'small orange diamond': '🔸', 'volleyball': '🏐', 
	'two o’clock': '🕑', 'shark': '🦈', 'chequered flag': '🏁', 'page facing up': '📄', 'index pointing up': '☝', 'male sign': '♂', 'eight-pointed star': '✴', 'men’s room': '🚹', 'orange book': '📙', 
	'Japanese castle': '🏯', 'ticket': '🎫', 'bus stop': '🚏', 'diving mask': '🤿', 'unamused face': '😒', 'wheelchair symbol': '♿', 'brown heart': '🤎', 'thinking face': '🤔', 'birthday cake': '🎂', 
	'bacon': '🥓', 'hibiscus': '🌺', 'badminton': '🏸', 'umbrella': '☂', 'woman’s boot': '👢', 'bubble tea': '🧋', 'no one under eighteen': '🔞', 'confounded face': '😖', 'squinting face with tongue': '😝',
	'fire': '🔥', 'heart with arrow': '💘', 'seat': '💺', 'videocassette': '📼', 'twelve o’clock': '🕛', 'flag: Serbia': '🇷🇸', 'hole': '🕳', 'old key': '🗝', 'drum': '🥁', 'clamp': '🗜', 'backpack': '🎒',
	'peanuts': '🥜', 'cupcake': '🧁', 'hamburger': '🍔', 'bomb': '💣', 'pineapple': '🍍', 'linked paperclips': '🖇', 'metro': '🚇', 'selfie': '🤳', 'handbag': '👜', 'fishing pole': '🎣', 'grapes': '🍇', 
	'barber pole': '💈', 'poultry leg': '🍗', 'rat': '🐀', 'crystal ball': '🔮', 'file cabinet': '🗄', 'no entry': '⛔', 'tear-off calendar': '📆', 'gloves': '🧤', 'hot pepper': '🌶', 
	'Japanese symbol for beginner': '🔰', 'red circle': '🔴', 'sports medal': '🏅', 'cloud with lightning and rain': '⛈', 'smiling face with smiling eyes': '😊', 'infinity': '♾', 'abacus': '🧮',
	'small blue diamond': '🔹', 'bald': '🦲', 'shower': '🚿', 'banana': '🍌', 'ribbon': '🎀', 'mosque': '🕌', 'person in tuxedo': '🤵', 'call me hand': '🤙', 'police car light': '🚨', 'pager': '📟',
	'globe showing Americas': '🌎', 'Japanese dolls': '🎎', 'bow and arrow': '🏹', 'dragon': '🐉', 'locked with key': '🔐', 'horse racing': '🏇', 'eight-thirty': '🕣', 'telescope': '🔭', 'input symbols': '🔣',
	'fairy': '🧚', 'lemon': '🍋', 'upside-down face': '🙃', 'waving hand': '👋', 'bullet train': '🚅', 'man': '👨', 'grinning squinting face': '😆', 'pen': '🖊', 'memo': '📝', 'high-heeled shoe': '👠', 
	'locomotive': '🚂', 'shaved ice': '🍧', 'fleur-de-lis': '⚜', 'milky way': '🌌', 'blossom': '🌼', 'shopping cart': '🛒', 'person in steamy room': '🧖', 'parrot': '🦜', 'tomato': '🍅', 
	'open file folder': '📂', 'woman dancing': '💃', 'bed': '🛏', 'chart decreasing': '📉', 'face with hand over mouth': '🤭', 'face with tears of joy': '😂', 'eagle': '🦅', 'tennis': '🎾', 'honeybee': '🐝',
	'camel': '🐪', 'monkey face': '🐵', 'game die': '🎲', 'fish': '🐟', 'children crossing': '🚸', 'safety pin': '🧷', 'mountain': '⛰', 'raccoon': '🦝', 'clapper board': '🎬', 'foot': '🦶', 'dagger': '🗡', 
	'couch and lamp': '🛋', 'cow face': '🐮', 'ice skate': '⛸', 'doughnut': '🍩', 'new moon': '🌑', 'tram': '🚊', 'full moon face': '🌝', 'oncoming bus': '🚍', 'mountain railway': '🚞', 
	'antenna bars': '📶', 'confused face': '😕', 'shield': '🛡', 'star of David': '✡', 'crescent moon': '🌙', 'OK hand': '👌', 'cloud with snow': '🌨', 'bottle with popping cork': '🍾', 'prayer beads': '📿',
	'church': '⛪', 'cross mark button': '❎', 'vulcan salute': '🖖', 'llama': '🦙', 'baby symbol': '🚼', 'police officer': '👮', 'yin yang': '☯', 'ten-thirty': '🕥', 'airplane': '✈', 
	'cowboy hat face': '🤠', 'love-you gesture': '🤟', 'white question mark': '❔', 'warning': '⚠', 'hushed face': '😯', 'cityscape at dusk': '🌆', 'high voltage': '⚡', 'department store': '🏬',
	'ten o’clock': '🕙', 'vampire': '🧛', 'control knobs': '🎛', 'keycap: 10': '🔟', 'lab coat': '🥼', 'superhero': '🦸', 'calendar': '📅', 'six o’clock': '🕕', 'love letter': '💌', 'roller skate': '🛼', 
	'exploding head': '🤯', 'spider': '🕷', 'club suit': '♣', 'person fencing': '🤺', 'vibration mode': '📳', 'kiwi fruit': '🥝', 'white heart': '🤍', 'hand with fingers splayed': '🖐', 'post office': '🏤',
	'meat on bone': '🍖', 'large orange diamond': '🔶', 'woman with headscarf': '🧕', 'envelope with arrow': '📩', 'ballot box with ballot': '🗳', 'sun behind cloud': '⛅', 'drooling face': '🤤',
	'wind face': '🌬', 'trumpet': '🎺', 'fuel pump': '⛽', 'chocolate bar': '🍫', 'french fries': '🍟', 'custard': '🍮', 'jeans': '👖', 'kissing face with closed eyes': '😚', 'woman': '👩', 
	'rolling on the floor laughing': '🤣', 'brain': '🧠', 'pensive face': '😔', 'taxi': '🚕', 'bridge at night': '🌉', 'left speech bubble': '🗨', 'menorah': '🕎', 'input latin letters': '🔤', 
	'fire extinguisher': '🧯', 'medium-dark skin tone': '🏾', 'waning crescent moon': '🌘', 'person pouting': '🙎', 'worried face': '😟', 'folded hands': '🙏', 'sun behind rain cloud': '🌦', 
	'wine glass': '🍷', 'person wearing turban': '👳', 'rabbit face': '🐰', 'satellite antenna': '📡', 'orthodox cross': '☦', 'soft ice cream': '🍦', 'newspaper': '📰', 'face with medical mask': '😷', 
	'white exclamation mark': '❕', 'dumpling': '🥟', 'cinema': '🎦', 'leopard': '🐆', 'money-mouth face': '🤑', 'wilted flower': '🥀', 'telephone': '☎', 'cityscape': '🏙', 'mosquito': '🦟',
	'dizzy': '💫', 'beaver': '🦫', 'cat': '🐈', 'see-no-evil monkey': '🙈', 'ewe': '🐑', 'broccoli': '🥦', 'goggles': '🥽', 'baby': '👶', 'musical keyboard': '🎹', 'minibus': '🚐', 'flag in hole': '⛳',
	'disappointed face': '😞', 'bellhop bell': '🛎', 'multiply': '✖', 'bell': '🔔', 'red exclamation mark': '❗', 'mammoth': '🦣', 'salt': '🧂', 'sun with face': '🌞', 'popcorn': '🍿', 
	'pine decoration': '🎍', 'cooking': '🍳', 'dog face': '🐶', 'prohibited': '🚫', 'red envelope': '🧧', 'watermelon': '🍉', 'paintbrush': '🖌', 'spiral notepad': '🗒', 'airplane arrival': '🛬', 
	'writing hand': '✍', 'oil drum': '🛢', 'right anger bubble': '🗯', 'person with skullcap': '👲', 'takeout box': '🥡', 'hot face': '🥵', 'fork and knife': '🍴', 'chipmunk': '🐿', 'money with wings': '💸', 
	'shortcake': '🍰', 'heart suit': '♥', 'chains': '⛓', 'female sign': '♀', 'peacock': '🦚', 'satellite': '🛰', 'dim button': '🔅', 'rocket': '🚀', 'recycling symbol': '♻', 'sunflower': '🌻',
	'straight ruler': '📏', 'rhinoceros': '🦏', 'baby bottle': '🍼', 'top hat': '🎩', 'bento box': '🍱', 'knocked-out face': '😵', 'person gesturing NO': '🙅', 'goblin': '👺', 'pill': '💊', 
	'shallow pan of food': '🥘', 'tooth': '🦷', 'rugby football': '🏉', 'skull': '💀', 'canoe': '🛶', 'butterfly': '🦋', 'american football': '🏈', 'carousel horse': '🎠', 'black circle': '⚫', 'skier': '⛷',
	'ice': '🧊', 'strawberry': '🍓', 'honey pot': '🍯', 'hatching chick': '🐣', 'paperclip': '📎', 'butter': '🧈', 'card index dividers': '🗂', 'black flag': '🏴', 'pig': '🐖', 'violin': '🎻', 
	'woman’s hat': '👒', 'ice hockey': '🏒', 'white flower': '💮', 'blue circle': '🔵', 'kaaba': '🕋', 'monorail': '🚝', 'cooked rice': '🍚', 'pickup truck': '🛻', 'Sagittarius': '♐', 
	'smiling cat with heart-eyes': '😻', 'teddy bear': '🧸', 'kiss mark': '💋', 'left luggage': '🛅', 'postbox': '📮', 'tent': '⛺', 'green apple': '🍏', 'deciduous tree': '🌳', 'melon': '🍈', 
	'oncoming taxi': '🚖', 'gorilla': '🦍', 'grinning face': '😀', 'water closet': '🚾', 'person in bed': '🛌', 'name badge': '📛', 'curly hair': '🦱', 'Christmas tree': '🎄', 'battery': '🔋', 
	'roller coaster': '🎢', 'dotted six-pointed star': '🔯', 'castle': '🏰', 'ear of corn': '🌽', 'elephant': '🐘', 'sailboat': '⛵', 'mountain cableway': '🚠', 'cocktail glass': '🍸', 'stop sign': '🛑',
	'older person': '🧓', 'page with curl': '📃', 'cyclone': '🌀', 'last quarter moon face': '🌜', 'rosette': '🏵', 'rabbit': '🐇', 'flower playing cards': '🎴', 'clutch bag': '👝', 'sled': '🛷', 
	'sunset': '🌇', 'disguised face': '🥸', 'person: beard': '🧔', 'collision': '💥', 'ear with hearing aid': '🦻', 'smiling face with halo': '😇', 'file folder': '📁', 'telephone receiver': '📞', 
	'mobile phone': '📱', 'oden': '🍢', 'duck': '🦆', 'eleven-thirty': '🕦', 'kick scooter': '🛴', 'cherries': '🍒', 'pig nose': '🐽', 'bathtub': '🛁', 'stuffed flatbread': '🥙', 'receipt': '🧾',
	'check box with check': '☑', 'currency exchange': '💱', 'sauropod': '🦕', 'spoon': '🥄', 'crossed flags': '🎌', 'Tokyo tower': '🗼', 'tiger': '🐅', 'hugging face': '🤗', 'pleading face': '🥺',
	'face with symbols on mouth': '🤬', 'baggage claim': '🛄', 'guard': '💂', 'card index': '📇', 'counterclockwise arrows button': '🔄', 'person getting massage': '💆', 'credit card': '💳', 'old man': '👴',
	'bookmark tabs': '📑', 'crying cat': '😿', 'fireworks': '🎆', 'station': '🚉', 'tongue': '👅', 'smirking face': '😏', 'sweat droplets': '💦', 'Leo': '♌', 'sake': '🍶', 'person shrugging': '🤷', 
	'woman’s sandal': '👡', 'person rowing boat': '🚣', 'fearful face': '😨', 'thought balloon': '💭', 'no smoking': '🚭', 'squid': '🦑', 'houses': '🏘', 'open hands': '👐', 'dragon face': '🐲',
	'sparkles': '✨', 'military medal': '🎖', 'musical note': '🎵', 'clockwise vertical arrows': '🔃', 'seedling': '🌱', 'broken heart': '💔', 'woozy face': '🥴', 'first quarter moon': '🌓', 'candle': '🕯', 
	'raising hands': '🙌', 'eleven o’clock': '🕚', 'running shirt': '🎽', 'persevering face': '😣', 'alien monster': '👾', 'fax machine': '📠', 'person swimming': '🏊', 'upwards button': '🔼', 
	'ambulance': '🚑', 'five-thirty': '🕠', 'spiral calendar': '🗓', 'white square button': '🔳', 'check mark': '✔', 'sport utility vehicle': '🚙', 'wrapped gift': '🎁', 'flag: Mongolia': '🇲🇳', 
	'face with raised eyebrow': '🤨', 'postal horn': '📯', 'love hotel': '🏩', 'speaker high volume': '🔊', 'bowl with spoon': '🥣', 'person bouncing ball': '⛹', 'office building': '🏢', 
	'speech balloon': '💬', 'anguished face': '😧', 'movie camera': '🎥', 'train': '🚆', 'detective': '🕵', 'small airplane': '🛩', 'shamrock': '☘', 'person climbing': '🧗', 'puzzle piece': '🧩', 
	'closed umbrella': '🌂', 'boar': '🐗', 'snowflake': '❄', 'round pushpin': '📍', 'light skin tone': '🏻', 'hammer and wrench': '🛠', 'bat': '🦇', 'brick': '🧱', 'pinched fingers': '🤌', 'frowning face': '☹',
	'cookie': '🍪', 'mouse': '🐁', 'beer mug': '🍺', 'luggage': '🧳', 'pancakes': '🥞', 'cloud with rain': '🌧', 'sheaf of rice': '🌾', 'nine-thirty': '🕤', 'ox': '🐂', 'spiral shell': '🐚', 
	'framed picture': '🖼', 'nauseated face': '🤢', 'fried shrimp': '🍤', 'television': '📺', 'articulated lorry': '🚛', 'trackball': '🖲', 'house': '🏠', 'four leaf clover': '🍀', 'pouting face': '😡', 
	'dog': '🐕', 'taco': '🌮', 'TOP arrow': '🔝', 'backhand index pointing up': '👆', 'seven o’clock': '🕖', 'person: blond hair': '👱', 'person lifting weights': '🏋', 'key': '🔑', 'spider web': '🕸', 
	'delivery truck': '🚚', 'two-thirty': '🕝', 'baguette bread': '🥖', 'bison': '🦬', 'fish cake with swirl': '🍥', 'purple heart': '💜', 'pencil': '✏', 'hedgehog': '🦔', 'jack-o-lantern': '🎃', 
	'astonished face': '😲', 'person gesturing OK': '🙆', 'magnifying glass tilted right': '🔎', 'lady beetle': '🐞', 'open mailbox with raised flag': '📬', 'non-potable water': '🚱', 'garlic': '🧄', 
	'wastebasket': '🗑', 'person tipping hand': '💁', 'curry rice': '🍛', 'kiss': '💏', 'women holding hands': '👭', 'falafel': '🧆', 'face savoring food': '😋', 'shuffle tracks button': '🔀', 
	'potable water': '🚰', 'sunglasses': '🕶', 'tiger face': '🐯', 'kangaroo': '🦘', 'billed cap': '🧢', 'tulip': '🌷', 'locked': '🔒', 'vertical traffic light': '🚦', 'octopus': '🐙', 'rooster': '🐓', 
	'zany face': '🤪', 'pizza': '🍕', 'no bicycles': '🚳', 'whale': '🐋', 'dark skin tone': '🏿', 'oncoming police car': '🚔', 'motorway': '🛣', 'raised fist': '✊', 'mobile phone off': '📴',
	'grinning face with big eyes': '😃', 'clown face': '🤡', 'sun': '☀', 'sparkling heart': '💖', 'spouting whale': '🐳', 'red question mark': '❓', 'boxing glove': '🥊', 'oncoming fist': '👊', 
	'safety vest': '🦺', 'camping': '🏕', 'bouquet': '💐', 'person surfing': '🏄', 'optical disk': '💿', 'bookmark': '🔖', 'door': '🚪', 'weary cat': '🙀', 'backhand index pointing left': '👈', 
	'bar chart': '📊', 'person in lotus position': '🧘', 'coat': '🧥', 'factory': '🏭', 'microphone': '🎤', 'girl': '👧', 'star-struck': '🤩', 'zipper-mouth face': '🤐', 'airplane departure': '🛫', 
	'hammer': '🔨', 'anxious face with sweat': '😰', 'graduation cap': '🎓', 'ON! arrow': '🔛', 'test tube': '🧪', 'face with thermometer': '🤒', 'label': '🏷', 'nut and bolt': '🔩', 'package': '📦', 
	'Capricorn': '♑', 'dress': '👗', 'derelict house': '🏚', 'computer mouse': '🖱', 'chestnut': '🌰', 'helicopter': '🚁', 'ninja': '🥷', 'cloud': '☁', 'curly loop': '➰', 'gear': '⚙', 'basketball': '🏀', 
	'ring': '💍', 'rainbow': '🌈', 'amphora': '🏺', 'construction worker': '👷', 'hot beverage': '☕', 'fountain': '⛲', 'person playing handball': '🤾', 'cow': '🐄', 'person bowing': '🙇', 'ram': '🐏', 
	'film projector': '📽', 'eight o’clock': '🕗', 'smiling face with tear': '🥲', 'horizontal traffic light': '🚥', 'twelve-thirty': '🕧', 'cheese wedge': '🧀', 'snake': '🐍', 'sparkler': '🎇', 
	'medium-light skin tone': '🏼', 'inbox tray': '📥', 'bicycle': '🚲', 'map of Japan': '🗾', 'two hearts': '💕', 'front-facing baby chick': '🐥', 'fork and knife with plate': '🍽', 'ship': '🚢', 
	'tropical drink': '🍹', 'tram car': '🚋', 'red heart': '❤', 'person running': '🏃', 'eye': '👁', 'otter': '🦦', 'dashing away': '💨', 'cloud with lightning': '🌩', 'boy': '👦', 'restroom': '🚻', 
	'beverage box': '🧃', 'firecracker': '🧨', 'police car': '🚓', 'speaker medium volume': '🔉', 'carrot': '🥕', 'crying face': '😢', 'video game': '🎮', 'white circle': '⚪', 
	'closed mailbox with lowered flag': '📪', 'grimacing face': '😬', 'child': '🧒', 'pinching hand': '🤏', 'white cane': '🦯', 'trident emblem': '🔱', 'sari': '🥻', 'volcano': '🌋', 
	'slightly smiling face': '🙂', 'auto rickshaw': '🛺', 'smiling face with hearts': '🥰', 'pool 8 ball': '🎱', 'shushing face': '🤫', 'men holding hands': '👬', 'bug': '🐛', 'medical symbol': '⚕', 
	'desert island': '🏝', 'heart exclamation': '❣', 'droplet': '💧', 'martial arts uniform': '🥋', 'coffin': '⚰', 'four o’clock': '🕓', 'softball': '🥎', 'snow-capped mountain': '🏔', 'nail polish': '💅', 
	'smiling face': '☺', 'dna': '🧬', 'nerd face': '🤓', 'victory hand': '✌', 'face without mouth': '😶', 'last quarter moon': '🌗', 'person golfing': '🏌', 'closed book': '📕', 'pig face': '🐷', 
	'hear-no-evil monkey': '🙉', 'no pedestrians': '🚷', 'person juggling': '🤹', 'hot springs': '♨', 'motorized wheelchair': '🦼', 'plus': '➕', 'swan': '🦢', 'backhand index pointing right': '👉', 
	'white hair': '🦳', 'radio button': '🔘', 'automobile': '🚗', 'soccer ball': '⚽', 'dove': '🕊', 'cigarette': '🚬', 'kissing face with smiling eyes': '😙', 'scroll': '📜', 'red triangle pointed up': '🔺', 
	'speedboat': '🚤', 'crown': '👑', 'baby chick': '🐤', 'globe showing Europe-Africa': '🌍'}
	
	if isinstance(n,int) and 1706>=n:
		return emoji[n]
	
	elif isinstance(n,str):
		try:
			return emoji2[n.lower()]

		except:
			print(f'{err} Emoji {facemoji} Not Found {err}')	

	else:
		print(f'{err} Arguments Must {facemoji} Be in int {err}')
		
def recmic(sec:int):
	if isinstance(sec,int):
		import pyaudio
		import wave

		audio=pyaudio.PyAudio()
		stream=audio.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)

		frames=[]

		fn = "Pydule Recorded Microphone-" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".wav"
		for i in range(0,int(44100/1024*(sec+1))):
			data=stream.read(1024)
			frames.append(data)

		stream.stop_stream()
		stream.close()
		audio.terminate()

		sound_file=wave.open(fn,'wb')
		sound_file.setnchannels(1)
		sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
		sound_file.setframerate(44100) 
		sound_file.writeframes(b''.join(frames))
		sound_file.close()
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in int {err}')	   

def mulmatrix(x:list,y:list) -> list:
	if isinstance(x,list) and isinstance(y,list):
		import numpy as np

		return np.dot(np.array(x), np.array(y))
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in list and list {err}')

def swapdict(d:dict) -> dict:
	if isinstance(d,dict):
		new={}

		for i in d:
			new[d.get(i)]=i

		return new
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in dict {err}')

def sepstr(st:str,n:int) -> list:
	if isinstance(st,str) and isinstance(n,int):
		l,s=[],''

		for i in st:
			if len(s)!=n:
				s+=i
			else:
				l+=[s]
				s=''
				s+=i
		if len(s)>0:
			l+=[s]    

		return l 
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str and int {err}')

def DecryptStr(st:str,k:dict) -> str:
	s,nd='',{}

	keys={'A': '+!=^-&!@', 'B': '&_-@@#^&', 'C': '@+!&@_^+', 'D': '^$%%!$+$', 'E': '-_-&!*_!', 'F': '^^+!=+%=', 'G': '==%&+_#&', 'H': '$%+==_@^', 'I': '=*$$^*#@', 'J': '=#=+$*_=', 'K': '#&##&^+&', 'L': '*+_$#_$%', 'M': '_!&!-^-+', 'N': '%-_^!!@@', 'O': '-+_=#^=!', 'P': '&!^^^#&=', 'Q': '*-&$%%*@', 'R': '!=!*=^^%', 'S': '##!+^$--', 'T': '%-@#%&$+', 'U': '^+&_$_%_', 'V': '!__^!#-!', 'W': '@$-_##--', 'X': '--^!=&@@', 'Y': '=#=@=!=%', 'Z': '_^-@-_=^', 'a': '*&=+&-=^', 'b': '^@+%!!*^', 'c': '$@@_&-@^', 'd': '!&=#--=+', 'e': '!%&%_+!#', 'f': '+_$_$@*^', 'g': '^**%!@!&', 'h': '*&&!=-^-', 'i': '*-^+@=%&', 'j': '+!$#_%**', 'k': '=*$&-_+=', 'l': '_=#_%=#_', 'm': '&+$%$#+*', 'n': '&^^%_+^_', 'o': '&&!$%&@@', 'p': '$-&==^&@', 'q': '_&$_*#_#', 'r': '#!*-!+*@', 's': '#&@&%+!+', 't': '!=_*=+%_', 'u': '#$*=&=!_', 'v': '=^-##+$*', 'w': '^$!_&$$&', 'x': '!==&$$=-', 'y': '@=&!*=$$', 'z': '^_=@_=+-', '1': '-_-@+=^@', '2': '$#=!$_%@', '3': '#-=+$%@$', '4': '=#__%&##', '5': '--&$@^#=', '6': '#@!+_##*', '7': '_%$%#@!$', '8': '*=-*@_^+', '9': '$_^^^+%=', '0': '+@=*$*+-', '!': '-^%@&-@-', '@': '+##=@%_-', '#': '=-$=-_&+', '$': '*%&@%@%*', '%': '=^^%*&&=', '^': '+@#-^!_&', '&': '&--&@!#!', '*': '=@=#*+$@', '_': '^$--@@-&', '=': '@%_*-&=#', '-': '@@-@+@+_', '+': '#-!@!+=@', '(': '#+$^@%%$', ')': '!&^$&-$+', '[': '%_%-#-==', ']': '#^%#_!%%', '`': '#@%+&&*_', '~': '_+@-_&@%', '{': '=%-#+-&!', '}': '_@!!_@+-', '?': '+@%^&&!@', '\\': '!_-$!&-@', "'": '&==++^-^', '/': '_%=*&__&', ';': '+-!=#=#@', ':': '_+*=!$_$', '"': '%_#_%$&=', '<': '%#&+_!!$', '>': '*#+=&*%#', '.': '=&-$#_-$', ',': '%&%-%#_&', ' ': '^=%@=#=!'}
	
	if isinstance(st,str) and isinstance(k,dict):
		for i in keys:
			if keys[i] in k:
				nd[i]=k[keys[i]]

		nd=swapdict(nd)
		sr=sepstr(st,7)

		for i in range(len(sr)):
			s+=nd[sr[i]]

		return s
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str and dict {err}')    

def EncryptStr(string:str) -> str and dict:
	if isinstance(string,str):
		import random as r

		ex=['!','@','#','$','%','^','&','*','_','=','-','+']

		s,Ans,d,e='',[],{'A': None, 'B': None, 'C': None, 'D': None, 'E': None, 'F': None, 'G': None, 'H': None, 'I': None, 'J': None, 'K': None, 'L': None, 'M': None, 'N': None, 'O': None, 'P': None, 'Q': None, 'R': None, 'S': None, 'T': None, 'U': None, 'V': None, 'W': None, 'X': None, 'Y': None, 'Z': None, 'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'i': None, 'j': None, 'k': None, 'l': None, 'm': None, 'n': None, 'o': None, 'p': None, 'q': None, 'r': None, 's': None, 't': None, 'u': None, 'v': None, 'w': None, 'x': None, 'y': None, 'z': None,'1':None,'2':None,'3':None,'4':None,'5':None,'6':None,'7':None,'8':None,'9':None,'0':None,'!':None,'@':None,'#':None,'$':None,'%':None,'^':None,'&':None,'*':None,'_':None,'=':None,'-':None,'+':None,'(':None,')':None,'[':None,']':None,'`':None,'~':None,'{':None,'}':None,'?':None,'\\':None,'\'':None,'/':None,';':None,':':None,'\"':None,'<':None,'>':None,'.':None,',':None,' ':None},{}
		keys,new={'A': '+!=^-&!@', 'B': '&_-@@#^&', 'C': '@+!&@_^+', 'D': '^$%%!$+$', 'E': '-_-&!*_!', 'F': '^^+!=+%=', 'G': '==%&+_#&', 'H': '$%+==_@^', 'I': '=*$$^*#@', 'J': '=#=+$*_=', 'K': '#&##&^+&', 'L': '*+_$#_$%', 'M': '_!&!-^-+', 'N': '%-_^!!@@', 'O': '-+_=#^=!', 'P': '&!^^^#&=', 'Q': '*-&$%%*@', 'R': '!=!*=^^%', 'S': '##!+^$--', 'T': '%-@#%&$+', 'U': '^+&_$_%_', 'V': '!__^!#-!', 'W': '@$-_##--', 'X': '--^!=&@@', 'Y': '=#=@=!=%', 'Z': '_^-@-_=^', 'a': '*&=+&-=^', 'b': '^@+%!!*^', 'c': '$@@_&-@^', 'd': '!&=#--=+', 'e': '!%&%_+!#', 'f': '+_$_$@*^', 'g': '^**%!@!&', 'h': '*&&!=-^-', 'i': '*-^+@=%&', 'j': '+!$#_%**', 'k': '=*$&-_+=', 'l': '_=#_%=#_', 'm': '&+$%$#+*', 'n': '&^^%_+^_', 'o': '&&!$%&@@', 'p': '$-&==^&@', 'q': '_&$_*#_#', 'r': '#!*-!+*@', 's': '#&@&%+!+', 't': '!=_*=+%_', 'u': '#$*=&=!_', 'v': '=^-##+$*', 'w': '^$!_&$$&', 'x': '!==&$$=-', 'y': '@=&!*=$$', 'z': '^_=@_=+-', '1': '-_-@+=^@', '2': '$#=!$_%@', '3': '#-=+$%@$', '4': '=#__%&##', '5': '--&$@^#=', '6': '#@!+_##*', '7': '_%$%#@!$', '8': '*=-*@_^+', '9': '$_^^^+%=', '0': '+@=*$*+-', '!': '-^%@&-@-', '@': '+##=@%_-', '#': '=-$=-_&+', '$': '*%&@%@%*', '%': '=^^%*&&=', '^': '+@#-^!_&', '&': '&--&@!#!', '*': '=@=#*+$@', '_': '^$--@@-&', '=': '@%_*-&=#', '-': '@@-@+@+_', '+': '#-!@!+=@', '(': '#+$^@%%$', ')': '!&^$&-$+', '[': '%_%-#-==', ']': '#^%#_!%%', '`': '#@%+&&*_', '~': '_+@-_&@%', '{': '=%-#+-&!', '}': '_@!!_@+-', '?': '+@%^&&!@', '\\': '!_-$!&-@', "'": '&==++^-^', '/': '_%=*&__&', ';': '+-!=#=#@', ':': '_+*=!$_$', '"': '%_#_%$&=', '<': '%#&+_!!$', '>': '*#+=&*%#', '.': '=&-$#_-$', ',': '%&%-%#_&', ' ': '^=%@=#=!'},{}
		
		while True:
			if len(Ans)!=95:
				n=''
				for i in range(7):
					n+=ex[r.randint(0,11)]
				if n not in Ans:
					Ans+=[n]
			
			else:
				break
		
		for i,j in zip(d,Ans):
			d[i]=j

		for i in string:
			s+=d[i]

		for i in d:
			n=ord(i)
			e[n]=d[i]

		for i,j in zip(keys,e):
			new[keys[i]]=e[j]

		new=shuffledict(new)

		return s,new
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')	

def zipfile(path:str or list, zip:str):
	if isinstance(path,str) and isinstance(zip,str):
		import zipfile as zf

		with zf.ZipFile(zip, 'w') as zipfile:
			if isinstance(path,list):
				for i in path:
					zipfile.write(i, arcname=i.split('/')[-1])

			elif isinstance(path,str):
				zf.write(i,arcname=i.split('/')[-1])

			else:
				print(f'{err} Arguments Must {facemoji} Be in str and str {err}')

	else:
		print(f'{err} Arguments Must {facemoji} Be in str and str{err}')

def wjson(data:str,path:str):
	if isinstance(data,dict) and isinstance(path,str):
		import json

		with open(path,'w') as json_file:
			json.dump(data,json_file)

	else:
		print(f'{err} Arguments Must {facemoji} Be in str and str {err}')		

def askfiles() -> list:
	import tkinter.filedialog as fd

	files = fd.askopenfilenames(title='Choose files')

	return list(files)

def askfile() -> str:
	from tkinter.filedialog import askopenfilename

	filepath = askopenfilename()

	return filepath

def delfile(filename:str):
	if isinstance(filename,str):
		if filename=='askfile':
			import os
			from tkinter.filedialog import askopenfilename
			
			filename = askopenfilename()
			os.remove(filename)

		else:	
			import os

			os.remove(filename)

	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')

def deljsonele(path:str):
	if isinstance(path,str):
		import json

		jsonfile=json.load(open(path))
		copy=jsonfile.copy()

		k=eval(input('Enter the Key : '))

		del copy[k]

		with open(path,'w') as json_file:
			json.dump(copy,json_file)	

	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')	

def upjson(path:str):
	if isinstance(path,str):
		import json

		jsonfile=json.load(open(path))
		copy=jsonfile.copy()

		k=eval(input('Enter the Key : '))
		v=eval(input('Enter the Value : '))
		copy[k]=v

		with open(path,'w') as json_file:
			json.dump(copy,json_file)

	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')		

def num(n:int) -> str:
	if isinstance(n,int):
		if str(n).endswith('1') and not(str(n).endswith('11')):
			s=str(n)+'st'

		elif str(n).endswith('2') and not(str(n).endswith('12')):
			s=str(n)+'nd'

		elif str(n).endswith('3') and not(str(n).endswith('13')):
			s=str(n)+'rd'   

		else:
			s=str(n)+'th'

		return s 
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in int {err}')	

def intuple(x:tuple,index:int,element:int or float or str or tuple or list or dict or set or frozenset or bool or None) -> tuple:
	if isinstance(x,tuple):
		new=()
		if len(x)<=index:
			new+=x+(element,)
		else:	
			for i,j in zip(range(len(x)),x):
				if i==index:
					new+=(element,)+(j,)

				else:
					new+=(j,)
		return new
		
	else:
		print(f'{err} Arguments Must {facemoji} Be in tuple and int and int or float or str or tuple or list or dict or set or frozenset or bool or None {err}')

def movefiles(current:str, destination:str):
	if isinstance(current,str) and isinstance(current,str):
		import shutil
		import os
		
		files = os.listdir(current)
		
		for file in files:
			source_path = os.path.join(current, file)
			destination_path = os.path.join(destination, file)
			shutil.move(source_path, destination_path)

	else:
		print(f'{err} Arguments Must {facemoji} Be in str and str {err}')

def instr(x:str,index:int,element:str) -> str:
	if isinstance(x,str):
		new=''

		if len(x)<=index:
			new+=x+element

		else:	
			for i,j in zip(range(len(x)),x):
				if i==index:
					new+=element+j

				else:
					new+=j

		return new
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str and int and str {err}')			

def askfolder():
	from tkinter import filedialog

	folder = filedialog.askdirectory()

	return folder

def msgbox(type:str,title:str='Pydule',text:str='YOUR TEXT HERE'):
	if isinstance(type,str) and isinstance(title,str) and isinstance(text,str):
		from tkinter import messagebox

		if type=='info':
			return messagebox.showinfo(title,text)
		
		elif type=='error':
			return messagebox.showerror(title,text)
		
		elif type=='warning':
			return messagebox.showwarning(title,text)
		
		elif type=='question':
			return messagebox.askquestion(title,text)
		
		elif type=='okcancel':
			return messagebox.askokcancel(title,text)
		
		elif type=='retrycancel':
			return messagebox.askretrycancel(title,text)
		
		elif type=='yesno':
			return messagebox.askyesno(title,text)
		
		elif type=='yesnocancel':
			return messagebox.askyesnocancel(title,text)	
								
		else:
			print(err)

	else:
		print(f'{err} Arguments Must {facemoji} Be in str and str and str {err}')			

def getkeypressed() -> str:
	import keyboard
		
	try:
		return keyboard.read_key()

	except Exception as e:
		print(e)	

def shuffletuple(l) -> tuple:
	if isinstance(l,tuple):
		import random as r
		
		ind,n=[],tuple()
		
		while True:
			ran=r.randint(0,len(l)-1)
		
			if len(ind)==len(l):
				break
		
			if ran not in ind:
		
				ind+=[ran]
		
		for i in ind:
			n+=(l[i],) 
		
		return n
	else:
		print(f'{err} Arguments Must {facemoji} Be in tuple {err}')

def dowhenkeypressed(command:str,func):
	if isinstance(command,str):
		import keyboard
		
		try:
			if keyboard.is_pressed(command):
				func()

		except Exception as e:
			print(e)

	else:
		print(f'{err} Arguments Must {facemoji} Be in str and function {err}')	

def SSort(l:list or tuple) -> list or tuple:
	if isinstance(l,list) or isinstance(l,tuple):
		def lower(s):
			return s.lower()
		
		l1=list(map(lower,l))
	
		l2,final=l1.copy(),[]
		
		l1.sort()

		for i in range(len(l)):
			for j in range(len(l)):

				if l1[i]==l2[j]:
					final.append(l[j])

		if isinstance(l,list):
			return final	

		else:
			return tuple(final)			
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in list or tuple {err}')	

def functions():
	def lower(s):
		return s.lower()

	l=['SSort()','RemoveBG()','SepColumn()','SepRowCsv()','DetectEmoji()','DesktopNotification()','Calender()','GenerateImage() Must Use from Pydule import AI','shuffletuple()','shufflelist()','combinevidandaud()',
	'removeaudfromvid()','vidtoaud()','dowhenkeypressed()','getkeypressed()','askfiles()','movefiles()','sepednumtoint()','getfilesize()','internetspeed()','Emoji()','zipfile()','inputpassword()','sepnum()',
	'shuffledict()','FIGlet()','pytoexe()','aboutbattery()','percent()','msgbox()','askfolder()','askfile()','delfile()','resizeimg()','GetWebHTML()','TrackLocation()','num()','screenshot()','SpeechtoText()',
	'ChatGPT() Use from Pydule import AI','recintaudio()','recmic()','recscreen()','mulmatrix()','EncryptStr()','DecryptStr()','swapdict()','sepstr()','wjson()','deljsonele()','upjson()','copy()','translate()',
	'cqrcode()','summatrix()','submatrix()','intuple()','instr()','reSet()','reDict()','reTuple()','pickcolor()','search()','playmusic()','restart_system()','shutdown_system()','todaysdate()','timenow()','say()',
	'openfile()','weathernow()','setvoice()','voicerate()']
	
	l1=list(map(lower,l))
	
	l2,final=l1.copy(),[]
	
	l1.sort()

	for i in range(len(l)):
		for j in range(len(l)):
			
			if l1[i]==l2[j]:
				final.append(l[j])

	print('Available Functions : \n')

	import time as t

	for i in range(len(l)):
		print(f'\t{i+1}.{final[i]}')
		t.sleep(0.1)

def summatrix(x:list,y:list) -> list:
	if isinstance(x,list) and isinstance(y,list):
		import numpy as np

		result = np.array(x) + np.array(y)
		
		return result
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in list and list {err}')

def submatrix(x:list,y:list) -> list:
	if isinstance(x,list)and isinstance(y,list):
		import numpy as np
		
		result = np.array(x) - np.array(y)

		return result
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in list and list {err}')

def reDict(x:dict,oele:int or float or str or tuple or list or dict or set or frozenset or bool or None,nele:int or float or str or tuple or list or dict or set or frozenset or bool or None) -> dict:
	if isinstance(x,dict):
		new={}
		for i in x:
			if i==oele:
				new[nele]=x.get(i)

			else:
				new[i]=x.get(i)

		return new	
		
	else:
		print(f'{err} Arguments Must {facemoji} Be in dict and int or float or str or tuple or list or dict or set or frozenset or bool or None and int or float or str or tuple or list or dict or set or frozenset or bool or None {err}')

def translate(content:str,language:str) -> str:
	if isinstance(content,str) and isinstance(language,str):
		from deep_translator import GoogleTranslator

		translated = GoogleTranslator(source='auto', target=language.lower()).translate(content)

		return translated
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str and str {err}')	

def combinevidandaud(vpath,apath,result):
	if isinstance(vpath,str) and isinstance(apath,str) and isinstance(result,str) and result.endswith('.mp4'):
		import moviepy.editor as mpe

		clip = mpe.VideoFileClip(vpath)

		audio = mpe.AudioFileClip(apath)
		
		finalclip = clip.set_audio(audio)
		
		finalclip.write_videofile(result,fps=45)

	else:
		print(f'{err} Arguments Must {facemoji} Be in str and str and str {err}')

def cqrcode(data:str,filename:str):
	if isinstance(data,str) and filename.endswith('.png') or filename.endswith('.jpg'):
		import qrcode

		img = qrcode.make(data)

		img.save(filename)

		print('\nQrcode Saved Successfully \U00002714\n')

	else:
		print(f'{err} Arguments Must {facemoji} Be in str and str {err}')	
	
def Author():
	print('\nThis Pydule is Created by D.Tamil Mutharasan \U0001F608\n')

def reSet(oldset:set,element:int or float or str or tuple or list or dict or set or frozenset or bool or None,newelement:int or float or str or tuple or list or dict or set or frozenset or bool or None) -> set:
	if isinstance(oldset,set):
		new=set()

		for i in oldset:
			if i==element:
				new.add(newelement)

			else:
				new.add(i)

		return new	
				
	else:
		print(f'{err} Arguments Must {facemoji} Be in list and set and int or float or str or tuple or list or dict or set or frozenset or bool or None and int or float or str or tuple or list or dict or set or frozenset or bool or None {err}')		

def reTuple(oldtup:tuple,index:int,newtup:int or float or str or tuple or list or dict or set or frozenset or bool or None) -> tuple:
	if isinstance(oldtup,tuple):
		new=tuple()

		for i in range(len(oldtup)):
			if i==index:
				new+=(newtup,)

			else:
				new+=(oldtup[i],)

		return new
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str and str int or float or str or tuple or list or dict or set or frozenset or bool or None {err}')	

def copy(string:str):
	if isinstance(string,str):	
		import pyperclip

		pyperclip.copy(string)

	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')

def pickcolor():
	from tkinter import colorchooser

	c=colorchooser.askcolor(title='Pydule Color Picker \U00002714')
	copy('\''+str(c[-1])+'\'')

def vidtoaud(path:str,filename:str):
	if isinstance(path,str) and isinstance(filename,str) and filename.endswith('.mp3'):
		import moviepy.editor as mp

		clip = mp.VideoFileClip(path)

		clip.audio.write_audiofile(filename)

	else:
		print(f'{err} Arguments Must {facemoji} Be in str and str {err}')	

def removeaudfromvid(path:str,filename:str):
	if isinstance(path,str) and isinstance(filename,str) and filename.endswith('.mp4'):
		import moviepy.editor as mp

		videoclip = VideoFileClip(path)
		
		new_clip = videoclip.without_audio()
		
		new_clip.write_videofile(filename)

	else:
		print(f'{err} Arguments Must {facemoji} Be in str and str {err}')	


def search(content:str):
	if isinstance(content,str):
		import pywhatkit as kt

		kt.search(content)	
		print('\nSearching \U0001F50E...\n')

	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')
	
def playmusic(path:str):
	if isinstance(path,str):
		if path=='askfile':
			import os
			from tkinter.filedialog import askopenfilename
			import time
			import pyglet

			filename = askopenfilename()

			media_player = pyglet.media.Player()

			song = pyglet.media.load(filename)

			media_player.queue(song)

			media_player.play()

			time.sleep(song.duration)

			media_player.pause()

		else:
			import os
			from tkinter.filedialog import askopenfilename
			import time
			import pyglet

			media_player = pyglet.media.Player()

			song = pyglet.media.load(path)

			media_player.queue(song)

			media_player.play()

			time.sleep(song.duration)

			media_player.pause()

	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')

def restart_system():
	print('\nRestarting the System \U0001F4BB...\n')	

	os.system("shutdown /r /t 1")
	
def shutdown_system():
	print('\nShutting Down Your System \U0001F4BB...\n')

	os.system("shutdown /s /t 1")
	
def todaysdate():
	from datetime import date

	d=date.today()

	return d
	
def timenow():
	from datetime import datetime

	now = datetime.now()
	current_time = now.strftime("%H:%M:%S %p")

	return current_time
	
def say(content:str,save:bool=False):
	if isinstance(content,str) and isinstance(save,bool):	
		engine.say(content)

		if save==True:
			engine.save_to_file(text=content,filename=content+'.mp3')
		engine.runAndWait() 

	else:
		print(f'{err} Arguments Must {facemoji} Be in str and bool {err}')

def openfile(path:str):
	if isinstance(path,str):	
		if path=='askfile':
			from tkinter import filedialog

			filename = filedialog.askopenfilename()
			os.startfile(filename)

		else:	
			os.startfile(path)

	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')		

def getfilesize(path:str) -> int:
	if isinstance(path,str):
		import os
		size = os.path.getsize(path)
		return size
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')

def weathernow(place:str) -> list:
	if isinstance(place,str):
		import requests
		from bs4 import BeautifulSoup
		
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

		def weather(city,place):
			city = city.replace(" ", "+")
			res = requests.get(
				f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
			soup = BeautifulSoup(res.text, 'html.parser')
			time = soup.select('#wob_dts')[0].getText().strip()
			info = soup.select('#wob_dc')[0].getText().strip()
			weather = soup.select('#wob_tm')[0].getText().strip()
			details=['City Name : '+place,info,weather+'°C']

			return details
			
		city = place+" weather"

		return weather(city,place)
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')	

def TrackLocation(string:str) -> str:
	if isinstance(string,str) and len(string)==13:
		import phonenumbers

		from phonenumbers import geocoder

		number = phonenumbers.parse(string)

		location = geocoder.description_for_number(number, "en")

		return location
	
	else:
		print(f'{err} Arguments Must {facemoji} Be in str {err}')	

def setvoice(num:int):
	if isinstance(num,int):
		voices=engine.getProperty('voices')
		engine.setProperty('voice',voices[num].id)	

	else:
		print(f'{err} Arguments Must {facemoji} Be in int {err}')	

def voicerate(num:int):
	if isinstance(num,int):
		engine.setProperty('rate',num)

	else:
		print(f'{err} Arguments Must {facemoji} Be in int {err}')	