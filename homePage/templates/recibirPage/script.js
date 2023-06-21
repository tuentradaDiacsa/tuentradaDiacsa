function enviarFormulario() {
    document.getElementById("estado").innerText = ""
    document.getElementById("botonRecibir").style.display = "none"
    $.ajax({
        type: 'POST',
        url: '/administrar/',
        data: {
            'comando': 'verificarTransferencia',
            'codigoTransferencia': document.getElementById("codigoTransferencia").value,
            'dniTransferencia': document.getElementById('dniTransferencia').value,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
            if (response.estado == "Correcto") {
                document.getElementById("estado").innerText = response.tipoEntrada
                document.getElementById("botonRecibir").style.display = "flex"
            }
            else {
                document.getElementById("estado").innerText = "NO VALIDO"
            }
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error
            console.error('Error:', error);
        }
    });
}
function continuarDatos() {
    document.getElementById("containerTodo").style.display = "none"
    document.getElementById("containerObligatorio").style.display = "grid"
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

function enviarSMS() {
    //console.log(document.getElementById("celular").value.trim().length)
    if (document.getElementById("celular").value.trim().length !== 9) {
        alert("El número de celular debe tener 9 dígitos.");
        return false;
    }
    $.ajax({
        type: 'POST',
        url: '/administrar/',
        data: {
            'comando': 'solicitarCodigo',
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

function enviarCodigo() {
    //console.log(document.getElementById("codigo").value.trim().length)
    if (document.getElementById("codigo").value.trim().length !== 6) {
        alert("El codigo de verificacion debe tener 6 caracteres.");
        return false; // Evita que el formulario se envíe
    }
    $.ajax({
        type: 'POST',
        url: '/administrar/',  // Reemplaza esto con la URL de tu vista de Django
        data: {
            'comando': 'verificarCodigo',
            'celular': $('#celular').val(),
            'codigo': $('#codigo').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
            //console.log(response.data)
            if (response.estado.toString() == "Correcto") {
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

function continuar() {
    if (verificarDatosCompletos()) {

        var formulario = document.getElementById("transferirForm");

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

        document.getElementById("boton").value = "transferirEntrada"
        document.getElementById("transferirForm").submit();
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



    var formulario = document.getElementById("transferirForm");

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




    document.getElementById("boton").value = "transferirEntrada"
    document.getElementById("transferirForm").submit();
}

