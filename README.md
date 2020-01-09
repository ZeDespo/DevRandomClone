# *DevRandomClone*

An emulator of Unix's /dev/random functionality and its processes. 

This replica uses reddit.com/r/all/new as a source of entropy. This specific url is a fire hose of
every new post, regardless of which subreddit (similar to a forum) it originates from. Given the constant stream of
new information, it makes a perfect source to collect noise for random data via hashing.

## Preparing to run the script

1) In order to use Reddit's API, one must have a reddit account. After creating an account, navigate to 
https://www.reddit.com/prefs/apps and create a new app. Click the checkmark that says "script", name the project, and 
point the redirect url to "http://localhost:8080" (in truth, this doesn't matter). Keep this page open as the app name, 
app id, and app secret are on this page.

2) Create a file called *reddit_creds.json* and place it on the same level as *main.py*. Fill it with the following
information: 
```
{
  "username":   "<reddit username>",
  "password":   "<reddit password>",
  "app_id":     "<the personal use script id underneath the app's name>",
  "app_secret": "<the secret key reddit assigned the app>",
  "app_name":   "<the name the developer gave the app>"
}
```

## Running the script

Although you can run main.py with its defaults to simulate /dev/random, there are several flags to use.
- --bytes INT
    - How many bytes to pop from the entropy pool.
    - *NOTE*: To align with unix systems, the largest number accepted for this is 512.
- --chunks INT
    - How many chunks of five posts does the user wish to hash at one time to generate entropy.
- --force INT (0 = False, 1 = True)
    - Emulates the O_NONSTOP flag for /dev/random 
        - If force is false, reads will not occur on the entropy pool when there is not enough entropy available. 
        - If force is true, reads will occur regardless of the entropy pool's resources. If the entropy available is 
            less than the entropy requested, all of the available entropy will be popped. If entropy available is 0, 
            and a read is requested, the EAGAIN flag will raise in the form of an exception.
            

