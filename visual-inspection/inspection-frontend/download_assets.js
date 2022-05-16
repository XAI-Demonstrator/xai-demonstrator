const fsp = require('fs').promises;
const fs = require('fs');
const request = require('request')

const download = (url, path, callback) => {
    request.head(url, (err, res, body) => {
        request(url)
            .pipe(fs.createWriteStream(path))
            .on('close', callback)
    })
}

const dir = './src/assets/'

fsp.stat(dir).catch(async (err) => {
    if (err.message.includes('no such file or directory')) {
        await fsp.mkdir(dir);
    }
});

const baseUrl = "https://storage.googleapis.com/xai-demo-assets/visual-inspection/images/"
const assets = [
    'table.jpg',
    'desk_small.jpg',
    'pencils.jpg',
    'cups.jpg',
    'smartphones.jpg'
]

assets.forEach(
    function (fileName) {
        fsp.stat(dir + fileName).catch(async () => {
            download(baseUrl + fileName, dir + fileName, () => {
                console.log('✅ Downloaded ' + fileName + ' from xai-demonstrator-assets!')
            })
        })
    }
)
