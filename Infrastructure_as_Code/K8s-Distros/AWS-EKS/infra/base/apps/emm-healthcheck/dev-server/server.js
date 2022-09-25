import express from 'express'
import { lambdaHandler } from 'emm-healthcheck'

const app = express()
const port = 3000

app.use(express.text({ type: '*/*' }))

app.all('/*', async (req, res) => {
  const result = await lambdaHandler(
    {
      path: req.path,
      httpMethod: req.method,
      body: req.body,
      isBase64Encoded: false,
      queryStringParameters: req.query,
      multiValueQueryStringParameters: toMultiValue(req.query),
      headers: req.headers,
      multiValueHeaders: toMultiValue(req.headers)
    },
    {}
  )

  if (result.statusCode) {
    res.status(result.statusCode)
  }
  if (result.headers) {
    for (const key in result.headers) {
      res.setHeader(key, result.headers[key])
    }
  }
  if (result.body) {
    res.send(result.body)
  }
  res.end();
})

function toMultiValue(obj) {
  const result = {}
  for (const key in obj) {
    const val = obj[key]
    result[key] = Array.isArray(val) ? val : [val]
  }

  return result
}

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})