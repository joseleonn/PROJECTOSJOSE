function getCitiesFromLocalStorage() {
    let cities = localStorage.getItem("CITIES");
    if (cities) {
        cities = JSON.parse(cities);
    } else {
        cities = [];
    }
    return cities;
}

function addNewCityToLocalStorage() {
    let ciudades = document.getElementById("agregarCiudad").value;
    console.log(ciudades);
    let cities = getCitiesFromLocalStorage();
    let validacion = llamarApi(ciudades);
    
    
    if (cities.includes(ciudades)) {
        document.getElementById("item").innerHTML = ("La ciudad agregada ya se encuentra almacenada");
        item.style.display = "Block";
        item.style.background = "#ffc107";
    }
    else{
        cities.push(ciudades);
        localStorage.setItem("CITIES", JSON.stringify(cities));
        document.getElementById("item").innerHTML = ("Ciudad agregada con exito");
        item.style.display = "Block";
        item.style.background = "#28a745";
    }

    if (validacion == false) {
        document.getElementById("item").innerHTML = ("Error: no se pudo llamar a la API. ");
        item.style.display = "Block";
        item.style.background = "#dc3545";
    }
}

async function llamarApi(ciudades) {
        try {
            let url = "https://api.openweathermap.org/data/2.5/weather?q="+ciudades+"&appid=252c74ef0a3d20796b391de13b392cdb&units=metric&lang=es";
            respuesta = await fetch(url);
            datos = respues.json();
            console.log(datos);
            console.log(datos.main.temp);

        } catch (error) {
            console.error(error);
            dato = false
            return false;
        }
}

