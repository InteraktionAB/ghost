import requests


inputs = {'image' : 'https://thumbs.dreamstime.com/b/beauty-woman-face-portrait-beautiful-model-girl-perfect-fresh-clean-skin-spa-brunette-female-looking-camera-smiling-66363112.jpg',
        'video' : 'https://joy1.videvo.net/videvo_files/video/free/video0454/large_watermarked/_import_6064b7eaaff605.68960435_preview.mp4'}

res = requests.post('http://localhost:8000/', json = inputs)

out = res.json()["text"]
