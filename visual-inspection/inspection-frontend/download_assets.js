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

const url1 = 'https://storage.googleapis.com/xai-demo-assets/visual-inspection/images/table.jpg'
const filename1 = 'table.jpg'
const url2 = 'https://storage.googleapis.com/xai-demo-assets/visual-inspection/images/desk.jpeg'
const filename2 = 'desk.jpg'

fsp.stat(dir).catch(async (err) => {
    if (err.message.includes('no such file or directory')) {
        await fsp.mkdir(dir);
    }
});

fsp.stat(dir + filename1).catch(async (err) => {
    download(url1, dir + filename1, () => {
    })
})

fsp.stat(dir + filename2).catch(async (err) => {
    download(url2, dir + filename2, () => {
    })
})

console.log('✅ Downloaded image files(s) from xai-demonstrator-assets!')