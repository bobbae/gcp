//https://github.com/googleapis/nodejs-bigtable#quickstart
//https://github.com/googleapis/nodejs-bigtable/blob/master/samples/hello-world/index.js
const {Bigtable} = require('@google-cloud/bigtable')
const bigtable = new Bigtable();

var instanceId = `${process.env.BIGTABLE_INSTANCE_ID}`
var tableId = `${process.env.BIGTABLE_TABLE_ID}`

var COLUMN_FAMILY_ID= 'cf1'
var COLUMN_QUALIFIER = 'cf1q1'
async function quickstart() {
    const instance = bigtable.instance(instanceId)
    const table = instance.table(tableId)
    const [tableExists] = await table.exists();
    if (!tableExists) {
	console.log(`Creating table ${tableId}`);
	const options = {
	    families: [
	        {
		    name: COLUMN_FAMILY_ID,
		    rule: {
		        versions: 1,
		    },
		},
	    ],
	};
	await table.create(options);
    }
    const [families] = await table.getFamilies();

    families.forEach(family => {
        const metadata = JSON.stringify(family.metadata);
        console.log(`Column family: ${family.id}, Metadata: ${metadata}`);

    });


    console.log('Write some greetings to the table');
    const greetings = ['Hello World!', 'Hello Bigtable!', 'Hello Node!'];
    const rowsToInsert = greetings.map((greeting, index) => ({
	// Note: This example uses sequential numeric IDs for simplicity, but this
	// pattern can result in poor performance in a production application.
	// Rows are stored in sorted order by key, so sequential keys can result
	// in poor distribution of operations across nodes.
	//
	// For more information about how to design an effective schema for Cloud
	// Bigtable, see the documentation:
	// https://cloud.google.com/bigtable/docs/schema-design
	key: `greeting${index}`,
	data: {
	    [COLUMN_FAMILY_ID]: {
	        [COLUMN_QUALIFIER]: {
		    // Setting the timestamp allows the client to perform retries. If
		    // server-side time is used, retries may cause multiple cells to
		    // be generated.
		    timestamp: new Date(),
		    value: greeting,
		},
	    },
	},
    }));
    await table.insert(rowsToInsert);

    const filter = [
	{
	    column: {
	        cellLimit: 1, // Only retrieve the most recent version of the cell.
	    },
	},
    ];

    console.log('Reading a single row by row key');
    const [singleRow] = await table.row('greeting0').get({filter});
    const getRowGreeting = row => {
	return row.data[COLUMN_FAMILY_ID][COLUMN_QUALIFIER][0].value;
    };
    console.log(`\tRead: ${getRowGreeting(singleRow)}`);

    console.log('Reading the entire table');
    // Note: For improved performance in production applications, call
    // `Table#readStream` to get a stream of rows. See the API documentation:
    // https://cloud.google.com/nodejs/docs/reference/bigtable/latest/Table#createReadStream
    const [allRows] = await table.getRows({filter});
    for (const row of allRows) {
        console.log(`\tRead: ${getRowGreeting(row)}`);
    }

    console.log('Delete the table');
    await table.delete();
}

(async () => {
    try {
	quickstart();
    } catch (error) {
	console.error('Something went wrong', error)
    }
})();
