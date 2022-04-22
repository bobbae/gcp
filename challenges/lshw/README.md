
Fill out JSON data structure containing system information and store it as a file with metadata on minio object storage


## Part 1

* Given a system, such as a laptop or a desktop or a server 
in the cloud you may be using, create the JSON data structure that 
contains the inventory information from your system. 

* The data to be filled into each field should be
retrieved and inserted into JSON programmatically, i.e. using a script or a program, but not manually. 

* Your data will be different than what is
shown below as an example, but should use the same basic structure. Note that the whole structure is an array, each element being the description for one machine. So
you may have an array of more than one machines, even though you may be collecting information for just one machine, you get extra credit for writing the program
that can handle collection of data from multiple machines and creating the appropriate JSON structure as below.


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

* Your solution for this part should be a program or a script. It should gather information via API from the machine you are using to construct the JSON structure as above and write the content of the JSON data structure out into a file called `machinedata.json`.  You can use any API to get the machine data from the laptop, desktop or cloud hosted machine you are using.  An example of usable API may be https://www.thepythoncode.com/article/get-hardware-system-information-python.  You can use any other APIs.

## Part 2

* Write another program or script  add code that will read the content of the `machinedata.json`

* The program should revise the content by updating the part of JSON tagged with "Network" with additional IPv6 related information. For example, the "Network" part of the JSON may be updated to look like this:

```
[ 
    {
        ...
        "Network": [
            {
                "Description": "Intel Ethernet",
                "IP": "192.168.1.111",
                "Netmask": "255.255.255.0" ,
                "IPv6": {
                     "Address": "fe80::d7ff:5db0:...",
                     "PrefixLen": 64,
                     "ScopeId": { 
                        "Value": 0x20,
                        "Description": "Link"
                     }
                }
            },
           {
               "Description": "Loopback",
                "IP": "127.0.0.1",
                "Netmask": "255.0.0.0",
                 "IPv6": {
                     "Address": "::1",
                     "PrefixLen": 128,
                     "ScopeId": { 
                        "Value": 0x10,
                        "Description": "Host"
                     }
                }
            }
        ]
     }
]
            
```

* Write the new program that updates the JSON structure and creates a new version of the machine data JSON into a file called `machinedata-2.json`

* Save the program and the data from Part 1 and 2 into a public git repo and send the URL.  Make sure your machine data in JSON files do not contain any sensitive data that need to be secured by you.

## Part 3

* This part is just thinking about some issues and preparing for further discussions. You can just think about them for later discussions. You do not need to write anything down but you can if you want to write down your thoughts into a file called `NOTES.txt` in your git repo.

* Think of how you may deal with many hundreds of thousands of `machineinfo.json` files.

* What kind of strategies can enhance search capability over large amount of machine data.  
* How would you store this kind of JSON data into a database?  What kind of database would you use?
* What kind of cloud services can be used in addition to storing  data in an object storage like minio, s3 or gcs?  Can other services be used together? What do you gain by using other services with object storage services?

* Given the file like `machinedata.json`, how would you select a specific tag and value from the JSON structure via command line tool at a shell prompt? If you were using
the bash shell, what command or a list of commands you would use to select and print only IP addresses of all of the network interfaces from all the machines in the file?

