window.onbeforeunload = function () {
    location.reload(true);
}

ScrollReveal().reveal('.resumenCompraBanner, .containerTodo', {
    delay: 200, // Retraso en milisegundos antes de que aparezca cada elemento
    distance: '50px', // Distancia de desplazamiento desde la posición original
    duration: 800, // Duración de la animación en milisegundos
    easing: 'ease-out', // Curva de animación
});

function miFuncion() {
    if (document.getElementById("comprarBoton")) {
        document.getElementById("comprarBoton").style.backgroundColor = "rgba(217, 103, 139, 0.97)";
        document.getElementById("comprarBotonFinal").style.backgroundColor = "rgba(217, 103, 139, 0.97)";
    }
    else {
        document.getElementById("comprarBoton").style.backgroundColor = "rgba(138, 138, 138, 0.97);";
        document.getElementById("comprarBotonFinal").style.backgroundColor = "rgba(138, 138, 138, 0.97);";
    }

}
setInterval(miFuncion, 500);
function copiarAlPortapapeles(texto) {
    var elementoTemporal = document.createElement('textarea');
    elementoTemporal.value = texto;

    // Asegurarse de que el elemento esté fuera de la vista
    elementoTemporal.style.position = 'absolute';
    elementoTemporal.style.left = '-9999px';

    document.body.appendChild(elementoTemporal);
    elementoTemporal.select();
    document.execCommand('copy');
    document.body.removeChild(elementoTemporal);

    alert('Texto copiado al portapapeles: ' + texto);
}

function confirmar() {
    document.getElementById("boton").value = "confirmarCompra"
    document.getElementById("comprarForm").submit()

}

function donwload(cadena) {
    console.log(cadena.toString())
}
document.getElementById("fechaBotonBanner").addEventListener("click", function () {
    document.getElementById("fechaSinCheck").hidden = true;
    document.getElementById("fechaConCheck").hidden = false;
    if (!document.getElementById("fechaConCheck").hidden) {
        document.getElementById("todoEntradas").style.visibility = "visible";
        document.getElementById("todoEntradas").style.display = "flex";
        document.getElementById("todoEntradas").scrollIntoView({ behavior: "smooth" });
    }
    else {
        document.getElementById("todoEntradas").style.visibility = "hidden";
        document.getElementById("todoEntradas").style.display = "none";

    }
});

document.getElementById("comprarBoton").addEventListener("mouseover", function () {
    if (camposLlenos()) {
        document.getElementById("comprarBoton").style.cursor = "pointer";
        document.getElementById("comprarBoton").style.opacity = "0.8";
    }
});

document.getElementById("comprarBoton").addEventListener("mouseleave", function () {
    // Acciones a realizar cuando el cursor sale del div (hover)
    document.getElementById("comprarBoton").style.cursor = "auto";
    document.getElementById("comprarBoton").style.opacity = "1";
});

document.getElementById("comprarBotonFinal").addEventListener("mouseover", function () {
    if (camposLlenos()) {
        document.getElementById("comprarBotonFinal").style.cursor = "pointer";
        document.getElementById("comprarBotonFinal").style.opacity = "0.8";
    }
});

document.getElementById("comprarBotonFinal").addEventListener("mouseleave", function () {
    // Acciones a realizar cuando el cursor sale del div (hover)
    document.getElementById("comprarBotonFinal").style.cursor = "auto";
    document.getElementById("comprarBotonFinal").style.opacity = "1";
});

function disminuir(id) {
    value = parseInt(document.getElementById("cantidadVisible" + id.toString()).innerText)
    if (value <= 0) return;
    document.getElementById("cantidadVisible" + id.toString()).innerText = (value - 1).toString().padStart(2, '0');
    document.getElementById("cantidadHidden" + id.toString()).value = value - 1;
    calcularTotal();
}
function aumentar(id) {
    value = parseInt(document.getElementById("cantidadVisible" + id.toString()).innerText)
    if (value > 20) return;
    document.getElementById("cantidadVisible" + id.toString()).innerText = (value + 1).toString().padStart(2, '0');
    document.getElementById("cantidadHidden" + id.toString()).value = value + 1;
    calcularTotal();
    document.getElementById("todoObligatorio").style.visibility = "visible";
    document.getElementById("todoObligatorio").style.display = "grid";
    document.getElementById("datosCompradorTexto").style.visibility = "visible";
    document.getElementById("datosCompradorTexto").style.display = "flex";
}
function calcularTotal() {
    var total = 0;
    for (var i = 1; i <= 6; i++) {
        total = total + parseInt(document.getElementById("cantidadHidden" + i.toString()).value) * parseInt(document.getElementById("entradaPrecio" + i.toString()).innerText.substring(4))
    }
    document.getElementById("totalEstatico").innerText = total.toString();
    if (total == 0) {
        document.getElementById("todoObligatorio").style.visibility = "hidden";
        document.getElementById("todoObligatorio").style.display = "none";
        document.getElementById("datosCompradorTexto").style.visibility = "hidden";
        document.getElementById("datosCompradorTexto").style.display = "none";
        document.getElementById("comprarBotonFinal").style.display = "none";
        document.getElementById("comprarBotonFinal").style.visibility = "hidden";
    }
}

