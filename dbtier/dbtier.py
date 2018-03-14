import rethinkdb as r


r.connect( "0.0.0.0", 28020).repl()

agentsCursor = r.db('supply_chain').table('agents').run()
agentsList=list(agentsCursor)

from bson.json_util import dumps
agentsJson=dumps(agentsList)

from json2html import *
agentsHtml = json2html.convert(json = agentsJson)

from flask import Flask
app = Flask(__name__)

@app.route("/")
def dbtier():
	return (agentsHtml)

app.run(host='0.0.0.0', port=40080)








