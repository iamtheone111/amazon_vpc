## Usage instructions

### Install dependencies
```
pip3 install -r requirements.txt
```

### Run script

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

If you do not want to edit route tables add this param. Default will be edit.
```
--no_modify_route_table
```
If you do not want to edit security groups add this param. Default will be edit.
```
--no_modify_security_group
```

### Run with docker
Build inside directory with source

```
docker build . -t amazon_vpc_script 
```

Run
```
docker run --rm  -it -v <path_src_dir>:/app --name amazon_vpc_script amazon_vpc_script \
python3 /app/vpcaws.py \
--client_network=<specific_ippool> \
--main_vpc_id=vpc-<main_VpcId> \
--region_name=<region_name> \
--aws_access_key_id=<aws_access_key_id> \
--aws_secret_access_key=<aws_secret_access_key>
```

<path_src_dir> : for Linux $(PWD) or ${pwd}, for Windows $(PWD)/${pwd} or you must
write full path. It depends how docker mapped the folder.
