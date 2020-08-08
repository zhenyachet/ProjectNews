# ProjectNews
Project with some features with rss-feeds


#How to install
1) Clone the project to you own project directory
2) Install requirements file from "News" directory:
pip install -r requirements.txt
3) Run project:
python manage.py runserver
4) http://127.0.0.1:8000/ - open your local server (8000 - is port by default)

# About app
There are 3 endpoints:
 - /NewsApp/ - represents 2 lists of sportnews from BBC.com and CNN.com
 - /NewsApp/rss - contains of text edit and button GO. Represents list of news form your rss feed. 
 Trere is one more button "Save to my favourites", but I'm going to build up my application soon =).
 - /NewsApp/resources - represents list of bootstrap cards which contains of images, short descriptions and links of rss. 
