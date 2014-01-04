import pymongo

user1_info={
    "name":"britneyspears",
    "password":"12345",
    "image":"/static/image/britneyspears.jpg",
    "age":32,
    "email":"britneyspears@xxx.com",
    "friends":["greenday", "U2"],
    "twitters":[
        {"time":"Nov 18 2013 10:30:00",
         "content":"I have always been interested in the scientific discoveries underlying health advances in developing countries. The benefits of such breakthroughs are substantial, with the potential to save hundreds of thousands of lives."
        },

        {"time":"Nov 1 2013 22:35:00",
         "content":"How cool is that? I asked him to pay off my student loans if he got me. I guess that is a no go now. ;-)",
         "comments":[
             {"comment_date": "Nov 1 2013 22:37:16",
              "comment_by": "greenday",
              "comment_content": "Yes. It's really cool."
             },
             {"comment_date": "Nov 2 2013 20:45:10",
              "comment_by": "U2",
              "comment_content": "Amazing!"
             }
         ]
        },

        {"time":"Dec 11 2013 11:05:00",
         "content":"holy wow!!"
        },

        {"time":"Dec 20 2013 20:50:00",
         "content":"I laughed really hard at that. Those are wonderful gifts, and you are an awesome receiver! Very entertaining experience :)"
        },

        {"time":"Dec 15 2013 16:30:00",
         "content":"Thank you for sharing your experience! It was a fun read :)",
         "comments":[
             {"comment_date": "Dec 15 2013 22:30:00",
              "comment_by": "greenday",
              "comment_content": "Enjoy yourself."
             },
             {"comment_date": "Dec 15 2013 22:37:00",
              "comment_by": "britneyspears",
              "comment_content": "Thank you!"
             }
         ]
        },

        {"time":"Dec 24 2013 17:30:05",
         "content":"That is amazing! The picture alone is worth it!!"
        }
    ]
}

user2_info={
    "name":"greenday",
    "password":"123",
    "image":"/static/image/greenday.jpg",
    "age":26,
    "email":"greenday@xxx.com",
    "friends":["britneyspears", "U2"],
    "twitters":[
        {"time":"Nov 26 2013 10:30:00",
         "content":"The Idiot Nation T-Shirt design contest ends TODAY at 5pm PST!",
         "comments":[
             {"comment_date": "Nov 26 2013 11:30:00",
              "comment_by": "U2",
              "comment_content": "Very beautiful."
             },
             {"comment_date": "Nov 26 2013 11:38:00",
              "comment_by": "greenday",
              "comment_content": "You are right."
             }
         ]
        },

        {"time":"Nov 22 2013 04:35:50",
         "content":"Idiot Nation Giveaway: We're giving fans the chance to win @broadwayidiot on DVD or 10 digital downloads!"
        },

        {"time":"Dec 21 2013 18:28:00",
         "content":"New episode of The Jeff Matika Show featuring Tre Cool !"
        }
    ]
}

user3_info={
    "name":"U2",
    "password":"1234567",
    "image":"/static/image/U2.jpg",
    "age":37,
    "email":"U2@xxx.com",
    "friends":["greenday"],
    "twitters":[
        {"time":"Dec 1 2013 10:30:00",
         "content":"'Adam pretended he could play & talked about 'action' on the bass' North Side Stories."
        },

        {"time":"Nov 20 2013 15:30:00",
         "content":"We thought it should be a love song, a very human song.",
         "comments":[
             {"comment_date": "Nov 21 2013 15:35:00",
              "comment_by": "greenday",
              "comment_content": "Very good song."
             }
         ]
        },

        {"time":"Dec 25 2013 17:30:00",
         "content":"'Arrive in Denver, Edge discovers ski resort up country.' North Side Stories."
        }
    ]
}

def importUsers():
    userSets.remove()
    userSets.insert(user1_info)
    userSets.insert(user2_info)
    userSets.insert(user3_info)

def valid():
    for user in userSets.find():
        print user
        print '\n'

conn=pymongo.Connection("localhost",27017)
twitterDB=conn["twitterDB"]
userSets=twitterDB.userSets
importUsers()
valid()

