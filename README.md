#OWASP Pyttacker Project

_**Proof of Concept (PoC) creator for Pentesters**_

Most of the time is spent on finding the bad stuff during a Web PenTest, reporting is time consuming and you need to deliver your results as soon as possible, however in the end the one that will need to fix the issue (or push others to do it) will need to really understand the impact of the findings included in a report.
When you show raw Database data from a SQLi it's very visible for your customer that the impact is High, however when the finding need some other factors the impact become more complicated to be demonstrated to non technical people, just a _request_ and _response_ is not enough and how much time are you willing to take in order to create a nice screenshot for being included in your report.

What about using "something" that is the server you mention as 'evil.com' that can be used by the bad guys against your customer's company, even better if you know that the evil server is not that "evil" and you can validate, modify or disable it's contents, would be nice to have "something" for creating nice screen-shots, what about reproducing the finding during that meeting when your are trying to show the impact of your findings, not just a pop-up alert for XSS, what if you show an inoffensive but scaring partial defacement or a javascript keylogger in action.

Sounds good ? If yes then Pyttacker will be an interesting tool for you

Some features:

 * Minimal requirements (Just Python and a Web Browser)
 * Cross-platform
 * Portable
 * Easy Plug-ins Implementation

##Prerequisites
 * Python 2.6 or 2.7

##Installation

Linux:
```
git clone https://github.com/RoblesT/pyttacker.git
```
Windows:

* Download the ZIP file [Here](https://github.com/RoblesT/pyttacker/archive/master.zip)
* Unzip to the desired folder

##Quick Start
You just need two things (Excluding the Prerequisites):

* Start Pyttacker Server
* Use any Web Browser to access the server address

Basically you just need to start the server and then use the interface from your Web Browser that will be automatically opened once pyttacker is started

###Start Pyttacker Server

You can just double click the file _pyttacker.py_ or run it from command line:

```bash
python pyttacker.py
```
Pyttacker Server it's a simple web server that will be used for creating the PoCs so there are cases when the default TCP port  is locked by another tool your using as part of your testing, in that case you can specify the port number:
```bash
python pyttacker.py 9090
```
No worries if you just started the tool and the port is already used by another application since the tool will ask for another port until the process is started or aborted.

###Opening the interface

Once the service is started your default browser will be opened with the Pyttacker interface, by default the URL is:
```
http://127.0.0.1:9090
```

You will find more information about how to use the tool [here](https://github.com/roblest/pyttacker/wiki)
### Project Links:

 * [OWASP Pyttacker Project](https://github.com/roblest/pyttacker)
 * [OWASP](https://www.owasp.org)
 * [OWASP Costa Rica](https://www.owasp.org/index.php/Costa_Rica)
 * [Robles+](https://www.roblest.com) Roblest.com Security & Research


Mario Robles, [OWASP Costa Rica](https://www.owasp.org/index.php/Costa_Rica)
