import uuid


WRAPPER_HEAD = "950f7f7ba7c111eea5c4ff9ca9F3fcfd"
# WRAPPER_HEAD = "950f7f7b"
WRAPPER_HEAD_LENGTH = len(WRAPPER_HEAD)
CALLBACK_ID_LENGTH = 32


class PayloadWrapper:
    def __init__(self):
        self.binary_wrapper = BinaryWrapper(self.agent_uuid)
        self.text_wrapper = TextWrapper(self.agent_uuid)
        self.__callbacks = {}
        

    def _get_payload_wrapper(self, payload):
        if not payload or isinstance(payload, str):
            return self.text_wrapper.wrap(payload)
        elif isinstance(payload, bytes) or isinstance(payload, bytearray):
            return self.binary_wrapper.wrap(payload)
        else:
            return None


    def unpack(self, payload):
        wrapper = self._get_payload_wrapper(payload)
        if wrapper:
            payload1, callback_func = wrapper.unpack(payload)
            callback_id = str(uuid.uuid1()).replace('-', '')
            payload1 = wrapper.wrap(payload, callback_id)
            self.__callbacks[callback_id] = topic_callback

        
        
    def wrap(self, payload, topic_wait=None, topic_callback=None):
        if not (topic_wait and topic_callback):
            return payload
                    
        payload1 = payload
        wrapper = self._get_payload_wrapper(payload)
        if wrapper:
            callback_id = str(uuid.uuid1()).replace('-', '')
            payload1 = wrapper.wrap(payload, callback_id)
            self.__callbacks[callback_id] = topic_callback

        return payload1
        
        

class BinaryWrapper:
    def __init__(self, agent_uuid:str):
        self.agent_uuid = agent_uuid.encode('ascii')        
        
        
    def wrap(self, payload, callback_id):
        pass
        

            
class TextWrapper:
    def __init__(self):
        pass
        
        
    def unpack(self, payload) -> (str, str):
        if not payload:
            return payload, None
        
        if payload.startswith(WRAPPER_HEAD):
            content_index = WRAPPER_HEAD_LENGTH + CALLBACK_ID_LENGTH
            callback_id = payload[WRAPPER_HEAD_LENGTH, content_index]
            return payload[content_index], callback_id
        else:
            return payload, None
                
        
    def wrap(self, payload, callback_id) -> str:
        if payload:
            return f"{WRAPPER_HEAD}{callback_id}{payload}"
        else:
            return f"{WRAPPER_HEAD}{callback_id}"
