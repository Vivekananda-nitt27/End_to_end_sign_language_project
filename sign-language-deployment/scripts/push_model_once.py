import boto3

BUCKET = "sign-lang-2026-vivek"
KEY = "models/sign_language/latest/best.pt"
FILE = "artifacts/best.pt"

s3 = boto3.client("s3")
s3.upload_file(FILE, BUCKET, KEY)

print("UPLOAD SUCCESSFUL")
