import sys
import sqlite3
import redis
import gevent

BACKGROUND_WORKER_SECONDS = .1


class Consumer(object):
    def __init__(self, database_path):
        self.database_client = sqlite3.connect(database_path)
        self.redis_client = redis.StrictRedis() # will connect to localhost, standard port, db 0 by default

    def process(self):
        for key in self.redis_client.scan_iter():
            value_to_add = self.redis_client.rpop(key)
            while value_to_add: # will be None if the redis list is empty

                # This UPSERT is safe since we're single-threaded in this process
                cursor = self.database_client.execute('SELECT value FROM numbers WHERE key=?', (key,))
                result = cursor.fetchone()
                if result is None:
                    print "Insert new value {} into key {}".format(0, key)
                    self.database_client.execute('INSERT INTO numbers VALUES (?, ?)', (key, 0))
                else:
                    current_value = result[0]
                    new_value = int(current_value) + int(value_to_add)
                    print "Update existing value {} to {} for key {}".format(current_value, new_value, key)
                    self.database_client.execute('UPDATE numbers SET value=? WHERE key=?', (new_value, key))

                value_to_add = self.redis_client.rpop(key)


def run(database_path):
    consumer = Consumer(database_path)
    while True:
        gevent.sleep(BACKGROUND_WORKER_SECONDS)
        consumer.process()


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        raise ValueError("Must supply a path to the SQLite database! Exiting...")
    run(sys.argv[1])