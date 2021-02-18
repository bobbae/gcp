from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import argparse


def sub(project_id, subscription_id):
    timeout = 5.0
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    print(subscription_path)
    def callback(message):
        print(f"Received {message}.")
        message.ack()
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...\n")
    with subscriber:
        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # $PROJECT.dataset.table
    parser.add_argument("project_id", help="project ID")
    parser.add_argument("subscription_id", help="subscription ID")

    args = parser.parse_args()
    sub(args.project_id, args.subscription_id)
