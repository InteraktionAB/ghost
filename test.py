import requests


inputs = {'image' : 'https://img.freepik.com/free-photo/front-view-man-with-nose-ring_23-2149441219.jpg',
        'video' : 'https://joy1.videvo.net/videvo_files/video/free/video0454/large_watermarked/_import_6064b7eaaff605.68960435_preview.mp4'}

res = requests.post('http://localhost:8000/', json = inputs)

out = res.json()["output"]
