import sys

from qrcode.console_scripts import main as qr

from HiddenBackup.ConfigLoader import Config
from HiddenBackup.HiddenService import HiddenService
from HiddenBackup.LogWriter import Logger


class DisplayQR:
    def __init__(self):
        self._log = Logger()
        self._hs = HiddenService(self._log)
        self._config = Config()

    def display(self):
        # Start hidden services
        if not self._hs.connect(self._config.server_password()):
            print ("Unable to connect to Tor server")
            self._log.close()
            sys.exit(1)

        # Setup paths
        data_dir = self._hs.get_data_dir()
        hostname_path = data_dir + "/hostname"

        # Read hostname
        try:
            with open(hostname_path, 'r') as hostname:
                host = hostname.read().replace('\n', '')
        except IOError:
            print("No such file or directory: %s" % hostname_path)
            sys.exit(1)

        qr(host)