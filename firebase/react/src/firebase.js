import firebase from 'firebase'
const config = {
  apiKey: "AIzaSyBZ5cvTuqSCz_pf_y-tyDBbjzwsPVvKRlU",
    authDomain: "sada-univ-sess-1-94252.firebaseapp.com",
    projectId: "sada-univ-sess-1-94252",
    storageBucket: "sada-univ-sess-1-94252.appspot.com",
    messagingSenderId: "1002184455611",
    appId: "1:1002184455611:web:cbeaa5d149edea764d009e",
    measurementId: "G-BDL77CL4K9"
  };
firebase.initializeApp(config);
export const provider = new firebase.auth.GoogleAuthProvider();
export const auth = firebase.auth();

export default firebase;
