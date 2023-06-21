function onScanSuccess(decodedText, decodedResult) {
    if (!isPaused) {
        isPaused = true;
        document.getElementById("reader").style.display = "none"
        document.getElementById("containerRespuesta").style.display = "grid"

        // Handle on success condition with the decoded text or result.
        console.log(`Scan result: ${decodedText}`, decodedResult);
        //html5QrcodeScanner.clear();
        //html5QrcodeScanner.render(onScanSuccess);
        $.ajax({
            type: 'POST',
            url: '/escaner/',
            data: {
                'comando': 'QRenviado',
                'data': decodedText,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (response) {
                if (response.estado == "CORRECTO") {
                    document.getElementById("respuesta").innerText = "Ticket Valido"
                    document.getElementById("containerRespuesta").style.backgroundColor = "var(--verde)"
                }
                else {
                    document.getElementById("respuesta").innerText = "Ticket NO Valido"
                    document.getElementById("containerRespuesta").style.backgroundColor = "var(--red)"
                }
            },
            error: function (xhr, status, error) {
                // Lógica para manejar el error
                console.error('Error:', error);
            }
        });
    }
}

let qrboxFunction = function (viewfinderWidth, viewfinderHeight) {
    let minEdgePercentage = 0.7; // 70%
    let minEdgeSize = Math.min(viewfinderWidth, viewfinderHeight);
    let qrboxSize = Math.floor(minEdgeSize * minEdgePercentage);
    return {
        width: qrboxSize,
        height: qrboxSize
    };
}

isPaused = false;
var html5QrcodeScanner = new Html5QrcodeScanner(
    "reader", { fps: 10, qrbox: qrboxFunction });
html5QrcodeScanner.render(onScanSuccess);


function iniciarEscaner() {
    document.getElementById("containerRespuesta").style.display = "none"
    document.getElementById("reader").style.display = "block"
    setTimeout(function () {
        isPaused = false;
    }, 1000); // Retraso de 1 segundo (1000 ms)
}