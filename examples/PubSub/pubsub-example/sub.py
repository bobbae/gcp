from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import time

#pip install --upgrade google-cloud-pubsub
#gcloud pubsub topics create my-topic
#gcloud pubsub subscriptions create my-sub --topic my-topic
#gcloud pubsub topics publish my-special-topic --message '{ "kind": "hello" }'
#gcloud pubsub subscriptions pull my-special-subscription --auto-ack

project_id = "my-project-1"
subscription_id = "my-subscription"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        #streaming_pull_future.result(timeout=timeout)
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.

#while True:
#    print('waiting...')
#    time.sleep(10)
