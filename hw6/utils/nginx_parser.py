import os
import re
import json
import sys


lineformat = re.compile(r'(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - '
                        r'\[(?P<dateandtime>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] '
                        r'(["](?P<method>[^"]+)[ ](?P<url>.+)(http\/1\.[01]")) '
                        r'(?P<statuscode>\d{3}) (?P<bytessent>\d+|-) (?P<referer>-|"([^"]*)"|".*[^\\]") '
                        r'(?P<useragent>"([^"]*)"|".*[^\\]")', re.IGNORECASE)



