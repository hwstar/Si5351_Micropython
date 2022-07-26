# SI5351 Micropython

This is a port from C++ to Micropython of the Etherkit SI5351 driver

Please note that not all Etherkit functionallity is supported yet, but the most-used functions for non-DSP based QRP radios are there.

Differences between the C++ library and the this Micropython module:

1. The constant names have been shortened to reduce the size of the image by eliminating the SI5351 prefix.
2. The signature of the set_freq method is reversed from the Etherkit version it is set_freq(clk, freq).
    which is more consistent with the rest of the methods

#### Methods supported

*SI5351.output_enable(clk: int, enable: bool)*

**Arguments**

clk         - The clock source constant (SI5351.CLKx) where x is 0-2
enable      - Set to True to enable, or False to disable

*SI5351.init (xtal_load_c: int, xo_freq: int, corr: int)*

**Arguments**

xtal_load_c - The crystal load capacitance constant (SI5351.CRYSTAL_LOAD_xPF)
xo_freq     - The frequency of the crystal used.
corr        - The correction factor in parts per billion (ppb)


*SI5351.set_freq(clk: int, freq: int)*

**Arguments**

clk         - The clock source constant (SI5351.CLKx) where x is 0-2
freq        - The desired output frequency in 100th's of Hz. Example: 1 MHz would be 100000000.

*SI5351.drive_strength(self, clk: int, drive: int)*

**Arguments**

clk         - The clock source constant (SI5351.CLKx) where x is 0-2
drive       - The desired drive level (SI5351.DRIVE_xMA) where x is 2,4,6 or 8


See the example file si5351_test.py for more hints on how to use.

