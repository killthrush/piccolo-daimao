const express = require('express')
const bodyParser = require('body-parser')

const app = express()
const port = 3333

app.use(bodyParser.urlencoded({ extended: true }))
app.use(function (err, request, response, next) {
  console.error(err.stack)
  response.sendStatus(500)
})

app.post('/increment', (request, response, next) => {
  const key = request.body.key
  const value = request.body.value
  if (!key || !value) {
    response.sendStatus(400)
    return next()
  }
  response.send(`${key} - ${value}`)
})

app.listen(port, () => {
  console.log(`Listening on port ${port}...`)
})
