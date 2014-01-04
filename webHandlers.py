#coding=utf-8
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import datetime
import json
import codecs
codecs.register(lambda name: name == 'cp65001' and codecs.lookup('utf-8') or None)

from dataRetriever import DataRetriever

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        self.dataRetriever = DataRetriever()
        handlers = [(r"/login", LoginHandler),
                    (r"/twitter/(\w+)", MainPageHandler),
                    (r"/comment", CommentHandler),
                    (r"/logout", LogoutHandler),
                    (r"/getInfo", FloatWindowHandler)]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        user = self.application.dataRetriever.getUser(username)
        if user and user["password"] == password:
            self.set_secure_cookie("user", username)
            self.redirect("/twitter/" + username)
        else:
            self.redirect("/login")

class MainPageHandler(tornado.web.RequestHandler):
    def get(self, input):
        user = self.application.dataRetriever.getUser(input)
        userInCookie = self.get_secure_cookie("user")
        if user == None or userInCookie != input or userInCookie == None or userInCookie == "":
            self.redirect("/login")
        else:
            allTwitters = user["twitters"]
            for oneTwitter in allTwitters:
                oneTwitter["username"] = user["name"]
                date = datetime.datetime.strptime(oneTwitter["time"], "%b %d %Y %H:%M:%S")
                oneTwitter["time"] = date.strftime("%Y-%m-%d %H:%M:%S")
            for i in range(len(user["friends"])):
                for oneTwitter in self.application.dataRetriever.getUser(user["friends"][i])["twitters"]:
                    oneTwitter["username"] = user["friends"][i]
                    date = datetime.datetime.strptime(oneTwitter["time"], "%b %d %Y %H:%M:%S")
                    oneTwitter["time"] = date.strftime("%Y-%m-%d %H:%M:%S")
                    allTwitters.append(oneTwitter)
            sortedList = sorted(allTwitters, key=lambda k: k["time"])
            self.render("index.html", user=user, allTwitters=sortedList)

    def post(self, input):
        pass
    
class CommentHandler(tornado.web.RequestHandler):
    def get(self):
        username = self.get_argument("username")
        twitterDate = datetime.datetime.strptime(self.get_argument("twitterDate"), "%Y-%m-%d %H:%M:%S")
        user = self.application.dataRetriever.getUser(username)
        allTwitters = user["twitters"]
        comments = []
        for oneTwitter in allTwitters:
            if twitterDate == datetime.datetime.strptime(oneTwitter["time"], "%b %d %Y %H:%M:%S") and "comments" in oneTwitter:
                comments = oneTwitter["comments"]
                break
        self.write(json.dumps(comments))

    def post(self):
        twitterOwnerUsername = self.get_argument("twitterOwnerUsername")
        twitterDate = datetime.datetime.strptime(self.get_argument("twitterDate"), "%Y-%m-%d %H:%M:%S")
        commentContent = self.get_argument("commentContent")
        commentDate = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
        commentUser = self.get_secure_cookie("user")

        newComment = {"comment_date": commentDate, "comment_by": commentUser, "comment_content": commentContent}
        user = self.application.dataRetriever.getUser(twitterOwnerUsername)
        for oneTwitter in user["twitters"]:
            if twitterDate == datetime.datetime.strptime(oneTwitter["time"], "%b %d %Y %H:%M:%S"):
                if "comments" in oneTwitter:
                    oneTwitter["comments"].append(newComment)
                else:
                    oneTwitter["comments"] = []
                    oneTwitter["comments"].append(newComment)
                break
        self.application.dataRetriever.updateTwitter(twitterOwnerUsername, user["twitters"])
        self.write(json.dumps(newComment))


class FloatWindowHandler(tornado.web.RequestHandler):
    def get(self):
        user = self.application.dataRetriever.getUser(self.get_secure_cookie("user"))
        friendsNum = 0
        twittersNum = 0
        if user["friends"]:
            friendsNum = len(user["friends"])
        if user["twitters"]:
            twittersNum = len(user["twitters"])
        self.write(json.dumps({"friendsNum": friendsNum, "twittersNum": twittersNum}))

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_secure_cookie("user", "")
        self.redirect("/login")
        

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()