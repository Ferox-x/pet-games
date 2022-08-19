from django.test import TestCase

from core.templatetags.template_tags import header_max_len, message_max_len


class TestCustomTags(TestCase):

    def test_header_max_len(self):
        long_header = 'TestTestTestTestTestTestTest'
        header = 'TestTest'
        len_after_tag = 23
        short_header = header_max_len(long_header)
        normal_header = header_max_len(header)
        self.assertEqual(len(short_header), len_after_tag)
        self.assertEqual(len(normal_header), len(normal_header))

    def test_message_max_len(self):
        long_message = 'MessageMessageMessageMessageMessageMessageMessageMessageMessageMessageMessageMessageMessageMessageMessageMessageMessageMessageMessageMessageMessageMessage'
        message = 'Message Message'
        len_after_tag = 63
        short_message = message_max_len(long_message)
        normal_message = message_max_len(message)
        self.assertEqual(len(short_message), len_after_tag)
        self.assertEqual(len(normal_message), len(message))
