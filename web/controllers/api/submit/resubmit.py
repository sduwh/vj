from tornado.web import RequestHandler
from tornado import gen
from bson import ObjectId

class Handler(RequestHandler):
    """
    重新提交 API
    """

    @gen.coroutine
    def get(self, submit_id):
        print(submit_id)
        r = yield self.settings["database"]["submission"].update_one({
            '_id': ObjectId(submit_id)
        },{
            '$set': {'result': 'Queueing'}
        })
        if not r.acknowledged:
            raise RuntimeError('Resubmit {} error'.format(submit_id))
        referer = self.request.headers["referer"]
        self.redirect(referer)
