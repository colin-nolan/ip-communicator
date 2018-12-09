# Copyright (c) 2018 Genome Research Limited
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import logging
from typing import Dict

VERBOSE_PARAMETER_KEY = "short_parameter"
DEFAULT_LOG_VERBOSITY_KEY = "default_verbosity"

verbosity_parser_configuration = {
    VERBOSE_PARAMETER_KEY: "v",
    DEFAULT_LOG_VERBOSITY_KEY: logging.ERROR
}


def get_verbosity(parsed_arguments: Dict) -> int:
    """
    Gets the verbosity level from parsed arguments.
    
    Assumes parameter is being parsed similarly to:
    ```
    parser.add_argument(f"-{verbosity_parser_configuration[VERBOSE_PARAMETER_KEY]}", action="count", default=0,
                        help="increase the level of log verbosity (add multiple increase further)")
    ```

    Parsed arguments can be gathered into an appropriate dict as show below:
    ```
    assert type(argument_parser) is ArgumentParser
    parsed_arguments = {x.replace("_", "-"): y for x, y in vars(argument_parser.parse_args(arguments)).items()}
    ```
    :param parsed_arguments: parsed arguments in dictionary form
    :return: the verbosity level implied
    :raises ValueError: if the logging level is too high
    """
    verbosity_parameter = verbosity_parser_configuration[VERBOSE_PARAMETER_KEY]
    verbosity = verbosity_parser_configuration[DEFAULT_LOG_VERBOSITY_KEY] - (
            int(parsed_arguments.get(verbosity_parameter)) * 10)
    if verbosity < 10:
        raise ValueError("Cannot provide any further logging - reduce log verbosity")
    assert verbosity <= logging.CRITICAL
    return verbosity
