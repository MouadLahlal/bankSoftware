import protocolloClient

client = protocolloClient.Client('192.168.1.87', 7777)

client.send("ciao", "p")
print(client.receive())
client.send("ciao", "p")
print(client.receive())
client.send("ciao", "p")
print(client.receive())