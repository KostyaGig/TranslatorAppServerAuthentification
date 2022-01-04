
<h1>Translator App Server</h1>

**Base url**: https://uehuf.pythonanywhere.com

<h2>Features</h2>

<h3>1. Authentication on server</h3>

<h4>Start with register user in system<h4/>

For register user in system he must enter yours number phone and name.
<br/><br/>If user with entered number phone not found in database then notify our user about  success register in system, also return him unique key,in order to sent his when we will make request on server 
Otherwise we notify our user about failure auth in system and sent him error message

<h4>Login user in system</h4>

Two cases for login user in system

1. Login by generated unique id

    Our android app must store unique id in local storage. This is unique id user gets from server after success register or login. 
    <br/><br/>When we launch our app we make request on server for send our unique id.<br/> If unique id will be find in database then we navigate our user on main screen app. <br/>If our unique id will be lost, we may suggest user second way for login in system<br/><br/>
2. Login by number phone user and his name 
    If our unique id will be lost (cache was cleared or our unique id will be lost the occurs ) we should use in this way for login in system.
    <br/>When we make request on server for login in system then should put name and phone number (already exist user).
    <br/>If our number and phone same with number and form which persist in remote database then return unique id user for further fast login in system 
    
<h3>2. Synchronization local and remote words</h2>
User can use our app without auth in there.
\n We have two situation
1. Translate words in app without auth in system
    Translated words will save to local store on phone
    <br><br>If user want auth in system (success login or register) 
    then all local words which sent before auth will be sent to server.
    <br><br>Server should receive this words and save to remote store
    

3. Translate words when user already authorization in system
    <br><br>Translated word will save on server and save on local db
    <br>Synchronization not needs

**Request**: baseUrl/syncWords/UniqueKey
<br>**Param**: wordsJson
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

**Request**: baseUrl/users/UserName/words
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

**Request**: baseUrl/deleteWords/UniqueKey
<br>**Response**:
``` json
{
    "mark": "Success",
    "message": "Words were deleted"
}
```

<br>2.Delete certain translated word by user unique key

**Request**: baseUrl/deleteWord/UniqueKey
<br>**Param**: translatedWord, **value**: Home
<br>**Response**:
``` json
{
    "mark": "Success",
    "message": "Home deleted"
}
```

<h3>5. Fetch all users which is authorized in system</h3>

**Request**: baseUrl/users
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


**Request**: baseUrl/users/UserName/words
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
