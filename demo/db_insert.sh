mongoimport --db example --collection people  ./info/user.json
mongoimport --db example --collection users  ./info/valid_user.json
mongo example ./info/db_user.js