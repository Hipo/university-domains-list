# University Domains and Names Data List & API

Do you need a list of universites and their domain names? You found it! 


This package includes a JSON file that contains domains, names and countries of most of the universities of the world.
 - You can create a validation script that checks the email domain. 
 - You can automatically generate a user's country and university by looking at their emails.

You can use this data source in three ways:
 - Use the JSON file as your data source and do whatever you like with your favourite programming language.
 - Use our free hosted-API.
 - Use the tiny Python app to serve a superfast API that you can query data.


## 1 - Using the Data Source

The whole data source is located in the `world_universities_and_domains.json` file. It is just a list of dictionaries in following format:

	[
		...
		{
		    "alpha_two_code": "TR",
		    "country": "Turkey",
		    "domain": "sabanciuniv.edu.tr",
		    "name": "Sabanci University",
		    "web_page": "http://www.sabanciuniv.edu.tr/"
		},
		...
	]


NOTE: Some universities use a format like `[user]@[department].[domain].edu`, but this list only contains the `[domain]` portion. 
For example, an email address might be `[student]@cs.usc.edu`, and this list will contain 'usc.edu', the domain for the 
University of Southern California. Take this into consideration if using this list for email address validation.

### 2 - Using our Hosted API

This is the easiest method if you're making a small project or just want to discover the data without any hassle.
It is sponsored by [Hipo](http://www.hipolabs.com) and free. If you have a big project, please host it on your own server.

Some example searches:

 - http://universities.hipolabs.com
 - http://universities.hipolabs.com/search?name=middle
 - http://universities.hipolabs.com/search?name=middle&country=turkey


## 3 - Using the built-in API on your server

The package contains a small python project that provides a fast search endpoint. 
You can use it for making an autocomplete for university names or filtering them by country.

### Instalation
	git clone https://github.com/hipo/university-domains-list.git
	pip install -r requirements.txt
	python app.py

# Contribution
Please contribute to this list! We need your support to keep this list up-to-date.
If you see any wrong data, do not hesitate to fix it. It is extremely easy. Just open a PR, or create an issue. 

# Contributors

 - Yiğit Güler
 - Tuna Vargı
 - Patrick Michelberger
 - Barricadenick
 - Rasim Demirbay
 - Ryan White
 - Bilal Arslan
 - anwilli5
 - Thomas Bauer
 - Emin Mastizada
 - Jai
 - Jimi Ford
 - Lars Schwegmann

# [Hipo](http://www.hipolabs.com)
