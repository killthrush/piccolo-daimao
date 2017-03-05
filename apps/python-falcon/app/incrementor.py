#from gevent import monkey, pywsgi
#monkey.patch_all()
import falcon
import bjoern


class NumberResource(object):
    def on_post(self, request, response):
        key = request.get_param('key')
        value = request.get_param('value')
        if not key or not value:
            raise falcon.HTTPBadRequest(
                'Missing parameter(s)',
                'An alphanumeric key and integer value must be supplied.'
            )
        response.status = falcon.HTTP_200
        #print key, value


app = falcon.API()
numbers = NumberResource()
app.add_route('/increment', numbers)


#bjoern.listen(app, '0.0.0.0', 3000)
#bjoern.run()