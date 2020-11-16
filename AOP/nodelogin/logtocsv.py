import json


# {'level': 'info', 'timeStamp': '11/15/2020, 11:13:36 PM', 'ip': '192.168.189.1', 'message': 'User << test >> tried a clear authentication'}

with open("output.csv", "w") as fd:
    fd.write("Level,timeStamp,IP,message\n")

with open("JuiceShop.log", "r") as fd:
    content = fd.readlines()
content = [x.strip() for x in content]
with open("output.csv", "a") as fd:
    for x in content:
        x = json.loads(x)
        fd.write(f"{x['level']},{x['timeStamp']},{x['ip']},{x['message']}\n")
