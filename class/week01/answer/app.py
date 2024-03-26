## import a python library for working with the OS
import os
## import a specific defined function from the dotenv python library
from dotenv import load_dotenv


#load the environment file
load_dotenv(".env", override=True)

## get the secret from the environment variables
secret = os.environ["MY_SECRET"]

## print a line of text with that secret to standard out
print(f"That's my secret, Cap: {secret}")