
import requests
import json
import brotli

import logs
import logging

logger = logging.getLogger(logs.LOG_NAME)


class RequestResponseInterpreter:


    def __init__(self, show_logs: bool = True) -> None:
        self.logger = logs.LogController(show_logs)
        self.logger.log_debug("Starting Parser...")



    def handle_response(self, request_response: requests.Response) -> dict:
        
        self.logger.log_debug("Handling with response parse...")

        request_response_text = request_response

        if request_response.headers.get('Content-Encoding') == 'br':
            request_response_text = self.brotli_parse(request_response)

        return self.json_parse(request_response_text)    
    

    def json_parse(self, respose_text) -> dict:
        self.logger.log_debug("JSON decode started....")        


        if type(respose_text) == type(""):
            self.logger.log_info("Trying to parse response type equal str...")
            return self._try_json_loads(respose_text)
            
        elif isinstance(respose_text, requests.models.Response):
            self.logger.log_info("Trying to parse response type equal requests.models.Response...")
            return self._try_json_loads(respose_text.text) 

        else:
            self.logger.log_info(f"None of parsement available match to {type(respose_text)}...")
            return respose_text
        

    def _try_json_loads(self, respose_text):

        
        try:
            return json.loads(respose_text)
        except (json.JSONDecodeError, json.decoder.JSONDecodeError) as jde:
            self.logger.log_info(f"Error ({jde}) to decode response ({respose_text}) of type ({type(respose_text)}) into JSON ....")
            return {}
        except TypeError as te:
            self.logger.log_info(f"Error ({te}) to decode response ({respose_text}) of type ({type(respose_text)}) into JSON ....")
            return {}   

    def brotli_parse(self, request_response: requests.Response) -> str:
        self.logger.log_debug("Brotli decompression started....")

        try:
            decompressed_content = brotli.decompress(request_response.content)
            return decompressed_content.decode('utf-8')
        except brotli.error:
            self.logger.log_debug("Brotli decompression failed....")
            return request_response.text