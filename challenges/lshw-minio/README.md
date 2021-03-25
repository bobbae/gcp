## Challenge lshw-minio

* First read the `Basic rules for challenges` first. It should be in a `README.md` one directory up from here.

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

## Part 2

* Go to https://min.io/ and read the Overview https://min.io/product/overview

* Install a local minio server using the quickstart information on min.io.  An
easy way may be to use docker image at https://hub.docker.com/r/minio/minio/ 

* Create a bucket named `lshwminio`

* Create a file/object named `machineinfo.json` inside this bucket `lshwminio` containing the JSON data created in Part 1

* FYI: Each object/file can have data which is the content as in our JSON machine data.  Each object/file can also have meta-data, which is data about data, attached to the file.

* Create meta data for this object/file `machineinfo.json` that contains tag `NumberOfCores` with and integer value, e.g. { "NumberOfCores": 4}.  You will read
the `NumberOfCores` information from your `machineinfo.json` content and create a meta data
for the `machineinfo.json` file which is attached to the file.

* An easy way to
create meta data for an object may be available in various APIs, e.g. https://github.com/mmm1513/pyminio whic happens to be for Python. You do not have to use Python or this API. 

## Part 3

* The Part 3 is just thinking about some issues and preparing for further discussions. You can just think about them for later discussions. You do not need to write anything down but you can if you want to write down your thoughts into a file called `NOTES.txt` in your git repo.

* Think of how you may deal with many hundreds of thousands of `machineinfo.json` files.

* What kind of meta data would you store per object to enhance search capability over large amount of machine data.  

* What kind of additional methods would you consider to make the storage and searching of such machine data, aside from storing into an object storage like minio, s3 or gcs?
