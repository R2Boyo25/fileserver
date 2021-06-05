A simple fileserver written in flask. 

Has per-account file storage and can have infinitely nested folders

Requires flask and you need to change the `UPLOAD_FOLDER` (in `f2.py`) to a valid folder on your machine.

The program generates a file called `logins.json` with the contents of:
```
{}
```
(x) Hashes passwords