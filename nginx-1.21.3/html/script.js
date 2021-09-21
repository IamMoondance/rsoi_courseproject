function checkAuth() {
    //Читаем куки
    authCookie = getCookie("Authorization");
    if(authCookie == "")
    {
        window.location.replace("/signin.html");
    }
    return authCookie;
}

function redirectToHome(){
    window.location.replace("/")
}

function redirectToSignUp() {
    
    window.location.replace("/signup.html")
}

function logout(){
    document.cookie = "Authorization=expired; max-age=-1";
}

function getCookie(cname) {
    let name = cname+'=';
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';')
    for(let i = 0; i < ca.length; i++)
    {
        let c = ca[i];
        while(c.charAt(0) == ' ')
        {
            c = c.substring(1);
        }
        if(c.indexOf(name) == 0)
        {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

async function cancelRental(rentalUid)
{
    authheader = getCookie("Authorization")

    response = await httpRequest('/gateway/rental/'+rentalUid, 'DELETE', {}, {Authorization: 'Bearer '+authheader});
    if(response.ok)
    {
        window.location.replace("/myrentals.html");
    }
    else
    {
        let error = await response.json()
        document.getElementById('errormsg').innerHTML=error["Message"];
    }
}

async function finishRental(rentalUid)
{
    authheader = getCookie("Authorization")

    response = await httpRequest('/gateway/rental/'+rentalUid, 'PATCH', {}, {Authorization: 'Bearer '+authheader});
    if(response.ok)
    {
        window.location.replace("/myrentals.html");
    }
    else
    {
        let error = await response.json()
        document.getElementById('errormsg').innerHTML=error["Message"];
    }
}

async function fillRentalTable()
{
    authheader = getCookie("Authorization")
    response = await httpRequest('/gateway/rental', 'GET', {}, {Authorization: 'Bearer '+authheader});
    json_response = await response.json()
    var table = document.getElementById("rentaltable");
    for (i in json_response)
    {
        var row = table.insertRow(-1);
        var cell1 = row.insertCell(-1);
        var cell2 = row.insertCell(-1);
        var cell3 = row.insertCell(-1);
        var cell4 = row.insertCell(-1);
        var cell5 = row.insertCell(-1);
        var cell6 = row.insertCell(-1);
        var cell7 = row.insertCell(-1);
        var cell8 = row.insertCell(-1);
        cell1.innerHTML = json_response[i]["car"];
        cell2.innerHTML = json_response[i]["rent_from"];
        cell3.innerHTML = json_response[i]["rent_until"];
        cell4.innerHTML = json_response[i]["office"];
        cell5.innerHTML = json_response[i]["price"];
        cell6.innerHTML = json_response[i]["status"];
        cell7.innerHTML = "<button id='fbtn" + i + "' class=\"btn \" style=\"background-color:#c2847a; color:#280003;\"'>Завершить</button>";
        cell8.innerHTML = "<button id='cbtn" + i + "' class=\"btn \" style=\"background-color:#c2847a; color:#280003;\"'>Отменить</button>";

    }
    for(let i in json_response)
    {
        let id = json_response[i]["rental_uid"];
        finishButton = document.getElementById("fbtn"+i)
        finishButton.addEventListener('click', function (){
            finishRental(id);
        })
        cancelButton = document.getElementById("cbtn"+i)
        cancelButton.addEventListener('click', function (){
            cancelRental(id);
        })
    }
}

async function fillRentLocation() {
    authheader = getCookie("Authorization")
    officeUid = getParameterByName("officeUid",document.URL)
    response = await httpRequest('/gateway/offices/'+officeUid, 'GET', {}, {Authorization: 'Bearer '+authheader});
    json_response = await response.json()
    p_location = document.getElementById("location")
    p_location.innerHTML = json_response["location"]
}

async function fillCarList() {
    authheader = getCookie("Authorization")
    officeUid = getParameterByName("officeUid",document.URL)
    response = await httpRequest('/gateway/cars/'+officeUid, 'GET', {}, {Authorization: 'Bearer '+authheader});
    json_response = await response.json()
    carlist = document.getElementById("carlist")
    for (let i in json_response){
        let opt = document.createElement('option');
        opt.value = json_response[i]["carUid"];
        opt.innerHTML = json_response[i]["brand"]+" "+json_response[i]["car_model"];
        carlist.appendChild(opt);
    }
}


async function fillOfficesTable() {
    authheader = getCookie("Authorization")
    response = await httpRequest('/gateway/offices', 'GET', {}, {Authorization: 'Bearer '+authheader});
    offices_json = await response.json()
    var table = document.getElementById("officestable");
    for (i in offices_json)
    {
        var row = table.insertRow(-1);
        var cell1 = row.insertCell(-1);
        var cell2 = row.insertCell(-1);
        cell1.innerHTML = offices_json[i]["location"];
        cell2.innerHTML = "<a style='color:#280003;' href=\"rental.html?officeUid="+offices_json[i]["officeUid"]+"\">Заказать в этом офисе</a>";
    }
}

async function fillCarsTable() {
    authheader = getCookie("Authorization")
    response = await httpRequest('/gateway/cars', 'GET', {}, {Authorization: 'Bearer '+authheader});
    cars_json = await response.json()
    var table = document.getElementById("carstable");
    for (i in cars_json)
    {
        var row = table.insertRow(-1);
        var cell1 = row.insertCell(-1);
        var cell2 = row.insertCell(-1);
        var cell3 = row.insertCell(-1);
        var cell4 = row.insertCell(-1);
        var cell5 = row.insertCell(-1);
        cell1.innerHTML = cars_json[i]["brand"];
        cell2.innerHTML = cars_json[i]["car_model"];
        cell3.innerHTML = cars_json[i]["power"];
        cell4.innerHTML = cars_json[i]["car_type"];
        cell5.innerHTML = cars_json[i]["price_per_hour"];
    }
}

async function newRental(){
    authheader = getCookie("Authorization")
    let data = {
        'officeUid':getParameterByName("officeUid",document.URL),
        'carUid':document.getElementById('carlist').value,
        'rent_from':document.getElementById('rent_from').value,
        'rent_until':document.getElementById('rent_until').value
    }
    response = await httpRequest('/gateway/rental', 'POST', data, {Authorization: 'Bearer '+authheader});
    if(response.ok)
    {
        window.location.replace("/");
    }
    else
    {
        let error = await response.json()
        document.getElementById('errormsg').innerHTML=error["Message"];
    }
}

async function signUp() {
    let data = {
            'login':document.getElementById('loginfield').value,
            'password':document.getElementById('passwordfield').value,
            'name':document.getElementById('namefield').value,
            'surname':document.getElementById('surnamefield').value,
            'patronymic':document.getElementById('patronymicfield').value
    }
    response = await httpRequest('/gateway/signup', 'POST', data, {});
    if(response.ok)
    {
        window.location.replace("/signin.html");
    }
    else
    {
        let error = await response.text()
        document.getElementById('errormsg').innerHTML=error;
    }
}

async function signIn() {
    let data = { 
            'login':document.getElementById('loginfield').value,
            'password':document.getElementById('passwordfield').value
    }
    base = btoa(data['login']+":"+data['password']);
    response = await httpRequest('/gateway/signin', 'GET', {}, {Authorization: 'Basic '+base});
    body = await response.text();
    if(response.status==200)
    {
      document.cookie = 'Authorization='+body+"; max-age=3600";
      document.getElementById('errormsg').innerHTML = "";
      redirectToHome();
    }
    else if(response.status==404)
    {
      document.getElementById('errormsg').innerHTML="Неверный логин и/или пароль"
    }
    else
    {
      document.getElementById('errormsg').innerHTML="Неизвестная ошибка"
    }
}

async function httpRequest(url = '', type = '', data = {}, extraHeaders = {}, ) {
    // Default options are marked with *
    let object = {
      method: type, // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {...{
        'Content-Type': 'application/json'
        },
        ...extraHeaders
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer' // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
       // body data type must match "Content-Type" header
    }
    if(type!='GET')
    {
      object = { ...object, ...{body: JSON.stringify(data)}};
    }
    const response = await fetch(url, object);
    return response; // parses JSON response into native JavaScript objects
  }

  function getParameterByName(name, url) {
        if (!url) url = window.location.href;
        name = name.replace(/[\[\]]/g, '\\$&');
        var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
            results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, ' '));
    }