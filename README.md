# University Domains and Names Data List & API

Do you need a list of universities and their domain names? You found it!

This package includes a JSON file that contains domains, names and countries of most of the universities of the world.

Example usecases:
- You can create a validation script that checks the email domain.
- You can automatically generate a user's country and university by looking at their emails.

You can use this data source in three ways:

- Use the JSON file as your data source and do whatever you like with your favourite programming language.
- Use free hosted-API.
- Use the tiny Python app to serve a fast API that you can query data.


### 1 - Using the Data Source

The whole data source is located in the `world_universities_and_domains.json` file. It is just a list of dictionaries in the following format:

    [
    	...
    	{
    	    "alpha_two_code": "TR",
    	    "country": "Turkiye",
    	    "state-province": null,
    	    "domains": [
    	        "sabanciuniv.edu",
    	        "sabanciuniv.edu.tr"
    	    ],
    	    "name": "Sabanci University",
    	    "web_pages": [
    	        "http://www.sabanciuniv.edu/",
    	        "http://www.sabanciuniv.edu.tr/"
    	    ],
    	},
    	...
    ]

If you want a smaller final payload and only need a subset of countries, run

```bash
filter.py $country1 [Optional: $country2]
```

from the root directory to return

```
filtered_world_universities_and_domains.json
```

NOTE: Some universities use a format like `[user]@[department].[domain]`, but this list only contains the `[domain]` portion.
For example, an email address might be `[student]@cs.usc.edu`, and this list will contain 'usc.edu', the domain for the
University of Southern California. Take this into consideration if using this list for email address validation.

### 2 - Using The Hosted API

This is the easiest method if you're making a small project or just want to discover the data without any hassle.
It is sponsored by [Hipo](http://www.hipolabs.com) and free. If you have a big project, please host it on your own server.

Some example searches:

- http://universities.hipolabs.com
- http://universities.hipolabs.com/search?name=middle
- http://universities.hipolabs.com/search?name=middle&country=turkiye

The hosted API uses [university-domains-list-api](https://github.com/Hipo/university-domains-list-api) package.

### 3 - Using the built-in API on your server

You can access the python API via [university-domains-list-api](https://github.com/Hipo/university-domains-list-api)

# Contribution

Please contribute to this list! We need your support to keep this list up-to-date.
Do not hesitate to fix any wrong data. It is extremely easy. Just open a PR, or create an issue.

# Contributors

- Yiğit Güler
- Tuna Vargı
- Patrick Michelberger
- Rasim Demirbay
- Ryan White
- Bilal Arslan
- anwilli5
- Thomas Bauer
- Emin Mastizada
- Ceyda Duzgec
- Jai
- Jimi Ford
- Lars Schwegmann
- Sedat Karancı
- Charles Bedrosian
- Harrison Lo
- mattdfloyd
- Ender Ahmet Yurt
- Enis Behiç Tuysuz
- Syed Zakawat
- Daksh Shah
- Maizer Gomes
- Denys Vitali
- Ary Wibowo
- Matt Floyd
- Joris Boquet
- Konstantin Ladutenko
- Romain Odeval
- remediate
- Errorific
- summerplaybook
- hamedty
- Sedat
- Sotirios Roussis
- majilesh
- Itay Grudev
- luungoc2005
- Ajithkumar Sekar
- Christopher Chen
- Dimitris Karakostas
- Chun Fei Lung
- Mamat Rahmat
- Wisnu Adi Nurcahyo
- jvanstraten
- Ekin Dursun
- Kevin Bohinski
- Lachlan Marnham
- Baptiste Pellarin
- Kelian Baert
- [more](https://github.com/Hipo/university-domains-list/graphs/contributors)

### Created and maintained by [Hipo](http://www.hipolabs.com)
