## Methods for Establish SQL-Server in Mac-Docker

### 1. Install Docker in Server and Configure it

> Check it via google




### 2. Pull `sql-server` Image

```shell
sudo docker run -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=<YourStrong!Passw0rd>' \
   --name 'mssql' -p 1401:1433 \
   -v sql1data:/var/opt/mssql \
   -d microsoft/mssql-server-linux:2017-latest
```



#### 2.1 Check the status of the image

```shell
sudo docker ps -a

# if the status is existed, do:
docker start mssql # mssql is the docker name, or use the name sql1
```



### 3. Enter the Docker and Change the Password

```shell
sudo docker ps -a

# In this way, enter the docker
sudo docker exec -it mssql "bash"

## |--> In docker
## change the password
/opt/mssql-tools/bin/sqlcmd  -S localhost -U SA -P '<YourStrong!Passw0rd>'

#### |---> in mssql
ALTER LOGIN SA WITH PASSWORD="freud211@cct"

```



### 4. Log outside of the Docker

**Install sqlcmd and Run sqlcmd**

```shell
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install --no-sandbox mssql-tools

sqlcmd  -S 127.0.0.1,1401  -U SA
```



### 5. Copy the Backup File to Docker Image 

```Shell
sudo docker cp medicine.bak mssql:/var/opt/mssql/backup
```

> Where the file `medicine.bak` is the given mssql backup file.



### 6. Migrate Bak into SQL-server database

1. Find record and log file

```shell
# enter the image mssql
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P '<-password->' -Q 'restore filelistonly from disk = "/var/opt/mssql/backup/medicine.bak"' | tr -s ' ' | cut -d ' ' -f 1-2

/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'freud211@cct' -Q 'restore filelistonly from disk = "/var/opt/mssql/backup/medicine.bak"' | tr -s ' ' | cut -d ' ' -f 1-2


# then enter the sql # change the password 
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P '<-password->' 
```

2. Restore the database file

```sql

-- inside the sql
RESTORE DATABASE cctdb FROM DISK = "/var/opt/mssql/backup/medicine.bak"

RESTORE DATABASE medicine FROM DISK = "/var/opt/mssql/backup/medicine.bak"
WITH MOVE "xml" TO "/var/opt/mssql/data/xml",

go

```

3. Check the Results

```sql
-- check the result

-- 1. Find the database name list
select name from sys.databases
Go

-- 2. Change into cctdb context
use cctdb

-- 3. Find all tables in the cctdb
SELECT name FROM sys.Tables

-- 4. Count the row's number in the table
select count(*) from xml_table
GO
```



### 7. Access the Database from Other Computer [Optional]

1. In the Server, get the IP address by:

```shell
ifconfig
```

Current IP is: `10.30.19.158`

2. In other computers

Install the `sqlcmd`.

```shell
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
brew install --no-sandbox mssql-tools
```

Enter the sql-server

```shell
sqlcmd -S 10.30.19.158,1401 -U sa
```



### 8. Read the Database by Python

```shell
conda create -n cctdb python=2 pymssql

source activate cctdb
pip install ipykernel
python -m ipykernel install --user --name cctdb --display-name "CCTDB"
```

