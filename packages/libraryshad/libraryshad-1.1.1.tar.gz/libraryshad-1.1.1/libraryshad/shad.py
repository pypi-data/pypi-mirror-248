from encryption import encryption
from random import randint,choices
from aiohttp import ClientSession
import base64,json,asyncio
from pathlib import Path
from os.path import exists


class Bot:
	def __init__(self,session=None,auth=None,key=None):
		self.session = session
		if session == None:
			
			self.enc = encryption(auth, f"-----BEGIN RSA PRIVATE KEY-----\n{key}\n-----END RSA PRIVATE KEY-----")
		else:
			self.public_key,self.private_key = encryption.rsaKeyGenerate()
			if exists(f"{self.session}.shad"):
				aut = json.loads(open(f"{self.session}.shad","r").read())
				self.enc = encryption(aut["auth"],aut["private_key"])
			else:
				asyncio.run(self.logi())
		self.auth = auth if not auth == None else aut["auth"]
		self.key = key if not key == None else aut["private_key"]
		
	
	async def post_data_ssesion(self,data):
				session_tmp = "".join(choices("abcdefghijklmnopqrstuvwxyz", k=32))
				
				enc = encryption(session_tmp,self.private_key)
				async with ClientSession() as session:
						async with session.post(url=f"https://shadmessenger{randint(1,140)}.iranlms.ir/",data=json.dumps({"api_version":"6","tmp_session":session_tmp,"data_enc":enc.encrypt(json.dumps(data))})) as res:
							result = await res.json()
							return json.loads(enc.decrypt(result["data_enc"]))["data"]
							
	async def get_byte(self,url,header=None):
		async with ClientSession() as session:
			async with session.post(url,headers=header) as res:
				data = await res.text()
				return data
	async def post_byte(self,url,data,header):
		async with ClientSession() as session:
			async with session.post(url,data=data,headers=header) as res:
				data = await res.json()
				return data
				
	async def post_data(self,data):
				
				enc = self.enc
				jso = json.dumps({"api_version":"6","auth":encryption.changeAuthType(self.auth),"data_enc":enc.encrypt(json.dumps(data)),"sign":enc.makeSignFromData(enc.encrypt(json.dumps(data)))})
				async with ClientSession() as session:
						async with session.post(url=f"https://shadmessenger{randint(1,140)}.iranlms.ir/",data=jso) as res:
							result = await res.json()
							return json.loads(enc.decrypt(result["data_enc"]))
		
	async def logi(self):
			phone = input("your phone number : ")
			data = await self.sendCode(phone)
			phone_code_hash = data["phone_code_hash"]
			js = await self.signIn(phone,phone_code_hash,input("your code send : "))
			open(f"{self.session}.shad","w").write(json.dumps(js,indent=4))
			res = await Bot.registerDevice(auth=js["auth"],key=js["private_key"])
			return js["private_key"],js["auth"]
		
	
	async def sendCode(self,phone):
		Json = {"method":"sendCode","input":{"phone_number":f"98{phone[1:]}","send_type":"SMS"},"client":{"app_name":"Main","app_version":"3.5.5","lang_code":"fa","package":"ir.medu.shad","temp_code":"31","platform":"Android"}}
		data = await self.post_data_ssesion(Json)
		return data
		
		
	async def signIn(self,phone,phone_code_hash,phone_code):
			Json = {"method":"signIn","input":{"phone_number":f"98{phone[1:]}","phone_code_hash":phone_code_hash,"phone_code":phone_code,"public_key":self.public_key},"client":{"app_name":"Main","app_version":"3.5.5","lang_code":"fa","package":"ir.medu.shad","temp_code":"31","platform":"Android"}}
			data = await self.post_data_ssesion(Json)
			data["auth"] = encryption.decryptRsaOaep(self.private_key,data["auth"])
			data["private_key"] = self.private_key
			return data

	async def registerDevice(auth,key):
		Json = {"method":"registerDevice","input":{"app_version":"MA_3.5.5","device_hash":"0501110712007200125373640870428014153736","device_model":"rubiran-library","lang_code":"fa","system_version":"SDK 28","token":" ","token_type":"Firebase"},"client": {"app_name":"Main","app_version":"3.5.5","lang_code":"fa","package":"ir.medu.shad","temp_code":"31","platform":"Android"}}
		
		enc = encryption(auth,key)
				
		async with ClientSession() as session:
			async with session.post(url="https://shadmessenger142.iranlms.ir/",data=json.dumps({"api_version":"6","auth":encryption.changeAuthType(auth),"data_enc":enc.encrypt(json.dumps(Json)),"sign":enc.makeSignFromData(enc.encrypt(json.dumps(Json)))})) as res:
				result = await res.json()
				return json.loads(enc.decrypt(result["data_enc"]))
				
	async def joinGroup(self,link):
				hashLink = link.split("/")[-1]
				Json = {"method": "joinGroup", "input": {"hash_link":hashLink,"action":"Join"},"client": {"app_name":"Main","app_version":"3.5.5","lang_code":"fa","package":"ir.medu.shad","temp_code":"31","platform":"Android"}}
				data = await self.post_data(Json)
				return data
				
	async def leaveGroup(self,guid):
				data = await self.post_data({"method": "leaveGroup", "input": {"group_guid": guid},"client": {"app_name":"Main","app_version":"3.5.5","lang_code":"fa","package":"ir.medu.shad","temp_code":"31","platform":"Android"}})
				return data
				
	async def getLinkFromAppUrl(self,app_link):
		return await self.post_data({"method": "getLinkFromAppUrl", "input": {"app_url": app_link},"client": {"app_name":"Main","app_version":"3.5.5","lang_code":"fa","package":"ir.medu.shad","temp_code":"31","platform":"Android"}})
			
	async def forwardMessages(self,from_object_guid,message_ids,to_object_guid):
		return await self.post_data({"method": "forwardMessages", "input":  {"from_object_guid": from_object_guid, "to_object_guid": to_object_guid, "message_ids":message_ids, "rnd": int(randint(100000, 999999))},"client": {"app_name":"Main","app_version":"3.5.5","lang_code":"fa","package":"ir.medu.shad","temp_code":"31","platform":"Android"}})
			
	async def getChannelInfo(self,channel_guid):
		data = await self.post_data({"method": "getChannelInfo", "input": {"channel_guid": channel_guid},"client": {"app_name":"Main","app_version":"3.5.5","lang_code":"fa","package":"ir.medu.shad","temp_code":"31","platform":"Android"}})
		return data["data"]
		
	async def getMessages(self,chat_id,ms_id):
		data = await self.post_data({"method": "getMessagesInterval", "input":{"object_guid":chat_id,"middle_message_id":ms_id},"client": {"app_name":"Main","app_version":"3.5.5","lang_code":"fa","package":"ir.medu.shad","temp_code":"31","platform":"Android"}})
		return data
				
	async def searchGlobalObject(self,text):		
		data = await self.post_data({"method": "searchGlobalObjects", "input":{"filter_types": ['Bot', 'Channel', 'User'], "search_text": text},"client": {"app_name":"Main","app_version":"3.5.5","lang_code":"fa","package":"ir.medu.shad","temp_code":"31","platform":"Android"}})
		return data
	async def sendMessages(self,chat_id,text, message_id=None,metadata=[]):
		data = await self.post_data({"method": "sendMessage", "input": {"object_guid":chat_id,"rnd":f"{randint(100000,999999999)}","text":text,"reply_to_message_id":message_id},"client": {"app_name":"Main","app_version":"3.5.5","lang_code":"fa","package":"ir.medu.shad","temp_code":"31","platform":"Android"}})
		if metadata != [] : data["input"]["metadata"] = {"meta_data_parts":metadata}
		return data
	async def _requestSendFile(self, file):
		data = await self.post_data({"method":"requestSendFile", "input": {"file_name": str(file.split("/")[-1]),"mime": file.split(".")[-1],"size": Path(file).stat().st_size},"client": {"app_name":"Main","app_version":"3.5.5","lang_code":"fa","package":"ir.medu.shad","temp_code":"31","platform":"Android"}})
		
		return data["data"]
	async def upload(self,file):
			test = await self._requestSendFile(file=file)
			bytef = open(file,"rb").read()
			id = test["id"]
			dc_id = test["dc_id"]
			access_hash_send = test["access_hash_send"]
			url = test["upload_url"]
			header = {
				'access-hash-send':access_hash_send,
				'auth':self.auth,
				'file-id':str(id),
				'chunk-size':str(len(bytef)),
			}
			
			if len(bytef) <= 131072:
				header['part-number'],header['total-part'] = "1","1"
				
				while True:
					try:
						o = await self.post_byte(url=url,data=bytef,header=header)
						
						o = o["data"]["access_hash_rec"]
						break
					except: continue
				return [test,o]
			else:
				t = len(bytef) // 131072 + 1
				print(len(bytef))
				for i in range(1,t+1):
					
					if i != t:
						k = (i - 1) * 131072
						header["chunk-size"], header["part-number"], header["total-part"] = "131072", str(i),str(t)
						print('\r' + f'{round(k / 1024) / 1000} MB /', sep='', end=f' {round(len(bytef) / 1024) / 1000} MB')
						
						while True:
							try:
								j = await self.post_byte(url=url,data=bytef[k:k + 131072],header=header)
								j = j["data"]
								
								break
							except: continue 
					else:
						k = (i - 1) * 131072
						header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:])), str(i),str(t)
						print('\r' + f'{round(k / 1024) / 1000} MB /', sep='', end=f' {round(len(bytef) / 1024) / 1000} MB')
						print("\n")
						while True:
							try:
								dr = await self.post_byte(url=url,data=bytef[k:],header=header)
								dr = dr["data"]["access_hash_rec"]
								break
							except: continue
				return [test,dr]
				
	async def send_file(self,file):
		uresponse = await self.upload(file)
		file_id = str(uresponse[0]["id"])
		mime = file.split(".")[-1]
		dc_id = uresponse[0]["dc_id"]
		access_hash_rec = uresponse[1]
		file_name = file.split("/")[-1]
		size = str(len(open(file,"rb").read()))
		inData = {"method":"sendMessage","input":{"object_guid":chat_id,"reply_to_message_id":message_id,"rnd":f"{randint(100000,999999999)}","file_inline":{"dc_id":str(dc_id),"file_id":str(file_id),"type":"File","file_name":file_name,"size":size,"mime":mime,"access_hash_rec":access_hash_rec}},"client": {"app_name":"Main","app_version":"3.5.5","lang_code":"fa","package":"ir.medu.shad","temp_code":"31","platform":"Android"}}
		if caption != None: inData["input"]["text"] = caption
		data = await self.post_data(inData)
		return data
		
	async def getChats(self):
		data = await self.post_data({"method": "getChats", "input": {},"client": {"app_name":"Main","app_version":"3.5.5","lang_code":"fa","package":"ir.medu.shad","temp_code":"31","platform":"Android"}})
		return data["data"]["chats"]
