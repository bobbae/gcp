from google.cloud import pubsub_v1
from concurrent import futures

#pip install --upgrade google-cloud-pubsub
#gcloud pubsub topics create my-topic
#gcloud pubsub subscriptions create my-sub --topic my-topic
#gcloud pubsub topics publish my-special-topic --message '{ "kind": "hello" }'
#gcloud pubsub subscriptions pull my-special-subscription --auto-ack

project_id = "my-project-1"
topic_id = "my-topic-1"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

publish_futures = []

#def get_callback(
#    publish_future: pubsub_v1.publisher.futures.Future, data: str
#) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
#    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
#        try:
#            # Wait 60 seconds for the publish call to succeed.
#            print(publish_future.result(timeout=60))
#        except futures.TimeoutError:
#            print(f"Publishing {data} timed out.")
#
#    return callback

message = ' { "story_prompt": "dogs and cats", "filename": "dogcat" } '
message_data = message.encode('utf-8')

future=publisher.publish(topic_path, message_data)

#publish_future.add_done_callback(get_callback(publish_future, data))
#publish_futures.append(publish_future)
#futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)
print(future.result())

print(f'sent {message} to {topic_path}')
