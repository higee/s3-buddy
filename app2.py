import datetime
import argparse

import boto3

def copy_rename_s3_objects(**kwargs):

    session = boto3.Session(profile_name=kwargs["profile"])
    s3 = session.resource('s3')
    source_objects = s3.Bucket(name=kwargs["source_bucket"]).objects
    source_objects_matched = source_objects.filter(Prefix=kwargs["source_folder_key_prefix"])
    index = 0

    for source_object in source_objects_matched:
        
        # check whether collections is empty
        # following approaches are too expensive
        # sum(1 for _ in source_objects_matched.all())
        # len(list(source_objects_matched.all()))
        index += 1

        # in the absence of dest_bucket,
        # obejcts will be copied inside source_bucket
        if not kwargs["dest_bucket"]:
            kwargs["dest_bucket"] = kwargs["source_bucket"]
        
        # extract key with full-path
        source_folder_key = source_object.key
        
        # separate key and folder
        source_key = source_folder_key[source_folder_key.rindex('/')+1:]
        source_folder = source_folder_key[:source_folder_key.rindex('/')]
            
        # rename key (exact match)
        if kwargs["dest_key_str"]:
            dest_key = source_key.replace(kwargs["source_key_str"], kwargs["dest_key_str"])
        else:
            dest_key = source_key

        # rename folder (exact match)
        if kwargs["dest_folder_str"]:
            dest_folder = source_folder.replace(kwargs["source_folder_str"], kwargs["dest_folder_str"])
        else:
            dest_folder = source_folder
        
        source_object_w_bucket = '/'.join([kwargs["source_bucket"], source_folder, source_key])
        dest_object_w_bucket = '/'.join([kwargs["dest_bucket"], dest_folder, dest_key])
        source_object_wo_bucket = '/'.join([source_folder, source_key])
        dest_object_wo_bucket = '/'.join([dest_folder, dest_key])
            
        # no effect to S3 objects
        if eval(kwargs["dryrun"]):
            if eval(kwargs["delete"]):
                print(f"[dryrun] (copied) s3://{source_object_w_bucket} to {dest_object_w_bucket}")
                print(f"[dryrun] (removed) s3://{source_object_w_bucket}")        
            else:
                print(f"[dryrun] (copied) s3://{source_object_w_bucket} to s3://{dest_object_w_bucket}")
            
        # copy S3 objects
        else:
            dest_params = {
                'bucket_name' : kwargs["dest_bucket"],
                'key' : dest_object_wo_bucket
            }
            s3.Object(**dest_params).copy_from(CopySource=source_object_w_bucket)        
            print(f'(copied) s3://{source_object_w_bucket} to s3://{dest_object_w_bucket}')
            
            # remove S3 objects
            if eval(kwargs["delete"]):
                source_params = {
                    'bucket_name' : kwargs["source_bucket"],
                    'key' : source_object_wo_bucket
                }
                s3.Object(**source_params).delete()
                print(f"(removed) s3://{source_object_w_bucket}")        
        
    if not index:
        print('No object found')

def main():
    
    # argparse configuration
    parser = argparse.ArgumentParser(
        description='ex: $ python app.py --source-bucket higee-bucket --source-folder-key-prefix incoming/2019/01' \
            '--source-folder-str incoming --dest-folder-str processed --profile higee'
    )
    parser.add_argument("--source-bucket", required=True, help="pass the source S3 bucket name")
    parser.add_argument("--dest-bucket", required=False, help="pass the destination S3 bucket name")
    parser.add_argument("--source-folder-key-prefix", required=True, help="pass the prefix of S3 objects you want to rename")
    parser.add_argument("--source-key-str", required=False, help="pass the original key name")
    parser.add_argument("--dest-key-str", required=False, help="pass the new key name you want to rename to")
    parser.add_argument("--source-folder-str", required=False, help="pass the original folder name you want to rename")
    parser.add_argument("--dest-folder-str", required=False, help="pass the new folder name you want to rename to")
    parser.add_argument("--dryrun", required=False, default="True", help="set to True if you want to test first", choices=["True", "False"])
    parser.add_argument("--delete", required=False, default="False", help="set to True if you want to remove original objects?", choices=["True", "False"])
    parser.add_argument("--profile", required=True, help="pass the profile allowed to access the S3 bucket")
    args = parser.parse_args()

    check_required_arguments = (args.source_folder_str and args.dest_folder_str) or (args.source_key_str and args.dest_key_str)
    if not check_required_arguments:
        error_message = " either (source-key-str & dest-key-str) or (source-folder-str & dest-folder-str) should be provided"
        print(error_message)
        return
    
    copy_rename_s3_objects(
        profile=args.profile, source_bucket=args.source_bucket, dest_bucket=args.dest_bucket,
        source_folder_key_prefix=args.source_folder_key_prefix, source_key_str=args.source_key_str, 
        dest_key_str=args.dest_key_str, source_folder_str=args.source_folder_str, 
        dest_folder_str=args.dest_folder_str, dryrun=args.dryrun, delete=args.delete
    )

if __name__ == "__main__":
    main()
