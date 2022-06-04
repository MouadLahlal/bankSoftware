import protocolloServer

server = protocolloServer.Server('192.168.1.87', 7777)

print(server.receive())
server.send("ciao", "p")
print(server.receive())
server.send("dhsfgskv jfdj nvcmcvcm jkj xcm", "p")
print(server.receive())
server.send("ciao", "p")