function soloNumeros(event) {
    var charCode = event.which ? event.which : event.keyCode;
    if (charCode < 48 || charCode > 57) {
        event.preventDefault();
        return false;
    }
    return true;
}

function enviarSMS() {
    console.log(document.getElementById("celular").value.trim().length)
    if (document.getElementById("celular").value.trim().length !== 9) {
        alert("El número de celular debe tener 9 dígitos.");
        return false; // Evita que el formulario se envíe
    }
    $.ajax({
        type: 'POST',
        url: '/comprar/',  // Reemplaza esto con la URL de tu vista de Django
        data: {
            'boton': 'sms',
            'celularValue': $('#celular').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
            document.getElementById("contenedorCodigo").style.visibility = "visible";
            document.getElementById("contenedorCodigo").style.display = "grid";
            console.log(response);
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error
            console.error('Error:', error);
        }
    });
}

function enviarCodigo() {
    console.log(document.getElementById("codigo").value.trim().length)
    if (document.getElementById("codigo").value.trim().length !== 6) {
        alert("El codigo de verificacion debe tener 6 caracteres.");
        return false; // Evita que el formulario se envíe
    }
    document.getElementById("contenedorPin").style.visibility = "visible";
    document.getElementById("contenedorPin").style.display = "grid";
    document.getElementById("contenedorMedioPago").style.visibility = "visible";
    document.getElementById("contenedorMedioPago").style.display = "grid";
    document.getElementById("contenedorDNI").style.visibility = "visible";
    document.getElementById("contenedorDNI").style.display = "grid";
    document.getElementById("contenedorNombre").style.visibility = "visible";
    document.getElementById("contenedorNombre").style.display = "grid";
    document.getElementById("contenedorPregunta1").style.visibility = "visible";
    document.getElementById("contenedorPregunta1").style.display = "grid";
    document.getElementById("contenedorRespuesta1").style.visibility = "visible";
    document.getElementById("contenedorRespuesta1").style.display = "grid";
    document.getElementById("contenedorPregunta2").style.visibility = "visible";
    document.getElementById("contenedorPregunta2").style.display = "grid";
    document.getElementById("contenedorRespuesta2").style.visibility = "visible";
    document.getElementById("contenedorRespuesta2").style.display = "grid";
    document.getElementById("comprarBotonFinal").style.display = "flex";
    document.getElementById("comprarBotonFinal").style.visibility = "visible";


    $.ajax({
        type: 'POST',
        url: '/comprar/',  // Reemplaza esto con la URL de tu vista de Django
        data: {
            'boton': 'verificar',
            'celular': $('#celular').val(),
            'codigo': $('#codigo').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
            console.log(response);
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error
            console.error('Error:', error);
        }
    });
}
function comprar() {
    if (camposLlenos()) {
        document.getElementById("boton").value = "comprar"
        document.getElementById("comprarForm").submit();
    }

}
function camposLlenos() {
    if (document.getElementById("celular").value.trim().length !== 9) return false;
    if (document.getElementById("codigo").value.trim().length !== 6) return false;
    if (document.getElementById("pin").value.trim().length < 4) return false;
    var opciones = document.getElementsByName("opciones");
    var opcionSeleccionada = "";
    for (var i = 0; i < 3; i++) {
        if (opciones[i].checked) {
            opcionSeleccionada = opciones[i].value;
            break;
        }
    }
    console.log(opcionSeleccionada)
    console.log(parseInt(document.getElementById("totalEstatico").innerText))
    if (opcionSeleccionada !== "Yape" && opcionSeleccionada !== "Plin" && opcionSeleccionada !== "Transferencia") return false;
    if (parseInt(document.getElementById("totalEstatico").innerText) == 0) return false;

    return true;
}

function miFuncion() {
    if (camposLlenos()) {
        document.getElementById("comprarBoton").style.backgroundColor = "rgba(217, 103, 139, 0.97)";
        document.getElementById("comprarBotonFinal").style.backgroundColor = "rgba(217, 103, 139, 0.97)";
    }
    else {
        document.getElementById("comprarBoton").style.backgroundColor = "rgba(138, 138, 138, 0.97);";
        document.getElementById("comprarBotonFinal").style.backgroundColor = "rgba(138, 138, 138, 0.97);";
    }

}
setInterval(miFuncion, 500);

