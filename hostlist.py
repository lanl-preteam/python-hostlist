#!/usr/bin/env python
# Hostlist utilities

# WARNING: The behaviour in odd corner cases (such as 
# nested brackets) have not been compared for compatibility
# with pdsh et al.

import re

# Exceptions
class BadHostlist(Exception): pass

# Configuration
MAX_SIZE = 100000

# Helper functions

def expand_part(s):
    """Expand a part (e.g. x[1-2]y[1-3][1-3]) (no outer level commas)."""

    # print "EXPAND_PART", s

    # Base case: the empty part expand to the singleton list of ""
    if s == "":
        return [""]

    # Split into:
    # 1) prefix string (may be empty)
    # 2) rangelist in brackets (may be missing)
    # 3) the rest

    m = re.match(r'([^,\[]*)(\[[^\]]*\])?(.*)', s)
    (prefix, rangelist, rest) = m.group(1,2,3)
    #print "PREFIX", prefix, "RL", rangelist, "REST", rest

    # Expand the rest first (here is where we recurse!)
    rest_expanded = expand_part(rest)

    # Expand our own part
    if not rangelist:
        # If there is no rangelist, our own contribution is the prefix only
        us_expanded = [prefix]
    else:
        # Otherwise expand the rangelist (adding the prefix before)
        us_expanded = expand_rangelist(prefix, rangelist[1:-1])

    # Combine our list with the list from the expansion of the rest
    # (but guard against too large results first)
    if len(us_expanded) * len(rest_expanded) > MAX_SIZE:
        raise BadHostlist, "results too large"

    return [us_part + rest_part
            for us_part in us_expanded
            for rest_part in rest_expanded]

def expand_rangelist(prefix, rangelist):
    """ Expand a rangelist (e.g. 1-10,12-14), putting a prefix before."""
    
    # Split at commas and expand each range separately
    results = []
    for range_ in rangelist.split(","):
        results.extend(expand_range(prefix, range_))
    return results

def expand_range(prefix, range_):
    """ Expand a rangelist (e.g. 1-10 or 14), putting a prefix before."""

    # Check for a single number first
    try:
        single_number = int(range_)
        return ["%s%s" % (prefix, range_)]
    except ValueError:
        pass

    # Otherwise split low-high
    m = re.match(r'^([0-9]+)-([0-9]+)$', range_)
    if not m:
        raise BadHostlist, "bad range"

    (s_low, s_high) = m.group(1,2)
    low = int(s_low)
    high = int(s_high)
    width = len(s_low)

    if high < low:
        raise BadHostlist, "start > stop"
    elif high - low > MAX_SIZE:
        raise BadHostlist, "range too large"

    results = []
    for i in xrange(low, high+1):
        results.append("%s%0*d" % (prefix, width, i))
    return results

# Main entry point

def expand_hostlist(s):
    """Expand a Livermore hostlist (e.g. n[1-10,12-14],d[1-3])."""

    results = []
    bracket_level = 0
    part = ""
    
    for c in s + ",":
        if c == "," and bracket_level == 0:
            # Comma at top level, split!
            if part: results.extend(expand_part(part))
            part = ""
            bad_part = False
        else:
            part += c

        if c == "[": bracket_level += 1
        elif c == "]": bracket_level -= 1

        if bracket_level > 1:
            raise BadHostlist, "nested brackets"
        elif bracket_level < 0:
            raise BadHostlist, "unbalanced brackets"

    if bracket_level > 0:
        raise BadHostlist, "unbalanced brackets"

    return results

# MAIN
if __name__ == '__main__':
    import sys
    for host in expand_hostlist(sys.argv[1]):
        print host


