from dotenv import load_dotenv, find_dotenv
import os, base64, bcrypt

load_dotenv(find_dotenv())

KEY = os.getenv('KEY').encode('utf-8')

def encrypt(pssw: str):
    return base64.b64encode(bcrypt.hashpw(pssw.encode('utf-8'), KEY)) # Should have a better incryption method ;-;

def checkHash(check: str, hash: str):
    return bcrypt.checkpw(check.encode('utf-8'), base64.b64decode(hash))