import unittest
import sys
sys.path.insert(0, "/Users/saeid/Documents/03 Computer Science/__PROJECTS__/eazyconfig/eazyconfig")
from eazyconfig.ezcfg import Configure, ConfigureText


PATH_CONFIGURE = "/Users/saeid/Documents/03 Computer Science/__PROJECTS__/eazyconfig/eazyconfig/eazyconfig/tests/configure.cfg"
PATH_CONFIGURE_TEXT = "/Users/saeid/Documents/03 Computer Science/__PROJECTS__/eazyconfig/eazyconfig/eazyconfig/tests/configuretext.cfg"

class TestEazyConfig(unittest.TestCase):
    def test_configure(self):
        parameters = Configure(
            config_settings={
                "path": ["input", "output"],
                "specs": ["unit", "planet", "speed", "years", "days", "ready"]
            },
            path_config_file=PATH_CONFIGURE,
            float_vars=["speed"],
            comma_sep_vars=["years"],
            int_vars=["days"],
            boolean_vars=["ready"]
        ).get_params()

        print(parameters)
        self.assertNotEqual(parameters, {})

    def test_configure_text(self):
        parameters = ConfigureText(
            path_config_file=PATH_CONFIGURE_TEXT,
            float_vars=["speed"],
            comma_sep_vars=["years"],
            int_vars=["days"],
            boolean_vars=["ready"]
        ).get_params()

        print(parameters)
        self.assertNotEqual(parameters, {})

if __name__ == '__main__':
    unittest.main() 