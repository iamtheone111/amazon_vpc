### Usage example

Install dependents
```
pip3 install -r requirements.txt
```

Run script

```

python3 vpcaws.py \
--client_network=<specific_ippool> \
--main_vpc_id=vpc-<main_VpcId> \
--region_name=<region_name> \
--aws_access_key_id=<aws_access_key_id> \
--aws_secret_access_key=<aws_secret_access_key>

```

Example:
```
python3 vpcaws.py \
--client_network=10.0.0.0/24 \
--main_vpc_id=vpc-f2c45097 \
--region_name=eu-central-1 \
--aws_access_key_id=BKIAJ2QRZBHJYT2K3NDVS \
--aws_secret_access_key=GuEYgTlQrTRZdxpkEHIC92ydsGf0Sans9Sjf3CaD
```