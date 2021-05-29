A simple fileserver written in flask. 

Has per-account file storage and can have infinitely nested folders

Requires flask and you need to change the `UPLOAD_FOLDER` (in `f2.py`) to a valid folder on your machine.

The program generates a file called `logins.json` with the contents of:
```
{}
```
You can add accounts manually in that file, heres an example:
```json
{
"Name1":"password1",
"Name2":"password2",
"Name3":"password3"
}
```
(Will switch to hashing passwords later on)