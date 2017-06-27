import socket, sys
import time, datetime
from thread import *

def accessdenied ():
	# Funcao que carrega o HTML de resposta a pagina nao autorizada
	arq = open ("accessdenied.txt", 'r')
	d = arq.read()
	arq.close()
	return d

def replycode(reply):
	# Funcao que auxilia o registro do codigo correto no log.
	respostas = ['100', '101', '200', '201', '202', '203', '204', '205','206','300', '301', '302', '303', '304', '305','306', '307','400', '401', '402', '403', '404', '405', '406', '407', '408', '409', '410', '411', '412', '413', '414', '415', '416', '417', '500', '501', '502', '503', '504', '505']

	for x in respostas:
		if (reply.find(x)>=0):
			code = x;
			break
		else:
			code = ''
	if len(code)!=3:
		return '';
	elif code =='100':
		return "HTTP/1.1 100 Continue"
	elif code =='101':
		return "HTTP/1.1 101 Switching Protocols"
	elif code =='200':
		return "HTTP/1.1 200 OK"
	elif code =='201':
		return "HTTP/1.1 201 Createad"
	elif code =='202':
		return "HTTP/1.1 202 Accepted"
	elif code =='203':
		return "HTTP/1.1 203 Non-Authoritative Information"
	elif code =='204':
		return "HTTP/1.1 204 No content"
	elif code =='205':
		return "HTTP/1.1 205 Reset Content"
	elif code =='206':
		return "HTTP/1.1 206 Partial Content"
	elif code =='300':
		return "HTTP/1.1 300 Multiple Choices"
	elif code =='301':
		return "HTTP/1.1 301 Moved Permanently"
	elif code =='302':
		return "HTTP/1.1 302 Found"
	elif code =='303':
		return "HTTP/1.1 303 See Other"
	elif code =='304':
		return "HTTP/1.1 304 Not Modified"
	elif code =='305':
		return "HTTP/1.1 305 Use Proxy"
	elif code =='306':
		return "HTTP/1.1 306 (Unused)"
	elif code =='307':
		return "HTTP/1.1 307 Temporary Redirect"
	elif code =='400':
		return "HTTP/1.1 400 Bad Request"
	elif code =='401':
		return "HTTP/1.1 401 Unauthorized"
	elif code =='402':
		return "HTTP/1.1 402 Payment Required"
	elif code =='403':
		return "HTTP/1.1 403 Forbidden"
	elif code =='404':
		return "HTTP/1.1 404 Not found"
	elif code =='405':
		return "HTTP/1.1 405 Method Not Allowed"
	elif code =='406':
		return "HTTP/1.1 406 Not Acceptable"
	elif code =='407':
		return "HTTP/1.1 407 Proxy Authentication Required"
	elif code =='408':
		return "HTTP/1.1 408 Request Timeout"
	elif code =='409':
		return "HTTP/1.1 409 Conflict"
	elif code =='410':
		return "HTTP/1.1 410 Gone"
	elif code =='411':
		return "HTTP/1.1 411 Length Required"
	elif code =='412':
		return "HTTP/1.1 412 Precondition Failed"
	elif code =='413':
		return "HTTP/1.1 413 Request Entity Too Large"
	elif code =='414':
		return "HTTP/1.1 414 Request-URI Too Long"
	elif code =='415':
		return "HTTP/1.1 415 Unsupported Media Type"
	elif code =='416':
		return "HTTP/1.1 416 Requested Range Not Satisfiable"
	elif code =='417':
		return "HTTP/1.1 417 Expectation Failed"
	elif code =='500':
		return "HTTP/1.1 500 Internal Server Error"
	elif code =='501':
		return "HTTP/1.1 501 Not Implemented"
	elif code =='502':
		return "HTTP/1.1 502 Bad Gateway"
	elif code =='503':
		return "HTTP/1.1 503 Service Unavailable"
	elif code =='504':
		return "HTTP/1.1 504 Gateway Timeout"
	elif code =='505':
		return "HTTP/1.1 505 HTTP Version Not Supported"

def registerlog(req, reply, ip):
	# Funcao que registra o log em arquivo txt.
	try:
		ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y, %B %d. %H:%M:%S');
		arq = open ("log.txt", "a");
		code = replycode(reply);
		if (len(code)>0):
			arq.write (ts + "\t" + ip + "\t" + req + "\t" + code + "\n")
		arq.close()
	except:
		print "Err0r Log"

def treatdash (s):
	# Funcao que auxilia os registros da cache tirando as barras / 
	# substituindo-as por contrabarras \
	p = s.find('/')
	s = list(s)
	
	while (p != -1):
		s[p]='\\'

		s = "".join(s)
		p = s.find('/')
		s = list(s)

	s = "".join(s)
	return s

def searchcache(filename):
	# Busca um arquivo na cache referente a uma requisicao
	filename = treatdash(filename)
	filename = "cache/" + filename + ".txt"
	try:
		arq = open(filename, 'r')
	except:
		return [-1]

	var = arq.read()
	arq.close()
	return var

