#
# Copyright (C) 2022 Stephen Rodgers <steve@rodgers619.com>
# See the license.txt file for license info
#                          

from machine import I2C
from micropython import const
import array

#
# Values which are for exclusive use by this module
#

_BUS_DEVICE_ADDR                = const(0x60)
_XTAL_FREQ                      = const(25000000)
_PLL_FIXED                      = const(80000000000)
_FREQ_MULT                      = const(100)

_PLL_VCO_MIN                    = const(600000000)
_PLL_VCO_MAX                    = const(900000000)
_MULTISYNTH_MIN_FREQ            = const(500000)
_MULTISYNTH_DIVBY4_FREQ         = const(150000000)
_MULTISYNTH_MAX_FREQ            = const(225000000)
_MULTISYNTH_SHARE_MAX           = const(100000000)
_MULTISYNTH_SHARE_MIN           = const(1024000)
_MULTISYNTH67_MAX_FREQ          = _MULTISYNTH_DIVBY4_FREQ
_CLKOUT_MIN_FREQ                = const(4000)
_CLKOUT_MAX_FREQ                = const(_MULTISYNTH_MAX_FREQ)
_CLKOUT67_MS_MIN                = _PLL_VCO_MIN // _MULTISYNTH67_MAX_FREQ
_CLKOUT67_MIN_FREQ              = _CLKOUT67_MS_MIN // 128
_CLKOUT67_MAX_FREQ              = _MULTISYNTH67_MAX_FREQ

_PLL_A_MIN                      = const(15)
_PLL_A_MAX                      = const(90)
_PLL_C_MAX                      = const(1048575)
_PLL_B_MAX                      = (_PLL_C_MAX-1)
_MULTISYNTH_A_MIN               = const(6)
_MULTISYNTH_A_MAX               = const(1800)
_MULTISYNTH67_A_MAX             = const(254)
_MULTISYNTH_C_MAX               = const(1048575)
_MULTISYNTH_B_MAX               = (_MULTISYNTH_C_MAX-1)
_MULTISYNTH_P1_MAX              = const(((1<<18)-1))
_MULTISYNTH_P2_MAX              = const(((1<<20)-1))
_MULTISYNTH_P3_MAX              = const(((1<<20)-1))
_VCXO_PULL_MIN                  = const(30)
_VCXO_PULL_MAX                  = const(240)
_VCXO_MARGIN                    = const(103)


_DEVICE_STATUS                  = const(0)
_INTERRUPT_STATUS               = const(1)
_INTERRUPT_MASK                 = const(2)
_STATUS_SYS_INIT                = const((1<<7))
_STATUS_LOL_B                   = const((1<<6))
_STATUS_LOL_A                   = const((1<<5))
_STATUS_LOS                     = const((1<<4))
_OUTPUT_ENABLE_CTRL             = const(3)
_OEB_PIN_ENABLE_CTRL            = const(9)
_PLL_INPUT_SOURCE               = const(15)
_CLKIN_DIV_MASK                 = const((3<<6))
_CLKIN_DIV_1                    = const((0<<6))
_CLKIN_DIV_2                    = const((1<<6))
_CLKIN_DIV_4                    = const((2<<6))
_CLKIN_DIV_8                    = const((3<<6))
_PLLB_SOURCE                    = const((1<<3))
_PLLA_SOURCE                    = const((1<<2))

_CLK0_CTRL                      = const(16)
_CLK1_CTRL                      = const(17)
_CLK2_CTRL                      = const(18)
_CLK3_CTRL                      = const(19)
_CLK4_CTRL                      = const(20)
_CLK5_CTRL                      = const(21)
_CLK6_CTRL                      = const(22)
_CLK7_CTRL                      = const(23)
_CLK_POWERDOWN                  = const((1<<7))
_CLK_INTEGER_MODE               = const((1<<6))
_CLK_PLL_SELECT                 = const((1<<5))
_CLK_INVERT                     = const((1<<4))
_CLK_INPUT_MASK                 = const((3<<2))
_CLK_INPUT_XTAL                 = const((0<<2))
_CLK_INPUT_CLKIN                = const((1<<2))
_CLK_INPUT_MULTISYNTH_0_4       = const((2<<2))
_CLK_INPUT_MULTISYNTH_N         = const((3<<2))
_CLK_DRIVE_STRENGTH_MASK        = const((3<<0))
_CLK_DRIVE_STRENGTH_2MA         = const((0<<0))
_CLK_DRIVE_STRENGTH_4MA         = const((1<<0))
_CLK_DRIVE_STRENGTH_6MA         = const((2<<0))
_CLK_DRIVE_STRENGTH_8MA         = const((3<<0))

_CLK3_0_DISABLE_STATE           = const(24)
_CLK7_4_DISABLE_STATE           = const(25)
_CLK_DISABLE_STATE_MASK         = const(3)
_CLK_DISABLE_STATE_LOW          = const(0)
_CLK_DISABLE_STATE_HIGH         = const(1)
_CLK_DISABLE_STATE_FLOAT        = const(2)
_CLK_DISABLE_STATE_NEVER        = const(3)

