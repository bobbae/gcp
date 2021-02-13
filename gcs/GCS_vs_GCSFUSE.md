# Unscientific benchmark to show performance of gcsfuse vs. gcs.

1. Create/use service account with "storage admin" role and download the key in json format.

2. activate service account
```
  gcloud auth activate-service-account --key-file=/home/bob/bob-key.json /home/bob/tmpmnt/
```
3. create a bucket
``` 
    gsutil mb gs://bobtest1
``` 
4. Use gcsfuse to mount the bucket to a directory /home/bob/tmpmnt
```
    gcsfuse  --key-file /home/bob/bob-key.json bobtest1 /home/bob/tmpmnt
```    
5. copy a large file to bobtest1 bucket using gcsfuse
```
    time cp testfile1 tmpmnt
    real	0m22.540s
    user	0m0.009s
    sys	0m1.436s
```    
6. copy the same large file to bobtest bucket using gsutil
```
time gsutil cp testfile1 gs://bobtest1/testfile2
 [1 files][821.9 MiB/821.9 MiB]                                                
Operation completed over 1 objects/821.9 MiB.                                    

real	0m12.743s
user	0m5.090s
sys	0m2.562s
```
7. Note that in a large file (about 821.9 MiB) copy case the gsutil method is almost twice as fast as gcsfuse.
Gcsfuse has to copy data in and out of kernel/user boundary more times than gsutil case.
[FUSE diagram](https://en.wikipedia.org/wiki/Filesystem_in_Userspace#/media/File:FUSE_structure.svg)

8. Let see how gsutil and gcsfuse perform when dealing with many small files, rather than a large file. 
   Let's create a directory with many (1000) small files in it.
```
    mkdir manyfiles
    cd manyfiles
    for n in {1..1000}; do
        dd if=/dev/urandom of=file$( printf %03d "$n" ).bin bs=1 count=$(( RANDOM + 1024 ))
    done
```    
    This creates 1000 small files of varying sizes.
```
ls -l manyfiles/|head
total 19064
-rw-r--r-- 1 bob_bae bob_bae 19360 Nov 24 22:05 file001.bin
-rw-r--r-- 1 bob_bae bob_bae 26807 Nov 24 22:05 file002.bin
-rw-r--r-- 1 bob_bae bob_bae 15370 Nov 24 22:05 file003.bin
-rw-r--r-- 1 bob_bae bob_bae 10914 Nov 24 22:05 file004.bin
-rw-r--r-- 1 bob_bae bob_bae 23243 Nov 24 22:05 file005.bin
-rw-r--r-- 1 bob_bae bob_bae 24531 Nov 24 22:05 file006.bin
-rw-r--r-- 1 bob_bae bob_bae  6089 Nov 24 22:05 file007.bin
-rw-r--r-- 1 bob_bae bob_bae 31778 Nov 24 22:05 file008.bin
-rw-r--r-- 1 bob_bae bob_bae 17713 Nov 24 22:05 file009.bin
```    
 9. copy the many small files from step 8 above to bobtest1 bucket using gcsfuse
 ```
     time cp manyfiles/* tmpmnt/
     real	10m24.300s
     user	0m0.038s
     sys	0m0.273s
 ```    
 10. remove the many small files from step 9 above
 ```
      time rm tmpmnt/*
      real	2m36.128s
      user	0m0.021s
      sys	0m0.115s
 ```     
  11. copy the many small files from step 8 above to bobtest1 bucket using gsutil
  
 ```
     time gsutil cp manyfiles/* gs://bobtest1/
      Operation completed over 1.0k objects/16.6 MiB.                                  

      real	4m49.090s
      user	0m16.443s
      sys	0m1.647s
  ```    
  12. remove the many small files from step 11 above
  ```
      time gsutil rm gs://bobtest1/*
      Operation completed over 1.0k objects.                                           

      real	2m22.183s
      user	0m3.334s
      sys	0m0.572s
  ```   
  13.  Removal of 1000 small files take about the same amount of time for both gsutil and gcsfuse cases.
       Copying 1000 small files is about twice as slow for gcsfuse case.  Gsutil is still the faster case here.
