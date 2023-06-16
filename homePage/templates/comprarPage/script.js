function showBox(item, action) {
    console.log("OK")
    if (action == "down") {
        console.log(parseInt(document.getElementById("containerEntrada" + item).style.height))
        document.getElementById("downIcon" + item).style.display = "none"
        document.getElementById("upIcon" + item).style.display = "flex"
        document.getElementById("containerEntrada" + item).style.height = "165px"
        document.getElementById("containerBoxes" + item).style.display = "flex"
    }
    else if (action == "up") {
        document.getElementById("downIcon" + item).style.display = "flex"
        document.getElementById("upIcon" + item).style.display = "none"
        document.getElementById("containerEntrada" + item).style.height = "95px"
        document.getElementById("containerBoxes" + item).style.display = "none"
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
    //console.log(document.getElementById("celular").value.trim().length)
    if (document.getElementById("celular").value.trim().length !== 9) {
        alert("El número de celular debe tener 9 dígitos.");
        return false;
    }
    $.ajax({
        type: 'POST',
        url: '/comprar/',
        data: {
            'boton': 'sms',
            'celular': $('#celular').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
            SMSenviado = true;
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error
            console.error('Error:', error);
        }
    });
}

tiempo = 60;
SMSenviado = false
validado = false
function ActBotSMSValidar() {
    if (validado) {
        document.getElementById("buttonSMSenEspera").innerText = "Validado"
        document.getElementById("buttonSMS").style.display = "none";
        document.getElementById("buttonSMSenEspera").style.display = "block";
        document.getElementById("containerCodigo").style.display = "none"
        document.getElementById("celular").readOnly = true
    }
    else if (SMSenviado) {
        document.getElementById("buttonSMS").style.display = "none";
        document.getElementById("buttonSMSenEspera").style.display = "block";
        document.getElementById("containerCodigo").style.display = "flex"
        document.getElementById("celular").readOnly = true
        tiempo = tiempo - 1
        document.getElementById("buttonSMSenEspera").innerText = tiempo.toString()
        if (tiempo <= 0) {
            SMSenviado = false;
            tiempo = 60;
        }
    }
    else {
        document.getElementById("buttonSMS").style.display = "block";
        document.getElementById("buttonSMSenEspera").style.display = "none";
        document.getElementById("containerCodigo").style.display = "none"
        document.getElementById("celular").readOnly = false
    }
}
setInterval(ActBotSMSValidar, 999);


function enviarCodigo() {
    //console.log(document.getElementById("codigo").value.trim().length)
    if (document.getElementById("codigo").value.trim().length !== 6) {
        alert("El codigo de verificacion debe tener 6 caracteres.");
        return false; // Evita que el formulario se envíe
    }
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
            //console.log(response.data)
            if (response.data.toString() == "Codigo correcto") {
                validado = true
            }
            else {
                alert("El codigo ingresado no es correcto.");
            }
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error

            console.error('Error:', error);

        }
    });
}

function uppercase(event) {
    var input = event.target;
    input.value = input.value.toUpperCase().replace(/[^A-Z 0-9]/g, "");
}

function documentoSeleccionado(radioButton) {
    const valorSeleccionado = radioButton.value;
    const input = document.getElementById("dni");
    input.value = ""
    input.removeAttribute("onkeypress");
    input.removeAttribute("oninput");
    if (valorSeleccionado === "DNI") {
        input.setAttribute("onkeypress", "return soloNumeros(event)");
        input.setAttribute("maxlength", "8");
    } else if (valorSeleccionado === "CE" || valorSeleccionado === "Pass") {
        input.setAttribute("oninput", "uppercase(event)");
        input.setAttribute("maxlength", "20");
    }
}