_PARAMETERS_LENGTH              = const(8)
_PLLA_PARAMETERS                = const(26)
_PLLB_PARAMETERS                = const(34)
_CLK0_PARAMETERS                = const(42)
_CLK1_PARAMETERS                = const(50)
_CLK2_PARAMETERS                = const(58)
_CLK3_PARAMETERS                = const(66)
_CLK4_PARAMETERS                = const(74)
_CLK5_PARAMETERS                = const(82)
_CLK6_PARAMETERS                = const(90)
_CLK7_PARAMETERS                = const(91)
_CLK6_7_OUTPUT_DIVIDER          = const(92)
_OUTPUT_CLK_DIV_MASK            = const((7 << 4))
_OUTPUT_CLK6_DIV_MASK           = const((7 << 0))
_OUTPUT_CLK_DIV_SHIFT           = const(4)
_OUTPUT_CLK_DIV6_SHIFT          = const(0)
_OUTPUT_CLK_DIV_1               = const(0)
_OUTPUT_CLK_DIV_2               = const(1)
_OUTPUT_CLK_DIV_4               = const(2)
_OUTPUT_CLK_DIV_8               = const(3)
_OUTPUT_CLK_DIV_16              = const(4)
_OUTPUT_CLK_DIV_32              = const(5)
_OUTPUT_CLK_DIV_64              = const(6)
_OUTPUT_CLK_DIV_128             = const(7)
_OUTPUT_CLK_DIVBY4              = const((3<<2))

_SSC_PARAM0                     = const(149)
_SSC_PARAM1                     = const(150)
_SSC_PARAM2                     = const(151)
_SSC_PARAM3                     = const(152)
_SSC_PARAM4                     = const(153)
_SSC_PARAM5                     = const(154)
_SSC_PARAM6                     = const(155)
_SSC_PARAM7                     = const(156)
_SSC_PARAM8                     = const(157)
_SSC_PARAM9                     = const(158)
_SSC_PARAM10                    = const(159)
_SSC_PARAM11                    = const(160)
_SSC_PARAM12                    = const(161)

_VXCO_PARAMETERS_LOW            = const(162)
_VXCO_PARAMETERS_MID            = const(163)
_VXCO_PARAMETERS_HIGH           = const(164)

_CLK0_PHASE_OFFSET              = const(165)
_CLK1_PHASE_OFFSET              = const(166)
_CLK2_PHASE_OFFSET              = const(167)
_CLK3_PHASE_OFFSET              = const(168)
_CLK4_PHASE_OFFSET              = const(169)
_CLK5_PHASE_OFFSET              = const(170)

_PLL_RESET                      = const(177)
_PLL_RESET_B                    = const((1<<7))
_PLL_RESET_A                    = const((1<<5))

_CRYSTAL_LOAD                   = const(183)
_CRYSTAL_LOAD_MASK              = const((3<<6))

_FANOUT_ENABLE                  = const(187)
_CLKIN_ENABLE                   = const((1<<7))
_XTAL_ENABLE                    = const((1<<6))
_MULTISYNTH_ENABLE              = const((1<<4))

_RFRAC_DENOM                    = const(1000000)

#
# indexes to "data structures" in original C version
#

# Register set indexes
_P1                             = const(0)
_P2                             = const(1)
_P3                             = const(2)

# Status bit indexes
_SYS_INIT                       = const(0)
_LOL_B                          = const(1)
_LOL_A                          = const(2)
_LOS                            = const(3)
_REVID                          = const(4)

# Interrupt status bit indexes

_SYS_INIT_STKY                  = const(0)
_LOL_B_STKY                     = const(1)
_LOL_A_STKY                     = const(2)
_LOS_STKY                       = const(3)





#
# Values which must be visible externally
#

DEFAULT_CLK                     = const(1000000000)


# Clock outputs
CLK0                            = const(0)
CLK1                            = const(1)
CLK2                            = const(2)
CLK3                            = const(3)
CLK4                            = const(4)
CLK5                            = const(5)
CLK6                            = const(6)
CLK7                            = const(7)

CRYSTAL_LOAD_0PF                = const((0<<6))
CRYSTAL_LOAD_6PF                = const((1<<6))
CRYSTAL_LOAD_8PF                = const((2<<6))
CRYSTAL_LOAD_10PF               = const((3<<6))

# PLL's
PLLA                            = 0
PLLB                            = 1

# Drive levels
DRIVE_2MA                       = 0
DRIVE_4MA                       = 1
DRIVE_6MA                       = 2
DRIVE_8MA                       = 3

# Clock sources
CLK_SRC_XTAL                    = 0
CLK_SRC_CLKIN                   = 1
CLK_SRC_MS0                     = 2
CLK_SRC_MS                      = 3

# Clock disables
CLK_DISABLE_LOW                 = 0
CLK_DISABLE_HIGH                = 1
CLK_DISABLE_HI_Z                = 2
CLK_DISABLE_NEVER               = 3

# Clock fanout
FANOUT_CLKIN                    = 0
FANOUT_XO                       = 1
FANOUT_MS                       = 2

# PLL input
PLL_INPUT_XO                    = 0
PLL_INPUT_CLKIN                 = 1



