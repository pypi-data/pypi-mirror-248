import base64
import binascii
import hashlib
import importlib
import math
import warnings

from . crypto import (
     RANDOM_STRING_CHARS, constant_time_compare, get_random_string, pbkdf2,
)

UNUSABLE_PASSWORD_PREFIX = '!'
UNUSABLE_PASSWORD_SUFFIX_LENGTH = 40


def check_password(password: str, encoded):
    hasher = PBKDF2PasswordHasher()
    prefix = "%s$%d$" % (hasher.algorithm, hasher.iterations)
    encoded = prefix + encoded
    is_correct = hasher.verify(password, encoded)
    return is_correct


def make_password(password, salt=None):
    if password is None:
        return UNUSABLE_PASSWORD_PREFIX + get_random_string(UNUSABLE_PASSWORD_SUFFIX_LENGTH)
    if not isinstance(password, (bytes, str)):
        raise TypeError('Password must be a string or bytes, got %s.' % type(password).__qualname__)
    hasher = PBKDF2PasswordHasher()
    salt = salt or hasher.salt()
    return hasher.encode(password, salt)


def make_password2(password, salt=None):
    if password is None:
        raise TypeError('Password must be a string or bytes, got %s.' % type(password).__qualname__)
    if not isinstance(password, (bytes, str)):
        raise TypeError('Password must be a string or bytes, got %s.' % type(password).__qualname__)
    hasher = PBKDF2PasswordHasher()
    salt = salt or hasher.salt()
    encoded_passwd = hasher.encode(password, salt)
    prefix = "%s$%d$" % (hasher.algorithm, hasher.iterations)
    return encoded_passwd.replace(prefix, '')


def mask_hash(hash, show=6, char="*"):
    masked = hash[:show]
    masked += char * len(hash[show:])
    return masked


def must_update_salt(salt, expected_entropy):
    return len(salt) * math.log2(len(RANDOM_STRING_CHARS)) < expected_entropy


class BasePasswordHasher:
    """
    Abstract base class for password hashers

    When creating your own hasher, you need to override algorithm,
    verify(), encode() and safe_summary().

    PasswordHasher objects are immutable.
    """
    algorithm = None
    library = None
    salt_entropy = 128

    def _load_library(self):
        if self.library is not None:
            if isinstance(self.library, (tuple, list)):
                name, mod_path = self.library
            else:
                mod_path = self.library
            try:
                module = importlib.import_module(mod_path)
            except ImportError as e:
                raise ValueError("Couldn't load %r algorithm library: %s" %
                                 (self.__class__.__name__, e))
            return module
        raise ValueError("Hasher %r doesn't specify a library attribute" %
                         self.__class__.__name__)

    def salt(self):
        """
        Generate a cryptographically secure nonce salt in ASCII with an entropy
        of at least `salt_entropy` bits.
        """
        # Each character in the salt provides
        # log_2(len(alphabet)) bits of entropy.
        char_count = math.ceil(self.salt_entropy / math.log2(len(RANDOM_STRING_CHARS)))
        return get_random_string(char_count, allowed_chars=RANDOM_STRING_CHARS)

    def verify(self, password, encoded):
        """Check if the given password is correct."""
        raise NotImplementedError('subclasses of BasePasswordHasher must provide a verify() method')

    def encode(self, password, salt):
        """
        Create an encoded database value.

        The result is normally formatted as "algorithm$salt$hash" and
        must be fewer than 128 characters.
        """
        raise NotImplementedError('subclasses of BasePasswordHasher must provide an encode() method')

    def decode(self, encoded):
        """
        Return a decoded database value.

        The result is a dictionary and should contain `algorithm`, `hash`, and
        `salt`. Extra keys can be algorithm specific like `iterations` or
        `work_factor`.
        """
        raise NotImplementedError(
            'subclasses of BasePasswordHasher must provide a decode() method.'
        )

    def safe_summary(self, encoded):
        """
        Return a summary of safe values.

        The result is a dictionary and will be used where the password field
        must be displayed to construct a safe representation of the password.
        """
        raise NotImplementedError('subclasses of BasePasswordHasher must provide a safe_summary() method')

    def must_update(self, encoded):
        return False

    def harden_runtime(self, password, encoded):
        """
        Bridge the runtime gap between the work factor supplied in `encoded`
        and the work factor suggested by this hasher.

        Taking PBKDF2 as an example, if `encoded` contains 20000 iterations and
        `self.iterations` is 30000, this method should run password through
        another 10000 iterations of PBKDF2. Similar approaches should exist
        for any hasher that has a work factor. If not, this method should be
        defined as a no-op to silence the warning.
        """
        warnings.warn('subclasses of BasePasswordHasher should provide a harden_runtime() method')


