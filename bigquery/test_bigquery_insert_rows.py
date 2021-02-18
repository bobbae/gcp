import argparse

from google.cloud import bigquery


def table_insert_rows(table_id):
    client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of table to append to.
    # table_id = "your-project.your_dataset.your_table"

    rows_to_insert = [
        {u"field1": u"Phred Phlyntstone", u"field2": "I am"},
        {u"field1": u"Wylma Phlyntstone", u"field2": "I was"},
    ]

    errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # $PROJECT.dataset.table
    parser.add_argument("table_id", help="table ID")

    args = parser.parse_args()
    print(args.table_id) 
    table_insert_rows(args.table_id)
