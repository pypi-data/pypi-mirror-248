import argparse
from bigsansar.core.init import deploy, initsetup


class root:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('init', help='Create a django server and related files ')
        self.parser.add_argument('init server', help=' this is a base in to linux ubuntu. careate a server in to deploy side . ')

        self.args = self.parser.parse_args()

    def execute(self):

        if self.args.init == 'init':

            return initsetup()
        
        elif self.args.init.server == 'init server':
            return deploy()
    
        else:
            print('usage: bigsansar --help')
            exit()

def main():
   cli = root()
   cli.execute()
