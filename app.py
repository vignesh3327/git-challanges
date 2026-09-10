import boto3
from botocore.exceptions import ClientError

# Initialize EC2 resource
ec2 = boto3.resource('ec2', region_name='us-east-1')

def create_instance():
    try:
        print("Launching EC2 instance...")
        instances = ec2.create_instances(
            ImageId='ami-0c7217cdde317cfec',  # Replace with a valid AMI ID for your region (e.g., Ubuntu or Amazon Linux 2023)
            InstanceType='t2.medium',
            MinCount=1,
            MaxCount=1,
            KeyName='your-key-pair-name',     # Replace with your EC2 Key Pair name
            # SubnetId='subnet-xxxxxxxx',     # Optional: specify subnet
            # SecurityGroupIds=['sg-xxxxxx'], # Optional: specify security group
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'DevOps-Practice-Instance'},
                        {'Key': 'Environment', 'Value': 'Dev'}
                    ]
                }
            ]
        )

        instance = instances[0]
        print(f"Instance requested. Instance ID: {instance.id}")
        
        # Wait until the instance is running
        print("Waiting for instance to enter 'running' state...")
        instance.wait_until_running()
        
        # Reload attributes to fetch public IP/DNS
        instance.reload()
        print(f"Instance is running! Public IP: {instance.public_ip_address}")
        
    except ClientError as e:
        print(f"Failed to create EC2 instance: {e}")

if __name__ == "__main__":
    create_instance()
