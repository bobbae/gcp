//https://github.com/minio/minio-js

// https://github.com/minio/operator/blob/master/README.md
// my-minio-tenant

// kubectl minio init
// kubectl get deployments -A --field-selector metadata.name=minio-operator
// kubectl minio tenant create my-minio-tenant-1 --servers 4 --volumes 8 --capacity 1G 

// Username: admin 
// Password: cdade76e-1847-47ac-a35e-b24b721d6d39 
//

var Minio = require('minio')

var minioClient = new Minio.Client({
    endPoint: '192.168.49.2',
    port: 9000,
    useSSL: false,
    accessKey: 'minio',
    secretKey: 'minio123' 
    /* endPoint: 'play.min.io',
    port: 9000,
    useSSL: true,
    accessKey: 'Q3AM3UQ867SPQQA43P2F',
    secretKey: 'zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG' */
});

var file = '/tmp/meme.png';
minioClient.makeBucket('memes', 'us-east-1', function(err){
    if (err) return console.log(err);
    console.log('bucket created successfully');
    var metaData={
        'Content-Type': 'application/octet-stream',
        'X-Amz-Meta-Testing': 1234,
        'example': 5678
    };
    minioClient.fPutObject('memes', 'meme.png', file, metaData, function(err,etag){
        if (err) return console.log(err);
        console.log('File uploaded successfuly');
    });
});

