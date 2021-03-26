# Challenge: lshw

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

* This part is just thinking about some issues and preparing for further discussions. You can just think about them for later discussions. You do not need to write anything down but you can if you want to write down your thoughts into a file called `NOTES.txt` in your git repo.

* Think of how you may deal with many hundreds of thousands of `machineinfo.json` files.

* What kind of strategies can enhance search capability over large amount of machine data.  
* What kind of cloud services can be used in addition to storing  data in an object storage like minio, s3 or gcs?  Can other services be used together? What do you gain by using other services with object storage services?

