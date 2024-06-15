import argparse
import platform
import socket
import subprocess


def perform_ping(host: str, payload_size: int, verbose: bool) -> bool:
    system = platform.system()
    tries_flag = '-n' if system == 'Windows' else '-c'
    size_flag = '-l' if system == 'Windows' else '-s'
    no_frag_flag = ['-f'] if system == 'Windows' else ['-M', 'do']

    try:
        ping_command = ['ping', host, tries_flag, '1'] + no_frag_flag + [size_flag, str(payload_size)]
        ping_result = subprocess.run(ping_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        if verbose:
            print(f'Ошибка при выполнении команды ping: {e}')
        return None

    if verbose:
        print(f'Пинг к узлу {host} с размером полезной нагрузки {payload_size}, код возврата={ping_result.returncode}')
    return ping_result.returncode == 0


def resolve_host(host: str) -> bool:
    try:
        socket.gethostbyname(host)
        return True
    except socket.error:
        print(f'Не удалось разрешить имя узла: {host}')
        return False


def is_host_reachable(host: str) -> bool:
    try:
        if subprocess.run(['ping', '-c', '1', host], stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL).returncode != 0:
            print(f'Узел {host} недоступен')
            return False
    except Exception as e:
        print(f'Неожиданная ошибка при первичном пинге: {e}')
        return False
    return True


def discover_mtu(host: str, verbose: bool) -> int:
    lower_bound = 1
    upper_bound = 5000

    while upper_bound - lower_bound > 1:
        mid_point = (lower_bound + upper_bound) // 2
        ping_result = perform_ping(host, mid_point, verbose)
        if ping_result is None:
            print('Неожиданная ошибка при попытке обнаружения MTU')
            return -1
        elif ping_result:
            lower_bound = mid_point
        else:
            upper_bound = mid_point

    total_packet_size = lower_bound + 28  # + заголовок
    print(f'MTU к узлу {host} = {lower_bound} байт, размер пакета с заголовком = {total_packet_size} байт')
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