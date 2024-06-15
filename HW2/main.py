import argparse
import logging
import platform
import socket
import subprocess
import time
import traceback

IP_HEADER_SIZE = 20
ICMP_HEADER_SIZE = 8


def perform_ping(host: str, payload_size: int, verbose: bool) -> bool:
    system = platform.system().lower()
    tries_flag = '-n' if system == 'windows' else '-c'
    size_flag = '-l' if system == 'windows' else '-s'
    no_frag_flag = ['-f'] if system == 'windows' else ['-M', 'do']

    try:
        ping_command = ['ping', host, tries_flag, '1'] + no_frag_flag + [size_flag, str(payload_size)]
        ping_result = subprocess.run(ping_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        return None

    if verbose:
        print(f'Ping host# {host} with payload_size# {payload_size}, returncode={ping_result.returncode}')
    return ping_result.returncode == 0


def resolve_host(host: str) -> bool:
    try:
        socket.gethostbyname(host)
        return True
    except socket.error:
        print(f'Host name {host} cannot be resolved')
        return False


def is_host_reachable(host: str) -> bool:
    try:
        if subprocess.run(['ping', '-c', '1', host], stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL).returncode != 0:
            print(f'Host {host} is unreachable')
            return False
    except Exception as e:
        print('Unexpected exception raised while initial ping')
        logging.error(traceback.format_exc())
        return False
    return True


def discover_mtu(host: str, verbose: bool) -> int:
    lower_bound = 1
    upper_bound = 2000

    while upper_bound - lower_bound > 1:
        mid_point = (lower_bound + upper_bound) // 2
        ping_result = perform_ping(host, mid_point, verbose)
        if ping_result is None:
            print('Unexpected exception raised while trying to discover MTU')
            logging.error(traceback.format_exc())
            return -1
        elif ping_result:
            lower_bound = mid_point
            time.sleep(0.5)
        else:
            upper_bound = mid_point

    total_packet_size = lower_bound + IP_HEADER_SIZE + ICMP_HEADER_SIZE
    print(f'MTU to host# {host} = {lower_bound} bytes, packet size with headers = {total_packet_size} bytes')
    return lower_bound


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    parser.add_argument('-v', '--verbose', help='Вывести полную информацию о каждом пинге', action='store_true')
    return parser.parse_args()


def main():
    args = parse_arguments()
    host = args.host
    verbose = args.verbose

    if not resolve_host(host):
        return 1

    if not is_host_reachable(host):
        return 1

    if discover_mtu(host, verbose) == -1:
        return 1

    return 0


if __name__ == '__main__':
    main()
