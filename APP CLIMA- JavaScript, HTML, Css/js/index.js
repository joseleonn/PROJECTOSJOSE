
function addOptions(domElement, cities) {
    var select = document.getElementById("SelecCiudad");

    for (value in cities) {
        var option = document.createElement("option");
        option.text = cities[value];
        select.add(option);
    }
}



function renderWheather(ciudad) {

    document.getElementById("nombreCiudad").innerHTML = (ciudad.name);
    
    document.getElementById("temperatura").innerHTML = ("Temp: " + ciudad.main.temp + "°C");

    document.getElementById("sensacionTermica").innerHTML = ("Sensacion termica: " + ciudad.main.feels_like + "°C");

    document.getElementById("humedad").innerHTML = ("Humedad: " + ciudad.main.humidity + "%");

    document.getElementById("viento").innerHTML = ("Velocidad del viento:  " + ciudad.wind.speed + " km/h");

    document.getElementById("presion").innerHTML = ("Presion: " + ciudad.main.pressure + " P");
}

function fetchWeather(query) {
    ciudad = document.getElementById("SelecCiudad").value;
    console.log(ciudad);
    let url = `https://api.openweathermap.org/data/2.5/weather?q=${ciudad}&appid=252c74ef0a3d20796b391de13b392cdb&units=metric&lang=es`;
                
    fetch(url)
        .then((response) =>{
            console.log("Respuesta JSON");
            return response.json();
        })
        
        .then((data) =>{
            renderWheather(data);
        })
}


let cities = localStorage.getItem("CITIES");
console.log(cities);
cities = JSON.parse(cities)
addOptions("seleccionar_ciudad", cities);
let respuesta = [];
