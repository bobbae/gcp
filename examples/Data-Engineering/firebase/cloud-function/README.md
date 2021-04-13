# Firebase cloud function
Cloud function to add data to firebase from [firebase getting started documentation](https://firebase.google.com/docs/functions/get-started)

## steps

1. Edit .firebaserc and set project ID 
      gcloud config get-value project
2.

```
$ firebase login
$ firebase init firestore
$ firebase init functions
$ firebase deploy --only functions
```
