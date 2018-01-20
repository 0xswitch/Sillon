Sillon
------

This project was created in the context of python class while my studies. I wanted to do something usefull for CTF challenge


#### What does it do :
* Scrapping the website looking for link leading to new page of the site
* Harversting informations from the HTML :
  * HTML forms
  * PHP errors
* Fuzzing found attack vectors like forms, url and HTTP headers
* to be completed


##### Compulsory parameters :
* __--url URL__ : the url of the site which must be scanned

##### optionals parameters :
* __--default_page index.php__ : where index.php is the default index page of the server, default is index.php
* __--recursive__ integer : Define the recurisivity level, default is -1 which mean infinity
* __--alias__ alias,separated : Define allowed alias for host (127.0.0.1 / localhost / ..)
* __--remove__ word,forbidden : Forbid word in link (the link will NOT be saved)
* __--timeout__ : Specify request timeout
* __--max_retries__ : Specify max retries for request
* __--stop__ : Ask if the script must continue even if an attack vector is found

##### display parameters:
* __--fields__ fields,comma,separated : specify which fields will be displayed
* __--excluded__ fields,comma,separated : remove theses fields from default fields list
* __--verbose__ : Enable verbose
* __--debug__ : Display errors
* __--p__ : Display parameters
* __--hide__ : Hide output

___

##### Thank you
Do not hesitate to report bug or any new idea, I will be glad to implement it

[My personnal web site : 0xswitch.fr](https://0xswitch.fr)