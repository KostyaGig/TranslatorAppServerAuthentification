<h1>Authentication on server</h1>

<h3>Start with register user in system<h3/>

For register user in system he should enter number phone and own name.
<br/><br/>If such user by number phone not found in database then see user about  success register and return his generated unique id,which here will be persistence in shared preferences for fast auth in app. 

Else we see user about which user with entered number already exist!

<h3>Login user in system</h3>

Two cases login user in system

1. Login by generated unique id

    Our android app should store unique id in shared preferences. This is unique id user will be fetched from server (after success register). 
    <br/><br/>When we launch our app we make request on server and put our unique id.<br/> If unique id will be find in database then we move our user on main screen app. <br/>If our unique id will be lost, we should use second way for login in system<br/><br/>
2. Login by number phone and name user
    If our unique id will be lost (cache was cleared or our unique id will be lost the occurs ) we should use in this way for login in system.
    <br/>When we make request on server for login in system then should put name and phone number (already exist user).
    <br/>If our number and phone same with number and form which persist in remote database then return unique id user for further fast login in system 
    
    
