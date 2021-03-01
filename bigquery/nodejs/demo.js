const bq = require('./bq');

var keyFile = `${process.env.HOME}/key.json`;
var project = `${process.env.PROJECT}`;


var datasetName = 'test1';
var tableName = 'table2';

function createTableDemo(
    datasetId = datasetName, // Existing dataset
    tableId = tableName, // Table to be created
    schema = [
      {name: 'name', type: 'STRING', mode: 'REQUIRED'},
      {name: 'top', type: 'STRING'},
      {name: 'bottom', type: 'STRING'},
      {name: 'votes', type: 'INT64'},
      {name: 'uuid', type: 'STRING'},
      {name: 'meme', type: 'STRING'},
      {name: 'image', type: 'STRING'},
      {name: 'url', type: 'STRING'},
      {name: 'dimensions', type: 'STRING'},
    ]
  ) {
    bq.createTable(datasetId, tableId, schema);
}


function insertRowsDemo(datasetId = datasetName, tableId = tableName, 
    rows = [
      {name: 'Tom', votes: 1},
      {name: 'Jane', votes: 1},
      {name: 'Bob', votes: 10}
    ]
) {
    bq.insertRows(datasetId, tableId, rows);
}
//createTableDemo();
//insertRowsDemo();

async function queryDemo() {
  const query = `SELECT *
  FROM \`${project}.${datasetName}.${tableName}\`
  LIMIT 100`;
  const [rows] = await bq.runQuery(query);
  //rows.forEach(row => console.log(row));
  console.log(rows);
  /* for (row of rows) {
    console.log('row',row);
  } */
}

queryDemo();

