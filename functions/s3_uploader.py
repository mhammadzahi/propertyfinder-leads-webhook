from botocore.client import Config
from dotenv import load_dotenv
import os, boto3, mimetypes, random, string, json, time, csv

load_dotenv()

access_key_id = os.getenv("aws_access_key_id")
secret_access_key = os.getenv("aws_secret_access_key")

# ----------------------------------------------------------------------
# Generate a valid random bucket name
# ----------------------------------------------------------------------
def generate_valid_bucket_name(length):
    characters = string.ascii_lowercase + string.digits
    first_char = random.choice(string.ascii_lowercase + string.digits)
    middle = ''.join(random.choice(characters) for _ in range(length - 2))
    last_char = random.choice(string.ascii_lowercase + string.digits)
    return first_char + middle + last_char


# ----------------------------------------------------------------------
# Create a new bucket with public read policy (no ACL)
# ----------------------------------------------------------------------
def create_a_bucket(bucket_name):
    boto3_config = Config(region_name='ap-south-1', signature_version='s3v4')
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        config=boto3_config
    )

    try:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})

        # Remove all block-public-access settings
        s3.delete_public_access_block(Bucket=bucket_name)

        # Set bucket policy to allow public read (no ACL needed)
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
                }
            ]
        }

        s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
        print(f"✅ Bucket '{bucket_name}' created and made public (no ACLs used).")

    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"⚠️ Bucket '{bucket_name}' already exists and is owned by you.")
    except Exception as e:
        print(f"❌ Error creating bucket: {e}")


# ----------------------------------------------------------------------
# Upload file to S3 (no ACLs)
# ----------------------------------------------------------------------
def upload_file_to_s3(bucket_name, file_path):
    boto3_config = Config(region_name='ap-south-1', signature_version='s3v4')
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        config=boto3_config
    )

    try:
        file_name = os.path.basename(file_path)
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = "application/octet-stream"

        s3.upload_file(
            Filename=file_path,
            Bucket=bucket_name,
            Key=file_name,
            ExtraArgs={'ContentType': content_type}
        )

        public_url = f"https://{bucket_name}.s3.ap-south-1.amazonaws.com/{file_name}"
        print(f"✅ Uploaded: {public_url}")
        return public_url

    except Exception as e:
        print(f"❌ Error uploading '{file_path}': {e}")
        return None


# ----------------------------------------------------------------------
# Upload all .mp3 files in directory
# ----------------------------------------------------------------------
def main_upload(directory_path):
    if not os.path.isdir(directory_path):
        print(f"❌ Invalid directory: {directory_path}")
        return []

    bucket_name = generate_valid_bucket_name(random.choice(range(15, 31)))
    create_a_bucket(bucket_name)

    uploaded_urls = []

    for root, _, files in os.walk(directory_path):
        for f in files:
            if f.lower().endswith(".mp3"):
                full_path = os.path.join(root, f)
                url = upload_file_to_s3(bucket_name, full_path)
                time.sleep(0.5)  # brief pause between uploads
                if url:
                    uploaded_urls.append(url)

    # Save URLs to a CSV file
    csv_file_path = os.path.join(directory_path, "uploaded_urls.csv")
    with open(csv_file_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Uploaded URLs"])
        for url in uploaded_urls:
            writer.writerow([url])

    print(f"\n🎵 Uploaded Files saved to: {csv_file_path}")
    for u in uploaded_urls:
        print(" -", u)

    return uploaded_urls




# if __name__ == "__main__":
#     main_upload("recordings")
