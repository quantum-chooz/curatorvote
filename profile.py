import requests
import re
import time
from bs4 import BeautifulSoup
from auth import authentication
import json

# declares variables
username = 'chooz'
sleep = 30

# calls authentication
s, headers = authentication()

# posts a comment for um just verifying it's working I guess
#r = s.post("https://scratch.mit.edu/site-api/comments/user/chooz-eets/add/", headers=headers, data=json.dumps({"content": "void", "parent_id": "", "commentee_id": ""}))
#print(r.status_code)

# parses the most recent page of comments on the profile
html = s.get("https://scratch.mit.edu/site-api/comments/user/" + username + "/?page=1").text
soup = BeautifulSoup(html, "html.parser")
comments = soup.find_all("div", class_="comment")

while True:

    # just moves on to wait again if there are no comments matching the criteria
    if (len(comments) == 0):
        print('there are no comments here wonko')
        pass

    else:
        # loops through all the matching comments
        for i in comments:
            content = soup.find_all("div", class_="content")
            # if the comment contains /vote
            # deletes the comment
            r = s.post("https://scratch.mit.edu/site-api/comments/user/chooz-eets/del/",data=json.dumps({"id":i["data-comment-id"]}),headers=headers)

            # outputs the comment info
            print(r.status_code)
            print("#" + i["data-comment-id"])
            print("@" + i.find(class_="name").text.strip() + ":")
            print(" ".join(i.find(class_="content").text.split()))
            print("")

            time.sleep(5)

    time.sleep(sleep)
