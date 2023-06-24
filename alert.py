# Standard Library Imports
import os
import configparser
import logging
# External Library
import vonage

class alertProccess():
    def __init__(self, website) -> None:
        logging.info(f"{website} has triggered an alert!")
        config_file = configparser.ConfigParser()
        if os.path.isfile("config.ini"):
            logging.info("Config.ini exists")
            
        else: 
            logging.info('Process to create config file started')
            alertProccess.create_config(self, config_file)
            logging.info("config.ini file has been created")
            
        
        config_file.read("config.ini")
        key = config_file.get('Vonage API', 'key')
        secret = config_file.get('Vonage API', 'secret')
        client = vonage.Client(key=key, secret=secret)
        sms = vonage.Sms(client)
        alertProccess.send_message(self, config_file, sms, website)
        
    def send_message(self, config_file, sms, website):
        logging.info("Message being sent")
        responseData = sms.send_message(
            {
                "from": "Dr Passmore",
                "to": f"{config_file.get('Vonage API', 'countrycode')}{config_file.get('Vonage API', 'phonenumber')}",
                "text": f"{website} in stock!"
                
            }
            
        )
        
        
    def create_config(self, config_file):
        # ADD SECTION
        config_file.add_section("Vonage API")

        key = input("Please input API key: ")
        secret = input("Please input API secret: ")
        country = input("Please input country code - UK for example is 44: ")
        phonenumber = input("Please input phone number for text (remove the starting 0): ")
        
        # ADD SETTINGS TO SECTION
        config_file.set("Vonage API", "key", key)
        config_file.set("Vonage API", "secret", secret)
        config_file.set("Vonage API", "countrycode", country)
        config_file.set("Vonage API", "phonenumber", phonenumber)
        
        alertProccess.save_config(self, config_file)
    
    
    def save_config(self, config_file):
        
        with open(r"config.ini", 'w') as configfileObj:
            config_file.write(configfileObj)
            configfileObj.flush()
            configfileObj.close()
        
# Logging
logging.basicConfig(filename='checkforchange.log', 
                    filemode='a', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')