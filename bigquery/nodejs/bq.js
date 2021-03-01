//'use strict';
// N.B. this api only works from node not inside brower. No 'fs' support there.
const {BigQuery} = require('@google-cloud/bigquery');

var keyFile = `${process.env.HOME}/key.json`;
var project = `${process.env.PROJECT}`;

const options = {
    keyFilename: keyFile,
    projectId: project,
  };
const bigqueryClient = new BigQuery(options);

const createDataset = async (datasetId) => {
    const [dataset] = await bigqueryClient.createDataset(datasetId);
    //console.log(`Dataset ${dataset.id} created.`);
} 

async function createTable(datasetId, tableId, schema) {
    const options = {
      schema: schema,
      location: 'US',
    };
    const [table] = await bigqueryClient
      .dataset(datasetId)
      .createTable(tableId, options);

    //console.log(`Table ${table.id} created.`);
}

async function insertRowsAsStream(datasetId, tableId, rows) {
  // Insert data into a table
  await bigqueryClient
    .dataset(datasetId)
    .table(tableId)
    .insert(rows);
  //console.log(`Inserted ${rows.length} rows`);
}

async function insertRows(datasetId, tableId, rows) {
  insertRowsAsStream(datasetId, tableId, rows)
}

async function runQuery(query) {
  // Queries the U.S. given names dataset for the state of Texas.

  const options = {
    query: query,
    location: 'US',
  };

  const [job] = await bigqueryClient.createQueryJob(options);
  //console.log(`Job ${job.id} started.`);

  const [rows] = await job.getQueryResults();

  //console.log('Rows:');
  //rows.forEach(row => console.log(row));
  return [rows];
}

module.exports = { bigqueryClient,runQuery, insertRows, createTable, createDataset}