def createcache (filename, filecontent):
	# Criacao da cache em arquivo: Um arquivo para cada requisicao do cliente.
	# Os arquivos sao validos enquanto o programa estiver rodando.
	filename = treatdash(filename)
	filename = "cache/" + filename + ".txt"
	try:
		arq = open (filename, 'a')
		arq.write(filecontent)
		arq.close()
	except:
		# print "Erro criando arquivo."
		pass

def proxy (webserver, port, conn, data, addr, in_wl, url, ip):
	# Essa funcao pega os dados da requisicao e liga um socket a porta 80
	# Para receber os dados da Web. Aqui eh onde acontece a maior parte do programa.
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((webserver, port))
		s.send(data)

		while 1:
			reply = s.recv (buffer)
			if (in_wl == 1):	# white listed
				if (len(reply) > 0):
					createcache(url, reply)
					registerlog(url, reply, ip)	
					conn.send(reply)
					pass
				else:
					break
			else:
				achou = False		# flag de deny term
				for term in deny_terms:
					if reply.find(term) > -1:	# analise da resposta
						print term
						achou = True
						break
					if data.find(term) > -1:	# analise da requisicao
						print term
						achou = True
						break;
				if (achou):
					print "Deny term encontrado. Acesso negado!"
					conn.send(accessdenied())	# retorna pag de acesso nao autorizado
					registerlog(url, "401", ip)
					sys.exit(3)
					break;
				else:		# carregar pagina
					if (len(reply) > 0):
						conn.send(reply)	# responder ao cliente
						createcache(url, reply)
						registerlog(url, reply, ip)
						pass
					else:
						break
		s.close()
		conn.close()
	except socket.error, (value, message):
		s.close()
		conn.close()
		sys.exit(1)

def treat_data (conn, data, addr, ip):
	# Funcao que trata os dados na requisicao.
	# Separa a URL, testa black e white lists.
	# Extrai webserver e porta.

	try:
		primeira_linha = data.split ('\n')[0]
		url = primeira_linha.split (' ')[1]
		http_pos = url.find("://")

		if (http_pos != -1):
			url = url [(http_pos+3):]	# pega o resto da url			

		port_pos = url.find(":")
		webserver_pos = url.find ("/")

		if webserver_pos == -1:
			webserver_pos = len(url)
		
		webserver = ""
		port = -1

		if (port_pos == -1 or webserver_pos < port_pos):
			port = 80
			webserver = url[:webserver_pos]
		else:
			port = int ((url[(port_pos+1):])[:webserver_pos-port_pos-1])
			webserver = url [:port_pos]
		

		# print ("Solicitado: " + url + "\n\n")	# mensagem para acompanhar o proxy no terminal.

		# tratando o link para testar blacklist
		temp = url
		aux = temp.find('www.')
		if (aux != -1):
			temp = temp[(aux+4):]

		aux = temp.find('/')
		if (aux!=-1):
			temp = temp[:(aux)]

		in_wl = 0	# flag de liberacao da pag
		# teste blacklist 
		if(temp in bl_sites):
			in_wl = -1
			conn.send(accessdenied())
			registerlog(url, "401", ip)	
		elif(temp in wl_sites):
			in_wl = 1;
			registerlog(url, "202", ip)
		if (in_wl != -1):
			# Se a pagina esta autorizada nesse ponto,
			# devemos conferir se ela esta armazenada em cache.

			var = searchcache(url)
			if var[0] != -1:	# tem na cache
				conn.send(var)
				registerlog(url, var, ip)
			else:				# nao tem na cache
				proxy(webserver, port, conn, data, addr, in_wl, url, ip)
	except Exception, e:
	 	pass

def restrictions():
	# Funcao que extrai do arquivo as restricoes de acesso
	# Armazena-as em um array.
	arq = open ('blacklist.txt', 'r')
	bl = arq.read().split('\n')
	arq.close()
	arq = open ('whitelist.txt', 'r')
	wl = arq.read().split('\n');
	arq.close()
	arq = open ('deny_terms.txt', 'r')
	dnt = arq.read().split('\n');
	arq.close()

	for i in xrange(len(bl)):
		pos = bl[i].find('www.')
		bl[i] = bl[i][(pos+4):]

	for i in xrange(len(wl)):
		pos = wl[i].find('www.')
		wl[i] = wl[i][(pos+4):]
	# print bl
	# print wl
	# print dnt

	return bl, wl, dnt

def main():
	try:
		listening = 12001	# listening port
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# essa linha cria o socket
		s.bind (('', listening))	# essa liga ele a uma porta
		print "Socket ouvindo a porta " + str(listening)
		s.listen(5)		# 5 eh o numero maximo de requisicoes na fila
	except Exception, e:
		print "Porta invalida. Tente outra."
		sys.exit (2)

	while (1):
		try: 
			conn, addr = s.accept()		# aceita uma conexao
			data = conn.recv(buffer) 	# recebe os dados
			ip = socket.gethostbyname(socket.gethostname())
			start_new_thread(treat_data, (conn, data, addr, ip)) # inicia uma thread
		except KeyboardInterrupt:
			# Tratamento de excecao para o socket ser fechado no caso de um Ctrl + C
			s.close()
			sys.exit(1)
	s.close()

(bl_sites, wl_sites, deny_terms) = restrictions()

buffer = 16384

main()
