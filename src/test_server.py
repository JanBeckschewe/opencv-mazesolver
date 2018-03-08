import threading

import server

threading.Thread(target=server.continually_append_random_turn()).start()
