ScrollReveal().reveal('.header', { delay: 1000 });
ScrollReveal().reveal('.footer', { delay: 1000 });
ScrollReveal().reveal('.todoEntradas', { delay: 1000 });
ScrollReveal().reveal('.ticketLabel', { delay: 1000 });
ScrollReveal().reveal('.cipLabel', { delay: 1000 });
ScrollReveal().reveal('.textInput', { delay: 1000 });
ScrollReveal().reveal('.verificarBtn', { delay: 1000 });
ScrollReveal().reveal('.footer', { delay: 1000 });

function soloNumeros(event) {
    var charCode = event.which ? event.which : event.keyCode;
    if (charCode < 48 || charCode > 57) {
        event.preventDefault();
        return false;
    }
    return true;
}

function verificar() {
    if (document.getElementById("ticket").value.trim().length !== 6 || document.getElementById("cip").value.trim().length !== 6) {
        alert("El codigo de verificacion debe tener 6 caracteres.");
        return false; // Evita que el formulario se envíe
    }
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
            document.getElementById("resultado").innerText = response.estado.toString();
            if (response.estado.toString() == "Ticket valido") document.getElementById("datosCompradorTexto").style.backgroundColor = "green";
            if (response.estado.toString() == "Ticket no valido") document.getElementById("datosCompradorTexto").style.backgroundColor = "red";
            if (response.estado.toString() == "Ticket en validacion") document.getElementById("datosCompradorTexto").style.backgroundColor = "orange";
            console.log(response);
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error
            console.error('Error:', error);
        }
    });
}