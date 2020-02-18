from Crypto.Cipher import AES
import base64
import json
import re

mystr = '''Wp8Ao/2IW7xiIhmbqv8oz85AsLUdsj71jgnRFru36ltapBjgIQl+hwpVvKI0CDmtHGYyj9yHSDbbM/O1t/H8RJCXBX7lsaa0QLpwPr1w
+2PsF26m/9xM+Xy4Lfuv9KzjD9QxvONpRy1Bned76C0C+KHdPfZQHQzx51C1wkkXSdTvYmInGmTD/vcZ0R0/Wo8knYiADDJozCsr0N5pq/HRAxdmck+v
/jUyn1+6SvM0WO4CdHnyaRQ1P200cUwDBsu6dvbkGDxsNXFHwJRHwH0cGLEy5w/LcCjLWoeeYPM+XSfb+ZclgwV
+R661qznOjenLu6SAfra0vFQKNbHPkywxTQuqo3AgdlIBMPGQrvbUXX9Z+/2D53PBLrL0h4kYgDpfzG4lWVo3912+/XBHK/Mz1H6+LQI7
+uk6YRTDLSJfxg57CzUIiY5x1WRmWnfr5KW1yQn1MJCLt17YRWfilYWK7HQIwJOicOX1nO9ROuTfuK+JAue9XhfDew7j95/4IncjTj
/lowA0NFdSIZdYxMEXeWbFs88Gcd6XODE+YqGHtnEg4uJQNuU/+rNjVAafiDovRnmnDqJva6c3
+MGRQomxasE1osOsMZbus7wEqdhndrDEEazH8A2f9OxHyjNKuIReUlHBM60of2rXIdBsUMC/1mFbYOAnymIn6
+UQmxOgNntH9EdT6hxAkz75jVZuuCJSOyL74e8J7lqg9oJ9p4GANMF0xTXh8Bv2dAFRRG1VguyjvNBh7u
/NpaQxvsGfCvK84YfXLTaul3ilJvPtVSrpXOrU+ptJvWDob0RTePTH57B4Vvx2CGMLJg6XO8/7NqWc4Rz+a4O70YxfZlU0nJ3jVrdQsGIdHAlzt
+9EP4PZcZYc921je7fvP9NHg/2ZfOq+sMp0+kYU2+I/9b6ZkDflrkM21OlD+hubHK
/aa7Kfx4M4o89WrkZlw1xk4hU4yBvB0wtSsut4EpZEFywQMn4v3HBmEhRD3oGPtZt6Du8/GiDAiBucfj4yW6YYSng+LoxaT5tam7qwHma
/2h1YIBj6JUCzx4Rgk/jxvghm6vb19UfhnZwWDnkWcc/to71cteUyVfnXlfzVCUGdzyzGC
/aUDFZmw2rWlsI91jZz3v3SbIrmjPoMLBy1q0MabhArR80c1Nuyvqz+Y+F2b6YFKrKfEUOitO5dvBooNfz
+HzJVLLGSWCrmR74rq8b38hDaLiBTEfZqrQGIFPDzb8ND3m6Yu/AUGCGVke8XqpRE03IuE/cKvUkrrTJ6cf9TKDK8JA3y97Baly3gvS
+O7a5X286uwYUv1LSMpeQt8QX4zqEpP6VXVX0zWofWXYdQusVkVV42I0bpIhyYzCvW2/ALUfTQPMh9XLCnLb9xmhQOZXyZU2k= '''

key = '123456781234567G'
iv = 'ABCDEF1G34123412'


def add_to_16(s):
    while len(s) % 16 != 0:
        s += (16 - len(s) % 16) * chr(16 - len(s) % 16)
    return str.encode(s)  # 返回bytes


def get_secret_url(text, mykey=key, myiv=iv):
    aes = AES.new(mykey, mode=AES.MODE_CBC, IV=myiv)
    text = base64.b64decode(text)
    result = aes.decrypt(text)
    result = result.decode('utf-8')
    ret = re.match(r"^\[.*\]", result)
    result = ret.group()
    # result = result.rstrip(' ')

    js = json.loads(result,encoding='utf-8')
    # encrypted_text = str(base64.encodebytes(aes.decrypt(add_to_16(text))), encoding='utf8').replace('\n', '')  # 加密
    # encrypted_text = str(base64.encodebytes(aes.encrypt(add_to_16(text))), encoding='utf8').replace('\n', '')  # 加密
    # encrypted_text = encrypted_text.replace('/', "^")  # ddd.replace(/\//g, "^")
    # return encrypted_text[:-2]
    return js





if __name__ == '__main__':
    print(get_secret_url(mystr, key, iv))