class PBKDF2PasswordHasher(BasePasswordHasher):
    """
    Secure password hashing using the PBKDF2 algorithm (recommended)

    Configured to use PBKDF2 + HMAC + SHA256.
    The result is a 64 byte binary string.  Iterations may be changed
    safely but you must rename the algorithm if you change SHA256.
    """
    algorithm = "pbkdf2_sha256"
    iterations = 260000
    digest = hashlib.sha256

    def encode(self, password, salt, iterations=None):
        assert password is not None
        assert salt and '$' not in salt
        iterations = iterations or self.iterations
        hash = pbkdf2(password, salt, iterations, digest=self.digest)
        hash = base64.b64encode(hash).decode('ascii').strip()
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)

    def decode(self, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        return {
            'algorithm': algorithm,
            'hash': hash,
            'iterations': int(iterations),
            'salt': salt,
        }

    def verify(self, password, encoded):
        decoded = self.decode(encoded)
        encoded_2 = self.encode(password, decoded['salt'], decoded['iterations'])
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        decoded = self.decode(encoded)
        return {
            _('algorithm'): decoded['algorithm'],
            _('iterations'): decoded['iterations'],
            _('salt'): mask_hash(decoded['salt']),
            _('hash'): mask_hash(decoded['hash']),
        }

    def must_update(self, encoded):
        decoded = self.decode(encoded)
        update_salt = must_update_salt(decoded['salt'], self.salt_entropy)
        return (decoded['iterations'] != self.iterations) or update_salt

    def harden_runtime(self, password, encoded):
        decoded = self.decode(encoded)
        extra_iterations = self.iterations - decoded['iterations']
        if extra_iterations > 0:
            self.encode(password, decoded['salt'], extra_iterations)


class PBKDF2SHA1PasswordHasher(PBKDF2PasswordHasher):
    """
    Alternate PBKDF2 hasher which uses SHA1, the default PRF
    recommended by PKCS #5. This is compatible with other
    implementations of PBKDF2, such as openssl's
    PKCS5_PBKDF2_HMAC_SHA1().
    """
    algorithm = "pbkdf2_sha1"
    digest = hashlib.sha1


class Argon2PasswordHasher(BasePasswordHasher):
    """
    Secure password hashing using the argon2 algorithm.

    This is the winner of the Password Hashing Competition 2013-2015
    (https://password-hashing.net). It requires the argon2-cffi library which
    depends on native C code and might cause portability issues.
    """
    algorithm = 'argon2'
    library = 'argon2'

    time_cost = 2
    memory_cost = 102400
    parallelism = 8

    def encode(self, password, salt):
        argon2 = self._load_library()
        params = self.params()
        data = argon2.low_level.hash_secret(
            password.encode(),
            salt.encode(),
            time_cost=params.time_cost,
            memory_cost=params.memory_cost,
            parallelism=params.parallelism,
            hash_len=params.hash_len,
            type=params.type,
        )
        return self.algorithm + data.decode('ascii')

    def decode(self, encoded):
        argon2 = self._load_library()
        algorithm, rest = encoded.split('$', 1)
        assert algorithm == self.algorithm
        params = argon2.extract_parameters('$' + rest)
        variety, *_, b64salt, hash = rest.split('$')
        # Add padding.
        b64salt += '=' * (-len(b64salt) % 4)
        salt = base64.b64decode(b64salt).decode('latin1')
        return {
            'algorithm': algorithm,
            'hash': hash,
            'memory_cost': params.memory_cost,
            'parallelism': params.parallelism,
            'salt': salt,
            'time_cost': params.time_cost,
            'variety': variety,
            'version': params.version,
            'params': params,
        }

    def verify(self, password, encoded):
        argon2 = self._load_library()
        algorithm, rest = encoded.split('$', 1)
        assert algorithm == self.algorithm
        try:
            return argon2.PasswordHasher().verify('$' + rest, password)
        except argon2.exceptions.VerificationError:
            return False

    def safe_summary(self, encoded):
        decoded = self.decode(encoded)
        return {
            _('algorithm'): decoded['algorithm'],
            _('variety'): decoded['variety'],
            _('version'): decoded['version'],
            _('memory cost'): decoded['memory_cost'],
            _('time cost'): decoded['time_cost'],
            _('parallelism'): decoded['parallelism'],
            _('salt'): mask_hash(decoded['salt']),
            _('hash'): mask_hash(decoded['hash']),
        }

    def must_update(self, encoded):
        decoded = self.decode(encoded)
        current_params = decoded['params']
        new_params = self.params()
        # Set salt_len to the salt_len of the current parameters because salt
        # is explicitly passed to argon2.
        new_params.salt_len = current_params.salt_len
        update_salt = must_update_salt(decoded['salt'], self.salt_entropy)
        return (current_params != new_params) or update_salt

    def harden_runtime(self, password, encoded):
        # The runtime for Argon2 is too complicated to implement a sensible
        # hardening algorithm.
        pass

    def params(self):
        argon2 = self._load_library()
        # salt_len is a noop, because we provide our own salt.
        return argon2.Parameters(
            type=argon2.low_level.Type.ID,
            version=argon2.low_level.ARGON2_VERSION,
            salt_len=argon2.DEFAULT_RANDOM_SALT_LENGTH,
            hash_len=argon2.DEFAULT_HASH_LENGTH,
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
        )


class BCryptSHA256PasswordHasher(BasePasswordHasher):
    """
    Secure password hashing using the bcrypt algorithm (recommended)

    This is considered by many to be the most secure algorithm but you
    must first install the bcrypt library.  Please be warned that
    this library depends on native C code and might cause portability
    issues.
    """
    algorithm = "bcrypt_sha256"
    digest = hashlib.sha256
    library = ("bcrypt", "bcrypt")
    rounds = 12

    def salt(self):
        bcrypt = self._load_library()
        return bcrypt.gensalt(self.rounds)

    def encode(self, password, salt):
        bcrypt = self._load_library()
        password = password.encode()
        # Hash the password prior to using bcrypt to prevent password
        # truncation as described in #20138.
        if self.digest is not None:
            # Use binascii.hexlify() because a hex encoded bytestring is str.
            password = binascii.hexlify(self.digest(password).digest())

        data = bcrypt.hashpw(password, salt)
        return "%s$%s" % (self.algorithm, data.decode('ascii'))

    def decode(self, encoded):
        algorithm, empty, algostr, work_factor, data = encoded.split('$', 4)
        assert algorithm == self.algorithm
        return {
            'algorithm': algorithm,
            'algostr': algostr,
            'checksum': data[22:],
            'salt': data[:22],
            'work_factor': int(work_factor),
        }

    def verify(self, password, encoded):
        algorithm, data = encoded.split('$', 1)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, data.encode('ascii'))
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        decoded = self.decode(encoded)
        return {
            _('algorithm'): decoded['algorithm'],
            _('work factor'): decoded['work_factor'],
            _('salt'): mask_hash(decoded['salt']),
            _('checksum'): mask_hash(decoded['checksum']),
        }

    def must_update(self, encoded):
        decoded = self.decode(encoded)
        return decoded['work_factor'] != self.rounds

    def harden_runtime(self, password, encoded):
        _, data = encoded.split('$', 1)
        salt = data[:29]  # Length of the salt in bcrypt.
        rounds = data.split('$')[2]
        # work factor is logarithmic, adding one doubles the load.
        diff = 2**(self.rounds - int(rounds)) - 1
        while diff > 0:
            self.encode(password, salt.encode('ascii'))
            diff -= 1


