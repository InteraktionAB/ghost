import requests


inputs = {'image' : 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fmedia.gettyimages.com%2Fid%2F1293903541%2Fphoto%2Fyoung-woman-stock-photo.jpg',
        'video' : 'https://joy1.videvo.net/videvo_files/video/free/video0454/large_watermarked/_import_6064b7eaaff605.68960435_preview.mp4'}

res = requests.post('http://localhost:8000/', json = inputs)

out = res.json()["text"]