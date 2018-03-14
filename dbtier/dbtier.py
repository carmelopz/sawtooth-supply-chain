import rethinkdb as r
r.connect( "0.0.0.0", 28020).repl()
print r.db('supply_chain').table('agents').run()
