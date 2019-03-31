import os
import datetime
import argparse

import dateutil.relativedelta

def main():

    # argparse configuration
    parser = argparse.ArgumentParser(
        description='example: $ python app.py --start-date "2019-01-03" --end-date "2019-01-04"' \
            ' --bucket higee --path incoming --interval month --delta 1 --profile higee' 
    )
    parser.add_argument("--start-date", required=True, help="pass in YYYY-MM-DD format")
    parser.add_argument("--end-date", required=True, help="pass in YYYY-MM-DD format")
    parser.add_argument("--bucket", required=True, help="pass the name of S3 bucket")
    parser.add_argument("--path", required=True, help="pass the path under the S3 bucket")
    parser.add_argument("--interval", required=True, choices=['year', 'month', 'day', 'hour'])
    parser.add_argument("--delta", required=False, default=1, type=int, help="pass the value you want to increment interval by")
    parser.add_argument("--profile", required=True, help="pass the profile allowed to access the S3 bucket")
    args = parser.parse_args()

    # user-input arguments configuration
    start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d') + dateutil.relativedelta.relativedelta(hours=23)

    while start_date <= end_date:

        # set date_path according to args.interval
        if args.interval == 'year':
            date_path = f"{start_date.year:02d}"
        elif args.interval == 'month':
            date_path = f"{start_date.year:02d}/{start_date.month:02d}"
        elif args.interval == 'day':
            date_path = f"{start_date.year:02d}/{start_date.month:02d}/{start_date.day:02d}"
        elif args.interval == 'hour':
            date_path = f"{start_date.year:02d}/{start_date.month:02d}/{start_date.day:02d}/{start_date.hour:02d}"

        cmd = f"aws s3 ls --summarize --human-readable --recursive {args.bucket}/{args.path}/{date_path}/ --profile {args.profile} | grep Total"
        
        # print meta-data
        print('='*50)
        print(f"bucket : {args.bucket}")
        print(f"object path : {'/'.join([args.path, date_path, ''])}")
        print('='*50)

        # run the command and print basic stats of S3 objects
        os.system(cmd)
        print('\n')
        
        # increment interval by delta
        if args.interval == 'year':
            start_date += dateutil.relativedelta.relativedelta(years=args.delta)
        elif args.interval == 'month':
            start_date += dateutil.relativedelta.relativedelta(months=args.delta)
        elif args.interval == 'day':
            start_date += dateutil.relativedelta.relativedelta(days=args.delta)
        elif args.interval == 'hour':
            start_date += dateutil.relativedelta.relativedelta(hours=args.delta)

if __name__ == "__main__":
    main()
