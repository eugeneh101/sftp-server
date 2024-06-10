# Test SFTP server

```python
import pysftp

cn_opts = pysftp.CnOpts()
cn_opts.hostkeys = None

with pysftp.Connection(
    "{SFTP_ENDPOINT}",  # SFTP endpoint
    username="any_user", password="any_password",  # doesn't matter as auth Lambda doesn't check
    port=22, cnopts=cn_opts,
) as conn:
    print(conn.listdir())
    conn.get(remotepath="/{S3_BUCKET_NAME}/test.txt", localpath="{DESIRED_PATH_ON_COMPUTER")  # if you already uploaded test.txt into S3 bucket
    conn.put(
        localpath="wordcount.py",  # file on your computer
        remotepath="/{S3_BUCKET_NAME}/wordcount.py",
    )
```