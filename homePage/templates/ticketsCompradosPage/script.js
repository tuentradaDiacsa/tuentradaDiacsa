window.onbeforeunload = function () {
    window.location.reload(true);
};



ScrollReveal().reveal('.containerTicketsDescargar', { delay: 1000 });
ScrollReveal().reveal('.seleccionarFechaBanner', { delay: 1000 });

function download(cadena) {
    console.log(cadena.toString())
}
