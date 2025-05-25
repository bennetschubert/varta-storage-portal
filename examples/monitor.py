from vartaclient import VartaStorageClient
from pprint import pp

IP_ADDRESS = "192.168.2.71"

def main():
    client = VartaStorageClient(IP_ADDRESS)
    ems_data = client.get_ems_data()
    pp(ems_data)

if __name__ == '__main__':
    main()
