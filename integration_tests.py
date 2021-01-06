import unittest
import brute
import hasher


class IntegrationTestCases(unittest.TestCase):
    def test_decryptMD5(self):
        """
        Test the successful run of decrypt() method with includes the get_type() method.
        Tested with MD5 hash of word 'password'.
        """
        word = "password"
        hashGiven = "5F4DCC3B5AA765D61D8327DEB882CF99"
        result = hasher.decrypt(hashGiven, "wordlist_unittest.txt")
        self.assertEqual(result, word)


    def test_decryptSHA1(self):
        """
        Test the successful run of decrypt() method with includes the get_type() method.
        Tested with SHA1 hash of word 'password'.
        """
        word = "password"
        hashGiven = "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8"
        result = hasher.decrypt(hashGiven, "wordlist_unittest.txt")
        self.assertEqual(result, word)


    def test_decryptSHA256(self):
        """
        Test the successful run of decrypt() method with includes the get_type() method.
        Tested with SHA256 hash of word 'password'.
        """
        word = "password"
        hashGiven = "5E884898DA28047151D0E56F8DC6292773603D0D6AABBDD62A11EF721D1542D8"
        result = hasher.decrypt(hashGiven, "wordlist_unittest.txt")
        self.assertEqual(result, word)


    def test_decideOK(self):
        """
        Test the decision of to call or not the decrypt() method based on the supported hash types.
        True variant with MD5 length long given hash.
        """
        hashGiven = "5F4DCC3B5AA765D61D8327DEB882CF99"
        result = hasher.decide(hashGiven)
        self.assertEqual(result, True)


    def test_decideOK(self):
        """
        Test the decision of to call or not the decrypt() method based on the supported hash types.
        False variant with not supported length given hash.
        """
        hashGiven = "5F4DCC3B5AA765D61D8327DEB882CF9"
        result = hasher.decide(hashGiven)
        self.assertEqual(result, False)


    def test_validAdressNOK(self):
        """
        Test if the address is correct.
        """
        stringGiven = "www.dirtbike.ro"
        result = brute.valid_address(stringGiven)
        self.assertEqual(result, ("Wrong domain!", False))


    def test_validAdressIPNOK(self):
        """
        Test if the address is correct.
        """
        stringGiven = "192.1618.1.1"
        result = brute.valid_address(stringGiven)
        self.assertEqual(result, ("Wrong IP format", False))


    def test_validAdressIPOK(self):
        """
        Test if the address is correct.
        """
        stringGiven = "192.168.1.1"
        result = brute.valid_address(stringGiven)
        self.assertEqual(result, ("Valid IP address!", False))


    def test_validAdressOK(self):
        """
        Test if the address is correct.
        """
        stringGiven = "www.juice-shop.herokuapp.com"
        result = brute.valid_address(stringGiven)
        self.assertEqual(result, ("Match domain", True))