

var precioEntradasTipoResumen = new Array(6)

window.onbeforeunload = function () {
    location.reload(true);
}

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
    // document.getElementById("boton").value = "confirmarCompra"
    // document.getElementById("comprarForm").submit()
    location.reload(true)

}

function donwload(cadena) {
    console.log(cadena.toString())
}

function confirmarPre() {
    $.ajax({
        type: 'POST',
        url: '/comprar/',  // Reemplaza esto con la URL de tu vista de Django
        data: {
            'comando': 'confirmarCompra',
            'cip': $('#cip').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
            if (response.estado == "Confirmado") {
                document.getElementById("columnaPago").style.display = "grid"
                document.getElementById("containerConfirmarCancelar").style.display = "none"
            }
            if (response.estado == "Timeout") {
                alert("Se acabo su tiempo de espera")
            }
            console.log(response)
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error
            console.error('Error:', error);
        }
    });
}

function cancelarPre() {
    location.reload(true)
}
