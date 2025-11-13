from fastapi import FastAPI, Request
import json
from pydantic import BaseModel
import time

app=FastAPI()




@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    with open("endpoints_data.json", "r", encoding="utf-8") as f:
        try:
            until_now=json.load(f)
        except:
            until_now=[]
    with open("endpoints_data.json", "w", encoding="utf-8") as f:
        until_now.append({"time":process_time})
        json.dump(until_now, f, ensure_ascii=False, indent=4)
    return response




abc=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
@app.get("/test")
def hi_test():
    return  { "msg":"hi from test"}

@app.get("/test/name{name}")
def save_user(name):
    with open("names.txt", "a", encoding="utf-8") as f:
        json.dump(name, f, ensure_ascii=False, indent=4)
    return  { "msg":"saved user"}

class Caesar(BaseModel):
    text : str
    offset : int
    mode : str

@app.post('/caesar')    
def caesar_cipher_endpoint(body: Caesar):
    print(body)
    key_word=body.offset
    if body.mode=="encrypt":
        encrypted_text=""
        for char in body.text:
            for i in range(len(abc)):
                if char==abc[i]:
                    if len(abc)>i+key_word-1:
                        encrypted_text+=abc[i+key_word]
                    else:
                        encrypted_text+=abc[(len(abc)-i)]
        return {"encrypted_text":encrypted_text}
    else:
        decrypted_text=""
        for char in body.text:
            for i in range(len(abc)):
                if char==abc[i]:
                    if 0<i-key_word:
                        decrypted_text+=abc[i-2]
                    else:
                        decrypted_text+=abc[i-key_word]
        return {"decrypted_text":decrypted_text}



@app.get('/fence/encrypt')
def fence_cipher_endpoints(text):
    encript1=""
    encript2=""
    for i in range(len(text)):
        if i%2==0:
            encript1+=text[i]
        else:
            encript2+=text[i]
    return encript1+encript2
class Urli(BaseModel):
    text:str
    offset : int #location of first num%2==0

@app.post('/fence/decrypt')
def  fence_decrypt(body : Urli):
    not_solved=body.text
    middle=body.offset
    solved=""
    if len(not_solved)%2==0:
        for i in range(len(not_solved)//2):
            solved+=not_solved[i]
            solved+=not_solved[middle+i]
    else:
        for i in range(len(not_solved)//2):
            solved+=not_solved[i]
            solved+=not_solved[middle+i]
        solved+=not_solved[middle-1]
    return {"decrypted": solved }
    


        


