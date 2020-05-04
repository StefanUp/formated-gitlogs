# import all stuff
import os
import sys
import time
import datetime
import subprocess

params = sys.argv
date = ""

if (len(params) > 1):
    
    # date from param - format "%d/%m/%Y"
    dateParam = params[1]
    isValid = True

    try:
        day,month,year = dateParam.split("/")
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        isValid = False    

    if isValid is False:
        print("Format must be 'DD/MM/YYYY'")    
    else:
        date = time.mktime(datetime.datetime.strptime(dateParam, "%d/%m/%Y").timetuple())

class CMD:
    hash = "%H"
    branch = "%d"
    commit = "%B"
    userName = "%aN"
    userEmail = "%ae"
    committerDate= "%ct" # committer date (unix timestamp)
    gitLog = "git log --format="
    delimiter = "---DELIMITER---"

    def script(self):
        return self.gitLog + "USERNAME" + self.userName + "USEREMAIL" + self.userEmail + "COMMITHASH" + self.hash + "COMMITCOMMENT" + self.commit + "COMMITBRANCH" + self.branch + "COMMITDATE" + self.committerDate + self.delimiter

def write():
    # write branch
    branch = commit[(commit.find('COMMITBRANCH')+13):]
    if branch: releaseNotes.write("# " + commit[(commit.find('COMMITBRANCH')+12):] + "\n")

    # write name + email
    releaseNotes.write("## Autor: " + commit[(commit.find('USERNAME')+8):commit.find('USEREMAIL')] + " - " + commit[(commit.find('USEREMAIL')+9):commit.find('COMMITHASH')] + "\n")
                            
    # write hash
    releaseNotes.write("** Hash: " + commit[(commit.find('COMMITHASH')+10):commit.find('COMMITCOMMENT')] + "\n")

    # write comment - splitlines function because in commit is sometimes new line 
    releaseNotes.write("** Commit: " + ' '.join(commit[(commit.find('COMMITCOMMENT')+13):commit.find('COMMITBRANCH')].splitlines()) + "\n")

    # write commit date
    releaseNotes.write("** Date: " + time.ctime(int(commit[(commit.find('COMMITDATE')+10):])) + "\n")
    releaseNotes.write("\n")

# run command
cmd = CMD()
cmdOutput = subprocess.getstatusoutput(cmd.script())

# check if no error - 0 == noError
if cmdOutput[0] == 0:

    # format output from git
    output = cmdOutput[1].split("---DELIMITER---")
    
    # create release notes file
    releaseNotesName = "release-notes-" + str(datetime.datetime.now().date()) + ".md"

    # check if file exists
    if not os.path.exists(releaseNotesName): 
        os.system("touch " + releaseNotesName)
    else:
        os.system("rm " + releaseNotesName)   

    # write output into release notes file
    with open(releaseNotesName, 'a') as releaseNotes:
            for commit in output:
                if (commit):
                    if date:
                        if date <= int(commit[(commit.find('COMMITDATE')+10):]):
                            write()
                    else:
                        write()

else:
    print("Sorry, something went wrong. " + cmdOutput[1])





