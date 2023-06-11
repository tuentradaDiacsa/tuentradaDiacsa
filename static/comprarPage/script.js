ScrollReveal().reveal('.header', { delay: 1000 });
ScrollReveal().reveal('#tituloPrincipal', { delay: 1000 });
ScrollReveal().reveal('#subTitulo1', { delay: 1000 });
ScrollReveal().reveal('.horizontal-line', { delay: 1000 });
ScrollReveal().reveal('#containerEntradas', { delay: 1000 });

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
    }*/
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

    $.ajax({
        type: 'POST',
        url: '',
        data:
        {
            'boton': 'sms',
            'celular': $("#celular").val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function () {
            console.log(response);
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