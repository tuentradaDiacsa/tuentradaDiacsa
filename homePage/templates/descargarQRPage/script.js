function ActivacionBotonComprar() {
    document.getElementById('descarga').value = document.getElementById('descarga').value.replace(/[^A-Za-z0-9]/g, '').toUpperCase();

    document.getElementById('pin').value = document.getElementById('pin').value.replace(/\D/g, '');
    // document.getElementById('celular').setAttribute('value', document.getElementById('celular').value.replace(/\D/g, ''))
}
setInterval(ActivacionBotonComprar, 100);