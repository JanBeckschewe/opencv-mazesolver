import threading

import ws_server

threading.Thread(target=ws_server.continually_append_random_turn()).start()
