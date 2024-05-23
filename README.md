# Advanced-ToolBox-for-LD - V5 (Previously Advanced Search)

<H2>Overview</H2><br>
It will allow you to copy the LD data to your CRDB and then be able to search across projects, environments, and flags.<br>
A video with the UI flow @"Adv Srch for LaunchDarkly quick overview.mp4" overview video <BR>
<H4>V2</H4>Adds cost allocation functionality shown on the home page. Cost can be assigned per department. Adding customers and departments is done manually directly on the DB by importing the data from your records to the CRDB tables. <BR>
<H4>V3</H4>Adds Data copy from CRDB to a new LaunchDarkly Subscription. <BR>
<H4>V4</H4>Adds a standalone tool to copy Segments across Projects and Subscriptions. the tool is not yet integrated into the UI and runs on the command-line<BR>
Adds a way to receive real-time status "Server-Sent-Events" from the backend to the frontend while long-running transactions are running the backend.<BR>
<H4>V5</H4>Adds Data copy from CSV file* to a project in a LaunchDarkly Subscription. <BR>

<h2> Technology</h2><br>
Backend: built on Python 3.10 or above<br>
Frontend: build on JS<br>
Database: SaaS CRDB instance<br>

<H2>Entry points for the project</H2>
"Python3 runEntLDTools.py" is the entry point for running the Python server and setting an HTTP server for the HTML files.<br>
"http://localhost:8080/index.html" is the entry point for the front end<br>

<H2>Notes</H2><br>
<UL>
  <LI>The first time you run the application (HTTP://...) you will need to create a user profile which will create a settings file on the Python App root directory </LI>
  <LI>The Settings file is encryped</LI>
  <LI>Please make sure you have installed locally (PIP3 ....) all the Python libraries used for the backend (requirements.txt)</LI> 
  <LI>Example CSV Upload Structure.xlsx, you use this file to add the flags that will be imported and then export the file to CSV.</LI>
</UL>

<H2>Dependencies</H2>
<UL>
  <LI><B>Python Data Access Library:</B> https://www.psycopg.org/docs/index.html</LI>
  <LI><B>JS UI Library: </B>https://demos.themeselection.com/sneat-bootstrap-html-admin-template/documentation/index.html</LI>
  <LI><B>Charts Library: </B>https://apexcharts.com/docs/methods/#updateOptions</LI>
  <LI><B>Cockroach DB (CRDB):</B>https://cockroachlabs.cloud/</LI>
</UL>
