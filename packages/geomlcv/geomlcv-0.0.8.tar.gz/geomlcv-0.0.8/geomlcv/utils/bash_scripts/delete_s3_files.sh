# Delete files from S3 bucket

# 1. List files
aws s3 ls s3://geoml-aquarry/output/gms/15dec2023/tang/ | awk '{print $4}' > all_files.txt

# 2. Delete files
while read file; do
    aws s3 rm s3://geoml-aquarry/output/gms/15dec2023/tang/$file
done < all_files.txt
