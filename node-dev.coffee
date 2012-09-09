http = require("http")
qs = require("querystring")

http.createServer((req, res) ->

  console.log('asdf')

  res.writeHead 200, "Content-Type": "text/plain"

  console.log('asdf')

  fs.readFile __dirname + "/views/chat.html", "utf8", (err, text) ->
    res.send text

  console.log message

  res.end message
).listen 80, "0.0.0.0"

console.log "Server running at http://0.0.0.0/"

#adjectives =  [
#  'hip'
#  'crazy'
#  'cool'
#  'fun'
#  'happy'
#  'uber'
#  'captain'
#  'fierce'
#  'amazing'
#  'fantastic'
#  'big'
#  'mister'
#  'phat'
#  'friendly'
#  'amiable'
#  'upbeat'
#  'hyper'
#  'chill'
#  'relaxed'
#  'tremendous'
#  'outstanding'
#  'little'
#  'tiny'
#]
#
#nouns = [
#  'cat'
#  'dawg'
#  'pants'
#  'head'
#  'fish'
#  'player'
#  'dude'
#  'animal'
#  'gamer'
#]
