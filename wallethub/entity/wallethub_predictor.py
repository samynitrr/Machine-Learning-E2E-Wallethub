import os
import sys
from wallethub.exception import WallethubException
from wallethub.util.util import load_object

import pandas as pd


class Data:

    def __init__(self,
                x001: int,x002: float,x003: float,x004: float,x005: float,x006: int,x007: int,x008: int,x009: int,x010: int,
                x011: int,x012: int,x013: int,x014: int,x015: int,x016: int,x017: int,x018: int,x019: int,x020: int,
                x021: int,x022: int,x023: int,x024: int,x025: int,x026: int,x027: int,x028: int,x029: int,x030: int,
                x031: int,x032: int,x033: int,x034: int,x035: int,x036: int,x037: int,x038: int,x039: int,x040: int,
                x041: float,x042: int,x043: int,x044: float,x045: float,x046: int,x047: int,x048: int,x049: int,x050: int,
                x051: int,x052: int,x053: int,x054: int,x055: int,x056: int,x057: float,x058: float,x059: int,x060: int,
                x061: int,
                x062: int,
                x063: int,
                x064: int,
                x065: int,
                x066: int,
                x067: int,
                x068: int,
                x069: int,
                x070: int,
                x071: int,
                x072: int,
                x073: int,
                x074: int,
                x075: int,
                x076: int,
                x077: int,
                x078: int,
                x079: int,
                x080: int,
                x081: int,
                x082: int,
                x083: int,
                x084: int,
                x085: int,
                x086: int,
                x087: int,
                x088: int,
                x089: int,
                x090: int,
                x091: int,
                x092: int,
                x093: int,
                x094: int,
                x095: int,
                x096: int,
                x097: int,
                x098: float,
                x099: int,
                x100: int,
                x101: int,
                x102: int,
                x103: int,
                x104: int,
                x105: int,
                x106: int,
                x107: int,
                x108: int,
                x109: int,
                x110: int,
                x111: int,
                x112: int,
                x113: int,
                x114: int,
                x115: int,
                x116: int,
                x117: int,
                x118: int,
                x119: int,
                x120: int,
                x121: int,
                x122: int,
                x123: int,
                x124: int,
                x125: int,
                x126: int,
                x127: int,
                x128: int,
                x129: int,
                x130: int,
                x131: int,
                x132: int,
                x133: int,
                x134: int,
                x135: int,
                x136: int,
                x137: int,
                x138: int,
                x139: int,
                x140: int,
                x141: int,
                x142: int,
                x143: int,
                x144: int,
                x145: int,
                x146: int,
                x147: int,
                x148: float,
                x149: int,
                x150: int,
                x151: int,
                x152: int,
                x153: int,
                x154: int,
                x155: float,
                x156: int,
                x157: int,
                x158: int,
                x159: int,
                x160: int,
                x161: int,
                x162: float,
                x163: int,
                x164: int,
                x165: int,
                x166: int,
                x167: int,
                x168: int,
                x169: int,
                x170: int,
                x171: int,
                x172: int,
                x173: int,
                x174: int,
                x175: int,
                x176: int,
                x177: int,
                x178: int,
                x179: int,
                x180: int,
                x181: int,
                x182: int,
                x183: int,
                x184: int,
                x185: int,
                x186: int,
                x187: int,
                x188: int,
                x189: int,
                x190: int,
                x191: int,
                x192: int,
                x193: int,
                x194: int,
                x195: int,
                x196: int,
                x197: int,
                x198: int,
                x199: int,
                x200: int,
                x201: int,
                x202: int,
                x203: int,
                x204: int,
                x205: int,
                x206: int,
                x207: int,
                x208: int,
                x209: int,
                x210: int,
                x211: int,
                x212: int,
                x213: int,
                x214: int,
                x215: int,
                x216: int,
                x217: int,
                x218: int,
                x219: int,
                x220: int,
                x221: int,
                x222: float,
                x223: float,
                x224: int,
                x225: int,
                x226: int,
                x227: int,
                x228: int,
                x229: int,
                x230: int,
                x231: int,
                x232: int,
                x233: int,
                x234: float,
                x235: float,
                x236: int,
                x237: float,
                x238: float,
                x239: float,
                x240: int,
                x241: int,
                x242: float,
                x243: int,
                x244: int,
                x245: int,
                x246: int,
                x247: int,
                x248: int,
                x249: int,
                x250: int,
                x251: int,
                x252: int,
                x253: float,
                x254: int,
                x255: float,
                x256: float,
                x257: float,
                x258: int,
                x259: float,
                x260: int,
                x261: int,
                x262: int,
                x263: int,
                x264: int,
                x265: float,
                x266: float,
                x267: float,
                x268: float,
                x269: int,
                x270: int,
                x271: int,
                x272: float,
                x273: int,
                x274: int,
                x275: float,
                x276: int,
                x277: int,
                x278: int,
                x279: int,
                x280: int,
                x281: int,
                x282: int,
                x283: int,
                x284: int,
                x285: int,
                x286: int,
                x287: float,
                x288: float,
                x289: float,
                x290: float,
                x291: int,
                x292: int,
                x293: float,
                x294: int,
                x295: float,
                x296: int,
                x297: float,
                x298: int,
                x299: int,
                x300: int,
                x301: int,
                x302: float,
                x303: int,
                x304: float,
                y: int
                 ):
        try:
            self.x001 = x001
            self.x002 = x002
            self.x003 = x003
            self.x004 = x004
            self.x005 = x005
            self.x006 = x006
            self.x007 = x007
            self.x008 = x008
            self.x009 = x009
            self.x010 = x010
            self.x011 = x011
            self.x012 = x012
            self.x013 = x013
            self.x014 = x014
            self.x015 = x015
            self.x016 = x016
            self.x017 = x017
            self.x018 = x018
            self.x019 = x019
            self.x020 = x020
            self.x021 = x021
            self.x022 = x022
            self.x023 = x023
            self.x024 = x024
            self.x025 = x025
            self.x026 = x026
            self.x027 = x027
            self.x028 = x028
            self.x029 = x029
            self.x030 = x030
            self.x031 = x031
            self.x032 = x032
            self.x033 = x033
            self.x034 = x034
            self.x035 = x035
            self.x036 = x036
            self.x037 = x037
            self.x038 = x038
            self.x039 = x039
            self.x040 = x040
            self.x041 = x041
            self.x042 = x042
            self.x043 = x043
            self.x044 = x044
            self.x045 = x045
            self.x046 = x046
            self.x047 = x047
            self.x048 = x048
            self.x049 = x049
            self.x050 = x050
            self.x051 = x051
            self.x052 = x052
            self.x053 = x053
            self.x054 = x054
            self.x055 = x055
            self.x056 = x056
            self.x057 = x057
            self.x058 = x058
            self.x059 = x059
            self.x060 = x060
            self.x061 = x061
            self.x062 = x062
            self.x063 = x063
            self.x064 = x064
            self.x065 = x065
            self.x066 = x066
            self.x067 = x067
            self.x068 = x068
            self.x069 = x069
            self.x070 = x070
            self.x071 = x071
            self.x072 = x072
            self.x073 = x073
            self.x074 = x074
            self.x075 = x075
            self.x076 = x076
            self.x077 = x077
            self.x078 = x078
            self.x079 = x079
            self.x080 = x080
            self.x081 = x081
            self.x082 = x082
            self.x083 = x083
            self.x084 = x084
            self.x085 = x085
            self.x086 = x086
            self.x087 = x087
            self.x088 = x088
            self.x089 = x089
            self.x090 = x090
            self.x091 = x091
            self.x092 = x092
            self.x093 = x093
            self.x094 = x094
            self.x095 = x095
            self.x096 = x096
            self.x097 = x097
            self.x098 = x098
            self.x099 = x099
            self.x100 = x100
            self.x101 = x101
            self.x102 = x102
            self.x103 = x103
            self.x104 = x104
            self.x105 = x105
            self.x106 = x106
            self.x107 = x107
            self.x108 = x108
            self.x109 = x109
            self.x110 = x110
            self.x111 = x111
            self.x112 = x112
            self.x113 = x113
            self.x114 = x114
            self.x115 = x115
            self.x116 = x116
            self.x117 = x117
            self.x118 = x118
            self.x119 = x119
            self.x120 = x120
            self.x121 = x121
            self.x122 = x122
            self.x123 = x123
            self.x124 = x124
            self.x125 = x125
            self.x126 = x126
            self.x127 = x127
            self.x128 = x128
            self.x129 = x129
            self.x130 = x130
            self.x131 = x131
            self.x132 = x132
            self.x133 = x133
            self.x134 = x134
            self.x135 = x135
            self.x136 = x136
            self.x137 = x137
            self.x138 = x138
            self.x139 = x139
            self.x140 = x140
            self.x141 = x141
            self.x142 = x142
            self.x143 = x143
            self.x144 = x144
            self.x145 = x145
            self.x146 = x146
            self.x147 = x147
            self.x148 = x148
            self.x149 = x149
            self.x150 = x150
            self.x151 = x151
            self.x152 = x152
            self.x153 = x153
            self.x154 = x154
            self.x155 = x155
            self.x156 = x156
            self.x157 = x157
            self.x158 = x158
            self.x159 = x159
            self.x160 = x160
            self.x161 = x161
            self.x162 = x162
            self.x163 = x163
            self.x164 = x164
            self.x165 = x165
            self.x166 = x166
            self.x167 = x167
            self.x168 = x168
            self.x169 = x169
            self.x170 = x170
            self.x171 = x171
            self.x172 = x172
            self.x173 = x173
            self.x174 = x174
            self.x175 = x175
            self.x176 = x176
            self.x177 = x177
            self.x178 = x178
            self.x179 = x179
            self.x180 = x180
            self.x181 = x181
            self.x182 = x182
            self.x183 = x183
            self.x184 = x184
            self.x185 = x185
            self.x186 = x186
            self.x187 = x187
            self.x188 = x188
            self.x189 = x189
            self.x190 = x190
            self.x191 = x191
            self.x192 = x192
            self.x193 = x193
            self.x194 = x194
            self.x195 = x195
            self.x196 = x196
            self.x197 = x197
            self.x198 = x198
            self.x199 = x199
            self.x200 = x200
            self.x201 = x201
            self.x202 = x202
            self.x203 = x203
            self.x204 = x204
            self.x205 = x205
            self.x206 = x206
            self.x207 = x207
            self.x208 = x208
            self.x209 = x209
            self.x210 = x210
            self.x211 = x211
            self.x212 = x212
            self.x213 = x213
            self.x214 = x214
            self.x215 = x215
            self.x216 = x216
            self.x217 = x217
            self.x218 = x218
            self.x219 = x219
            self.x220 = x220
            self.x221 = x221
            self.x222 = x222
            self.x223 = x223
            self.x224 = x224
            self.x225 = x225
            self.x226 = x226
            self.x227 = x227
            self.x228 = x228
            self.x229 = x229
            self.x230 = x230
            self.x231 = x231
            self.x232 = x232
            self.x233 = x233
            self.x234 = x234
            self.x235 = x235
            self.x236 = x236
            self.x237 = x237
            self.x238 = x238
            self.x239 = x239
            self.x240 = x240
            self.x241 = x241
            self.x242 = x242
            self.x243 = x243
            self.x244 = x244
            self.x245 = x245
            self.x246 = x246
            self.x247 = x247
            self.x248 = x248
            self.x249 = x249
            self.x250 = x250
            self.x251 = x251
            self.x252 = x252
            self.x253 = x253
            self.x254 = x254
            self.x255 = x255
            self.x256 = x256
            self.x257 = x257
            self.x258 = x258
            self.x259 = x259
            self.x260 = x260
            self.x261 = x261
            self.x262 = x262
            self.x263 = x263
            self.x264 = x264
            self.x265 = x265
            self.x266 = x266
            self.x267 = x267
            self.x268 = x268
            self.x269 = x269
            self.x270 = x270
            self.x271 = x271
            self.x272 = x272
            self.x273 = x273
            self.x274 = x274
            self.x275 = x275
            self.x276 = x276
            self.x277 = x277
            self.x278 = x278
            self.x279 = x279
            self.x280 = x280
            self.x281 = x281
            self.x282 = x282
            self.x283 = x283
            self.x284 = x284
            self.x285 = x285
            self.x286 = x286
            self.x287 = x287
            self.x288 = x288
            self.x289 = x289
            self.x290 = x290
            self.x291 = x291
            self.x292 = x292
            self.x293 = x293
            self.x294 = x294
            self.x295 = x295
            self.x296 = x296
            self.x297 = x297
            self.x298 = x298
            self.x299 = x299
            self.x300 = x300
            self.x301 = x301
            self.x302 = x302
            self.x303 = x303
            self.x304 = x304
            self.y = y
        except Exception as e:
            raise WallethubException(e, sys) from e

    def get_input_data_frame(self):

        try:
            input_dict = self.get_data_as_dict()
            return pd.DataFrame(input_dict)
        except Exception as e:
            raise WallethubException(e, sys) from e

    def get_data_as_dict(self):
        try:
            input_data = {
                "x001" : [self.x001],
                "x002" : [self.x002],
                "x003" : [self.x003],
                "x004" : [self.x004],
                "x005" : [self.x005],
                "x006" : [self.x006],
                "x007" : [self.x007],
                "x008" : [self.x008],
                "x009" : [self.x009],
                "x010" : [self.x010],
                "x011" : [self.x011],
                "x012" : [self.x012],
                "x013" : [self.x013],
                "x014" : [self.x014],
                "x015" : [self.x015],
                "x016" : [self.x016],
                "x017" : [self.x017],
                "x018" : [self.x018],
                "x019" : [self.x019],
                "x020" : [self.x020],
                "x021" : [self.x021],
                "x022" : [self.x022],
                "x023" : [self.x023],
                "x024" : [self.x024],
                "x025" : [self.x025],
                "x026" : [self.x026],
                "x027" : [self.x027],
                "x028" : [self.x028],
                "x029" : [self.x029],
                "x030" : [self.x030],
                "x031" : [self.x031],
                "x032" : [self.x032],
                "x033" : [self.x033],
                "x034" : [self.x034],
                "x035" : [self.x035],
                "x036" : [self.x036],
                "x037" : [self.x037],
                "x038" : [self.x038],
                "x039" : [self.x039],
                "x040" : [self.x040],
                "x041" : [self.x041],
                "x042" : [self.x042],
                "x043" : [self.x043],
                "x044" : [self.x044],
                "x045" : [self.x045],
                "x046" : [self.x046],
                "x047" : [self.x047],
                "x048" : [self.x048],
                "x049" : [self.x049],
                "x050" : [self.x050],
                "x051" : [self.x051],
                "x052" : [self.x052],
                "x053" : [self.x053],
                "x054" : [self.x054],
                "x055" : [self.x055],
                "x056" : [self.x056],
                "x057" : [self.x057],
                "x058" : [self.x058],
                "x059" : [self.x059],
                "x060" : [self.x060],
                "x061" : [self.x061],
                "x062" : [self.x062],
                "x063" : [self.x063],
                "x064" : [self.x064],
                "x065" : [self.x065],
                "x066" : [self.x066],
                "x067" : [self.x067],
                "x068" : [self.x068],
                "x069" : [self.x069],
                "x070" : [self.x070],
                "x071" : [self.x071],
                "x072" : [self.x072],
                "x073" : [self.x073],
                "x074" : [self.x074],
                "x075" : [self.x075],
                "x076" : [self.x076],
                "x077" : [self.x077],
                "x078" : [self.x078],
                "x079" : [self.x079],
                "x080" : [self.x080],
                "x081" : [self.x081],
                "x082" : [self.x082],
                "x083" : [self.x083],
                "x084" : [self.x084],
                "x085" : [self.x085],
                "x086" : [self.x086],
                "x087" : [self.x087],
                "x088" : [self.x088],
                "x089" : [self.x089],
                "x090" : [self.x090],
                "x091" : [self.x091],
                "x092" : [self.x092],
                "x093" : [self.x093],
                "x094" : [self.x094],
                "x095" : [self.x095],
                "x096" : [self.x096],
                "x097" : [self.x097],
                "x098" : [self.x098],
                "x099" : [self.x099],
                "x100" : [self.x100],
                "x101" : [self.x101],
                "x102" : [self.x102],
                "x103" : [self.x103],
                "x104" : [self.x104],
                "x105" : [self.x105],
                "x106" : [self.x106],
                "x107" : [self.x107],
                "x108" : [self.x108],
                "x109" : [self.x109],
                "x110" : [self.x110],
                "x111" : [self.x111],
                "x112" : [self.x112],
                "x113" : [self.x113],
                "x114" : [self.x114],
                "x115" : [self.x115],
                "x116" : [self.x116],
                "x117" : [self.x117],
                "x118" : [self.x118],
                "x119" : [self.x119],
                "x120" : [self.x120],
                "x121" : [self.x121],
                "x122" : [self.x122],
                "x123" : [self.x123],
                "x124" : [self.x124],
                "x125" : [self.x125],
                "x126" : [self.x126],
                "x127" : [self.x127],
                "x128" : [self.x128],
                "x129" : [self.x129],
                "x130" : [self.x130],
                "x131" : [self.x131],
                "x132" : [self.x132],
                "x133" : [self.x133],
                "x134" : [self.x134],
                "x135" : [self.x135],
                "x136" : [self.x136],
                "x137" : [self.x137],
                "x138" : [self.x138],
                "x139" : [self.x139],
                "x140" : [self.x140],
                "x141" : [self.x141],
                "x142" : [self.x142],
                "x143" : [self.x143],
                "x144" : [self.x144],
                "x145" : [self.x145],
                "x146" : [self.x146],
                "x147" : [self.x147],
                "x148" : [self.x148],
                "x149" : [self.x149],
                "x150" : [self.x150],
                "x151" : [self.x151],
                "x152" : [self.x152],
                "x153" : [self.x153],
                "x154" : [self.x154],
                "x155" : [self.x155],
                "x156" : [self.x156],
                "x157" : [self.x157],
                "x158" : [self.x158],
                "x159" : [self.x159],
                "x160" : [self.x160],
                "x161" : [self.x161],
                "x162" : [self.x162],
                "x163" : [self.x163],
                "x164" : [self.x164],
                "x165" : [self.x165],
                "x166" : [self.x166],
                "x167" : [self.x167],
                "x168" : [self.x168],
                "x169" : [self.x169],
                "x170" : [self.x170],
                "x171" : [self.x171],
                "x172" : [self.x172],
                "x173" : [self.x173],
                "x174" : [self.x174],
                "x175" : [self.x175],
                "x176" : [self.x176],
                "x177" : [self.x177],
                "x178" : [self.x178],
                "x179" : [self.x179],
                "x180" : [self.x180],
                "x181" : [self.x181],
                "x182" : [self.x182],
                "x183" : [self.x183],
                "x184" : [self.x184],
                "x185" : [self.x185],
                "x186" : [self.x186],
                "x187" : [self.x187],
                "x188" : [self.x188],
                "x189" : [self.x189],
                "x190" : [self.x190],
                "x191" : [self.x191],
                "x192" : [self.x192],
                "x193" : [self.x193],
                "x194" : [self.x194],
                "x195" : [self.x195],
                "x196" : [self.x196],
                "x197" : [self.x197],
                "x198" : [self.x198],
                "x199" : [self.x199],
                "x200" : [self.x200],
                "x201" : [self.x201],
                "x202" : [self.x202],
                "x203" : [self.x203],
                "x204" : [self.x204],
                "x205" : [self.x205],
                "x206" : [self.x206],
                "x207" : [self.x207],
                "x208" : [self.x208],
                "x209" : [self.x209],
                "x210" : [self.x210],
                "x211" : [self.x211],
                "x212" : [self.x212],
                "x213" : [self.x213],
                "x214" : [self.x214],
                "x215" : [self.x215],
                "x216" : [self.x216],
                "x217" : [self.x217],
                "x218" : [self.x218],
                "x219" : [self.x219],
                "x220" : [self.x220],
                "x221" : [self.x221],
                "x222" : [self.x222],
                "x223" : [self.x223],
                "x224" : [self.x224],
                "x225" : [self.x225],
                "x226" : [self.x226],
                "x227" : [self.x227],
                "x228" : [self.x228],
                "x229" : [self.x229],
                "x230" : [self.x230],
                "x231" : [self.x231],
                "x232" : [self.x232],
                "x233" : [self.x233],
                "x234" : [self.x234],
                "x235" : [self.x235],
                "x236" : [self.x236],
                "x237" : [self.x237],
                "x238" : [self.x238],
                "x239" : [self.x239],
                "x240" : [self.x240],
                "x241" : [self.x241],
                "x242" : [self.x242],
                "x243" : [self.x243],
                "x244" : [self.x244],
                "x245" : [self.x245],
                "x246" : [self.x246],
                "x247" : [self.x247],
                "x248" : [self.x248],
                "x249" : [self.x249],
                "x250" : [self.x250],
                "x251" : [self.x251],
                "x252" : [self.x252],
                "x253" : [self.x253],
                "x254" : [self.x254],
                "x255" : [self.x255],
                "x256" : [self.x256],
                "x257" : [self.x257],
                "x258" : [self.x258],
                "x259" : [self.x259],
                "x260" : [self.x260],
                "x261" : [self.x261],
                "x262" : [self.x262],
                "x263" : [self.x263],
                "x264" : [self.x264],
                "x265" : [self.x265],
                "x266" : [self.x266],
                "x267" : [self.x267],
                "x268" : [self.x268],
                "x269" : [self.x269],
                "x270" : [self.x270],
                "x271" : [self.x271],
                "x272" : [self.x272],
                "x273" : [self.x273],
                "x274" : [self.x274],
                "x275" : [self.x275],
                "x276" : [self.x276],
                "x277" : [self.x277],
                "x278" : [self.x278],
                "x279" : [self.x279],
                "x280" : [self.x280],
                "x281" : [self.x281],
                "x282" : [self.x282],
                "x283" : [self.x283],
                "x284" : [self.x284],
                "x285" : [self.x285],
                "x286" : [self.x286],
                "x287" : [self.x287],
                "x288" : [self.x288],
                "x289" : [self.x289],
                "x290" : [self.x290],
                "x291" : [self.x291],
                "x292" : [self.x292],
                "x293" : [self.x293],
                "x294" : [self.x294],
                "x295" : [self.x295],
                "x296" : [self.x296],
                "x297" : [self.x297],
                "x298" : [self.x298],
                "x299" : [self.x299],
                "x300" : [self.x300],
                "x301" : [self.x301],
                "x302" : [self.x302],
                "x303" : [self.x303],
                "x304" : [self.x304],
                "y": [self.y]
                
                }
            return input_data
        except Exception as e:
            raise WallethubException(e, sys)


class Predictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise WallethubException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise WallethubException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            y_pred = model.predict(X)
            return y_pred[0]
        except Exception as e:
            raise WallethubException(e, sys) from e