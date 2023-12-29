from argparse import ArgumentParser
from wiliot_deployment_tools.gw_certificate.gw_certificate import GWCertificate

def main():
    parser = ArgumentParser(prog='wlt-gw-certificate',
                            description='Gateway Certificate - CLI Tool to test Wiliot GWs')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-owner', type=str, help="Owner ID", required=True)
    required.add_argument('-gw', type=str, help="Gateway ID", required=True)
    
    args = parser.parse_args()
    gwc = GWCertificate(gw_id=args.gw, owner_id=args.owner)
    gwc.run_tests()
    
def main_cli():
    main()

if __name__ == '__main__':
    main()
