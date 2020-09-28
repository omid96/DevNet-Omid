import paramiko
import telnetlib
import time
import re


devices = [
    { "HOST":"192.168.56.3", "PORT":5000 ,"hostname": "R1#"},
    { "HOST":"192.168.56.3", "PORT":5001 ,"hostname": "R2#"}
]


def read_terminal(telnet_connection, hostname):
	time.sleep(5)
	return telnet_connection.read_very_eager().decode('utf-8')


def write_terminal(telnet_connection, string):
	telnet_connection.write(bytes(string, 'utf-8'))


def connect(host,port):
	return telnetlib.Telnet(host,port)


def terminal_prepare(telnet_connection):
	write_terminal(telnet_connection,"\r\n")
	write_terminal(telnet_connection,"terminal length 512 \r\n")
	write_terminal(telnet_connection,"terminal width 512 \r\n")
	write_terminal(telnet_connection,"\r\n")


if __name__ == "__main__":

    for device in devices:

        print("-" * 20, device['hostname'].split('#')[0], "-" * 20)
        telnet_connection = connect(device["HOST"], device["PORT"])
        terminal_prepare(telnet_connection)

        write_terminal(telnet_connection, "show archive config difference \r\n")
        output = read_terminal(telnet_connection, device["hostname"])

        match_object = re.search(r'No changes were found', output, re.DOTALL)
        if not match_object:
            prompt = input("Config need to be saved. Do you want to save it? (y,n): ")
            if prompt.lower() in ['y', 'yes']:
                write_terminal(telnet_connection, "wr \r\n")
                print("Config saved!!!")
            else:
                print("Skip saving config")
        else:
            print("There are no new changes in config")

        telnet_connection.close()

    exit()