document.addEventListener('DOMContentLoaded', () => {
    const clothingSelect = document.getElementById('clothingId');
    const customerImageInput = document.getElementById('customerImage');
    const customerImagePreview = document.getElementById('customerImagePreview');
    const clothingImagePreview = document.getElementById('clothingImagePreview');
    const resultImage = document.getElementById('resultImage');
    const progress = document.getElementById('progress');
    const progressBar = document.getElementById('progressBar');

    // Fetch clothing items
    fetch('/api/clothing')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.id;
                option.textContent = item.name;
                option.dataset.image = item.imageUrl;
                clothingSelect.appendChild(option);
            });
        });

    // Preview customer image
    customerImageInput.addEventListener('change', () => {
        const file = customerImageInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                customerImagePreview.src = e.target.result;
                customerImagePreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else {
            customerImagePreview.style.display = 'none';
        }
    });

    // Preview clothing image
    clothingSelect.addEventListener('change', () => {
        const selectedOption = clothingSelect.options[clothingSelect.selectedIndex];
        if (selectedOption && selectedOption.dataset.image) {
            clothingImagePreview.src = selectedOption.dataset.image;
            clothingImagePreview.style.display = 'block';
        } else {
            clothingImagePreview.style.display = 'none';
        }
    });
});

function tryOn() {
    const customerImage = document.getElementById('customerImage').files[0];
    const clothingId = document.getElementById('clothingId').value;
    const progress = document.getElementById('progress');
    const progressBar = document.getElementById('progressBar');
    const resultImage = document.getElementById('resultImage');

    if (!customerImage || !clothingId) {
        alert('Please upload an image and select clothing.');
        return;
    }

    progress.style.display = 'block';
    progressBar.style.width = '0%';
    progressBar.textContent = '0%';
    resultImage.style.display = 'none';

    const formData = new FormData();
    formData.append('customerImage', customerImage);
    formData.append('clothingId', clothingId);

    fetch('/api/tryon', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        function processStream() {
            return reader.read().then(({ done, value }) => {
                if (done) {
                    return;
                }
                buffer += decoder.decode(value || new Uint8Array(), {stream: true});
                const lines = buffer.split('\n\n');
                buffer = lines.pop();
                lines.forEach(line => {
                    if (line.startsWith('data: ')) {
                        const dataStr = line.slice(6).trim();
                        if (dataStr) {
                            try {
                                const data = JSON.parse(dataStr);
                                if (data.progress !== undefined) {
                                    const prog = data.progress;
                                    progressBar.style.width = `${prog}%`;
                                    progressBar.textContent = `${prog}%`;
                                } else if (data.resultImage) {
                                    progress.style.display = 'none';
                                    resultImage.src = data.resultImage;
                                    resultImage.style.display = 'block';
                                } else if (data.error) {
                                    alert(`Error: ${data.error}`);
                                    progress.style.display = 'none';
                                }
                            } catch (err) {
                                console.error('JSON parse error:', err);
                            }
                        }
                    }
                });
                return processStream();
            });
        }
        return processStream();
    })
    .catch(error => {
        alert(`Connection error: ${error.message}`);
        progress.style.display = 'none';
    });
}