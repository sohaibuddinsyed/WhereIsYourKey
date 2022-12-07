# webauthn.io
Our project uses WebAuthn library and implementaion by Duo labs
[py_webauthn](https://github.com/duo-labs/py_webauthn).

## Prerequisites

- Docker
- Pipenv
  - Make sure Python3 is available
  - Enables `pipenv install` to set up libraries locally for the editor to crawl. 
  - The Django container also uses Pipenv to install dependencies to encourage use of this new Python package management tool.
  - To add any new package add package name to Pipfile and run pipenv install to generate Pipfile.lock that will be imported in docker container
## Environmental Variable

- `DJANGO_SECRET_KEY`: A sufficiently random string
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `PROD_HOST_NAME`: The domain name the site will be hosted at
- `RP_ID`: The Relying Party ID, typically the same as `PROD_HOST_NAME`
- `RP_NAME`: A representation of the site's name to be shown to users
- `RP_EXPECTED_ORIGIN`: The domain name plus protocol at which WebAuthn will be invoked (e.g. `https://webauthn.io`)

## Development

Run the following command to get started:

```sh
$> ./start-dev.sh
```

The webauthn website will be available at https://localhost
and KMS server will be avilable at http://localhost:5000

## Example usage
### For account revocation
1. Open http://localhost:5000 in your browser it'll lead to Key management flask server.
2. Register with your credentials and have a unique ID that will be used across different websites, we suggest user to make it a sha256 hash of their private key, these ID will be used by KMS to uniquely identify user keys across different website.
3. After registration login with the credentials from previous step.
4. We have to manually add this Id and backup URL to chrome localstorage since this value must be passed along with registration request and in real world scenario they must be supplied by the autenticator.
5. 