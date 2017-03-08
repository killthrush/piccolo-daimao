from gevent import monkey, pywsgi, Greenlet
monkey.patch_all()
import sys
import falcon
import redis
import gevent
from gevent.lock import Semaphore

PORT = 3333
HOST = '0.0.0.0'
BACKGROUND_WORKER_SECONDS = 1


class NumberResource(object):
    def __init__(self):
        self.work_map = {}
        self.redis_client = redis.StrictRedis() # will connect to localhost, standard port, db 0 by default
        self.semaphore = Semaphore()
        self.total_requests = 0
        self.total_sum = 0

    def process_work_map(self):
        global total_sum
        finished_work_map = {}
        with self.semaphore:
            (self.work_map, finished_work_map) = (finished_work_map, self.work_map)
        pipeline = self.redis_client.pipeline()
        for key, values_list in finished_work_map.items():
            print "work list {} has {} items".format(key, len(values_list))
            sum = reduce(lambda accumulator, n: accumulator + n, values_list, 0)
            self.total_sum += sum
            pipeline.lpush(key, sum)
            print "Pipelining sum {} for transmission".format(sum)
            print "total requests {}".format(self.total_requests)
            print "total sum {}".format(self.total_sum)
        pipeline.execute()

    def store_periodically(self):
        while True:
            gevent.sleep(BACKGROUND_WORKER_SECONDS)
            self.process_work_map()

    def on_post(self, request, response):
        with self.semaphore:
            self.total_requests += 1  # Maybe not the best idea to add the extra lock, but I really want this info =)
        key = request.get_param('key')
        value = request.get_param('value')
        if not key or not value:
            raise falcon.HTTPBadRequest(
                'Missing parameter(s)',
                'An alphanumeric key and integer value must be supplied.'
            )
        with self.semaphore:
            if not key in self.work_map:
                self.work_map[key] = []
            self.work_map[key].append(int(value))
        response.status = falcon.HTTP_200
        response.body = "Total Requests: {}".format(self.total_requests)


app = falcon.API()
app.req_options.auto_parse_form_urlencoded=True
numbers = NumberResource()
gevent.spawn(numbers.store_periodically)
app.add_route('/increment', numbers)


if __name__ == '__main__' and len(sys.argv) > 1:
    if sys.argv[1] == 'bjoern':
        # Bjoern is blazing fast, but its event loop is opaque.
        # This means no background workers, and thus no guarantee that the server
        # state will be completely flushed to the database at any given moment.
        print "Bjoern WSGI server active - host {} port {}...".format(HOST, PORT)
        import bjoern
        bjoern.listen(app, HOST, PORT)
        bjoern.run()
    elif sys.argv[1] == 'pywsgi':
        # PyWSGI with gevent support is far faster than I expected - faster
        # it seems than an out-of-the-box node/express installation.
        print "PyWSGI server active - host {} port {}...".format(HOST, PORT)
        server = pywsgi.WSGIServer((HOST, PORT), app, log=None)
        server.serve_forever()