#!/usr/bin/env python
"""
Take 8-digit-hex-strings or float values and print detailed
information about the single precision float they represent
"""
import math
import struct
import sys
import decimal
import re
import binascii
from optparse import OptionParser

BIAS = 127                 # constant to be subtracted from the stored exponent
SIGN_BIT = 31              # bit index at which the sign is stored
EXP_BIT = 23               # bit index at which the exponent starts
EXP_MASK = 0x0007fffff     # bit-mask to remove exponent, leaving mantissa
NAN_EXP = 0xff             # special exponent which encodes NaN/Infinity


def float2decimal(fval):
    """ Convert a floating point number to a Decimal with no loss of
        information
    """
    # Transform (exactly) a float to a mantissa (0.5 <= abs(m) < 1.0) and an
    # exponent.  Double the mantissa until it is an integer.  Use the integer
    # mantissa and exponent to compute an equivalent Decimal.  If this cannot
    # be done exactly, then retry with more precision.
    #
    # This routine is from
    # http://docs.python.org/release/2.5.2/lib/decimal-faq.html

    mantissa, exponent = math.frexp(fval)
    try:
        while mantissa != int(mantissa):
            mantissa *= 2.0
            exponent -= 1
        mantissa = int(mantissa)
    except (OverflowError, ValueError):
        return "---"

    oldcontext = decimal.getcontext()
    decimal.setcontext(decimal.Context(traps=[decimal.Inexact]))
    try:
        while True:
            try:
                return mantissa * decimal.Decimal(2) ** exponent
            except decimal.Inexact:
                decimal.getcontext().prec += 1
    finally:
        decimal.setcontext(oldcontext)


def hex2float(hexstring):
    """ Take a string of 8 hex digits and convert it to the single precision
        float represented by it .
    """
    return struct.unpack('!f', hexstring.decode('hex'))[0]

def float2hex(float_val):
    """ Take a float and return 8 hex digits representing it in single
        precision.
    """
    return binascii.hexlify(struct.pack('!f', float_val))

def test_bit(int_type, offset):
    """ Return a nonzero result, 2**offset, if the bit at 'offset' is one. """
    mask = 1 << offset
    return(int_type & mask)

def set_bit(int_type, offset):
    """ Return an integer with the bit at 'offset' set to 1. """
    mask = 1 << offset
    return(int_type | mask)

def clear_bit(int_type, offset):
    """ Return an integer with the bit at 'offset' cleared. """
    mask = ~(1 << offset)
    return(int_type & mask)


def parse_hex(hexstring, float_format='%.6e', no_decimal=False):
    """ Take a 4-byte hex string (8 digits) representing a single precision,
        parse it, and print detailed information about the represented float
        value.
    """
    bits = int('0x%s' % hexstring, 16)
    sign = '+1'
    if test_bit(bits, SIGN_BIT) > 0:
        sign = '-1'
    bits = clear_bit(bits, SIGN_BIT)
    stored_exp = bits >> EXP_BIT
    mantissa = bits & EXP_MASK # mask the exponent bits

    print ""
    print "Bytes         = 0x%s" % hexstring
    print "Float         = "+ float_format \
                           % struct.unpack('!f', hexstring.decode('hex'))[0]
    print "Sign          = %s" % sign
    if stored_exp == 0:
        print "Exponent      = 0x%x (Special: Zero/Subnormal)" % stored_exp
        print "Mantissa      = 0x%x" % mantissa
        if not no_decimal:
            if mantissa == 0:
                print "Exact Decimal = %s0" % sign[0]
            else:
                print "Exact Decimal = %s (subnormal)" \
                    % float2decimal(hex2float(hexstring))
    elif stored_exp == NAN_EXP:
        print "Exponent      = 0x%x (Special: NaN/Infinity)" % stored_exp
        print "Mantissa      = 0x%x" % mantissa
        if not no_decimal:
            if mantissa == 0:
                print "Exact Decimal = %sInfinity" % sign[0]
            else:
                print "Exact Decimal = NaN"
    else:
        print "Exponent      = 0x%x = %i (bias %i)" % (stored_exp,
                                                       stored_exp, BIAS)
        print "Mantissa      = 0x%x" % mantissa
        if not no_decimal:
            mantissa = set_bit(mantissa, EXP_BIT) # set the implicit bit
            print "Exact Decimal = %s 2^(%i) * [0x%x * 2^(-23)]" \
                                % (sign[0], stored_exp-BIAS, mantissa)
            print "              = %s" % float2decimal(hex2float(hexstring))


def main(argv=None):
    """ Function to run if script is called directly """
    hex_pattern = re.compile(r'^[ 0-9abcdefABCEDF]{8,}$')
    if argv is None:
        argv = sys.argv
        arg_parser = OptionParser(
        usage="usage: %prog [options] values",
        description = __doc__)
        arg_parser.add_option(
          '--no-decimal', action='store_true', dest='no_decimal',
          help="Skip printing the exact represented decimal "
          "(which can take a long time to compute) ")
        arg_parser.add_option(
          '--decimal', action='store_true', dest='decimal',
          help="Only print the exact represented decimal")
        arg_parser.add_option(
          '--float', action='store_true', dest='float',
          help="Only print the represented float")
        arg_parser.add_option(
          '--hex', action='store_true', dest='hex',
          help="Only print the 16-digit hex representation")
        arg_parser.add_option(
          '--format', action='store', dest='format', default='%.6e',
          help="Format to use when printing floats (default '%.6e')")
        options, args = arg_parser.parse_args(argv)
        if len(args) < 2:
            arg_parser.error("No values given. "
                             "Try '--help' for more information")
        for value in args[1:]:
            if hex_pattern.match(value):
                value = value.replace(" ", "").lower()
            else:
                try:
                    value = float(value)
                    value = float2hex(value)
                except ValueError:
                    arg_parser.error("Value '%s' " % value +
                    "is neither a valid hex string nor a valid float" )
            # value at this point is a lowercase hex string without spaces
            if options.float:
                print options.format \
                      % struct.unpack('!d', value.decode('hex'))[0]
            elif options.hex:
                print value
            elif options.decimal:
                print float2decimal(hex2float(value))
            else:
                parse_hex(value, float_format=options.format,
                          no_decimal=options.no_decimal)


if __name__ == "__main__":
    sys.exit(main())
