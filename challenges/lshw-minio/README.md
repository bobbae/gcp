## Challenge lshw-minio

* First read the `Basic rules for challenges` (https://github.com/bobbae/gcp/blob/main/challenges/README.md). 

* Summary: Fill out JSON data structure containing system information and store it as a file with metadata on minio object storage


## Part 1

* Given a system, such as a laptop or a desktop or a server 
in the cloud you may be using, create the JSON data structure that 
contains the inventory information from your system. 

* The data to be filled into each field should be
retrieved and inserted into JSON programmatically, i.e. using a script or a program, but not manually. 

* Your data will be different than what is
shown below as an example, but should use the same basic structure.


```json
[
    {
        "CPUs": [
            {
                "Description": "Intel Core i7-3720QM CPU @ 2.6 Ghz",
                "NumberOfCores": 4
            }  
        ],
        "Memory": [
            {
                "InstalledGB": 16,
                "AvailableGB": 10
            }
        ],
        "Storage": [
            {
                "Description": "SEAGATE MAX3073RC",
                "CapacityGB": 100,
                "AvailableGB": 80,
                "Type": "SSD"
            },
            { 
                "Description": "TOSHIBA UJ232A",
                "CapacityGB": 400,
                "AvailableGB": 100,
                "Type": "CD/DVD"
            }
        ],
        "Network": [
            {
                "Description": "Intel Ethernet",
                "IP": "192.168.1.111",
                "Netmask": "255.255.255.0" 
            },
            {
                "Description": "Loopback",
                "IP": "127.0.0.1",
                "Netmask": "255.0.0.0"
            }
        ]
    }
]

```

* Your solution for this part should be a program or a script.

## Part 2

* Go to https://min.io/ and read the Overview https://min.io/product/overview

* Install a local minio server using the quickstart information on min.io.  An
easy way may be to use docker image at https://hub.docker.com/r/minio/minio/ 

* Create a bucket named `lshwminio`

* Create a file/object named `machineinfo.json` inside this bucket `lshwminio` containing the JSON data created in Part 1

* FYI: Each object/file can have data which is the content as in our JSON machine data.  Each object/file can also have meta-data, which is data about data, attached to the file.

* Create meta data for this object/file `machineinfo.json` that contains tag `MyMetadata` with and integer value, e.g. { "MyMetadata": 14}.  You will assign a random
number to `MyMetadata` which is  an additional metadata for your file.

* An easy way to
create meta data for an object may be available in various APIs, e.g. https://github.com/mmm1513/pyminio whic happens to be for Python. You do not have to use Python or this API. 

* Your solution to this part should be additional code to the program in Part 1.

## Part 3

* The Part 3 is just thinking about some issues and preparing for further discussions. You can just think about them for later discussions. You do not need to write anything down but you can if you want to write down your thoughts into a file called `NOTES.txt` in your git repo.

* Think of how you may deal with many hundreds of thousands of `machineinfo.json` files.

* What kind of strategies can enhance search capability over large amount of machine data.  

* What kind of cloud services can be used in addition to storing  data in an object storage like minio, s3 or gcs?  Can other services be used together? What do you gain by using other services with object storage services?