/*

function disminuirFila(fila) {
    var element = document.getElementById("entradasFila" + fila);
    var numero = parseInt(element.innerText);
    if (numero > 0) numero--;
    element.innerText = numero.toString().padStart(2, '0');
    document.getElementById("entradasFilaID" + fila).value = numero
    montoTotal();
}

function aumentarFila(fila) {
    var element = document.getElementById("entradasFila" + fila);
    var numero = parseInt(element.innerText);
    if (numero < 20 && numero < parseInt(document.getElementById("restantesFila" + fila).innerText)) numero++;
    element.innerText = numero.toString().padStart(2, '0');
    document.getElementById("entradasFilaID" + fila).value = numero
    montoTotal();
}

function montoTotal() {
    var total = 0;
    total = parseInt(document.getElementById("entradasFila1").innerText) * parseInt(document.getElementById("montoFila1").innerText.substring(0)) +
        parseInt(document.getElementById("entradasFila2").innerText) * parseInt(document.getElementById("montoFila2").innerText.substring(0)) +
        parseInt(document.getElementById("entradasFila3").innerText) * parseInt(document.getElementById("montoFila3").innerText.substring(0)) +
        parseInt(document.getElementById("entradasFila4").innerText) * parseInt(document.getElementById("montoFila4").innerText.substring(0));
    var element = document.getElementById("montoTotal");
    element.innerText = "S/. " + total.toString();
    var element2 = document.getElementById("monto");
    element2.value = total

    /*if (total > 0) {
        var contenedor = document.getElementById("regionObligatoria")
        contenedor.hidden = false;
    }
    else {
        var contenedor = document.getElementById("regionObligatoria")
        contenedor.hidden = true;
    }
}

function soloNumeros(event) {
    var charCode = event.which ? event.which : event.keyCode;
    if (charCode < 48 || charCode > 57) {
        event.preventDefault();
        return false;
    }
    return true;
}

function medioPagoElegido(checkbox) {
    var element;
    switch (checkbox) {
        case "yapeCheckBox":
            element = document.getElementById("plinCheckBox");
            element.checked = false;
            element = document.getElementById("bcpCheckBox");
            element.checked = false;
            break;

        case "plinCheckBox":
            var element = document.getElementById("yapeCheckBox");
            element.checked = false;
            element = document.getElementById("bcpCheckBox");
            element.checked = false;
            break;

        case "bcpCheckBox":
            var element = document.getElementById("plinCheckBox");
            element.checked = false;
            element = document.getElementById("yapeCheckBox");
            element.checked = false;
            break;
    }
}

function setBotonValue(value) {
    document.getElementById('boton').value = value;
}

function validarCelular() {
    var celularInput = document.getElementById("celular");
    var celularValue = celularInput.value.trim();
    if (celularValue.length !== 9) {
        alert("El número de celular debe tener 9 dígitos.");
        return false; // Evita que el formulario se envíe
    }

    var inputValue = $('#celular').val();
    $.ajax({
        type: 'POST',
        url: '/comprar/',  // Reemplaza esto con la URL de tu vista de Django
        data: {
            'boton': 'sms',
            'celularValue': inputValue,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {
            // Lógica para manejar la respuesta exitosa
            console.log(response);
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error
            console.error('Error:', error);
        }
    });
}

function comprarFunction(value) {
    if (document.getElementById("celular").value.trim().length != 9 ||
        document.getElementById("codigo").value.trim().length != 6 ||
        document.getElementById("pin").value.trim().length < 4 ||
        (!document.getElementById("yapeCheckBox").checked && !document.getElementById("plinCheckBox").checked && !document.getElementById("bcpCheckBox").checked)) {
        alert("Falta completar algun campo");
        return false; // Evita que el formulario se envíe
    }
    for (var i = 1; i < 5; i++) {
        document.getElementsByName("entradaID" + i.toString()).value = i;
        document.getElementsByName("entradasFila" + i.toString()).value = parseInt(document.getElementById("entradasFila" + i.toString()).innerText);
        document.getElementsByName("entradasPrecio" + i.toString()).value = parseInt(document.getElementById("montoFila" + i.toString()).innerText);
    }
    if (document.getElementById("yapeCheckBox").checked) document.getElementById("medioPago").value = 1;
    else if (document.getElementById("plinCheckBox").checked) document.getElementById("medioPago").value = 2;
    else if (document.getElementById("bcpCheckBox").checked) document.getElementById("medioPago").value = 3;
    setBotonValue(value);
    document.getElementById("comprarForm").submit();
}

function successFunction(msg) {
    if (msg.message === 'success') {
        alert('Success!');
        form.reset()
    }
}

function verificarCodigo() {
    var inputValue1 = $('#celular').val();
    var inputValue2 = $('#codigo').val();
    $.ajax({
        type: 'POST',
        url: '/comprar/',  // Reemplaza esto con la URL de tu vista de Django
        data: {
            'boton': 'verificar',
            'celular': inputValue1,
            'codigo': inputValue2,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {
            // Lógica para manejar la respuesta exitosa
            console.log(response);
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error
            console.error('Error:', error);
        }
    });
}
*/