class BCryptPasswordHasher(BCryptSHA256PasswordHasher):
    """
    Secure password hashing using the bcrypt algorithm

    This is considered by many to be the most secure algorithm but you
    must first install the bcrypt library.  Please be warned that
    this library depends on native C code and might cause portability
    issues.

    This hasher does not first hash the password which means it is subject to
    bcrypt's 72 bytes password truncation. Most use cases should prefer the
    BCryptSHA256PasswordHasher.
    """
    algorithm = "bcrypt"
    digest = None


class SHA1PasswordHasher(BasePasswordHasher):
    """
    The SHA1 password hashing algorithm (not recommended)
    """
    algorithm = "sha1"

    def encode(self, password, salt):
        assert password is not None
        assert salt and '$' not in salt
        hash = hashlib.sha1((salt + password).encode()).hexdigest()
        return "%s$%s$%s" % (self.algorithm, salt, hash)

    def decode(self, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        assert algorithm == self.algorithm
        return {
            'algorithm': algorithm,
            'hash': hash,
            'salt': salt,
        }

    def verify(self, password, encoded):
        decoded = self.decode(encoded)
        encoded_2 = self.encode(password, decoded['salt'])
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        decoded = self.decode(encoded)
        return {
            _('algorithm'): decoded['algorithm'],
            _('salt'): mask_hash(decoded['salt'], show=2),
            _('hash'): mask_hash(decoded['hash']),
        }

    def must_update(self, encoded):
        decoded = self.decode(encoded)
        return must_update_salt(decoded['salt'], self.salt_entropy)

    def harden_runtime(self, password, encoded):
        pass


class MD5PasswordHasher(BasePasswordHasher):
    """
    The Salted MD5 password hashing algorithm (not recommended)
    """
    algorithm = "md5"

    def encode(self, password, salt):
        assert password is not None
        assert salt and '$' not in salt
        hash = hashlib.md5((salt + password).encode()).hexdigest()
        return "%s$%s$%s" % (self.algorithm, salt, hash)

    def decode(self, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        assert algorithm == self.algorithm
        return {
            'algorithm': algorithm,
            'hash': hash,
            'salt': salt,
        }

    def verify(self, password, encoded):
        decoded = self.decode(encoded)
        encoded_2 = self.encode(password, decoded['salt'])
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        decoded = self.decode(encoded)
        return {
            _('algorithm'): decoded['algorithm'],
            _('salt'): mask_hash(decoded['salt'], show=2),
            _('hash'): mask_hash(decoded['hash']),
        }

    def must_update(self, encoded):
        decoded = self.decode(encoded)
        return must_update_salt(decoded['salt'], self.salt_entropy)

    def harden_runtime(self, password, encoded):
        pass


class UnsaltedSHA1PasswordHasher(BasePasswordHasher):
    """
    Very insecure algorithm that you should *never* use; store SHA1 hashes
    with an empty salt.

    This class is implemented because Django used to accept such password
    hashes. Some older Django installs still have these values lingering
    around so we need to handle and upgrade them properly.
    """
    algorithm = "unsalted_sha1"

    def salt(self):
        return ''

    def encode(self, password, salt):
        assert salt == ''
        hash = hashlib.sha1(password.encode()).hexdigest()
        return 'sha1$$%s' % hash

    def decode(self, encoded):
        assert encoded.startswith('sha1$$')
        return {
            'algorithm': self.algorithm,
            'hash': encoded[6:],
            'salt': None,
        }

    def verify(self, password, encoded):
        encoded_2 = self.encode(password, '')
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        decoded = self.decode(encoded)
        return {
            _('algorithm'): decoded['algorithm'],
            _('hash'): mask_hash(decoded['hash']),
        }

    def harden_runtime(self, password, encoded):
        pass


class UnsaltedMD5PasswordHasher(BasePasswordHasher):
    """
    Incredibly insecure algorithm that you should *never* use; stores unsalted
    MD5 hashes without the algorithm prefix, also accepts MD5 hashes with an
    empty salt.

    This class is implemented because Django used to store passwords this way
    and to accept such password hashes. Some older Django installs still have
    these values lingering around so we need to handle and upgrade them
    properly.
    """
    algorithm = "unsalted_md5"

    def salt(self):
        return ''

    def encode(self, password, salt):
        assert salt == ''
        return hashlib.md5(password.encode()).hexdigest()

    def decode(self, encoded):
        return {
            'algorithm': self.algorithm,
            'hash': encoded,
            'salt': None,
        }

    def verify(self, password, encoded):
        if len(encoded) == 37 and encoded.startswith('md5$$'):
            encoded = encoded[5:]
        encoded_2 = self.encode(password, '')
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        decoded = self.decode(encoded)
        return {
            _('algorithm'): decoded['algorithm'],
            _('hash'): mask_hash(decoded['hash'], show=3),
        }

    def harden_runtime(self, password, encoded):
        pass


class CryptPasswordHasher(BasePasswordHasher):
    """
    Password hashing using UNIX crypt (not recommended)

    The crypt module is not supported on all platforms.
    """
    algorithm = "crypt"
    library = "crypt"

    def salt(self):
        return get_random_string(2)

    def encode(self, password, salt):
        crypt = self._load_library()
        assert len(salt) == 2
        hash = crypt.crypt(password, salt)
        assert hash is not None  # A platform like OpenBSD with a dummy crypt module.
        # we don't need to store the salt, but Django used to do this
        return '%s$%s$%s' % (self.algorithm, '', hash)

    def decode(self, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        assert algorithm == self.algorithm
        return {
            'algorithm': algorithm,
            'hash': hash,
            'salt': salt,
        }

    def verify(self, password, encoded):
        crypt = self._load_library()
        decoded = self.decode(encoded)
        data = crypt.crypt(password, decoded['hash'])
        return constant_time_compare(decoded['hash'], data)

    def safe_summary(self, encoded):
        decoded = self.decode(encoded)
        return {
            _('algorithm'): decoded['algorithm'],
            _('salt'): decoded['salt'],
            _('hash'): mask_hash(decoded['hash'], show=3),
        }

    def harden_runtime(self, password, encoded):
        pass
