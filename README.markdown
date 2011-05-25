# Float Parsers

[http://github.com/goerz/float_parsers](http://github.com/goerz/float_parsers)

Author: [Michael Goerz](http://michaelgoerz.net)

Float Parsers is a collection of scripts for analyzing single and double
precision floating point numbers in their exact binary representation.

Given a representation (as a hex string) or a float value (as a string like
"1.2" or "-2.3456e-192") they decompose the binary representation into sign,
exponent, and mantissa, and print out this information along with the exact
decimal the binary representation corresponds to according to the floating
point model.

To understand the details of the binary representation for single and double
precision floats, look at the Wikipedia articles for the [Double precision
floating-point format][1] and [Single precision floating-point format][2].

A similar online tool for double precision floats is available at
[www.binaryconvert.com][3] (also [single precision][4] and [others][5]).

[1]: http://en.wikipedia.org/wiki/Double_precision_floating-point_format
[2]: http://en.wikipedia.org/wiki/Single_precision_floating-point_format
[3]: http://www.binaryconvert.com/convert_double.html
[4]: http://www.binaryconvert.com/convert_float.html
[5]: http://www.binaryconvert.com/index.html

## Install ##

Store the scripts anywhere in your `$PATH`.

## Usage ##

Some usage examples for the `parse_dp_float.py` (double precision) script:

    $> ./parse_dp_float.py 1.2

    Bytes         = 0x3ff3333333333333
    Float         = 1.200000000000000e+00
    Sign          = +1
    Exponent      = 0x3ff = 1023 (bias 1023)
    Mantissa      = 0x3333333333333
    Exact Decimal = + 2^(0) * (0x13333333333333 * 2^(-52))
                  = 1.1999999999999999555910790149937383830547332763671875

    $>./parse_dp_float.py -- "7fef ffff ffff ffff"  "8000 0000 0000 0000" "0.33333" "fff0 0000 0000 0000"

    Bytes         = 0x7fefffffffffffff
    Float         = 1.797693134862316e+308
    Sign          = +1
    Exponent      = 0x7fe = 2046 (bias 1023)
    Mantissa      = 0xfffffffffffff
    Exact Decimal = + 2^(1023) * (0x1fffffffffffff * 2^(-52))
                  = 17976931348623157081452742373170435679807056752584499659891
                    74768031572607800285387605895586327668781715404589535143824
                    64234321326889464182768467546703537516986049910576551282076
                    24549009038932894407586850845513394230458323690322294816580
                    85593321233482747978262041447231687381771809192998812504040
                    26184124858368

    Bytes         = 0x8000000000000000
    Float         = -0.000000000000000e+00
    Sign          = -1
    Exponent      = 0x0 (Special: Zero/Subnormal)
    Mantissa      = 0x0
    Exact Decimal = -0

    Bytes         = 0x3fd555475a31a4be
    Float         = 3.333300000000000e-01
    Sign          = +1
    Exponent      = 0x3fd = 1021 (bias 1023)
    Mantissa      = 0x555475a31a4be
    Exact Decimal = + 2^(-2) * (0x1555475a31a4be * 2^(-52))
                  = 0.33333000000000001517008740847813896834850311279296875

    Bytes         = 0xfff0000000000000
    Float         = -inf
    Sign          = -1
    Exponent      = 0x7ff (Special: NaN/Infinity)
    Mantissa      = 0x0
    Exact Decimal = -Infinity

    $> ./parse_dp_float.py --float --format='%.5f' "3fd5 5555 5555 5555"
    0.33333

The single precision script works completely equivalently:

    $> ./parse_sp_float.py
    "ff80 0000" c0000000 0.3333333333333333

    Bytes         = 0xff800000
    Float         = -inf
    Sign          = -1
    Exponent      = 0xff (Special: NaN/Infinity)
    Mantissa      = 0x0
    Exact Decimal = -Infinity

    Bytes         = 0xc0000000
    Float         = -2.000000e+00
    Sign          = -1
    Exponent      = 0x80 = 128 (bias 127)
    Mantissa      = 0x0
    Exact Decimal = -2

    Bytes         = 0x3eaaaaab
    Float         = 3.333333e-01
    Sign          = +1
    Exponent      = 0x7d = 125 (bias 127)
    Mantissa      = 0x200001
