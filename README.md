
<h1>Translator App Server</h1>

<h2>Features</h2>

<h3>1. Authentication on server</h3>

<h4>Register user in system<h4/>

For the registration user in system he needs to enter his number phone and name.
<br/><br/>If user with enterred data hasn't existed yet then notify user about a success registration  in the  system, also return him an unique key that will be used for future requests to the server
If wroted number phone by user has already existed then we notify user about a failure registration in the  system and navigate him to the login screen

<h4>How to Login user in the system?</h4>

We have a two cases login user to system

1. Login by generated unique id

    [TranslatorApp](https://github.com/KostyaGig/TranslatorApp) is storing unique id in local storage. It unique id user got from server after success register or login. 
    <br/><br/>When we launch app then do request on server and send unique id.<br/> If unique id will be find in the server database then we navigate  user to main screen app. <br/>If unique id is lost, we can use the second case<br/><br/>
2. Login by number phone and user name
    If unique id is lost (cached data on device is cleared) we can use in this way for login to system.
    <br/>When we this request we will should to send name and phone
    <br/>If user sent correctly data(wrote name and number phone was founded in the server database) then server will send unique id for further communication with server
    
<h3>2. Synchronization local and remote words</h2>
User can use our app without auth there.
\n We have two cases:
1. Translate words in app without auth in system
    Translated words will be save to local storage on user device
    <br><br>If user will want to auth in system(register or login to account)
    then all words on user device will be send to server for synchronization.
    <br><br>Server will need to receive them and save to remote storage
    

3. Translate words when user already auth in system
    <br><br>Translated words will be save on server and will be cache on user device
    <br>Synchronization not needs

**Request**: ```baseUrl/syncWords/UniqueKey```
<br>**Param**: ```wordsJson```
<br>**Value**:
```json
{
    "words" : [{
        "src":"Ноутбук",
        "translated":"Laptop"
    }, {
        "src":"Кнопка", 
        "translated":"Button"
    }]
}
```
<br>**Response:**
```json
{
    "mark": "Success",
    "message": "Success sync words"
}
```


<h3>3. Fetching user words by his name</h3>

**Request**: ```baseUrl/users/UserName/words```
<br>**Response:**

```json
{
    "user_name": "UserName",
    "user_words": [
        {
            "src": "Ноутбук",
            "translated": "Notebook"
        },
        {
            "src": "Пентхаус",
            "translated": "Penthouse"
        }
    ]
}
```

<h3>4. Delete translated words</h3>
    Two away
<br>1.Delete all translated words by user unique key

**Request**: ```baseUrl/deleteWords/UniqueKey```
<br>**Response**:
``` json
{
    "mark": "Success",
    "message": "Words were deleted"
}
```

<br>2.Delete certain translated word by user unique key

**Request**: ```baseUrl/deleteWord/UniqueKey```
<br>**Param**: translatedWord, **value**: Home
<br>**Response**:
``` json
{
    "mark": "Success",
    "message": "Home deleted"
}
```

<h3>5. Fetch all users which is authorized in system</h3>

**Request**: ```baseUrl/users```
<br>**Response:**
```json
{
    "users": [
        "FirstUser",
        "SecondUser"
    ]
}
```

<h3>6. Fetch all translated word user by his name</h3>


**Request**: ```baseUrl/users/UserName/words```
<br>**Response:**
```json
{
    "user_name": "UserName",
    "user_words": [
        {
            "src": "Дом",
            "translated": "House"
        },
        {
            "src": "Телефон",
            "translated": "Phone"
        }
    ]
}
```

<h2>API</h2>
   
**Base url**: https://uehuf.pythonanywhere.com
