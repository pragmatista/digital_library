# Digital Library
A useful everyday tool that is also provides a fun way to learn how to program wiht Python.

## Overview
This is a project I started as a practical way of learning Python by tackling some common every day challenes.
Specifically, I found it difficult to manage/backup all the content for everyone in my family. Combined with multiple computers, 
smart phones, cameras, etc., it has always been challenging to accurately maintain an inventory of all the content
and ensuring that important files were being backed up or archived regularly while avoiding duplication.

Although the project is currently limited to running within the command-line, there is a fairly organized workflow to 
manage libraries, inventories, and train the facial recognition model.

## Features
* Libraries
  * create custom libraries to manage various types of content
* Inventories
  * An inventory is like a collection of files that you associate with a particular library
  * You can easily add/update/delete from the inventory
  * You can find duplicates that may exist in your inventory
* Facial Recognition
  * This project allows you way to train a model and update your inventory with all the name(s) discovered.
  * You can apply the model to an entire inventory (although this can be very slow)


## 


## How to Run
* Run main.py


The duration of the program may depend on several factors such as the number of files and the speed of the disk/storage
media being used. It is intended currently for photos, videos, and audio files but will copy other types of files
in their original folder structure. Duplicates will be ignored if there is a high certainty that the file is an exact 
match with an existing file in the destination folder. Still doing tests to ensure this is working.

![](https://raw.githubusercontent.com/kking423/digital_library/main/readme_resources/media-files-tree-structure.png)
