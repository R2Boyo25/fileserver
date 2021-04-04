A simple fileserver written in flask. 

Has per-account file storage and can have 1-folder-deep folders

Requires flask and you need to change the `UPLOAD_FOLDER` (in `file.py`) to a valid folder on your machine.

To work you need to make a file called `logins.json` with:
```
{}
```
as the contents (this is due to me using the same server for testing and for me... sorry)
You can add accounts manually in that file, heres an example:
```json
{
"Name1":"password1",
"Name2":"password2",
"Name3":"password3"
}
```
