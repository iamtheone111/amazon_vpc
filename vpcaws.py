import boto3
import argparse
import asyncio

class ErrCantConnect(Exception):
    pass

class VpcManager:
    def __init__(self):
        pass

    async def connect(self):
        try:
            self.ec2 = boto3.resource('ec2')
        except Exception as err:
            raise ErrCantConnect(err)

    async def create_vpc(self, *, network):
        self.client_vpc = self.ec2.create_vpc(CidrBlock=network)

        self.subnet = self.client_vpc.create_subnet(CidrBlock=network)
        self.client_vpc.wait_until_available()

        self.gateway = self.ec2.create_internet_gateway()
        self.gateway.attach_to_vpc(VpcId = self.client_vpc.id)

    async def connect_vpc_to_main(self, *, vpcid):
        self.ec2.create_vpc_peering_connection(DryRun=False, VpcId=vpcid, PeerVpcId=self.client_vpc.id)

    async def assing_acl(self):
        pass
        #self.ec2.create_vpc_peering_connection(DryRun=False, VpcId=vpcid, PeerVpcId=self.client_vpc.id)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    parser = argparse.ArgumentParser()
    parser.add_argument("--client_network", help="Client network specific", required=True)
    parser.add_argument("--main_vpc_id", help="Main VPC id", required=True)
    args = parser.parse_args()

    vpcManager = VpcManager()
    loop.run_until_complete(vpcManager.connect())
    loop.run_until_complete(vpcManager.create_vpc(network=args.client_network))
    loop.run_until_complete(vpcManager.connect_vpc_to_main(vpcid=args.main_vpc_id))
    #loop.run_until_complete(vpcManager.assing_acl())
    loop.close()




