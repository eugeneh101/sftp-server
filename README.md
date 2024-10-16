# Test SFTP server

```python
import pysftp

cn_opts = pysftp.CnOpts()
cn_opts.hostkeys = None

with pysftp.Connection(
    "{SFTP_ENDPOINT}",  # SFTP endpoint
    username="demo", password="demo",  # auth now checks
    port=22, cnopts=cn_opts,
) as conn:
    print(conn.listdir())
    conn.get(remotepath="/{SOME_FOLDER}/test.txt", localpath="{DESIRED_PATH_ON_COMPUTER")
    conn.put(
        localpath="wordcount.py",  # file on your computer
        remotepath="/{S3_BUCKET_NAME}/wordcount.py",
    )
```