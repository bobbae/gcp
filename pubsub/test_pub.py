import argparse
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()

def pub(project_id, topic_id, message):
    topic_path = publisher.topic_path(project_id, topic_id)
    data = message
    data = data.encode("utf-8")
    future = publisher.publish(topic_path, data)
    print(future.result())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # $PROJECT.dataset.table
    parser.add_argument("project_id", help="project ID")
    parser.add_argument("topic_id", help="topic ID")
    parser.add_argument("message", help="message")

    args = parser.parse_args()
    pub(args.project_id, args.topic_id, args.message)
