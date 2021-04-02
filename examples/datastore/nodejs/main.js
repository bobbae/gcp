// This is for datastore in firestore mode
//https://github.com/googleapis/nodejs-datastore

// Imports the Google Cloud client library
const {Datastore} = require('@google-cloud/datastore');

// Creates a client
const datastore = new Datastore();

async function quickstart() {
  // The kind for the new entity
  const kind = 'Task';

  // The name/ID for the new entity
  const name = 'sampletask1';

  // The Cloud Datastore key for the new entity
  const taskKey = datastore.key([kind, name]);

  // Prepares the new entity
  const task = {
    key: taskKey,
    data: {
      description: 'Buy milk',
    },
  };

  // Saves the entity
  await datastore.save(task);
  console.log(`Saved ${task.key.name}: ${task.data.description}`);
}
quickstart();

// https://cloud.google.com/datastore/docs/concepts/queries
// query example: https://github.com/googleapis/nodejs-datastore/blob/master/samples/concepts.js
