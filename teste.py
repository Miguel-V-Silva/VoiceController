import hid

for d in hid.enumerate():
    if "Redragon" in d["manufacturer_string"] if d["manufacturer_string"] else False:
        print(d)
    else:
        print("Dispositivo não encontrado.")