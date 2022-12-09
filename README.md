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
5. Next, visit the webauthn website at https://localhost and register the key.
6. On successful registration, the KMS and webauthn website exchange backup public key and keyid respectively.
7. In order to revoke it, login back to KMS and click 'Revoke'.
8 Try signing into the webauthn website to verify.

### For account recovery
1. Make sure that key is first revoked through the above steps.
2. In order to recover the account, use the backup public key to login with webauthn website. 
3. Register a new key to recover.

## Sample Output
### Webauthn storage displaying the key id and the KMS URL
![localstorage](https://user-images.githubusercontent.com/49821723/206775949-2a6fa737-6c96-49ac-b708-1ca5564e0fae.png)

### Registration time logged without the KMS
![registration-time-kms](https://user-images.githubusercontent.com/49821723/206776062-bba4425c-2d64-448e-8533-9ca766982580.png)

### Registration time logged with the KMS
![registration-time-wkms](https://user-images.githubusercontent.com/49821723/206776166-bc4ddce1-66f6-4eca-b231-68df70051510.png)



