const express = require('express')
const axios = require('axios')

// init
const app = express()

// env
require('dotenv').config()

// respond with "hello world" when a GET request is made to the homepage
app.get('/', (req, res) => {
  if (req.query.name) res.send(`Welcome ${req.query.name}, you are logged in ✅`)
  else res.send('Hello 👋, you are not logged in ⛔')
})

function asyncWrapper(fn) {
  return (req, res, next) => {
    return Promise.resolve(fn(req))
      .then((result) => res.send(result))
      .catch((err) => next(err))
  }
}

app.get('/login', (req, res) => {
  res.redirect(`https://github.com/login/oauth/authorize?client_id=${process.env.CLIENT_ID}&scope=user`)
})

const getAccessToken = async (req, res) => {
  try {
  const { code } = req.query
  const { data } = await axios.post('https://github.com/login/oauth/access_token', {
    client_id: process.env.CLIENT_ID,
    client_secret: process.env.CLIENT_SECRET,
    code
  }, {
    headers: { Accept: 'application/json' }
  })
  const { access_token } = data
  const { data: profileData } = await axios.get('https://api.github.com/user', {
    headers: { Authorization: 'Bearer ' + access_token}
  })
  res.redirect('/?name=' + profileData.name)
  } catch (err) { console.log(err.response) }
}

app.get('/oauth/redirect', (req, res) => asyncWrapper(getAccessToken(req, res)))

// Listen on port
app.listen(23070)
