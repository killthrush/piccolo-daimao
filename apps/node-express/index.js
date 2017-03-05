const express = require('express')

const app = express()
const port = 3000


app.use(function (err, request, response, next) {
  console.error(err.stack)
  response.sendStatus(500)
})

app.post('/increment', (request, response, next) => {
  const key = request.query.key
  const value = request.query.value
  if (!key || !value) {
    response.sendStatus(400)
    return next()
  }
  response.send(`${key} - ${value}`)
})

app.listen(port, () => {
  console.log(`Listening on port ${port}...`)
})
