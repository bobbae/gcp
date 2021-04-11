# Challenge:  Longest-compound words

* First read the `Basic rules for challenges` (https://github.com/bobbae/gcp/blob/main/challenges/README.md). 
* Summary: Write a program that reads a file containing a sorted list of words (one word per line, no spaces, all lower case), 
then identifies the longest word in the file that can be constructed by concatenating copies of shorter words also found in the file.
* For example, if the file contained:

```
       cat
       cats
       catsdogcats
       catxdogcatsrat
       dog
       dogcatsdog
       hippopotamuses
       rat
       ratcatdogcat
```

The answer would be 'ratcatdogcat' - at 12 letters, it is the longest word made up of other words in the list. 

* The program should then go on to report how many of the words in the list can be constructed of other words in the list.
* The program should read the words from https://gist.github.com/bobbae/4ca309a1857158d5766d4ede4235cae0 
* There are many solutions to this problem in github and elsewhere. We expect a new answer constructed by you from scratch.
* Speed matters. Your solution's algorithm and execution speed in finding the answer matters. For example,  if your program takes more than  one minute on a modern consumer grade laptop to produce the answers, your code needs to be revised.
* Provide the answer (the longest compound word) in your README file.
