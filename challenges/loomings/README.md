# Challenge: loomings

* First read the `Basic rules for challenges` (https://github.com/bobbae/gcp/blob/main/challenges/README.md). 

* Summary: Install minio, create a bucket, create bunch of files and process them. `minio` is a distributed cloud centric object storage that can mimick `s3`.

## Part 1

* Go to https://min.io/ and read the overview https://min.io/product/overview. Learn 
 quickly about `minio` enough to do this challenge. This is part of the challenge.

* Install a local minio server using the quickstart information on min.io.  You
can install it on your computer or in the cloud. Or use `play.min.io`. If you use
the `play.min.io` figuring out Access and Secret key is part of this challenge.

* Create a minio bucket called `loomings`.  This should be done from a program that uses
API to create a bucket.  API can be `minio` specific or `s3` specific. An example API
is at https://docs.min.io/docs/java-client-quickstart-guide.html.  You do not have
to use Java. You can also use Go, Python, Javascript, .NET, Haskell, or REST API.

* From within the program, using a scripting language or a programming language, 
read each non-blank line of text from the file `loomings.txt` 
available at https://gist.github.com/bobbae/259e195f11cea0183ea93d378946a737

* From within the program, copy the `loomings.txt` file into the `loomings` bucket.

* From within the program, print the total number of non-blank 
lines in the `loomings.txt`.

* From within the program, create a file with a unique name containing 
each  non-blank line of  text read from  the file.
You may end up with lots of files. File-1, File-2, File-3, File-4, ..., etc.
File-1 will contain the first line read from the file. File-2 will contain the second line
read from the file, and so on.
Each file should be stored inside the minio bucket named `loomings`.  Writing each file
as an object inside the bucket should be done from within the program using the proper
API.

* From within the program, create a meta-data for each file and attach the meta-data to that file. 
Each meta-data should be a hash digest of the content of the file.
For example, File-1 may have a meta-data `{ "Content-hash": "3dsdfwewa..." }` 
which will contain hash digest of the File-1. The hash digest can be SHA-1, SHA-256 or MD5.  Writing meta-data and attaching to
the file object in the bucket should be done via `minio` API.

* From within the program, list the files sorted in order, from smallest to largest file based on the size (total bytes) of the content within the file. 
Print the name and size of each file on each line of the output.

* There will be one duplicate line in the `loomings.txt` file. Therefore, there will be two files that have the same hash digest of the content.  Print the name of the two files you created which contains a line from the `loomings.txt` that have the identical content.  Print  the original text line which is duplicated in loomings.txt. You may do the search 
for the matching content digest hash by looking at the meta-data of each file object. Do this from within your program using the API.

* Remove the duplicate (second occurance) line from loomings.txt 
and create a new version of the file and call it loomings-clean.txt.

## Part 2

* This part is just thinking about some issues and preparing for further discussions. You can just think about them for later discussions. You do not need to write anything down but you can if you want to write down your thoughts into a file called `NOTES.txt` in your git repo.

* Think of how you may deal with many hundreds of thousands of files, each of which may have duplicate lines. How would you remove duplicate lines in each file and do so efficiently and within reasonable amount of time?

* What kind of strategies can enhance search capability over large amount of textual data?

* What kind of cloud services can be used in addition to storing data in an object storage like minio, s3 or gcs?  Can you use databases?  If so, what are some example databases
you can choose to use for this?  Can other services be used together? What do you gain by using other services with object storage services?

