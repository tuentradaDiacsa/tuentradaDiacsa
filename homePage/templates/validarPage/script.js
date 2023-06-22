function soloNumeros(event) {
    var charCode = event.which ? event.which : event.keyCode;
    if (charCode < 48 || charCode > 57) {
        event.preventDefault();
        return false;
    }
    return true;
}

function verificar() {
    $.ajax({
        type: 'POST',
        url: '/administrar/',  // Reemplaza esto con la URL de tu vista de Django
        data: {
            'comando': 'verificarBotonValidarTemplate',
            'ticket': $('#ticket').val(),
            'cip': $('#cip').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
            document.getElementById("comprarBotonFinal").style.display = "none"
            document.getElementById("comprarBotonFinal").style.visibility = "visible"
            document.getElementById("datosCompradorTexto").style.visibility = "visible"
            document.getElementById("datosCompradorTexto").style.display = "flex"
            document.getElementById("notasAlFinal").style.display = "grid"

            if (response.estado.toString() == "Ticket valido") {
                document.getElementById("resultado").innerText = "Validado"
                document.getElementById("datosCompradorTexto").style.backgroundColor = "##7643F6";
                document.getElementById("notas").innerText = "Entrada valida para el concierto del Grupo 5 en Iquitos Domingo 25 de Junio de 2023 - 3:00 PM"
                document.getElementById("notas2").innerText = ""
            }
            if (response.estado.toString() == "Ticket no valido") {
                document.getElementById("resultado").innerText = "Entrada no valida"
                document.getElementById("datosCompradorTexto").style.backgroundColor = "black";
                document.getElementById("notas").innerText = "1. Puede que la entrada o apellido sea incorrecto."
                document.getElementById("notas2").innerText = "2. Verifique que la fecha del evento este vigente."
            }
            if (response.estado.toString() == "Ticket en validacion") {
                document.getElementById("resultado").innerText = "Entrada por validar"
                document.getElementById("datosCompradorTexto").style.backgroundColor = "gray";
                document.getElementById("notas").innerText = "Su entrada aun esta en proceso de verificacion de pago"
                document.getElementById("notas2").innerText = ""
            }
            console.log(response);
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error
            console.error('Error:', error);
        }
    });
}
function inicial() {
    document.getElementById("comprarBotonFinal").style.display = "flex"
    document.getElementById("comprarBotonFinal").style.visibility = "visible"
    document.getElementById("datosCompradorTexto").style.visibility = "none"
    document.getElementById("datosCompradorTexto").style.display = "flex"
    document.getElementById("notasAlFinal").style.display = "none"
}

function ActivacionBotonComprar() {

    document.getElementById('cip').value = document.getElementById('cip').value.replace(/[^A-Za-zÁÉÍÓÚÑáéíóúñ]/g, '').toUpperCase();

    // document.getElementById('celular').setAttribute('value', document.getElementById('celular').value.replace(/\D/g, ''))
}
setInterval(ActivacionBotonComprar, 100);