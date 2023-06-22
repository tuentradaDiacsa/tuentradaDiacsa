function enviarFormulario() {
    document.getElementById("codigoTransferencia").innerText = ""
    $.ajax({
        type: 'POST',
        url: '/administrar/',
        data: {
            'comando': 'generarTransferencia',
            'numeroEntrada': document.getElementById("numeroEntrada").value,
            'dni': document.getElementById('dni').value,
            'celular': document.getElementById("celular").value,
            'pin': document.getElementById("pin").value,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (response) {
            if (response.estado == "Correcto") {
                document.getElementById("codigoTransferencia").innerText = response.codigo
            }
            else {
                document.getElementById("codigoTransferencia").innerText = response.estado
            }
        },
        error: function (xhr, status, error) {
            // Lógica para manejar el error
            console.error('Error:', error);
        }
    });
}

function ActivacionBotonComprar() {
    document.getElementById('celular').value = document.getElementById('celular').value.replace(/\D/g, '');
    document.getElementById('dni').value = document.getElementById('dni').value.replace(/\D/g, '');
    document.getElementById('pin').value = document.getElementById('pin').value.replace(/\D/g, '');
    // document.getElementById('celular').setAttribute('value', document.getElementById('celular').value.replace(/\D/g, ''))
}
setInterval(ActivacionBotonComprar, 100);