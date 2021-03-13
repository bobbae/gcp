// https://firebase.google.com/docs/database/admin/save-data

var admin = require("firebase-admin");

var serviceAccount = require(`${process.env.HOME}/sada-univ-sess-2-305805-046954019201.json`);

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: "https://sada-univ-sess-2-305805-default-rtdb.firebaseio.com"
});

var db = admin.database();
//var ref = db.ref("restricted_access/secret_document");
var ref = db.ref("abc");

var usersRef = ref.child("users");
usersRef.set({
    ananisawesome: {
	date_of_birth: "June 22, 1922",
	full_name: "Alan Tours"
    },
    grapcehop: {
	date_of_birth: "December 9, 1900",
	full_name: "Grace Hip"
    }
});

usersRef.update({
    "alanisawesome/nickname": "Alan The Machine",
    "gracehop/nickname": "Amazing Grace"
});

usersRef.update({
    "alanisawesome": {
        "nickname": "Alan The Machine"
    },
    "gracehop": {
        "nickname": "Amazing Grace"
    }
});

/*
ref.once("value", function(snapshot) {
  console.log(snapshot.val());

});


ref.orderByChild("nickname").on("value", function(snapshot) {
    console.log("nickname",snapshot.val());
});
*/

ref.on("value", function(snapshot) {
    console.log(snapshot.val());
}, function (errorObject) {
    console.log('read failed', errorObject.code);
});



