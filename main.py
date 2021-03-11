#!/usr/bin/env python3
import argparse
import time

from fritzconnection import FritzConnection
import logging

logging.basicConfig(level=logging.WARN)


class Caller:
    def __init__(self, hostname, port, user, passwd):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.name = 'Caller'
        self.hostname = hostname
        self.port = port
        self.user = user
        self.passwd = passwd

    def call(self, number, duration=0):
        self.logger.info('Calling ' + number)

        my_fritz_connection = FritzConnection(self.hostname, self.port, self.user, self.passwd)

        # Todo: what about service discovery first?
        my_fritz_connection.call_action('X_VoIP1', 'X_AVM-DE_DialNumber', arguments={'NewX_AVM-DE_PhoneNumber': number})

        # Todo: maybe this should be a separate function?
        if duration > 0:
            time.sleep(duration)
            my_fritz_connection.call_action('X_VoIP1', 'X_AVM-DE_DialHangup')

        return True


def main():
    argument_parser = argparse.ArgumentParser(description='FritzBell')
    argument_parser.add_argument('--hostname', required=False, help='Hostname of your Fritz!Box (default: fritz.box)')
    argument_parser.add_argument('--port', required=False, help='TR064 port of your Fritz!Box (default: 49000)')
    argument_parser.add_argument('--user', required=True, help='Fritz!Box user name')
    argument_parser.add_argument('--passwd', required=True, help='Fritz!Box user\'s password')
    argument_parser.add_argument(
        '--number',
        required=True,
        help='Number to be called, e.g., \'**9\' for broadcast call (every connected phone).'
    )
    argument_parser.add_argument(
        '--duration',
        required=False,
        help='Duration of the call (default: 0, i.e., just call and don\'t hangup).'
    )
    args = argument_parser.parse_args()

    # Handle optional arguments
    hostname = 'fritz.box'
    if args.hostname:
        hostname = args.hostname
    port = 49000
    if args.port:
        port = args.port
    duration = 0
    if args.duration:
        duration = args.duration

    # Do the call
    my_caller = Caller(hostname, port, args.user, args.passwd)
    my_caller.call(args.number, duration)


if __name__ == '__main__':
    main()
