import firebase from 'firebase'

//XXX replace with config values  from firebase Project Settings
const config = {
  apiKey: "XXXXXXXXXXXXXXXXXXXXXXxxxxxx"                        
    authDomain: "XXXXX1-94252.firebaseapp.com",
    projectId: "XXXXX1-94252",
    storageBucket: "XXXXX1-94252.appspot.com",
    messagingSenderId: "xxxxxx11",
    appId: "1:xxxxx611:web:xxxxxxxxxxxxxxxxxxxxxxxx64d009e",
    measurementId: "xxxxxxx4K9"
  };

// XXX also change Realtime Database Rules to use auth != null or true
firebase.initializeApp(config);
export const provider = new firebase.auth.GoogleAuthProvider();
export const auth = firebase.auth();

export default firebase;
