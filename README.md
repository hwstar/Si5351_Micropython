This is an initial port from C++ to Micropython of the Etherkit SI5351 driver

Please note that not all Etherkit functionallity is supported yet, but the most-used functions for non-DSP based QRP radios are there.

Differences between the C++ library and the this Micropython module:

1. The constant names have been shortened to reduce the size of the image by eliminating the SI5351 prefix.
2. The signature of the set_freq method is reversed from the Etherkit version it is set_freq(clk, freq).
    which is more consistant with the rest of the methods


