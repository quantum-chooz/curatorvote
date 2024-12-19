import time
from scratchclient import *

from scratchclient import ScratchSession

# declare variables
wait = 20
candidates = ['@chooz-eets', '@user', '@bob']

# Get user info
print("Enter your username:")
username = input()

print("Enter your password:")
password = input()

# creates session
session = ScratchSession(username, password)
project = session.get_project(1110606932)

# opens file
curators_file = open("curators.txt", "r")
votes_file = open("votes.txt", "a")
invalid_file = open("invalid.txt", "a")

# finds all the curators who have voted
curators = []

# gets the valid curators
line = curators_file.readline()
while line != '':
    curators.append(line)
    line = curators_file.readline()
curators_file.close()

while True:

    curators_file = open("curators.txt", "a")
    votes_file = open("votes.txt", "a")
    invalid_file = open("invalid.txt", "a")

    # declares variables
    votes = [0, 0, 0]

    # deletes all comments
    for comment in project.get_comments(all=True):

        content = comment.content
        author = comment.author
        valid = True

        # checks for /vote
        if content.startswith("/vote ") and valid == True:

            # makes sure they haven't voted before
            if author.lower() not in curators and valid == True:

                # splits up the users
                split = content.split(" ")

                # makes sure split isn't greater than four, means that they voted for too many people
                if len(split) <= 4 and valid == True:

                    split.remove("/vote")

                    # makes sure they are voting for actual candidates
                    print(split)
                    for i in split:
                        print('i' + i)
                        if i.lower() in candidates:
                            votes[split.index(i)] +=1

                        else:
                            valid = False
                            print('not a valid candidate')

                    # makes sure they aren't voting for someone twice
                    print(votes)
                    if 2 not in votes and 3 not in votes and valid == True:

                        # formats the line
                        line = "\n"
                        line += author

                        for i in split:

                            # writes to vote file
                            i = i.strip("@")
                            line += "#" + i

                        # writes the vote file
                        votes_file.write(line)
                        # writes the curator file
                        line = "\n"
                        line += author
                        curators_file.write(line)
                        curators.append(author)

                    else:
                        valid = False
                        print('voted for the same person')
                else:
                    valid = False
                    print('voted for too many people')

            else:
                 valid = False
                 print('voted before')

        else:
             valid = False
             print('/vote not appear')

        # if the comment isn't valid
        if valid == False:

            print(content)
            # formats the line
            line = "\n"
            line += author
            line += '#'
            line += content

            # writes the vote file
            invalid_file.write(line)

        comment.delete()
        print('deleted')
        time.sleep(5)

    curators_file.close()
    invalid_file.close()
    votes_file.close()

    time.sleep(wait)
    print('waiting')
    print(time.localtime())
