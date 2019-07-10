import paramiko
import platform
import argparse

parser = argparse.ArgumentParser(description="Sends torrent magnet link to server running deluge daemon")
# parser.add_argument('password', metavar='P', type=int, nargs=1, help='The password for user in ssh')
parser.add_argument('username', help='The username to use when ssh\'ing into the deluge client', type=str)
parser.add_argument('password', help='The password to use when ssh\'ing into the deluge client', type=str)
parser.add_argument('hostname', help='The hostname (ip) of the deluge client', type=str)
parser.add_argument('-m', dest='magnet', help='The magnet link to add to torrent.', type=str)
args = parser.parse_args()

is_ios = platform.machine().startswith('iP')

if is_ios:
    import appex
    args.magnet = appex.get_text()
else:
    if not args.magnet:
        raise Exception('-m argument is required when running outside of iOS')

if not args.magnet.startswith('magnet'):
    raise Exception('Expecting magnet link but got: %s' % (args.magnet))
    exit(1)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=args.hostname, username=args.username,
    password=args.password)
deluge_command = "deluge-console add %s" % (args.magnet)
# deluge_command = "deluge-console info"
stdin, stdout, stderr = client.exec_command(deluge_command)
print(stdout.read())