function verificarDatosCompletos() {
    if (!validado) {
        alert("No ha validado su celular")
        return false
    }
    if (document.getElementById("dni").value.length < 8) {
        alert("Falta ingresar su documento")
        return false
    }
    if (document.getElementById("nombre").value.length < 3) {
        alert("Falta ingresar su nombre completo")
        return false
    }
    if (document.getElementById("pin").value.length < 3) {
        alert("Falta ingresar su pin")
        return false
    }
    if (!document.getElementById("Privacidad").checked) {
        alert("Debe aceptar la politica de privacidad")
        return false
    }
    document.getElementById("DNI").readOnly = true
    document.getElementById("CE").readOnly = true
    document.getElementById("Pass").readOnly = true
    document.getElementById("dni").readOnly = true
    document.getElementById("nombre").readOnly = true
    document.getElementById("pin").readOnly = true
    document.getElementById("Privacidad").readOnly = true
    document.getElementById("Spam").readOnly = true
    document.getElementById("buttonContinuar").readOnly = true
    document.getElementById("buttonOpcionales").style.display = "none"
    document.getElementById("buttonContinuar").style.display = "none"
    document.getElementById("buttonContinuar_1").style.display = "flex"
    return true
}

function continuar() {
    verificarDatosCompletos()
}

function datosOpcionales() {
    if (verificarDatosCompletos()) {
        document.getElementById("containerOpcional").style.display = "grid"
    }
}

function preguntaseleccionada() {
    //console.log(previa1)
    //console.log(previa2)
    //console.log(previa3)
    if (document.getElementsByName("mi_combobox")[0].selectedIndex == document.getElementsByName("mi_combobox")[1].selectedIndex ||
        document.getElementsByName("mi_combobox")[1].selectedIndex == document.getElementsByName("mi_combobox")[2].selectedIndex ||
        document.getElementsByName("mi_combobox")[2].selectedIndex == document.getElementsByName("mi_combobox")[0].selectedIndex) {
        alert("Las preguntas no pueden ser repetidas")
        repetidas = true
    }
    else {
        previa1 = document.getElementsByName("mi_combobox")[0].selectedIndex
        previa2 = document.getElementsByName("mi_combobox")[1].selectedIndex
        previa3 = document.getElementsByName("mi_combobox")[2].selectedIndex
    }
}

var previa1 = 0
var previa2 = 1
var previa3 = 2
var repetidas = true
function ActivacionBotonComprar() {
    if (repetidas) {
        repetidas = false;
        document.getElementsByName("mi_combobox")[0].selectedIndex = previa1
        document.getElementsByName("mi_combobox")[1].selectedIndex = previa2
        document.getElementsByName("mi_combobox")[2].selectedIndex = previa3
    }
}
setInterval(ActivacionBotonComprar, 100);

function verificarDatosOpcional() {
    if (document.getElementById("correo").value.length < 12) {
        alert("Ingrese un correo valido")
        return
    }
    if (document.getElementById("respuesta1").value.length < 3) {
        alert("Ingresar respuesta 1 valida")
        return
    }

    if (document.getElementById("respuesta2").value.length < 3) {
        alert("Ingresar respuesta 2 valida")
        return
    }

    if (document.getElementById("respuesta3").value.length < 3) {
        alert("Ingresar respuesta 3 valida")
        return
    }

    document.getElementById("buttonContinuarOpcional").style.display = "none"
    document.getElementById("buttonContinuarOpcional_1").style.display = "flex"
    document.getElementById("correo").readOnly = true;
    document.getElementsByName("mi_combobox")[0].readOnly = true;
    document.getElementsByName("mi_combobox")[1].readOnly = true;
    document.getElementsByName("mi_combobox")[2].readOnly = true;
    document.getElementById("respuesta1").readOnly = true;
    document.getElementById("respuesta2").readOnly = true;
    document.getElementById("respuesta3").readOnly = true;
}

var cantEntradasTipoSelec = new Array(6)
var precioEntradasTipo = new Array(6)

