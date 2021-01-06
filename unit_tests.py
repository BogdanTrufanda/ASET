import unittest
import brute
import hasher

class UnitTestCases(unittest.TestCase):
    def test_ipValiderOK(self):
        """
        Test if the given string is a valid IP address.
        """
        stringGiven = "204.120.0.15"
        result = brute.valid_ip(stringGiven)
        self.assertEqual(result, True)


    def test_ipValiderNOK(self):
        """
        Test if the given string is a valid IP address.
        """
        stringGiven = "204.120.sd0.15"
        result = brute.valid_ip(stringGiven)
        self.assertEqual(result, False)


    def test_validAddressOK(self):
        """
        Test if the given address is correct.
        """
        stringGiven = "www.juice-shop.herokuapp.com"
        result = brute.valid_address(stringGiven)
        self.assertEqual(result, ("Match domain", True))


    def test_isJsonOK(self):
        """
        Test if the string is in JSON format.
        """
        stringGiven = '{ "name":"John", "age":30, "city":"New York"}'
        result = brute.is_json(stringGiven)
        self.assertEqual(result, True)


    def test_isJsonNOK(self):
        """
        Test if the string is not in json format.
        """
        stringGiven = "name=john, age=30, city=new york"
        result = brute.is_json(stringGiven)
        self.assertEqual(result, False)


    def test_leetWords(self):
        """
        Test if it modifies the words.
        """
        stringGiven = "oli"
        result = brute.leet_words(stringGiven)
        self.assertEqual(result, ['oli', 'ol1', 'o1i', 'o11', '0li', '0l1', '01i', '011'])


    def test_upperLeet(self):
        """
        Test if it modifies the words.
        """
        stringGiven = "OLI"
        result = brute.leet_words(stringGiven)
        self.assertEqual(result, ['oli', 'ol1', 'o1i', 'o11', '0li', '0l1', '01i', '011'])


    def test_sha1Decrypt(self):
        """
        Test that it can sha1 encrypt.
        """
        word = "password"
        result = hasher.sha1_decrypt("5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8","wordlist_unittest.txt")
        self.assertEqual(result, word)


    def test_sha256Decrypt(self):
        """
        Test that it can sha256 encrypt.
        """
        word = "password"
        result = hasher.sha256_decrypt("5E884898DA28047151D0E56F8DC6292773603D0D6AABBDD62A11EF721D1542D8","wordlist_unittest.txt")
        self.assertEqual(result, word)


    def test_md5Decrypt(self):
        """
        Test that it can md5 encrypt.
        """
        word = "password"
        result = hasher.md5_decrypt("5F4DCC3B5AA765D61D8327DEB882CF99","wordlist_unittest.txt")
        self.assertEqual(result, word)


    def test_getType(self):
        """
        Test if it can identify type by the lenght of the hash.
        """
        guessedHash = "5F4DCC3B5AA765D61D8327DEB882CF99"
        hashType = hasher.get_type(guessedHash)
        self.assertEqual(hashType, "MD5")


    def test_getNoType(self):
        """
        Test if it can identify type by the lenght of the hash.
        """
        guessedHash = "lessChar"
        hashType = hasher.get_type(guessedHash)
        self.assertEqual(hashType, "Hash type not supported or not hash.")



if __name__ == '__main__':
    unittest.main()