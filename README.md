
## Table of Contents
![Python Version](https://img.shields.io/badge/Python-3.6%2B-brightgreen.svg) ![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)

<details><summary>app.py : get basic stats of S3 buckets :video_game: </summary><p>

* [about](#about1)
* [demo](#demo1)
* [prerequisite](#prerequisite1)
* [install](#install1)
* [example](#example1)

</p></details>

<details><summary>app2.py : dynamically rename S3 objects within/between buckets :video_game: </summary><p>

* [about](#about2)
* [demo](#demo2)
* [prerequisite](#prerequisite2)
* [install](#install2)
* [arguments](#arguments2)
* [example](#example2)

</p></details>
<br>

---

### 1. [app.py](https://github.com/higee/s3-buddy/blob/master/app.py) : get basic stats of S3 buckets 

<a name='about1'></a>
#### About
* [aws cli](https://docs.aws.amazon.com/cli/latest/reference/s3/ls.html) lets you figure out the number of S3 objects and their size .
* What if you want to know hourly/daily/monthly stats within a given range of specific dates?

<a name='demo1'></a>
#### Demo
[![demo](https://asciinema.org/a/1SVNerw5cRjTV621rLgeVz2tG.svg)](https://asciinema.org/a/1SVNerw5cRjTV621rLgeVz2tG)

<a name='prerequisite1'></a>
#### Prerequisite
* the `profile` in your `credentials` must have an access to S3 buckets

```
$ cat ~/.aws/credentials
>>>
[higee]
aws_access_key_id = something
aws_secret_access_key = something
```

<a name='install1'></a>
#### Install

```
$ cd {somewhere}
$ git clone https://github.com/higee/s3-wrapper
$ cd s3-wrapper
$ pip install -r requirements.txt
```

<a name='example1'></a>
#### Example
* [help message](https://asciinema.org/a/1SVNerw5cRjTV621rLgeVz2tG?t=8)
```
$ python app.py --help
```

* [the number of S3 obejcts and their size per hour](https://asciinema.org/a/1SVNerw5cRjTV621rLgeVz2tG?t=8)
```
$ python app.py --start-date 2019-02-01 --end-date 2019-02-01 \
                --bucket higee-bucket --path incoming --interval hour \
                --profile higee
```

* [the number of S3 objects and their size per day](https://asciinema.org/a/1SVNerw5cRjTV621rLgeVz2tG?t=58)
```
$ python app.py --start-date 2019-02-01 --end-date 2019-02-03 \
                --bucket higee-bucket --path incoming --interval day \
                --profile higee
```

* [the number of S3 objects and their size per month](https://asciinema.org/a/1SVNerw5cRjTV621rLgeVz2tG?t=1:12)
```
$ python app.py --start-date 2019-01-01 --end-date 2019-03-01 \
                --bucket higee-bucket --path incoming --interval month \
                --profile higee
```

* [the number of S3 objects and their size per year](https://asciinema.org/a/1SVNerw5cRjTV621rLgeVz2tG?t=1:41)
```
$ python app.py --start-date 2019-02-01 --end-date 2020-01-01 \
                --bucket higee-bucket --path incoming --interval year \
                --profile higee
```

* [the number of S3 objects and their size per every six hours](https://asciinema.org/a/1SVNerw5cRjTV621rLgeVz2tG?t=2:13)
```
$ python app.py --start-date 2019-02-01 --end-date 2019-02-01 \
                --bucket higee-bucket --path incoming --interval hour \
                --delta 6 --profile higee
```

<br>

---

### 2. [app2.py](https://github.com/higee/s3-buddy/blob/master/app2.py) : dynamically rename S3 objects within/between buckets

<a name='about2'></a>
#### About
* [aws cli](https://docs.aws.amazon.com/cli/latest/reference/s3/index.html#cli-aws-s3) lets you copy or move objects.
* What if you need to dynamically rename `keys` or `folders` as well?
* Term `key` and `folder` are slightly different from original meanings
    * example : `s3://higee-bucket/incoming/2019/01/01/00/higee.log`
        * `bucket` : `higee-bucket`
        * `folder` : `incoming/2019/01/01/00/`
        * `key` : `higee.log`
* this app renames objects by creating copies with new name. 
* So set `delete` to True if you want to remove them.

<a name='demo2'></a>
#### Demo
[![demo](https://asciinema.org/a/237976.svg)](https://asciinema.org/a/237976)

<a name='prerequisite2'></a>
#### Prerequisite
* the `profile` in your `credentials` must have an access to S3 buckets

```
$ cat ~/.aws/credentials
>>>
[higee]
aws_access_key_id = something
aws_secret_access_key = something
```

<a name='install2'></a>
#### Install

```
$ cd {somewhere}
$ git clone https://github.com/higee/s3-wrapper
$ cd s3-wrapper
$ pip install -r requirements.txt
```

<a name='arguments2'></a>
#### Arguments

| argument | description | required | default |
| -------  | ----------- | :-------: | :------: |
| profile | needs access to `source-bucket` and `dest-bucket` | ✓ | |
| source-bucket | S3 bucket with objects to be renamed | ✓ | |
| dest-bucket | S3 bucket where renamed objects will be moved to | | source-bucket |
| dryrun | whether you want to test it first | | True |
| delete | whether you want to remove source objects | | False |
| source-folder-key-prefix | prefix of S3 objects you want to rename | ✓ |
| source-key-str | sub-string of `key` to be replaced by `dest-key-str` |  |
| dest-key-str | sub-string that will replace `source-key-str` | |
| source-folder-str | original `folder` name |  |
| dest-folder-str | new `folder` name that will replace `dest-folder-str`  | |


<a name='example2'></a>
#### Example


* [help message](https://asciinema.org/a/237976?t=7)
```
$ python app2.py --help
```

* [rename keys and copy objects within a bucket](https://asciinema.org/a/237976?t=20)
    * source : `s3://higee-bucket/incoming/2019/01/01/01/higee-staging*`
    * dest : `s3://higee-bucket/incoming/2019/01/01/01/higee-prod*` 
    * dryrun : True
    * delete source objects : False
    
```
$ python app2.py --source-folder-key-prefix incoming/2019/01/01/01/higee-staging \
                 --source-bucket higee-bucket --source-key-str staging \
                 --dest-key-str prod --profile higee
```

* [rename keys and copy objects to a different bucket](https://asciinema.org/a/237976?t=35)
    * source : `s3://higee-bucket/incoming/2019/01/01/02/higee-staging*`
    * dest : `s3://higee-bucket-2/incoming/2019/01/01/02/higee-dev*` 
    * dryrun : True
    * delete source objects : False
```
$ python app2.py --source-bucket higee-bucket --dest-bucket higee-bucket-2 \
                 --source-folder-key-prefix incoming/2019/01/01/02/higee-staging \
                 --source-key-str staging --dest-key-str dev --profile higee
```

* [rename folder and copy objects within a bucket](https://asciinema.org/a/237976?t=50)
    * source : `s3://higee-bucket/incoming/2019/02/*`
    * dest : `s3://higee-bucket/processed/2019/02/*`
    * dryrun : True
    * delete source objects : False
    
```
$ python app2.py --source-folder-key-prefix incoming/2019/02 \
                 --source-bucket higee-bucket --source-folder-str incoming \
                 --dest-folder-str processed --profile higee
```

* [rename folder and copy objects to a different bucket](https://asciinema.org/a/237976?t=1:23)
    * source : `s3://higee-bucket/incoming/2019/03/*`
    * dest : `s3://higee-bucket-2/processed/2019/03/*`
    * dryrun : True
    * delete source objects : False
    
```
$ python app2.py --source-bucket higee-bucket --dest-bucket higee-bucket-2 \
                 --source-folder-key-prefix incoming/2019/03 \
                 --source-folder-str incoming --dest-folder-str processed \
                 --profile higee
```

* :bomb: [execute the command without dryrun](https://asciinema.org/a/237976?t=1:52) :bomb:
    * source : `s3://higee-bucket/incoming/2019/01/01/01/higee*`
    * dest : `s3://higee-bucket/incoming/2019/01/01/01/higee-staging*`
    * dryurn : False
    * delete source objects : False

```
$ python app2.py --source-folder-key-prefix incoming/2019/01/01/01 \
                 --source-bucket higee-bucket --source-key-str higee \
                 --dest-key-str higee-staging --dryrun False --profile higee
```

* :bomb: [remove source S3 objects after creating copies](https://asciinema.org/a/237976?t=2:10) :bomb:
    * source : `s3://higee-bucket/incoming/2019/02/01/01/*`
    * dest : `s3://higee-bucket/incoming/2019/02/01/01/*`
    * dryrun : True
    * delete source objects : True

```
$ python app2.py --source-folder-key-prefix incoming/2019/01 \
                 --source-bucket higee-bucket --source-key-str higee \
                 --dest-key-str higee-staging --dryrun False --delete True \
                 --profile higee
```
* [no objects found](https://asciinema.org/a/237976?t=2:53)
```
$ python app2.py --source-bucket higee-bucket --dest-bucket higee-bucket-2 \
                 --source-folder-key-prefix incoming/2019/01/01/01/02/higee-staging \
                 --source-key-str staging --dest-key-str dev --profile higee
```