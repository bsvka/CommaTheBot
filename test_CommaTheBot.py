import unittest
from CommaTheBot import *

class TestCommaTheBot(unittest.TestCase):
    def test_no_title(self):
        title = ""
        assert needs_fixing(title) == False

    def test_no_fixing(self):
        title = "The Foo"
        assert needs_fixing(title) == False
    
    def test_needs_fixing(self):
        title = "Foo, The"
        assert needs_fixing(title) == True
    
    def test_fix(self):
        title = "Foo, The"
        fixed_title = fix_title(title)
        assert fixed_title == "The Foo"
    
    def test_pattern_match(self):
        # case of article is kept, with and without space
        title = "Foo, The"
        assert fix_title(title) == "The Foo"
        title = "Foo, the"
        assert fix_title(title) == "the Foo"
        title = "Foo,The"
        assert fix_title(title) == "The Foo"
        title = "Foo,the"
        assert fix_title(title) == "the Foo"

        # convoluted title
        title = "Foo 1234 asf__bdf, the cool, the"
        assert fix_title(title) == "the Foo 1234 asf__bdf, the cool"

    def test_pattern_no_match(self):
        title = "Foo, The blah"
        assert needs_fixing(title) == False

        # no title
        title = ", The"
        assert needs_fixing(title) == False
        title = "The"
        assert needs_fixing(title) == False

        # article not at end of line
        title = "Foo, The "
        assert needs_fixing(title) == False

        # maybe support for these should be added
        title = "Foo (bar), The"
        assert needs_fixing(title) == False
        title = "Foo., The"
        assert needs_fixing(title) == False
        title = "foo-bar, The"
        assert needs_fixing(title) == False