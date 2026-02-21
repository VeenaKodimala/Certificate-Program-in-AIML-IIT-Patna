#First we will install "dotenv" package using pip from python. This package 
# is used the read the configs present in .env file.

from dotenv import load_dotenv
#The below import will help us to interact with the operating sys.
import os
#We need to have a ".env" file in our folder and not "name.env"

#the bwlow method will load all the configs from .env file and 
# make them system env variables. 
load_dotenv()
# Now we interact with the os whether will have the needed key or not(since we are 
# temporarily loading the keys as system variables.)
print("API_KEY:::: ",os.getenv("API_KEY"))

a =40


