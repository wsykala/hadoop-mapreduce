# Hadoop-mapreduce

## Building and running the container

First build the container. To do it execute the command below inside root directory of the project:

```bash
docker build -t hdfs-mapreduce .
```

The process will take some time when building for the first time.
After successful build run the container in interactive mode.

**Important**: Exiting from the terminal/console will stop the container (all of the data and progress inside of it will be lost)

```bash
docker run -it hdfs-mapreduce:latest /etc/bootstrap.sh -bash
``` 


While inside the container the data needs to be downloaded and then added to HDFS.

**TODO**: This is not yet implemented in a single script. Below is a description on how to do it right now:

```bash
# Download some data (if you don't want to have all of it, just ctrl+C after downloading a few files)
python3 request.py

# Run the parser and redirect stdin to file (choose an appropiate name)
python3 parser.py > test.txt

# Add the file to HDFS (the directories and files could be whatever you want, but remember them)
/usr/local/hadoop/bin/hdfs dfs -mkdir -p test_dir/
/usr/local/hadoop/bin/hdfs dfs -put /mapreduce/test.txt test_dir/

# If you want to see if the file was really added to HDFS run the comand below
/usr/local/hadoop/bin/hdfs dfs -ls test_dir

# To run the map reduce job (input is the file inside HDFS)
python3 run.py --input test_dir/test.txt --output test_dir/out/

# This script will create a directory inside specified --output dir (to prevent an error with 'file already exists')
# The directory name is the current timestamp
# To print the results of the job, first find the directory
/usr/local/hadoop/bin/hdfs dfs -ls test_dir/out

# Found 1 items
# drwxr-xr-x   - root supergroup          0 2019-12-04 16:44 test_dir/out/1575495825

# Then print the results
/usr/local/hadoop/bin/hdfs dfs -cat test_dir/out/1575495825/*
```
 
## How to run locally

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

* The parser step SHOULD be done before running the job. Do one of the following:
    * Download the files and then run the parser (create a new script)
    * Run the parser at the startup (5 GB of data is added to the image)
    * Change the **request.py** file so it saves already parsed data and then add it into the image
* Add crontab entry to run the jobs periodically
* Create a script that puts the parsed file into HDFS
* Do something about the initial data download (Data can be added into the build, but this will make the image bigger).
Unfortunately **-v** seems to not work properly.
