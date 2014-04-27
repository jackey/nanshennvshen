import xmlrpclib, urllib2
class CookieTransport(xmlrpclib.Transport):
	def __init__(self, SESSION_ID_STRING='PHPSESSID'):
		xmlrpclib.Transport.__init__(self)
		self.mycookies=None
		self.mysessid=None
		self.SESSION_ID_STRING = SESSION_ID_STRING
		self.token_host = None
	def parseCookies(self,s):
		if s is None: return {self.SESSION_ID_STRING:None}
		ret = {}
		tmp = s.split(';')
		for t in tmp:
			coppia = t.split('=')
			if len(coppia) > 1:
				k = coppia[0].strip()
				v = coppia[1].strip()
				ret[k]=v
				return ret
	def request(self, host, handler, request_body, verbose=0):
		# issue XML-RPC request
		h = self.make_connection(host)
		if verbose:
			h.set_debuglevel(1)
		self.send_request(h, handler, request_body)
		self.send_host(h, host)
		if not self.mysessid is None:
			h.putheader("Cookie", "%s=%s" % (self.SESSION_ID_STRING,self.mysessid) )
		if  not self.token_host is None:
			token = urllib2.urlopen(self.token_host).read()
			h.putheader("X_CSRF_TOKEN", token)
		self.send_user_agent(h)
		self.send_content(h, request_body)
		resp = h.getresponse()
		errcode = resp.status
		errmsg = resp.msg
		headers = resp.getheaders()
		if self.mysessid is None:
			self.mycookies = self.parseCookies( resp.getheader('set-cookie') )
			if self.mycookies.has_key(self.SESSION_ID_STRING):
				self.mysessid = self.mycookies[self.SESSION_ID_STRING]
		if errcode != 200:
			raise xmlrpclib.ProtocolError(
				host + handler,
				errcode, errmsg,
				headers
				)
		self.verbose = verbose
		try:
			sock = h._conn.sock
		except AttributeError:
			sock = None
		return self.parse_response(resp)