function inicializacion() {

    for (var i = 0; i < cantEntradasTipoSelec.length; i++) {
        cantEntradasTipoSelec[i] = 0;
        precioEntradasTipo[i] = parseInt(document.getElementById("entradaPrecio" + (i + 1).toString()).innerText.substring(document.getElementById("entradaPrecio" + (i + 1).toString()).innerText.length - 7));
    }
    console.log(precioEntradasTipo);
    //console.log(precioEntradasTipo[5]);
}
function disminuir(id) {
    $.ajax({
        type: 'POST',
        url: '/comprar/',
        data: {
            'comando': 'leerCantidadEntradas',
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
            for (var i = 0; i < 6; i++) {
                document.getElementById("entradasRestantes" + (i + 1).toString()).innerText = response.entradasRestantes[i] - cantEntradasTipoSelec[i];
                entradasElegidas = cantEntradasTipoSelec[i];
                if (response.entradasRestantes[i] - entradasElegidas <= 0) {
                    cantEntradasTipoSelec[i] = response.entradasRestantes[i]
                    document.getElementById("cantidadVisible" + (i + 1).toString()).innerText = response.entradasRestantes[i].toString();
                    document.getElementById("entradasRestantes" + (i + 1).toString()).innerText = "0";
                }
            }
            if (cantEntradasTipoSelec[id - 1] - 1 < 0) { calcularTotal(); return }
            entradasElegidas = cantEntradasTipoSelec[id - 1] - 1;
            cantEntradasTipoSelec[id - 1] = entradasElegidas;
            document.getElementById("cantidadVisible" + id).innerText = entradasElegidas.toString();
            for (var i = 0; i < 3; i++) {
                document.getElementById("entradasRestantes" + (i + 1).toString()).innerText = response.entradasRestantes[i] - cantEntradasTipoSelec[i];
            }

            for (var i = 0; i < response.boxes1Restantes.length; i++) {
                if (response.boxes1Restantes[i] == document.getElementById("boxes1").value) continue;
                document.getElementById("box" + response.boxes1Restantes[i]).classList.remove("boxOcupado")
                document.getElementById("box" + response.boxes1Restantes[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes1Restantes[i]).classList.add("boxDesocupado")
            }
            for (var i = 0; i < response.boxes1Ocupados.length; i++) {
                document.getElementById("box" + response.boxes1Ocupados[i]).classList.remove("boxDesocupado")
                document.getElementById("box" + response.boxes1Ocupados[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes1Ocupados[i]).classList.add("boxOcupado")
            }

            for (var i = 0; i < response.boxes2Restantes.length; i++) {
                if (response.boxes2Restantes[i] == document.getElementById("boxes2").value) continue;
                document.getElementById("box" + response.boxes2Restantes[i]).classList.remove("boxOcupado")
                document.getElementById("box" + response.boxes2Restantes[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes2Restantes[i]).classList.add("boxDesocupado")
            }
            for (var i = 0; i < response.boxes2Ocupados.length; i++) {
                document.getElementById("box" + response.boxes2Ocupados[i]).classList.remove("boxDesocupado")
                document.getElementById("box" + response.boxes2Ocupados[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes2Ocupados[i]).classList.add("boxOcupado")
            }

            for (var i = 0; i < response.boxes3Restantes.length; i++) {
                if (response.boxes3Restantes[i] == document.getElementById("boxes3").value) continue;
                document.getElementById("box" + response.boxes3Restantes[i]).classList.remove("boxOcupado")
                document.getElementById("box" + response.boxes3Restantes[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes3Restantes[i]).classList.add("boxDesocupado")
            }
            for (var i = 0; i < response.boxes3Ocupados.length; i++) {
                document.getElementById("box" + response.boxes3Ocupados[i]).classList.remove("boxDesocupado")
                document.getElementById("box" + response.boxes3Ocupados[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes3Ocupados[i]).classList.add("boxOcupado")
            }
            calcularTotal();
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error
            console.error('Error:', error);
        }
    });
}

function aumentar(id) {
    $.ajax({
        type: 'POST',
        url: '/comprar/',
        data: {
            'comando': 'leerCantidadEntradas',
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
            for (var i = 0; i < 3; i++) {
                document.getElementById("entradasRestantes" + (i + 1).toString()).innerText = response.entradasRestantes[i];
                entradasElegidas = cantEntradasTipoSelec[i];
                if (response.entradasRestantes[i] - entradasElegidas <= 0) {
                    cantEntradasTipoSelec[i] = response.entradasRestantes[i];
                    document.getElementById("cantidadVisible" + (i + 1).toString()).innerText = response.entradasRestantes[i].toString();
                    document.getElementById("entradasRestantes" + (i + 1).toString()).innerText = "0";
                }
            }
            if (cantEntradasTipoSelec[id - 1] + 1 > 20) { calcularTotal(); return }
            entradasElegidas = cantEntradasTipoSelec[id - 1] + 1;
            cantEntradasTipoSelec[id - 1] = entradasElegidas;
            document.getElementById("cantidadVisible" + id).innerText = entradasElegidas.toString();
            for (var i = 0; i < 3; i++) {
                document.getElementById("entradasRestantes" + (i + 1).toString()).innerText = response.entradasRestantes[i] - cantEntradasTipoSelec[i];
            }

            for (var i = 0; i < response.boxes1Restantes.length; i++) {
                if (response.boxes1Restantes[i] == document.getElementById("boxes1").value) continue;
                document.getElementById("box" + response.boxes1Restantes[i]).classList.remove("boxOcupado")
                document.getElementById("box" + response.boxes1Restantes[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes1Restantes[i]).classList.add("boxDesocupado")
            }
            for (var i = 0; i < response.boxes1Ocupados.length; i++) {
                document.getElementById("box" + response.boxes1Ocupados[i]).classList.remove("boxDesocupado")
                document.getElementById("box" + response.boxes1Ocupados[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes1Ocupados[i]).classList.add("boxOcupado")
            }

            for (var i = 0; i < response.boxes2Restantes.length; i++) {
                if (response.boxes2Restantes[i] == document.getElementById("boxes2").value) continue;
                document.getElementById("box" + response.boxes2Restantes[i]).classList.remove("boxOcupado")
                document.getElementById("box" + response.boxes2Restantes[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes2Restantes[i]).classList.add("boxDesocupado")
            }
            for (var i = 0; i < response.boxes2Ocupados.length; i++) {
                document.getElementById("box" + response.boxes2Ocupados[i]).classList.remove("boxDesocupado")
                document.getElementById("box" + response.boxes2Ocupados[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes2Ocupados[i]).classList.add("boxOcupado")
            }

            for (var i = 0; i < response.boxes3Restantes.length; i++) {
                if (response.boxes3Restantes[i] == document.getElementById("boxes3").value) continue;
                document.getElementById("box" + response.boxes3Restantes[i]).classList.remove("boxOcupado")
                document.getElementById("box" + response.boxes3Restantes[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes3Restantes[i]).classList.add("boxDesocupado")
            }
            for (var i = 0; i < response.boxes3Ocupados.length; i++) {
                document.getElementById("box" + response.boxes3Ocupados[i]).classList.remove("boxDesocupado")
                document.getElementById("box" + response.boxes3Ocupados[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes3Ocupados[i]).classList.add("boxOcupado")
            }
            calcularTotal();
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error
            console.error('Error:', error);
        }
    });
}

function calcularTotal() {
    var total = 0;
    for (var i = 0; i < 6; i++) {
        //console.log(cantEntradasTipoSelec[i])
        //console.log(precioEntradasTipo[i])
        total = total + cantEntradasTipoSelec[i] * precioEntradasTipo[i]
    }
    //console.log("Paso por calcular total")
    document.getElementById("totalEstatico").innerText = total.toString();
    if (total == 0) {
        document.getElementById("buttonComprar").style.display = "none"
    }
    else {
        document.getElementById("buttonComprar").style.display = "block"
    }
}

function comprar() {
    //document.getElementById("celular2").value = document.getElementById("celular").value;
    //document.getElementById("codigo2").value  = document.getElementById("codigo").value;
    if (!verificarDatosCompletos()) {
        return
    }
    console.log("holad")
    var formulario = document.getElementById("comprarForm");
    for (var i = 1; i <= cantEntradasTipoSelec.length; i++) {
        var nuevoCampo = document.createElement("input");
        nuevoCampo.name = "cantidadEntradas" + i.toString();
        nuevoCampo.value = cantEntradasTipoSelec[i - 1];
        formulario.appendChild(nuevoCampo);
        console.log(i)
    }
    var campoPregunta1 = document.createElement("input");
    var campoPregunta2 = document.createElement("input");
    var campoPregunta3 = document.createElement("input");
    campoPregunta1.name = "pregunta1";
    campoPregunta2.name = "pregunta2";
    campoPregunta3.name = "pregunta3";

    var selectpreg1 = document.getElementById("pregunta1Sel");
    var pregSel1 = selectpreg1.options[selectpreg1.selectedIndex].text;
    campoPregunta1.value = pregSel1;
    var selectpreg2 = document.getElementById("pregunta2Sel");
    var pregSel2 = selectpreg2.options[selectpreg2.selectedIndex].text;
    campoPregunta2.value = pregSel2;
    var selectpreg3 = document.getElementById("pregunta3Sel");
    var pregSel3 = selectpreg3.options[selectpreg3.selectedIndex].text;
    campoPregunta3.value = pregSel3;

    formulario.appendChild(campoPregunta1);
    formulario.appendChild(campoPregunta2);
    formulario.appendChild(campoPregunta3);
    //console.log(document.getElementById("comprarForm"))
    document.getElementById("boton").value = "comprar"
    document.getElementById("comprarForm").submit();

}

function seleccionBox(seleccionado) {
    $.ajax({
        type: 'POST',
        url: '/comprar/',
        data: {
            'comando': 'leerCantidadEntradas',
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },

        success: function (response) {
            for (var i = 0; i < 6; i++) {
                document.getElementById("entradasRestantes" + (i + 1).toString()).innerText = response.entradasRestantes[i];
                entradasElegidas = cantEntradasTipoSelec[i];
                if (response.entradasRestantes[i] - entradasElegidas <= 0) {
                    cantEntradasTipoSelec[i] = response.entradasRestantes[i];
                    document.getElementById("cantidadVisible" + (i + 1).toString()).innerText = response.entradasRestantes[i].toString();
                    document.getElementById("entradasRestantes" + (i + 1).toString()).innerText = "0";
                    if (i >= 3) {
                        document.getElementById("boxes" + i.toString()).value = "ninguno"
                        cantidadEntradasTipo[i] = 0
                    }
                }
            }

            boxes = document.getElementsByName("boxseleccionado")
            if (document.getElementById("box" + seleccionado).className == "boxOcupado") return;
            if (document.getElementById("box" + seleccionado).className == "boxElegido") {
                document.getElementById("boxes3").value = 0;
                document.getElementById("boxes2").value = 0;
                document.getElementById("boxes1").value = 0;
                cantEntradasTipoSelec[3] = 0
                cantEntradasTipoSelec[4] = 0
                cantEntradasTipoSelec[5] = 0
                document.getElementById("box" + seleccionado).classList.remove("boxElegido")
                document.getElementById("box" + seleccionado).classList.add("boxDesocupado")
                calcularTotal()
                return;
            }
            for (var i = 0; i < boxes.length; i++) {
                console.log(i + 1)
                console.log(seleccionado)
                if (document.getElementById("box" + (i + 1).toString()).className == "boxOcupado") {
                    continue;
                }
                if ((i + 1).toString() == seleccionado.toString()) {
                    console.log("IGUALES")
                    document.getElementById("box" + (i + 1).toString()).classList.remove("boxDesocupado")
                    document.getElementById("box" + (i + 1).toString()).classList.add("boxElegido")

                    if (1 <= seleccionado && seleccionado <= 18) {
                        document.getElementById("boxes3").value = seleccionado;
                        document.getElementById("boxes2").value = 0;
                        document.getElementById("boxes1").value = 0;
                        cantEntradasTipoSelec[3] = 0
                        cantEntradasTipoSelec[4] = 0
                        cantEntradasTipoSelec[5] = 1

                    }
                    if (19 <= seleccionado && seleccionado <= 23) {
                        document.getElementById("boxes3").value = 0;
                        document.getElementById("boxes2").value = 0;
                        document.getElementById("boxes1").value = seleccionado;
                        cantEntradasTipoSelec[3] = 1
                        cantEntradasTipoSelec[4] = 0
                        cantEntradasTipoSelec[5] = 0
                    }
                    if (24 <= seleccionado && seleccionado <= 28) {
                        document.getElementById("boxes3").value = 0;
                        document.getElementById("boxes2").value = seleccionado;
                        document.getElementById("boxes1").value = 0;
                        cantEntradasTipoSelec[3] = 0
                        cantEntradasTipoSelec[4] = 1
                        cantEntradasTipoSelec[5] = 0
                    }
                }
                else {
                    document.getElementById("box" + (i + 1).toString()).classList.remove("boxElegido")
                    document.getElementById("box" + (i + 1).toString()).classList.add("boxDesocupado")
                }
            }



            var opcionSeleccionadabox1 = document.getElementById("boxes1").value
            var opcionSeleccionadabox2 = document.getElementById("boxes2").value
            var opcionSeleccionadabox3 = document.getElementById("boxes3").value
            for (var i = 0; i < response.boxes1Restantes.length; i++) {
                if (response.boxes1Restantes[i] == document.getElementById("boxes1").value) continue;
                document.getElementById("box" + response.boxes1Restantes[i]).classList.remove("boxOcupado")
                document.getElementById("box" + response.boxes1Restantes[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes1Restantes[i]).classList.add("boxDesocupado")
            }
            for (var i = 0; i < response.boxes1Ocupados.length; i++) {
                document.getElementById("box" + response.boxes1Ocupados[i]).classList.remove("boxDesocupado")
                document.getElementById("box" + response.boxes1Ocupados[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes1Ocupados[i]).classList.add("boxOcupado")
            }

            for (var i = 0; i < response.boxes2Restantes.length; i++) {
                if (response.boxes2Restantes[i] == document.getElementById("boxes2").value) continue;
                document.getElementById("box" + response.boxes2Restantes[i]).classList.remove("boxOcupado")
                document.getElementById("box" + response.boxes2Restantes[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes2Restantes[i]).classList.add("boxDesocupado")
            }
            for (var i = 0; i < response.boxes2Ocupados.length; i++) {
                document.getElementById("box" + response.boxes2Ocupados[i]).classList.remove("boxDesocupado")
                document.getElementById("box" + response.boxes2Ocupados[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes2Ocupados[i]).classList.add("boxOcupado")
            }

            for (var i = 0; i < response.boxes3Restantes.length; i++) {
                if (response.boxes3Restantes[i] == document.getElementById("boxes3").value) continue;
                document.getElementById("box" + response.boxes3Restantes[i]).classList.remove("boxOcupado")
                document.getElementById("box" + response.boxes3Restantes[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes3Restantes[i]).classList.add("boxDesocupado")
            }
            for (var i = 0; i < response.boxes3Ocupados.length; i++) {
                document.getElementById("box" + response.boxes3Ocupados[i]).classList.remove("boxDesocupado")
                document.getElementById("box" + response.boxes3Ocupados[i]).classList.remove("boxElegido")
                document.getElementById("box" + response.boxes3Ocupados[i]).classList.add("boxOcupado")
            }




            /*if (!response.boxes1Restantes.includes(parseInt(opcionSeleccionadabox1))) {
                cantEntradasTipoSelec[3] = 0;
                document.getElementById("box" + opcionSeleccionadabox1).classList.remove("boxDesocupado")
                document.getElementById("box" + opcionSeleccionadabox1).classList.remove("boxElegido")
                document.getElementById("box" + opcionSeleccionadabox1).classList.add("boxOcupado")
                //console.log("Entro a ningun elemento seleccionado, no matcheo el substring en el arreglo de boxes 1")
            }

            if (!response.boxes2Restantes.includes(parseInt(opcionSeleccionadabox2))) {
                cantEntradasTipoSelec[4] = 0;
                document.getElementById("box" + opcionSeleccionadabox2).classList.remove("boxDesocupado")
                document.getElementById("box" + opcionSeleccionadabox2).classList.remove("boxElegido")
                document.getElementById("box" + opcionSeleccionadabox2).classList.add("boxOcupado")
            }

            if (!response.boxes3Restantes.includes(parseInt(opcionSeleccionadabox3))) {
                cantEntradasTipoSelec[5] = 0;
                document.getElementById("box" + opcionSeleccionadabox3).classList.remove("boxDesocupado")
                document.getElementById("box" + opcionSeleccionadabox3).classList.remove("boxElegido")
                document.getElementById("box" + opcionSeleccionadabox3).classList.add("boxOcupado")
            }*/



            calcularTotal()

            for (var i = 0; i < 6; i++) {
                document.getElementById("entradasRestantes" + (i + 1).toString()).innerText = response.entradasRestantes[i] - cantEntradasTipoSelec[i];
            }
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error
            console.error('Error:', error);
        }
    });
}