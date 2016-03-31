University Domains and Names API
=================================

An API and JSON list contains domains, names and countries of most of the universities of the world.
-----------------------------------


Provides a search endpoint you can search for an autocomplete for university name or/and filter by country.

You can easily create a validation script that checks the email domain. You can also automatically generate a user's country and university by looking their emails.

NOTE: Some university use a format like '[user]@[department].[domain]', but this list only contains the [domain] portion. For example, an email address might be [student]@cs.usc.edu, and this list will contain 'usc.edu', the domain for the University of Southern California. Take this into consideration if using this list for email address validation.

Feel free to update the list.

==================================

SEARCH FROM OUR PUBLIC API
-----------------

    http://universities.hipolabs.com
    
    http://universities.hipolabs.com/search?name=middle
    
    http://universities.hipolabs.com/search?name=middle&country=turkey
    
API Search Endpoint
-------------

### Request
    /search?name=Middle


### Response
    [
    {
    web_page: "http://www.meu.edu.jo/",
    country: "Jordan",
    domain: "meu.edu.jo",
    name: "Middle East University"
    },
    {
    web_page: "http://www.odtu.edu.tr/",
    country: "Turkey",
    domain: "odtu.edu.tr",
    name: "Middle East Technical University"
    },
    {
    web_page: "http://www.mtsu.edu/",
    country: "USA",
    domain: "mtsu.edu",
    name: "Middle Tennessee State University"
    },
    {
    web_page: "http://www.mga.edu/",
    country: "USA",
    domain: "mga.edu",
    name: "Middle Georgia State College"
    },
    {
    web_page: "http://www.mdx.ac.uk/",
    country: "United Kingdom",
    domain: "mdx.ac.uk",
    name: "Middlesex University"
    },
    {
    web_page: "http://www.middlebury.edu/",
    country: "USA",
    domain: "middlebury.edu",
    name: "Middlebury College"
    }
    ]

### Request
    /search?name=Middle&country=Turkey


### Response
    [
    {
    web_page: "http://www.odtu.edu.tr/",
    country: "Turkey",
    domain: "odtu.edu.tr",
    name: "Middle East Technical University"
    }
    ]


Run the Project
----------------

- Clone Project 
`git clone https://github.com/vargi/university-domains-list.git`
- Setup and activate your virtual environment
- Install requirements
`pip install -r requirements.txt`
- Run server `python app.py`

-------------------
