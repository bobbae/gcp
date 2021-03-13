const fs = require('firebase-admin');

const serviceAccount = require(`${process.env.HOME}/key.json`);


async function test1() {
    fs.initializeApp({
	credential: fs.credential.cert(serviceAccount)
    });
    const db = fs.firestore();
    const usersDb = db.collection('users');
    const liam = usersDb.doc('lragozzine');

    await liam.set({
	first: 'Liam',
	last: 'Ragozzine',
	address: '133 5th St., San Francisco, CA',
	birthday: '05/13/1990',
	age: '30'
    });
    await usersDb.doc('vpeluso').set({
	first: 'Vanessa',
	last: 'Peluso',
	address: '49 Main St., Tampa, FL',
	birthday: '11/30/1977',
	age: '47'
    });

    const users = await db.collection('users').get();
    console.log('users',users)
    const liamDoc = await db.collection('users').doc('lragozzine').get();
    if (!liamDoc.exists) {
	console.log('No document');
    } else {
	console.log(liamDoc.data());
    }

    const under30 = await db.collection('users').where('age', '<=', 40).get();
    const liam2 = db.collection('users').doc('lragozzine');
    const observer = liam2.onSnapshot(snapshot => {
	console.log(`changes: ${snapshot}`);
    }, err => {
	console.log(`Error: ${err}`);
    });
}

(async() => {
    try{
	var res = await test1();
	console.log('done', res);
    } catch (e) {
	console.error(e);
    }
})();


