#!/usr/bin/env python2
'''
    iDevice2Folder
    @author Pierre HUBERT 2017

    Copy/move files from a iDevice backup to structured folders

    commands :
    * copy [SRC] [DEST] [INDEX] Copy the data of the backup to structured destination
    * move [SRC] [DEST] [INDEX] MOVE the data from the backup to structured destination (this erase iTunes backup)
    * help Show this help

    [SRC] : The folder of the backup
    [DEST]: Destination folder
    [INDEX]: The CSV file containing the index of Apple backup. This index can be generated using idevicebackup2 program : 
                idevicebackup2 list /path/to/backup/container > index.csv

    NOTE : all the arguments are required
'''

# Required libaries
import sys, os;

# Check what to do
try: action = sys.argv[1];
except: action = "help";

# Show help if required
if(action == "help"):
    print(__doc__);
    exit();

# Check if action exists
if(action != "move") and (action != "copy"):
    print("Invalid command !");
    exit();

# Check if all argument are specified and get them
try: n, l, sourceFolder, destinationFolder, index = sys.argv;
except:
    print("Invalid arguments !");
    exit();

# Check source and destination arguments
if sourceFolder.endswith("/") == False :
    sourceFolder += "/";
if destinationFolder.endswith("/") == False :
    destinationFolder += "/";

# Show info
print("The action '" + action +"' will be done for the followings settings: ");
print("Source folder: " + sourceFolder);
print("Target folder: " + destinationFolder);
print("Index file: " + index);
print("\n");

# Get index content
print("Get and analyse index file...\n\n");
with file(index) as f:
    indexContent = f.read();

# Split list
indexContent = indexContent.replace(", ", ",");
filesList = indexContent.split("\n");

# Process each line
for i in filesList:
    
    # Get required arguments
    fileInfos = i.split(",")

    # We don't want an error
    try:
    #if 1 == 1:
        fileSource = fileInfos[0];
        fileDest = fileInfos[12];

        # Prepare copy/move
        completeFileSource = sourceFolder + fileSource;
        completeFileDest = destinationFolder + fileDest;

        # Check the path isn't empty
        if(fileDest != ""):

            # Get folder container name
            nbSlashDestFolder = completeFileDest.count("/");
            folderContainer = "";
            for i in list(completeFileDest):
                if(folderContainer.count("/") != nbSlashDestFolder):
                    folderContainer += i;

            # Infos...
            print("Processing file from '" + completeFileSource + "' to '" + completeFileDest + "'");
            print("Create the following folder (if required) : " + folderContainer);

            # Create folder
            os.system("mkdir -p '"+folderContainer+"'");

            # Move or copy the file
            if(action == "move"):
                os.system("mv '"+completeFileSource+"' '"+completeFileDest+"'");
            if(action == "copy"):
                os.system("cp '"+completeFileSource+"' '"+completeFileDest+"'");  

            # Done for the file
            print("Done for the file. \n\n");
    
    except:
        print("An error occured while trying to process a file !");

# Message to inform it is done
print("Operation is done !");