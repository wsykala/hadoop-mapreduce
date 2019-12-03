# Hadoop-mapreduce

## How to run

Create a virtualenv and install the requirements (this step can be skipped if the data is already downloaded): 

```bash
pip install -r requirements.txt
```

To get the data: 

```bash
python request.py
```

The downloaded files will be saved in the current directory under the **data/** path. The size of the directory is around **2GB**.   

**Important:** The script has builtin **0.25** second sleep after each request (to limit the calls to the API). Because of this, the download should be finished in around 10 minutes.


When the data is present inside **data/** directory, run the Mapreduce job as follows:

```bash
python parser.py | python mapper.py | python reducer.py
```

**Warning:** This command will take some time to finish and print **A LOT** of stuff to the stdout.


## What needs to be done

* The parser step should probably be ran before mapper/reducer jobs (create a big file from all of the files created by **request.py**).
This file is then used by HDFS.
* Add Dockerfile and try to run the jobs using Hadoop Streaming
* Add crontab entry to run the jobs periodically
* Create one script to run the job on demand