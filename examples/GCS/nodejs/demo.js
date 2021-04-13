const gcs = require('./gcs');

var keyFile = `${process.env.HOME}/key.json`;
var project = `${process.env.PROJECT}`;

var bucketName = 'sada-u'
var fileName = 'gcs.js'

async function listBucketsDemo() {
    const [buckets] = await gcs.listBuckets()
    console.log('buckets',buckets)
}

//listBucketsDemo()

async function uploadDemo() {
    await gcs.uploadFile(bucketName, fileName, fileName)
}

//uploadDemo()

async function downloadDemo() {
    await gcs.downloadFile(bucketName, fileName, '/tmp/xyz.xyz')
}
//downloadDemo()

async function listFilesDemo() {
   const [files] = await gcs.listFiles(bucketName)
   console.log('files',files)
}

//listFilesDemo()

async function setMetadataDemo() {
    const res = await gcs.setMetadata(bucketName, fileName, { metadata: { "abc": "def", "hello": "goodbye" }});
    console.log('metadata set', res)
}
setMetadataDemo()

async function getMetadataDemo() {
    const [metadata] = await gcs.getMetadata(bucketName, fileName)
    console.log('metadata', metadata);
}

getMetadataDemo();


