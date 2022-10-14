# notes and documentation of this app

we have two main apps here profiles which handles user related operations
and posts which handles all the posts related operations 

## Installation

covered in the readme.md file 

## load testing 
load testing was done using locust.py the reports are in the root directory of this porject under the names 
### "news_feed load test report.HTML" 
and 
### "news_feed load test report.csv"

you can also rerun the test but navigating to the root dir of the project and 

```bash
locust -f locust.py --host http://127.0.0.1:8080/ --users 100 --spawn-rate 50
```

## storage

I have chosen sqllite3 because its light and we can embed it in the folder  for easier testing 

## notes 
i used function based views  because it gives me more control and can show you my work better 

i could have used django-filters to do the filtering but i think its easier that way a

you will need a .env file which is provided via email


## License
[by khaled yasser](kikokhaled.u@gmail.com)