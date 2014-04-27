from nanshennvshen.library.cookietranport import CookieTransport
import xmlrpclib
import urllib2
import os, base64, time,mimetypes

class NanshennvshenStoreInToDatabasePipeLine(object):

	def process_item(self, item, spider):
		account = spider.settings.get("API_USER_NAME")
		pwd = spider.settings.get("API_USER_PASS")
		api_host = spider.settings.get("API_HOST")
		base_host = spider.settings.get("API_BASE_HOST")
		media_dir = spider.settings.get("IMAGES_STORE")

		trport = CookieTransport()
		server = xmlrpclib.Server(api_host, trport)
		server.system.connect()
		user = server.user.login(account, pwd)
		trport.SESSION_ID_STRING = user["session_name"]
		trport.mysessid = user["sessid"]
		trport.token_host = base_host + "/services/session/token"
		
		new_node = {'body': {'und': {'0': {'value': item["desc"]}}}, 'title': item["name"], 'type': 'shen'}
		new_node["field_gender"] = {"und": item["gender"]}
		
		field_shen_images = []
		for index, image in  enumerate(item["images"]):
			image_abs_path = os.path.join(media_dir, image["path"])
			f = open(image_abs_path, "rb")
			image_content = f.read()
			f.close()
			filename = os.path.split(image_abs_path)[1]
			file_obj = {
				'file': base64.b64encode(image_content),
				'filename': filename,
				'filepath': 'public://' + filename,
				'filesize': os.stat(image_abs_path).st_size,
				'timestamp': str(int(time.time())),
				'uid': user["user"]['uid'],
				'filemime': mimetypes.guess_type(image_abs_path)[0],
				'status': 0,
			}
			res = server.file.create(file_obj)
			if res:
				shen_image = {
					"fid": res["fid"],
					"new": 1,
					"_weight": index,
				}
				field_shen_images.append(shen_image)
		new_node["field_shen_image"] = {"und": field_shen_images}
		try:
			res = server.node.create(new_node)
		except Exception as e:
			print "Error when post shen: %s" %(new_node["title"])
			print new_node
			print e

		# The new node doesn't have image data but I post it 
		return item
		
