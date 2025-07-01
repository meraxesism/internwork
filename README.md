So these are just the engine scripts, couldn't add the whole thing because the whole thing is 6.3 gb
To put it simply, ive created a virtual environment where all packages and dependencies are present (5.5 gb)
and created detectronv2 from scratch because the original downloadable version did not support windows, built it using visual studio build tools and git repos
this project does everything automatically by first converting ur pdf to image, running detectron on it to detect the layout and then store it in .json file.....................Then running paddle ocr to detect text blocks in it...............Then extraction of tables 
which is in progress.

So far it has succeded very prominently.
