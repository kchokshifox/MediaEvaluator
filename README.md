Author: Kushal Chokshi
Description: SERVERLESS MEDIAINFO - Serverless MediaInfo utilizing the AWS Lambda Function to analyze media from the S3 bucket.

Prepare the environment to build the package


Deploy the EC2 instance

1.	Login to the AWS Management Console
2.	Select the EC2 Service
3.	Click on “Launch Instance”
4.	Select the “Amazon Linux AMI 2018.03.0 (HVM), SSD Volume Type - ami-0f2176987ee50226e” AMI
5.	Select the “t2.micro” instance type
6.	Configure the instance details with VPC, Subnet, etc.
7.	Select the default storage
8.	Add the appropriate tags
9.	Select/Create the appropriate Security Group
10.	Select/Create the key (.pem file)
11.	Let the EC2 instance launch
12.	Associate the appropriate IAM role with EC2 instance. IAM Role should be able to access the S3 bucket where the AWS Lambda function package to be uploaded.

Prepare the EC2 Instance environment 

Prepare the Amazon Linux AWS EC2 instance to prepare the AWS Lambda Function for MediaInfo

1.	Login to EC2 instance
    a.	Run the command “chmod 400 [keyfile (.pem file)]”
    b.	Login to the EC2 instance using command “ssh -i [keyfile (.pem file)] ec2-user@[EC2-Instance-IP]”
    c.	Answer “yes” for “Are you sure you want to continue connecting (yes/no)?”
2.	Install the development tools using the command “sudo yum groupinstall 'Development Tools'” in the EC2 instance. It will install the necessary development packages on the EC2 instance.
3.	Perform the full upgrade using the command “sudo yum upgrade”. It will install all the latest packages on the EC2 instance.

Install the Python3 and PIP3

1.	Install Python3 using the command “sudo yum install python36”. It will install the Python 3.6.
    a.	Check the python3 version using the command “python3 --version”
2.	Install PIP
    a.	Download the pip3 package using the command “curl -O https://bootstrap.pypa.io/get-pip.py”
    b.	Install the pip3 using the command “python3 get-pip.py --user”
    c.	Check the pip3 version using the command “pip3 --version”

Prepare the MediaInfo CLI

1.	Install the library using the command “sudo yum install libcurl-devel” to add CURL support to MediaInfo in order to use the AWS S3 signed URL for media.
2.	Create the directory using the command “mkdir mediainfocli” to prepare MediaInfo CLI
3.	Update the Read/Write permission to the directory using the command “chmod 700 mediainfocli”
4.	Get into the directory using the command “cd mediainfocli”
5.	Download the MediaInfo package using the command “wget https://old.mediaarea.net/download/binary/mediainfo/19.04/MediaInfo_CLI_19.04_GNU_FromSource.tar.xz”
6.	Untar MediaInfo Package using the command “tar xvf MediaInfo_CLI_19.04_GNU_FromSource.tar.xz”. It will untar the MediaInfo package in the directory “MediaInfo_CLI_19.04_GNU_FromSource”
7.	Get into the MediaInfo package directory using the command “cd MediaInfo_CLI_19.04_GNU_FromSource”
8.	Compile the MediaInfo with the support for URL input using the command “./CLI_Compile.sh --with-libcurl”
9.	Move to user’s home directory using the command “cd home/ec2-user/”
10.	Create the AWS Lambda Function package directory using the command “mkdir MediaEvaluator”
11.	Update the Real/Write permission to the directory using the command “chmod 700 MediaEvaluator”
12.	Get into the AWS Lambda Function package directory using the command “cd MediaEvaluator”
13.	Copy the compiled MediaInfo CLI from MediaInfo package to the AWS Lambda Function package directory using the command “cp /home/ec2-user/mediainfocli/MediaInfo_CLI_GNU_FromSource/MediaInfo/Project/GNU/CLI/mediainfo /home/ec2-user/MediaEvaluator/”
14.	Validate the MediaInfo version by running the command “./mediainfo –-version”. It will confirm that MediaInfo CLI is working or not.

Create the Python Script for the AWS Lambda Function

1.	Get into the AWS Lambda Function package directory using the command “cd MediaEvaluator”
2.	Create the Python Script file using the command “touch mediaEvaluator.py”
3.	Write the Python Script
    a.	Open the script file using the command “vim mediaEvaluator.py”
    b.	Put the script in edit mode by typing “i"
    c.	Update the python script and then save it with exit by “esc” and then “:wq”
 
Install the Python dependency packages (boto3, botocore, xmltodict, gcc7, etc.) locally for Python script

1.	 Get into the AWS Lambda Function package directory using the command “cd MediaEvaluator”
2.	Install boto3 locally using the command “pip3 install boto3 --target .”
3.	Install botocore locally using the command “pip3 install botocore --target .”
4.	Install xmltodict locally using the command “pip3 install xmltodict --target .”
5.	Install gcc7 locally using the command “pip3 install gcc7 --target .”

Package the AWS Lambda Function

1.	Get into the AWS Lambda Function package directory using the command “cd MediaEvaluator”
2.	Zip the package using the command “zip -r9 /home/ec2-user/MediaEvaluator.zip .”
3.	Upload the Zip file to the AWS S3 bucket using the AWS CLI command “aws s3 cp /home/ec2-user/MediaEvaluator.zip s3://[aws-s3-bucket-name]”
4.	Deploy the Python 3.6 AWS Lambda Function using the package from AWS S3 bucket
