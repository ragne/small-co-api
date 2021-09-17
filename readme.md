### Small but proud co API

This is a simple python API written in flask that does the following:

- get file from storage
- delete file from storage
- upload file from storage
- provide a /health endpoint
- uses AWS S3 for storage

### Assumptions

- if system ensures unique usernames, then one user perfectly maps to one avatar picture
- only small subset of image format is supported
- credentials to s3 are assumed to be presented in environment
-

### Usage

set S3_BUCKET env. var to the bucket you control. Ensure that AWS credentials are available in env.vars or in instance profile.

Run: `$S3_BUCKET="test" make run_prod`
It should output:

    INFO:waitress:Serving on http://0.0.0.0:8080

### Testing

use `make run` to run a dev build. It expects `moto_server` running on port 8000, use `make moto_server` for that in separate terminal tab.

There's also a postman collection in `small-co-api.postman_collection.json`, use it!

### TODO

- Docker
- Error handling

### Contacts

No. I'm an unpaid intern.
