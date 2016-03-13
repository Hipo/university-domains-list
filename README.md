University Domains and Names List
=================================

A JSON list that contains domains, names and countries of most of the universities of the world.

It is very useful if you are building a web service for students.

You can easily create a validation script that checks the email domain. You can also automatically generate a user's country and university by looking their emails.

NOTE: Some university use a format like '[user]@[department].[domain]', but this list only contains the [domain] portion. For example, an email address might be [student]@cs.usc.edu, and this list will contain 'usc.edu', the domain for the University of Southern California. Take this into consideration if using this list for email address validation.

Feel free to update the list.

Example Bundle
--------------

```bash
{
    "web_page": "http://www.sabanciuniv.edu/",
    "country": "Turkey",
    "domain": "sabanciuniv.edu",
    "name": "Sabancı University"
}
```
