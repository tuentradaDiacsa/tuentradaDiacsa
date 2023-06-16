

var precioEntradasTipoResumen   = new Array(6)

window.onbeforeunload = function () {
    location.reload(true);
}

ScrollReveal().reveal('.resumenCompraBanner, .containerTodo', {
    delay: 200, // Retraso en milisegundos antes de que aparezca cada elemento
    distance: '50px', // Distancia de desplazamiento desde la posición original
    duration: 800, // Duración de la animación en milisegundos
    easing: 'ease-out', // Curva de animación
});

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

