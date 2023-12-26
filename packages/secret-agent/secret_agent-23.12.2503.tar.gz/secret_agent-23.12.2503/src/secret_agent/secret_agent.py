import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# all encrypt functions point here
def _encrypt_(key, data) -> bytes:
  if not type(data) is bytes:
    data = str(data).encode('utf-8')
  return Fernet(key).encrypt(data)

# all decrypt functions point here
def _decrypt_(key, data) -> str:
  data = Fernet(key).decrypt(data)
  return data.decode('utf-8')

# convert data to a base64 encoded string
def toBase64String(data) -> str: 
  return base64.b64encode(data).decode('utf-8')

# convert a base64 encoded string to data
def fromBase64String(base64string) -> bytes:
  return base64.b64decode(base64string.encode('utf-8'))

# generate an encryption key
def generateKey() -> bytes:
  return Fernet.generate_key()

# generate an encryption key and return as a base64 encoded string
def generateKeyAsBase64() -> str:
  return toBase64String(generateKey())

# encrypt data with the provided encryption key
def encryptWithKey(key, data) -> bytes:
  return _encrypt_(key, data)

# encrypt data with the provided encryption key and return as base64 encoded string
def encryptWithKeyAsBase64(key, data) -> str:
  return toBase64String(_encrypt_(key, data))

# decrypt data with provided encryption key
def decryptWithKey(key, data) -> str:
  return _decrypt_(key, data)

# decrypt base64 encoded data with provided base 64 encryption key, all with a super long function name
def decryptWithBase64EncodedKeyAndBase64EncodedData(keyAsBase64, dataAsBase64) -> str:
  return _decrypt_(key=fromBase64String(keyAsBase64), data=fromBase64String(dataAsBase64))

# generate a key from a password
def generateKeyFromPassword(password: str) -> bytes:
  password = bytes(password, encoding="raw_unicode_escape")
  salt = password
  kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
  )
  key = base64.urlsafe_b64encode(kdf.derive(password))
  return key

# generate a base64 encoded key from a password
def generateKeyFromPasswordAsBase64(password: str) -> str:
  toBase64String(data=generateKeyFromPassword(password=password))

# decrypt with password
def decryptDataWithPassword(data, password: str) -> str:
  key = generateKeyFromPassword(password=password)
  return decryptWithKey(key=key, data=data)
  
# secret messages and their corresponding key
class Secret:
  
  key: bytes
  keyAsBase64: str
  encryptedData: bytes
  encryptedDataAsBase64: str

  def __init__(self, key: bytes = None, keyAsBase64: str = None, 
               passwordKeyAsClearText: str = None,
               data = None, base64Data: str = None, 
               encryptedData: bytes = None, encryptedDataAsBase64: str = None,
               forgetKeyOnCreation: bool = False) -> None:
    
    if (data and (encryptedData or encryptedDataAsBase64)) or (base64Data and (encryptedData or encryptedDataAsBase64)):
      raise AttributeError('Cannot supply both unencrypted and encrypted data, only pass one or the other!')

    if key:
      self.key = key
      self.keyAsBase64 = toBase64String(data=key)
    elif keyAsBase64:
      self.key = fromBase64String(base64string=keyAsBase64)
      self.keyAsBase64 = keyAsBase64
    elif passwordKeyAsClearText:
      self.key = generateKeyFromPassword(password=passwordKeyAsClearText)
      self.keyAsBase64 = toBase64String(data=self.key)
    else:
      self.key = generateKey()
      self.keyAsBase64 = toBase64String(data=self.key)

    if data:
      self.encryptedData = encryptWithKey(key=self.key, data=data)
      self.encryptedDataAsBase64 = toBase64String(data=self.encryptedData)
    elif base64Data:
      self.encryptedData = encryptWithKey(key=self.key, data=fromBase64String(base64string=base64Data))
      self.encryptedDataAsBase64 = toBase64String(data=self.encryptedData)
    else:
      self.encryptedData = encryptWithKey(key=self.key, data=b'')
      self.encryptedDataAsBase64 = toBase64String(data=self.encryptedData)

    if encryptedData:
      self.encryptedData = encryptedData
      self.encryptedDataAsBase64 = toBase64String(data=encryptedData)
    elif encryptedDataAsBase64:
      self.encryptedData = fromBase64String(base64string=encryptedDataAsBase64)
      self.encryptedDataAsBase64 = encryptedDataAsBase64

    if forgetKeyOnCreation:
      self.forget_key()

  # return the secret as clear text
  @property
  def clear_text(self) -> str:
    if not self.key:
      raise Exception('Secret missing key!')
    
    return _decrypt_(key=self.key, data=self.encryptedData)
  
  # re-encrypt data using a new key, generated if not provided
  def rekey(self, key: bytes = None, keyAsBase64: str = None) -> None:
    secret = self.clear_text

    if key:
      self.key = key
      self.keyAsBase64 = toBase64String(data=key)
    elif keyAsBase64:
      self.key = fromBase64String(base64string=keyAsBase64)
      self.keyAsBase64 = keyAsBase64
    else:
      self.key = generateKey()
      self.keyAsBase64 = toBase64String(data=self.key)

    self.encryptedData = encryptWithKey(key=self.key, data=secret)
    self.encryptedDataAsBase64 = toBase64String(data=self.encryptedData)

    secret = None

  # update the encrypted data value
  def update_value(self, data, key: bytes = None, password: str = None) -> None:
    if self.key and not key and not password:
      self.encryptedData = encryptWithKey(key=self.key, data=data)
      self.encryptedDataAsBase64 = toBase64String(data=self.encryptedData)
      return
    
    if key or password:
      if key and password:
        raise Exception('Must supply only key or password, not both!')
      
      if key:
        self.encryptedData = encryptWithKey(key=key, data=data)
        self.encryptedDataAsBase64 = toBase64String(data=self.encryptedData)
        return
      
      if password:
        self.encryptedData = encryptWithKey(key=generateKeyFromPassword(password=password), data=data)
        self.encryptedDataAsBase64 = toBase64String(data=self.encryptedData)
        return
      
    raise Exception('Secret missing key!')


  # delete the key (for use when using pw generated keys)
  def forget_key(self) -> None:
    self.key = None
    self.keyAsBase64 = None

  # unlock with key
  def _decrypt_(self, key: bytes) -> str:
    return _decrypt_(key=key, data=self.encryptedData)

  # unlock with password
  def unlock(self, password: str) -> str:
    return self._decrypt_(key=generateKeyFromPassword(password=password))
