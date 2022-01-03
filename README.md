
<h1>Translator App Server</h1>

<h2>Features</h2>

<h3>1. Authentication on server</h3>

<h4>Start with register user in system<h4/>

For register user in system he should enter number phone and own name.
<br/><br/>If such user by number phone not found in database then see user about  success register and return his generated unique id,which here will be persistence in shared preferences for fast auth in app. 

Else we see user about which user with entered number already exist!

<h4>Login user in system</h4>

Two cases login user in system

1. Login by generated unique id

    Our android app should store unique id in shared preferences. This is unique id user will be fetched from server (after success register). 
    <br/><br/>When we launch our app we make request on server and put our unique id.<br/> If unique id will be find in database then we move our user on main screen app. <br/>If our unique id will be lost, we should use second way for login in system<br/><br/>
2. Login by number phone and name user
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
    
2. Translate words when user already authorization in system
    <br><br>Translated word will save on server and save on local db
    <br>Synchronization not needs

<h3>3. Fetching user words by his name</h3>

<h3>4. Delete translated words</h3>
    Two away
<br>1.Delete all translated words by user unique key
<br>2.Delete certain translated word by user unique key

