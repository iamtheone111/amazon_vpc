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
        self.VpcId = None

    async def connect(self):
        try:
            self.cleint_ec2 = boto3.client('ec2', **self.connect_param)
            self.resource_ec2 = boto3.resource('ec2', **self.connect_param)
        except Exception as err:
            raise ErrCantConnect(err)

    async def create_vpc(self, *, network):
        client_vpc = self.cleint_ec2.create_vpc(CidrBlock=network)
        self.VpcId = client_vpc['Vpc']['VpcId']
        print(f"New VPC is created: {self.VpcId}")

        # From task I am not get nned to create subnets or not...
        #self.subnet = self.ec2.create_subnet(CidrBlock=network, VpcId=self.VpcId)
        #self.gateway.attach_to_vpc(VpcId = self.client_vpc.id)

    async def connect_vpc_to_main(self, *, vpcid):
        vpcconnect = self.cleint_ec2.create_vpc_peering_connection(DryRun=False, VpcId=vpcid, PeerVpcId=self.VpcId)
        connID = vpcconnect["VpcPeeringConnection"]["VpcPeeringConnectionId"]
        print(f"New VPC Connection is crated: {connID}")

    async def create_security_group(self, vpcid):
        #Try to do isolation by group id.
        #main_desc_group = self.cleint_ec2.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpcid]}])
        #mainGroupId = main_desc_group['SecurityGroups'][0]['GroupId']

        mainVpc = self.resource_ec2.Vpc(vpcid)

        new_desc_group = self.cleint_ec2.describe_security_groups(Filters=[{'Name':'vpc-id','Values': [self.VpcId]}])
        newGroupId = new_desc_group['SecurityGroups'][0]['GroupId']
        ec2SecurityGroup = self.resource_ec2.SecurityGroup(newGroupId)
        ec2SecurityGroup.revoke_egress(IpPermissions=[{"IpRanges":[{"CidrIp":"0.0.0.0/0"}],
                                                       "IpProtocol":"-1"}])
        ec2SecurityGroup.authorize_egress(IpPermissions=[{"IpRanges":[{"CidrIp":mainVpc.cidr_block}],
                                                       "IpProtocol":"-1"}])


        # :( but it didnt work error "You have specified two resources that belong to different networks."
        # so to do that i using CidrIp
        #ec2SecurityGroup.authorize_egress(IpPermissions=[{"UserIdGroupPairs":[{"GroupId":mainGroupId}],
        #                                               "IpProtocol":"-1"}])



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
    loop.run_until_complete(vpcManager.connect_vpc_to_main(vpcid=args.main_vpc_id))
    loop.run_until_complete(vpcManager.create_security_group(vpcid=args.main_vpc_id))
    loop.close()




