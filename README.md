# File System Utilities
Supports common use cases such as directory/file searches 

## Overview
This is a project in the early stages that can be used to manage all of your digital content. 
Currently, it's limited to just copying files from one directory to another, but it will automatically organize
content based into a folder hierarchy (YYYY --> YYYY-MM). This could easily be changed in the util.py module.

## Usage
Step 1. Run main.py
Step 2. Enter source directory
Step 3. Enter destination directory

The duration of the program may depend on several factors such as the number of files and the speed of the disk/storage
media being used. It is intended currently for photos, videos, and audio files but will copy other types of files
in their original folder structure. Duplicates will be ignored if there is a high certainty that the file is an exact 
match with an existing file in the destination folder. Still doing tests to ensure this is working.


