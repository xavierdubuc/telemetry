import argparse


class Command(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_argument("ip", help="Ip address")
        self.add_argument("--log-level", help="Log level", dest='log_level', default='info')

