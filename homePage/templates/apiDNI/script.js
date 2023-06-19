function enviarCosas() {
    $.ajax({
        type: 'POST',
        url: 'https://5942-102-38-204-8.ngrok-free.app/v1/reniec/prueba',
        headers: {
            'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlZtMTBVMUV4VlhoVGJrNVNZa1Z3VWxaclVrSlBVVDA5Iiwic2Vzc2lvbiI6Ijc4OTA5ZjBmLTBkYmEtNDE5NC04NDAxLTUyZDhjYmM2NTE4Mi44MGIwZDQ2NS0xNzkxLTQ4YjQtODMyZC0wMWVhMTM5MWY3OWIiLCJleHAiOjE2ODcyMTgzNjh9.nx9O1eCavw3hQMIMy0bAJzc1KxOJTup6CzXFeaXBgeLMczHXU9MgTviaHx9Zuj05PfygB5xMnc1pM3Ue86yUNw',
            'Content-Type': 'application/json',
        },
        data: JSON.stringify({ 'dni': document.getElementById("dni").value.toString() }),
        dataType: 'json',
        success: function (response) {
            if (response.message == "found data") {
                console.log(response.result)
                document.getElementById("resultado1").innerText = "A. Materno: " + response.result.apeMaterno
                document.getElementById("resultado2").innerText = "A. Paterno: " + response.result.apePaterno
                document.getElementById("resultado3").innerText = "Departamento nac.: " + response.result.departamento_nacimiento
                document.getElementById("resultado4").innerText = "Ultimo digito: " + response.result.digitoVerificacion
                document.getElementById("resultado5").innerText = "Distrito nac.: " + response.result.distrito_nacimiento
                document.getElementById("resultado6").innerText = "Fecha nac.: " + response.result.feNacimiento
                document.getElementById("resultado7").innerText = "Numero DNI: " + response.result.nuDni
                document.getElementById("resultado8").innerText = "Nombres: " + response.result.preNombres
                document.getElementById("resultado9").innerText = "Provincia nac.: " + response.result.provincia_nacimiento
                document.getElementById("resultado10").innerText = "Sexo: " + response.result.sexo
            }
            else {
                document.getElementById("resultado1").innerText = "No encontrado"
                document.getElementById("resultado2").innerText = ""
                document.getElementById("resultado3").innerText = ""
                document.getElementById("resultado4").innerText = ""
                document.getElementById("resultado5").innerText = ""
                document.getElementById("resultado6").innerText = ""
                document.getElementById("resultado7").innerText = ""
                document.getElementById("resultado8").innerText = ""
                document.getElementById("resultado9").innerText = ""
                document.getElementById("resultado10").innerText = ""
            }
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error
            console.error('Error:', error);
        }
    });
}