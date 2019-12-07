# Hadoop-mapreduce

## Building and running the container

First build the container. To do it execute the command below inside root directory of the project:

```bash
docker build -t hdfs-mapreduce .
```

The process will take some time when building for the first time.
After successful build, run the container in interactive mode.

**Important**: Exiting from the terminal/console will stop the container (all of the data and progress inside of it will be lost)

```bash
docker run -it hdfs-mapreduce:latest /etc/bootstrap.sh -bash
``` 

**Note**: While inside the container, the data needs to be downloaded first. 
By default it will be the first that is execute while running the **run.py** script.

To run the job:

```bash
# Optional flag --download true/false can be passed (by default it is true)
python3 run.py --input /mapreduce/parse.txt --output job_dir/
```

This command will by default download the data and save it to **/mapreduce/data** directory. After that the data will be
parsed and saved in a single file **/mapreduce/parse.txt**.

After preparing the data, the script will automatically create the **output** directory inside HDFS and put the
**parse.txt** file inside a timestamped directory inside. Then the mapreduce job will run and the data will be saved
inside the same directory as the inptu file.

To see the results of the job:

```bash
# List the job_dir directory
/usr/local/hadoop/bin/hdfs dfs -ls job_dir

Found 1 items
drwxr-xr-x   - root supergroup          0 2019-12-07 09:57 job_dir/1575730652

# List the last job directory
/usr/local/hadoop/bin/hdfs dfs -ls job_dir/1575730652

Found 2 items
drwxr-xr-x   - root supergroup          0 2019-12-07 09:58 job_dir/1575730652/out
-rw-r--r--   1 root supergroup     907326 2019-12-07 09:57 job_dir/1575730652/parse.txt

# Print the results
/usr/local/hadoop/bin/hdfs dfs -cat job_dir/1575730652/out/*
```

**Note**: The job also runs periodically every 15th minute (for example at 9:00, 9:15, 9:30, etc.)
 
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
