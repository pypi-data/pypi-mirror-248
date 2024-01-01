from bookshelf_common.events import create_connection

def init_listener(exchange_subject, queue_subject, callback, exchange_type='fanout', channel=None, **kwargs):
  if channel is None:
    channel, connection = create_connection(**kwargs)
  # Create fanout exchange
  channel.exchange_declare(exchange=exchange_subject, exchange_type=exchange_type)
  
  # Create queues and bind them to the exchange
  queue = channel.queue_declare(queue=queue_subject)
  channel.queue_bind(exchange=exchange_subject, queue=queue.method.queue)

  # Set up consumers
  channel.basic_consume(queue=queue.method.queue, on_message_callback=callback)
  
  print(' [*] Waiting for messages. To exit press CTRL+C')
  
  # Start consuming
  channel.start_consuming()

  
