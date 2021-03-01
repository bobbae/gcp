const {Storage} = require('@google-cloud/storage');

var keyFile = `${process.env.HOME}/key.json`;
var projectID = `${process.env.PROJECT}`

const storage = new Storage({
  projectId: projectID,
  keyFilename: keyFile});

// more options example https://github.com/googleapis/nodejs-storage/blob/master/samples/createNewBucket.js
async function createBucket(bucketName) {

  async function createBucketTry() {
    await storage.createBucket(bucketName);
    console.log(`Bucket ${bucketName} created.`);
  }
  createBucketTry().catch(console.error);
}

async function downloadFile(bucketName, srcFile, destFile) {
  const options = {
    destination: destFile
  }
  async function downloadFileTry() {
    await storage.bucket(bucketName).file(srcFile).download(options)
    console.log( `gs://${bucketName}/${srcFile} downloaded to ${destFile}.`)
  }
  downloadFileTry().catch(console.error)
}

async function uploadFile(bucketName, filename, destination) {
  async function uploadFileTry() {
    await storage.bucket(bucketName).upload(filename, {
      destination: destination,
      metadata: {
        cacheControl: 'public, max-age=31536000'
      }
    })
    console.log(`${filename} uploaded to ${bucketName}`)
  }
  uploadFileTry().catch(console.error)
}
async function listFiles(bucketName) {
  
  async function listFilesTry() { 
    const [files] = await storage.bucket(bucketName).getFiles()
    return [files]

  }
  [files] = await listFilesTry().catch(console.error)
  /*
  console.log('Files:');
  files.forEach(file => {
    console.log(file.name);
  });
  */
 return [files]
}

async function listBuckets(){
  async function listBucketsTry() {
    const [buckets] = await storage.getBuckets()
    return [buckets]
  }
  const [buckets] = await listBucketsTry().catch(console.error)
  /*
  console.log('Buckets:');
  buckets.forEach(bucket => {
    console.log(bucket.name)
  })
  */
  return [buckets]
}

module.exports = { listBuckets, createBucket, downloadFile, uploadFile, listFiles}
