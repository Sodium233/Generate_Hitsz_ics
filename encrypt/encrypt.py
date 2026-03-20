import execjs

with open("./encrypt/encrypt.js", "r", encoding="utf-8") as f:
    js_code = f.read()

ctx = execjs.compile(js_code)

def encrypt_password(password: str, salt: str) -> str:
    return ctx.call("encryptPassword", password, salt)