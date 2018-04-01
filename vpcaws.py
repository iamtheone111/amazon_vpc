import boto3
import argparse
import asyncio

class ErrCantConnect(Exception):
    pass

class VpcManager:
    def __init__(self, *,
                 region_name,
                 aws_access_key_id,
                 aws_secret_access_key):
        self.connect_param= dict(region_name = region_name,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key = aws_secret_access_key
                                 )

    async def connect(self):
        try:
            self.ec2 = boto3.resource('ec2', **self.connect_param)
        except Exception as err:
            raise ErrCantConnect(err)

    async def create_vpc(self, *, network):
        self.client_vpc = self.ec2.create_vpc(CidrBlock=network)
        print(self.client_vpc)
        self.subnet = self.client_vpc.create_subnet(CidrBlock=network)
        print(self.subnet)
        self.client_vpc.wait_until_available()

        self.gateway = self.ec2.create_internet_gateway()
        print(self.gateway)
        self.gateway.attach_to_vpc(VpcId = self.client_vpc.id)

    async def connect_vpc_to_main(self, *, vpcid):
        self.ec2.create_vpc_peering_connection(DryRun=False, VpcId=vpcid, PeerVpcId=self.client_vpc.id)

    async def modify_security_group(self):
        groups = self.ec2.describe_security_groups()
        for item in groups:
            print(item)





if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    parser = argparse.ArgumentParser()
    parser.add_argument("--client_network", help="Client network specific", required=True)
    parser.add_argument("--main_vpc_id", help="Main VPC id", required=True)

    parser.add_argument("--region_name", help="Region Name", required=True)
    parser.add_argument("--aws_access_key_id", help="AWS access key Id", required=True)
    parser.add_argument("--aws_secret_access_key", help="AWS secret access key", required=True)


    args = parser.parse_args()

    vpcManager = VpcManager(region_name = args.region_name,
                            aws_access_key_id = args.aws_access_key_id,
                            aws_secret_access_key=args.aws_secret_access_key)
    loop.run_until_complete(vpcManager.connect())
    loop.run_until_complete(vpcManager.create_vpc(network=args.client_network))
    #loop.run_until_complete(vpcManager.connect_vpc_to_main(vpcid=args.main_vpc_id))
    loop.run_until_complete(vpcManager.modify_security_group())
    loop.close()