class SI5351():
 
    #
    # Protected methods
    #
    
    def _debug_print_bytes(self, data_bytes, label=None):
        byte_string = bytes(data_bytes)
        if label is not None:
            print(label,end="")
        print(" ".join(["{:02x}".format(x) for x in byte_string]))
    
    def _write_reg(self, reg_addr: int, data: int):
        reg_data = bytearray([reg_addr, data])
        res = self._i2c.writeto(self._device_addr, bytes(reg_data))
        return res
    
    def _write_bulk(self, reg_addr: int, data: bytearray):
        reg_data = bytearray([reg_addr])
        reg_data += data
        res =  self._i2c.writeto(self._device_addr, bytes(reg_data))
        return res
    
    def _read_reg(self, reg_addr):
        reg = bytearray([reg_addr])             
        self._i2c.writeto(self._device_addr, reg, False)        
        res = self._i2c.readfrom(self._device_addr, 1)
        if len(res):
            res = int(res[0])
            return res
        else:
            return None
    
    
    
    def _pll_calc(self, pll: int, freq: int, correction : int, vcxo : bool):
        # Return (freq, register set array)
     
        
        ref_freq = self._xtal_freq[self._plla_ref_osc] if pll == PLLA else self._xtal_freq[self._pllb_ref_osc]
        
      
        ref_freq *= _FREQ_MULT
        
      
        
        # Factor calibration value into nominal xtal frequency.
        # Measured in ppb
      
        ref_freq +=((((correction << 31) // 1000000000) * ref_freq) >> 31)
       
  
        
        # PLL bounds check
        if freq < _PLL_VCO_MIN * _FREQ_MULT:
            freq = _PLL_VCO_MIN * _FREQ_MULT
        if freq > _PLL_VCO_MAX * _FREQ_MULT:
            freq = _PLL_VCO_MAX * _FREQ_MULT
            
       
        
        # Determine integer part of feedback eq.
        a = freq // ref_freq
       
       
        
        if a < _PLL_A_MIN:
            freq = ref_freq * _PLL_A_MIN
        if a > _PLL_A_MAX:
            freq = ref_freq * _PLL_A_MAX
        
        # Find best approximation for b/c = fVCO mod fIN
        if vcxo is True:
            b = (((freq % ref_freq)) * 1000000) // ref_freq
            c = 1000000
        else:
            b = (((freq % ref_freq)) * _RFRAC_DENOM) // ref_freq;
            c = _RFRAC_DENOM if b else 1
        
    
        
        
        # Calculate parameters
        p1 = 128 * a + ((128 * b) // c) - 512
        p2 = 128 * b - c * ((128 * b) // c)
        p3 = c
        
     
        
        
        # Recalculate frequency as fIN * (a + b/c)
        lltmp = ref_freq

        lltmp *= b
        lltmp = lltmp//c
     
        freq = lltmp
        freq += ref_freq * a
        reg_set = array.array('L', [p1,p2,p3])
       
        return (((128 * a * 1000000 + b) if vcxo else freq), reg_set)
       
    def _multisynth_calc(self, freq, pll_freq):
        # Returns (multi synth value, reg_set)
        divby4 = False
        ret_val = False
     
        
        # Multisynth bounds checking
        if freq > _MULTISYNTH_MAX_FREQ * _FREQ_MULT:
            freq = _MULTISYNTH_MAX_FREQ * _FREQ_MULT
        if freq < _MULTISYNTH_MIN_FREQ * _FREQ_MULT:
            freq = _MULTISYNTH_MIN_FREQ * _FREQ_MULT
        if freq >= _MULTISYNTH_DIVBY4_FREQ * _FREQ_MULT:
            divby4 = True
      
            
        if pll_freq == 0:
            if divby4 is False:
                lltmp = _PLL_VCO_MAX * _FREQ_MULT # margin needed?
                lltmp = lltmp // freq
                if lltmp == 5:
                    lltmp = 4
                elif lltmp == 7:
                    lltmp = 6
                a = lltmp
            else:
                a = 4
            b = 0
            c = 1
            pll_freq = a * freq
        
        else:
            # Preset PLL, so return the actual freq for these params instead of PLL freq
            ret_val = True
            # Determine integer part of feedback equation
            a = pll_freq // freq
            if a < _MULTISYNTH_A_MIN:
                freq = pll_freq // _MULTISYNTH_A_MIN
            if a > _MULTISYNTH_A_MAX:
                freq = pll_freq // _MULTISYNTH_A_MAX
            b = (pll_freq % freq * _RFRAC_DENOM) // freq
            c = _RFRAC_DENOM if b else 1
       
            
            
        # Calculate parameters
        if divby4 == True:
            p3 = 1
            p2 = 0
            p1 = 0
        else:
            p1 = 128 * a + ((128 * b) // c) - 512
            p2 = 128 * b - c * ((128 * b) // c)
            p3 = c
        reg_set = array.array('L')
        reg_set.append(p1)
        reg_set.append(p2)
        reg_set.append(p3)
        return((pll_freq if ret_val is False else freq), reg_set)
    
    def _multisynth67_calc(self, freq: int, pll_freq: int):
        # Multisynth bounds checking
        if freq > _MULTISYNTH67_MAX_FREQ * _FREQ_MULT:
            freq = _MULTISYNTH67_MAX_FREQ * _FREQ_MULT
        if freq < _MULTISYNTH_MIN_FREQ * _FREQ_MULT:
            freq = _MULTISYNTH_MIN_FREQ * _FREQ_MULT
        
        if pll_freq == 0:
            # Find largest integer divider for max
            # VCO frequency and given target frequency
            lltmp = (_PLL_VCO_MAX * _FREQ_MULT) - 100000000 # margin needed?
            a = lltmp // freq
            # Divisor has to be even
            if a % 2 != 0:
                a += 1
            # Divisor bounds check
            if a < _MULTISYNTH_A_MIN:
                a = _MULTISYNTH_A_MIN
            if a > _MULTISYNTH67_A_MAX:
                a = _MULTISYNTH67_A_MAX

            pll_freq = a * freq;
            
            # PLL bounds checking
            if pll_freq > (_PLL_VCO_MAX * _FREQ_MULT):
                a -= 2
                pll_freq = a * freq
            elif pll_freq < (_PLL_VCO_MIN * _FREQ_MULT):
                a += 2;
                pll_freq = a * freq;
            reg_set = array('L')
            reg_set.append(a & 0xFF)
            reg_set.append(0)
            reg_set.append(0)
            return (pll_freq, reg_set)
        else:
            if pll_freq % freq:
                # No good
                return (0, array('L',[0,0,0]))
            else:
                a = pll_freq // freq
                # Division ratio bounds check
                if a < _MULTISYNTH_A_MIN or a > _MULTISYNTH67_A_MAX:
                    # No bueno
                    return (0, array('L',[0,0,0]))
                else:
                    reg_set = array('L')
                    reg_set.append(a & 0xFF)
                    reg_set.append(0)
                    reg_set.append(0)
                    return(1, reg_set)
    
    def _update_int_status(self):
        reg_val = self._read_reg(_INTERRUPT_STATUS)
        # Parse the register
        reg_set = array('B')
        reg_set.append((reg_val >> 7) & 0x01) # _SYS_INIT_STKY
        reg_set.append((reg_val >> 6) & 0x01) # _LOL_B_STKY
        reg_set.append((reg_val >> 5) & 0x01) # _LOL_A_STKY
        reg_set.append((reg_val >> 4) & 0x01) # LOS_STKY
        return reg_set
    
                       
    def _ms_div(self, clk: int, r_div: int, div_by_4: bool):
        
        if clk == CLK0:
            reg_addr = _CLK0_PARAMETERS + 2
        elif clk == CLK1:
            reg_addr = _CLK1_PARAMETERS + 2
        elif clk == CLK2:
            reg_addr = _CLK2_PARAMETERS + 2
        elif clk == CLK3:
            reg_addr = _CLK3_PARAMETERS + 2
        elif clk == CLK4:
            reg_addr = _CLK4_PARAMETERS + 2
        elif clk == CLK5:
            reg_addr = _CLK5_PARAMETERS + 2
        elif clk == CLK6:
            reg_addr = _CLK6_7_OUTPUT_DIVIDER
        elif clk == CLK7:
            reg_addr = _CLK6_7_OUTPUT_DIVIDER
        # Read the register
        reg_val = self._read_reg(reg_addr)
        if clk <= CLK5:
            # Clear the relevant bits
            reg_val &= ~0x7c
            if div_by_4 is False:
                reg_val &= ~_OUTPUT_CLK_DIVBY4
            else:
                reg_val |= _OUTPUT_CLK_DIVBY4
                
            reg_val |= (r_div << _OUTPUT_CLK_DIV_SHIFT)
        elif clk == CLK6:
            reg_val &= ~0x07
            reg_val |= r_div
        elif clk == CLK7:
            reg_val &= ~0x70
            reg_val |= (r_div << _OUTPUT_CLK_DIV_SHIFT)
        self._write_reg(reg_addr, reg_val)
    
    def _select_r_div(self, freq: int):
        # return (r_div, freq)
        r_div = _OUTPUT_CLK_DIV_1
        # Choose the correct R divider
        if (freq >= _CLKOUT_MIN_FREQ * _FREQ_MULT) and (freq < _CLKOUT_MIN_FREQ * _FREQ_MULT * 2):
            r_div = _OUTPUT_CLK_DIV_128
            freq *= 128
        elif (freq >= _CLKOUT_MIN_FREQ * _FREQ_MULT * 2) and (freq < _CLKOUT_MIN_FREQ * _FREQ_MULT * 4):
            r_div = _OUTPUT_CLK_DIV_64
            freq *= 64
        elif (freq >= _CLKOUT_MIN_FREQ * _FREQ_MULT * 4) and (freq < _CLKOUT_MIN_FREQ * _FREQ_MULT * 8):
            r_div = _OUTPUT_CLK_DIV_32
            freq *= 32
        elif(freq >= _CLKOUT_MIN_FREQ * _FREQ_MULT * 8) and (freq < _CLKOUT_MIN_FREQ * _FREQ_MULT * 16):
            r_div = _OUTPUT_CLK_DIV_16
            freq *= 16
        elif(freq >= _CLKOUT_MIN_FREQ * _FREQ_MULT * 16) and (freq < _CLKOUT_MIN_FREQ * _FREQ_MULT * 32):
            r_div = _OUTPUT_CLK_DIV_8
            freq *= 8
        elif(freq >= _CLKOUT_MIN_FREQ * _FREQ_MULT * 32) and (freq < _CLKOUT_MIN_FREQ * _FREQ_MULT * 64):
            r_div = _OUTPUT_CLK_DIV_4
            freq *= 4
        elif(freq >= _CLKOUT_MIN_FREQ * _FREQ_MULT * 64) and (freq < _CLKOUT_MIN_FREQ * _FREQ_MULT * 128):
            r_div = _OUTPUT_CLK_DIV_2
            freq *= 2
        return (r_div, freq)

    def _select_r_div_ms67(self, freq):
        # return (r_div, freq)
        r_div = _OUTPUT_CLK_DIV_1
        # Choose the correct R divider
        if(freq >= _CLKOUT67_MIN_FREQ * _FREQ_MULT) and (freq < _CLKOUT67_MIN_FREQ * _FREQ_MULT * 2):
            r_div = _OUTPUT_CLK_DIV_128
            freq *= 128
        elif (freq >= _CLKOUT67_MIN_FREQ * _FREQ_MULT * 2) and (freq < _CLKOUT67_MIN_FREQ * _FREQ_MULT * 4):
            r_div = _OUTPUT_CLK_DIV_64
            freq *= 64
        elif (freq >= _CLKOUT67_MIN_FREQ * _FREQ_MULT * 4) and (freq < _CLKOUT67_MIN_FREQ * _FREQ_MULT * 8):
            r_div = _OUTPUT_CLK_DIV_32
            freq *= 32
        elif(freq >= _CLKOUT67_MIN_FREQ * _FREQ_MULT * 8) and (freq < _CLKOUT67_MIN_FREQ * _FREQ_MULT * 16):
            r_div = _OUTPUT_CLK_DIV_16
            freq *= 16
        elif(freq >= _CLKOUT67_MIN_FREQ * _FREQ_MULT * 16) and (freq < _CLKOUT67_MIN_FREQ * _FREQ_MULT * 32):
            r_div = _OUTPUT_CLK_DIV_8
            freq *= 8
        elif(freq >= _CLKOUT67_MIN_FREQ * _FREQ_MULT * 32) and (freq < _CLKOUT67_MIN_FREQ * _FREQ_MULT * 64):
            r_div = _OUTPUT_CLK_DIV_4
            freq *= 4
        elif(freq >= _CLKOUT67_MIN_FREQ * _FREQ_MULT * 64) and (freq < _CLKOUT67_MIN_FREQ * _FREQ_MULT * 128):
            r_div = _OUTPUT_CLK_DIV_2
            freq *= 2
        return (r_div, freq)

    def __init__(self, i2c_object, device_addr = 0x60, xtal_freq=25000000):
        self._xtal_freq = [0] * 2
        self._xtal_freq[0] = xtal_freq
        self._clk_freq = [0] * 8
        self._plla_freq  = 0
        self._pllb_freq = 0
        self._clkin_div = [0]
        self._i2c_bus_error = 0
        self._clk_first_set = [False] * 8
        self._i2c = i2c_object
        self._device_addr = device_addr
        self._dev_status = bytes(5)
        self._dev_int_status = bytes(4)
        self._plla_ref_osc = PLL_INPUT_XO
        self._pllb_ref_osc = PLL_INPUT_XO
        self._clkin_div = _CLKIN_DIV_1
        self._ref_correction = [0] * 2
        self._pll_assignment = [0] * 8
   
    # Set the reference frequency value for the desired reference oscillator
    def _set_ref_freq(self, ref_freq: int, ref_osc: int):
        ref_osc &= 1
        if ref_freq <= 30000000:
            self._xtal_freq[ref_osc] = ref_freq
            if ref_osc == PLL_INPUT_CLKIN:
                self._clkin_div = _CLKIN_DIV_1
        elif ref_freq > 30000000 and ref_freq <= 60000000:
            self._xtal_freq[ref_osc] = ref_freq // 2;
            if ref_osc == PLL_INPUT_CLKIN:
                self._clkin_div = _CLKIN_DIV_2       
        elif ref_freq > 60000000 and ref_freq <= 100000000:
            self._xtal_freq[ref_osc] = ref_freq // 4;
            if ref_osc == PLL_INPUT_CLKIN:
                self._clkin_div = _CLKIN_DIV_4       
            
    
    # Set the correction factor
    def _set_correction(self, corr: int, ref_osc: int):
        self._ref_correction[ref_osc & 0xFF] = corr
        # Recalculate and set PLL freqs based on correction value
        self._set_pll(self._plla_freq, PLLA)
        self._set_pll(self._pllb_freq, PLLB)

    # Set the indicated multisynth into integer mode.
    def _set_int(self, clk, enable):
        clk &= 0x07
        reg_val = self._read_reg(_CLK0_CTRL + clk)
        if enable is True:
            reg_val |= _CLK_INTEGER_MODE
        else:
            reg_val &= ~_CLK_INTEGER_MODE
        self._write_reg(_CLK0_CTRL + clk, reg_val);
        
             
             
             
    # Set the specified PLL to a specific oscillation frequency
    def _set_pll(self, pll_freq, pll_assignment):
          
            if pll_assignment == PLLA:
                (freq, pll_reg) = self._pll_calc(PLLA, pll_freq, self._ref_correction[self._plla_ref_osc], 0)
            else:
                (freq, pll_reg) = self._pll_calc(PLLB, pll_freq, self._ref_correction[self._pllb_ref_osc], 0)
              
      
            
            # Derive the register values to write
            # Prepare a bytearray for parameters to be written to
            params = bytearray()
          
            
            # Registers 26,27
            params.append((pll_reg[_P3] >> 8) & 0xFF)
           
            params.append((pll_reg[_P3]) & 0xFF)
            
            
            # Register 28
            params.append((pll_reg[_P1] >> 16) & 0x03)
           
            
            # Registers 29,30
            params.append((pll_reg[_P1] >> 8) & 0xFF)
           

            params.append(pll_reg[_P1]  & 0xFF)
            
            
            # Register 31
            temp = ((pll_reg[_P3] >> 12) & 0xF0)
            temp2 = ((pll_reg[_P2] >> 16) & 0x0F)
            temp += temp2
            params.append(temp)
           
            
            # Registers 32,33
            temp = (pll_reg[_P2] >> 8) & 0xFF
            params.append(temp)
        
            temp = pll_reg[_P2]  & 0xFF
            params.append(temp)
                             
            
            # Write the parameters
            if pll_assignment == PLLA:
                self._write_bulk(_PLLA_PARAMETERS, params)
                self._plla_freq = pll_freq
            elif pll_assignment == PLLB:
                self._write_bulk(_PLLB_PARAMETERS, params)
                self._pllb_freq = pll_freq
    
    # Set the specified multisynth parameters.
    def _set_ms(self, clk, ms_reg, int_mode, r_div, div_by_4):
        if clk <= CLK5:
            params = bytearray()
            clk &= 7
            
            # Registers 42,43 for CLK0
            temp = ((ms_reg[_P3] >> 8) & 0xFF)
            params.append(temp)
            temp = ms_reg[_P3]  & 0xFF
            params.append(temp)
            
            # Register 44 for CLK0
            reg_val = self._read_reg((_CLK0_PARAMETERS + 2) + (clk * 8))
            
            reg_val &= ~0x03
           
            temp = reg_val | ((ms_reg[_P1] >> 16) & 0x03)
            params.append(temp)
            
            # Registers 45-46 for CLK0
            temp = (ms_reg[_P1] >> 8) & 0xFF
            params.append(temp)
            temp = ms_reg[_P1]  & 0xFF           
            params.append(temp)
            
            # Register 47 for CLK0
            temp = ((ms_reg[_P3] >> 12) & 0xF0)
            temp += ((ms_reg[_P2] >> 16) & 0x0F)
            params.append(temp)
            
            # Registers 48, 49 for CLK0
            temp = (ms_reg[_P2] >> 8) & 0xFF
            params.append(temp)
            temp = ms_reg[_P2]  & 0xFF
            params.append(temp)
          
        else:
            # MS6 and MS7 only use one register
            temp = ms_reg[_P1] & 0xFF
        
        if clk == CLK0:
            self._write_bulk(_CLK0_PARAMETERS, params)
            self._set_int(clk, int_mode)
            self._ms_div(clk, r_div, div_by_4)
        elif clk == CLK1:
            self._write_bulk(_CLK1_PARAMETERS, params)
            self._set_int(clk, int_mode)
            self._ms_div(clk, r_div, div_by_4)
        elif clk == CLK2:
            self._write_bulk(_CLK2_PARAMETERS, params)
            self._set_int(clk, int_mode)
            self._ms_div(clk, r_div, div_by_4)
        elif clk == CLK3:
            self._write_bulk(_CLK3_PARAMETERS, params)
            self._set_int(clk, int_mode)
            self._ms_div(clk, r_div, div_by_4)
        elif clk == CLK4:
            self._write_bulk(_CLK4_PARAMETERS, params)
            self._set_int(clk, int_mode)
            self._ms_div(clk, r_div, div_by_4)
        elif clk == CLK5:
            self._write_bulk(_CLK5_PARAMETERS, params)
            self._set_int(clk, int_mode)
            self._ms_div(clk, r_div, div_by_4)
        elif clk == CLK6:
            self._write_reg(_CLK6_PARAMETERS, temp)
        elif clk == CLK7:
            self._write_reg(_CLK7_PARAMETERS, temp)

    
    # Set the desired PLL source for a multisynth
    def _set_ms_source(self, clk, pll):
        reg_val = self._read_reg(_CLK0_CTRL + clk)
        if pll == PLLA:
            reg_val &= ~_CLK_PLL_SELECT
        elif pll == PLLB:
            reg_val |= _CLK_PLL_SELECT
        self._write_reg(_CLK0_CTRL + clk, reg_val)
        self._pll_assignment[clk] = pll;
    
    # Apply a reset to the indicated PLL
    def _pll_reset(self, target_pll):
        if target_pll == PLLA:
            self._write_reg(_PLL_RESET, _PLL_RESET_A)
        elif target_pll == PLLB:
            self._write_reg(_PLL_RESET, _PLL_RESET_B)
  
   
            
    # Enable or disable a chosen output        
    def output_enable(self, clk: int, enable: bool):
        reg_val = self._read_reg(_OUTPUT_ENABLE_CTRL)
        if enable is True:
            reg_val &= ~(1<< clk)
        else:
            reg_val |= (1<< clk)
        self.__write_reg(_OUTPUT_ENABLE_CTRL, reg_val)
            
        
    
    def reset(self):
        # First, turn the clocks off
        for i in range (16, 24):
            self._write_reg(i, 0x80)
        # Turn the clocks back on
        for i in range(16, 24):
            self._write_reg(i, 0x0c)
            
        # Set PLLA and PLLB to 800 MHz for automatic tuning
        self._set_pll(_PLL_FIXED, PLLA)
        self._set_pll(_PLL_FIXED, PLLB)
        # Make PLL to CLK assignments for automatic tuning
        for i in range(0,6):
            self._pll_assignment[i] = PLLA
        for i in range(6,8):
            self._pll_assignment[i] = PLLB
            
        self._set_ms_source(CLK0, PLLA)
        self._set_ms_source(CLK1, PLLA)
        self._set_ms_source(CLK2, PLLA)
        self._set_ms_source(CLK3, PLLA)
        self._set_ms_source(CLK4, PLLA)
        self._set_ms_source(CLK5, PLLA)
        self._set_ms_source(CLK6, PLLB)
        self._set_ms_source(CLK7, PLLB)
        
        # Reset the VCXO param
        self._write_reg(_VXCO_PARAMETERS_LOW, 0)
        self._write_reg(_VXCO_PARAMETERS_MID, 0)
        self._write_reg(_VXCO_PARAMETERS_HIGH, 0)

        # Then reset the PLLs
        self._pll_reset(PLLA)
        self._pll_reset(PLLB)
        
        # Set the initial frequencies
        for i in range(0, 8):
            self._clk_freq[i] = 0
            self.output_enable(i, False)
            self._clk_first_set[i] = False
            

    # Initialize the SI5351
    
    def init (self, xtal_load_c: int, xo_freq: int, corr: int):
        # return bool
        device_addresses = self._i2c.scan()
        if self._device_addr not in device_addresses:
            # No device
            return False
        # Wait for _SYS_INIT flag to be clear, indicating the device is ready
        while True:
            status_reg = self._read_reg(_DEVICE_STATUS)
            if (status_reg >> 7) == 0:
                break;
        # Set crystal load capacitance
        self._write_reg(_CRYSTAL_LOAD, (xtal_load_c & _CRYSTAL_LOAD_MASK) | 0b00010010);
        
        # Set up the XO reference frequency
        if xo_freq != 0: # Zero def means select _XTAL_FREQ
            self._set_ref_freq(xo_freq, PLL_INPUT_XO)
        else:
            self._set_ref_freq(_XTAL_FREQ, PLL_INPUT_XO);
        
        # Set coeection
        self._set_correction(corr, PLL_INPUT_XO)
        
        self.reset()
                     
        return True
    
    # Set a specific output to a desired clock frequency
    def set_freq(self, clk: int , freq: int):
        # Return False if failure to set, else True
        int_mode = False
        div_by_4 = False
        clk &= 0x07
        
        # Check which Multisynth is being set
        if clk <= CLK5:
            #
            # MS0 through MS5 logic
            #
            
            # Lower bounds check
            if freq > 0 and freq < _CLKOUT_MIN_FREQ * _FREQ_MULT:
                freq = _CLKOUT_MIN_FREQ * _FREQ_MULT
            # Upper bounds check
            if freq > _MULTISYNTH_MAX_FREQ * _FREQ_MULT:
                freq = _MULTISYNTH_MAX_FREQ * _FREQ_MULT
            # If requested freq >100 MHz and no other outputs are already >100 MHz,
            # we need to recalculate PLLA and then recalculate all other CLK outputs
            # on same PLL
            if freq > (_MULTISYNTH_SHARE_MAX * _FREQ_MULT):
                # Check other clocks on the same PLL
                for i in range(0,6):
                    if self._clk_freq[i] > (_MULTISYNTH_SHARE_MAX * _FREQ_MULT):
                        if (i != clk) and  (self._pll_assignment[i] == self._pll_assignment[clk]):
                            return False # won't set if any other clks already >100 MHz
            
                # Enable the output on first set_freq only
                if self._clk_first_set[clk] == False:
                    self.output_enable(clk, 1)
                    self._clk_first_set[clk] = True
                # Set the freq in memory
                self._clk_freq[clk] = freq
                # Calculate the proper PLL frequency
                (res, ms_reg) = self._multisynth_calc(freq, 0)
                # Set PLL
                #self._set_pll(pll_freq, self._pll_assignment[clk])
                # Recalculate params for other synths on the same PLL
                for i in range(0,6):
                    if self._clk_freq[i] != 0:
                        if self._pll_assignment[i] == self._pll_assignment[clk]:
                            # Select the proper R div value
                            temp_freq = clk_freq[i]
                            (r_div, temp_freq) = self._select_r_div(temp_freq)
                            (ms_value, temp_reg) = self._multisynth_calc(temp_freq, pll_freq)
                            # If freq > 150 MHz, we need to use DIVBY4 and integer mode
                            if temp_freq >= _MULTISYNTH_DIVBY4_FREQ * _FREQ_MULT:
                                div_by_4 = True
                                int_mode = True
                            else:
                                div_by_4 = False
                                int_mode = False
                            self._set_ms(i, temp_reg, int_mode, r_div, div_by_4)
                self._pll_reset(self._pll_assignment[clk])
            else:
                self._clk_freq[clk] = freq
                # Enable the output on the first set_freq only
                if self._clk_first_set[clk] == False:
                    self.output_enable(clk, 1)
                    self._clk_first_set[clk] = True
                # Select the proper R div value
                (r_div, freq) = self._select_r_div(freq)
                # Calculate the proper r_div value
                
                if self._pll_assignment[clk] == PLLA:
                    (res, ms_reg) = self._multisynth_calc(freq, self._plla_freq)
                else:
                    (res, ms_reg) = self._multisynth_calc(freq, self._pllb_freq)
                # Set the multisynth registers
                self._set_ms(clk, ms_reg, int_mode, r_div, div_by_4)
            return 0
        else: #if clk <= CLK5:
            #
            # MS7 and MS7 logic
            #
        
            # Lower bounds check
            if freq > 0 and freq < _CLKOUT67_MIN_FREQ * _FREQ_MULT:
                freq = _CLKOUT_MIN_FREQ * _FREQ_MULT
                
            # Upper bounds check
            if freq >= _MULTISYNTH_DIVBY4_FREQ * _FREQ_MULT:
                freq = _MULTISYNTH_DIVBY4_FREQ * _FREQ_MULT - 1
            # If one of CLK6 or CLK7 is already set when trying to set the other,
            # we have to ensure that it will also have an integer division ratio
            # with the same PLL, otherwise do not set it.
            if clk == CLK6:
                if self._clk_freq[7] != 0:
                    if self._pllb_freq % freq == 0:
                        if (self._pllb_freq // freq) % 2 != 0:
                            # Not an even divide ratio, no bueno
                            return 1
                        else:
                            self._clk_freq[clk] = freq
                            (r_div, freq) = select_r_div_ms67(freq)
                            (res, ms_reg) = multisynth67_calc(freq, pllb_freq)
                    else:
                        # Not an integer, divide ratio no good        
                        return 1
                else:
                    # No previous assignment, so set PLLB based on CLK6
                    
                    # Set the freq in memory
                    self._clk_freq[clk] = freq
                    
                    # Select the proper R div value
                    (r_div, freq) = self._select_r_div_ms67(freq)
                    
                    (pll_freq, ms_reg) = self._multisynth67_calc(freq, 0)
                    self._set_pll(pll_freq, PLLB)
            else: # if clk == CLK6:
                if self._clk_freq[6] != 0:
                    if self._pllb_freq % freq == 0:
                        if (self._pllb_freq // freq) % 2 != 0:
                            # Not an even divide ratio, no bueno
                            return 1
                        else:
                            # Set the freq in memory
                            self._clk_freq[clk] = freq
                            (r_div, freq) = self._select_r_div_ms67(freq)
                            (pll_freq, ms_reg) = self._multisynth67_calc(freq, self._pllb_freq)
                    else:
                        # Not an integer divide ratio, no good
                        return 1
                else:
                    # No previous assignment, so set PLLB based on CLK7
                    
                    # Set the freq in memory
                    self._clk_freq[clk] = freq
                    # select the proper R div value
                    (r_div, freq) = self._select_r_div_ms67(freq)
                    (pll_freq, ms_reg) = self._multisynth67_calc(freq, 0)
                    self._set_pll(pll_freq, self._pll_assignment[clk])
        div_by_4 = False
        int_mode = False
        # Set multisynth registers (MS must be set before PLL)
        self._set_ms(clk, ms_reg, int_mode, r_div, div_by_4)
        return 0
    
    # Enable or disable a chosen output
    #  clk - Clock output
    # enable - Set to True to enable, False to disable
    
    def output_enable(self, clk: int, enable: bool):
        clk &= 0x07
        reg_val = self._read_reg(_OUTPUT_ENABLE_CTRL)
        if enable is True:
            reg_val &= ~(1<<clk)
        else:
            reg_val |= (1<<clk)
        self._write_reg(_OUTPUT_ENABLE_CTRL, reg_val)

    # Sets the drive strength of the specified clock output
    #
    # clk - Clock output
    #
    # drive - Desired drive level
   
    def drive_strength(self, clk: int, drive: int):
        clk &= 0x07
        reg_val = self._read_reg(_CLK0_CTRL + clk);
        reg_val &= ~0x03 # Mask
        if drive == DRIVE_4MA:
            reg_val |= 0x01
        elif drive == DRIVE_6MA:
            reg_val |= 0x02
        elif drive == DRIVE_8MA:
            reg_val |= 0x03
        self._write_reg(_CLK0_CTRL + clk, reg_val)
        
 
    
    
    
        
            
    
    
            
            
        
  
            
    
    
    
   

                    
                            
                            
                            
                        
                        
                    
                
                
                    
                    
                
                
                            
                            
                        
                        
                


            
                
                
                        
            

            
            
            
            
            

            
        
        
        
                              
      
        
    