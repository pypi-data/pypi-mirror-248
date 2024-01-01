import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import logging
import multiprocessing
import signal

import Helper
from src.holon import AbdiConfig
from src.holon.HolonicAgent import HolonicAgent

from src.holon.HolonicAgent import HolonicAgent
# from visual.Visual import Visual
from hearing import Hearing
# from voice.Voice import Voice
from navi import Navigator
# from dialog import DialogSystem
import guide_config
from hearing.trans import Transcriptionist


if __name__ == '__main__':
    # Helper.init_logging()
    # logging.info('***** Main start *****')
    print('***** RunTrans start *****')

    def signal_handler(signal, frame):
        print("signal_handler")
    signal.signal(signal.SIGINT, signal_handler)

    cfg = AbdiConfig()
    cfg.mqtt_address = guide_config.mqtt_address
    cfg.mqtt_port = guide_config.mqtt_port
    cfg.mqtt_keepalive = guide_config.mqtt_keepalive
    cfg.mqtt_username = guide_config.mqtt_username
    cfg.mqtt_password = guide_config.mqtt_password
    cfg.log_level = guide_config.log_level
    cfg.log_dir = guide_config.log_dir    
    os.environ["OPENAI_API_KEY"] = guide_config.openai_api_key

    Helper.init_logging(log_dir='tests/guide/_log', log_level=logging.DEBUG)
    multiprocessing.set_start_method('spawn')

    a = Transcriptionist(cfg)
    a.start()
    # a.test()

    # time.sleep(5)
    # a.terminate()
