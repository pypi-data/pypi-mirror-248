# Secret-Agent

### Examples
```
# automatically generates a key and encrypts an empty string
secret = SecretAgent.Secret()

# rekey the secret
secret.rekey()

# update the secret value
secret.update_value(data='new string value')

# fetch the secret value as clear text
secret_text = secret.clear_text


# encrypt using user supplied password
secret = SecretAgent.Secret(passwordKeyAsClearText='P@ssw0rd!!', data='secret text', forgetKeyOnCreation=True)
secret_text = secret.unlock(password=input())
```