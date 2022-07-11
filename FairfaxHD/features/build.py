#!/usr/bin/env python

from __future__ import print_function
import re

psNameTable = {
	0x0000: '.null',
	0x000D: 'nonmarkingreturn',
	0x0020: 'space',
	0x0021: 'exclam',
	0x0022: 'quotedbl',
	0x0023: 'numbersign',
	0x0024: 'dollar',
	0x0025: 'percent',
	0x0026: 'ampersand',
	0x0027: 'quotesingle',
	0x0028: 'parenleft',
	0x0029: 'parenright',
	0x002A: 'asterisk',
	0x002B: 'plus',
	0x002C: 'comma',
	0x002D: 'hyphen',
	0x002E: 'period',
	0x002F: 'slash',
	0x0030: 'zero',
	0x0031: 'one',
	0x0032: 'two',
	0x0033: 'three',
	0x0034: 'four',
	0x0035: 'five',
	0x0036: 'six',
	0x0037: 'seven',
	0x0038: 'eight',
	0x0039: 'nine',
	0x003A: 'colon',
	0x003B: 'semicolon',
	0x003C: 'less',
	0x003D: 'equal',
	0x003E: 'greater',
	0x003F: 'question',
	0x0040: 'at',
	0x0041: 'A',
	0x0042: 'B',
	0x0043: 'C',
	0x0044: 'D',
	0x0045: 'E',
	0x0046: 'F',
	0x0047: 'G',
	0x0048: 'H',
	0x0049: 'I',
	0x004A: 'J',
	0x004B: 'K',
	0x004C: 'L',
	0x004D: 'M',
	0x004E: 'N',
	0x004F: 'O',
	0x0050: 'P',
	0x0051: 'Q',
	0x0052: 'R',
	0x0053: 'S',
	0x0054: 'T',
	0x0055: 'U',
	0x0056: 'V',
	0x0057: 'W',
	0x0058: 'X',
	0x0059: 'Y',
	0x005A: 'Z',
	0x005B: 'bracketleft',
	0x005C: 'backslash',
	0x005D: 'bracketright',
	0x005E: 'asciicircum',
	0x005F: 'underscore',
	0x0060: 'grave',
	0x0061: 'a',
	0x0062: 'b',
	0x0063: 'c',
	0x0064: 'd',
	0x0065: 'e',
	0x0066: 'f',
	0x0067: 'g',
	0x0068: 'h',
	0x0069: 'i',
	0x006A: 'j',
	0x006B: 'k',
	0x006C: 'l',
	0x006D: 'm',
	0x006E: 'n',
	0x006F: 'o',
	0x0070: 'p',
	0x0071: 'q',
	0x0072: 'r',
	0x0073: 's',
	0x0074: 't',
	0x0075: 'u',
	0x0076: 'v',
	0x0077: 'w',
	0x0078: 'x',
	0x0079: 'y',
	0x007A: 'z',
	0x007B: 'braceleft',
	0x007C: 'bar',
	0x007D: 'braceright',
	0x007E: 'asciitilde',
	0x00A0: 'nonbreakingspace',
	0x00A1: 'exclamdown',
	0x00A2: 'cent',
	0x00A3: 'sterling',
	0x00A4: 'currency',
	0x00A5: 'yen',
	0x00A6: 'brokenbar',
	0x00A7: 'section',
	0x00A8: 'dieresis',
	0x00A9: 'copyright',
	0x00AA: 'ordfeminine',
	0x00AB: 'guillemotleft',
	0x00AC: 'logicalnot',
	0x00AD: 'hyphen',
	0x00AE: 'registered',
	0x00AF: 'macron',
	0x00B0: 'degree',
	0x00B1: 'plusminus',
	0x00B2: 'twosuperior',
	0x00B3: 'threesuperior',
	0x00B4: 'acute',
	0x00B5: 'mu',
	0x00B6: 'paragraph',
	0x00B7: 'periodcentered',
	0x00B8: 'cedilla',
	0x00B9: 'onesuperior',
	0x00BA: 'ordmasculine',
	0x00BB: 'guillemotright',
	0x00BC: 'onequarter',
	0x00BD: 'onehalf',
	0x00BE: 'threequarters',
	0x00BF: 'questiondown',
	0x00C0: 'Agrave',
	0x00C1: 'Aacute',
	0x00C2: 'Acircumflex',
	0x00C3: 'Atilde',
	0x00C4: 'Adieresis',
	0x00C5: 'Aring',
	0x00C6: 'AE',
	0x00C7: 'Ccedilla',
	0x00C8: 'Egrave',
	0x00C9: 'Eacute',
	0x00CA: 'Ecircumflex',
	0x00CB: 'Edieresis',
	0x00CC: 'Igrave',
	0x00CD: 'Iacute',
	0x00CE: 'Icircumflex',
	0x00CF: 'Idieresis',
	0x00D0: 'Eth',
	0x00D1: 'Ntilde',
	0x00D2: 'Ograve',
	0x00D3: 'Oacute',
	0x00D4: 'Ocircumflex',
	0x00D5: 'Otilde',
	0x00D6: 'Odieresis',
	0x00D7: 'multiply',
	0x00D8: 'Oslash',
	0x00D9: 'Ugrave',
	0x00DA: 'Uacute',
	0x00DB: 'Ucircumflex',
	0x00DC: 'Udieresis',
	0x00DD: 'Yacute',
	0x00DE: 'Thorn',
	0x00DF: 'germandbls',
	0x00E0: 'agrave',
	0x00E1: 'aacute',
	0x00E2: 'acircumflex',
	0x00E3: 'atilde',
	0x00E4: 'adieresis',
	0x00E5: 'aring',
	0x00E6: 'ae',
	0x00E7: 'ccedilla',
	0x00E8: 'egrave',
	0x00E9: 'eacute',
	0x00EA: 'ecircumflex',
	0x00EB: 'edieresis',
	0x00EC: 'igrave',
	0x00ED: 'iacute',
	0x00EE: 'icircumflex',
	0x00EF: 'idieresis',
	0x00F0: 'eth',
	0x00F1: 'ntilde',
	0x00F2: 'ograve',
	0x00F3: 'oacute',
	0x00F4: 'ocircumflex',
	0x00F5: 'otilde',
	0x00F6: 'odieresis',
	0x00F7: 'divide',
	0x00F8: 'oslash',
	0x00F9: 'ugrave',
	0x00FA: 'uacute',
	0x00FB: 'ucircumflex',
	0x00FC: 'udieresis',
	0x00FD: 'yacute',
	0x00FE: 'thorn',
	0x00FF: 'ydieresis',
	0x0100: 'Amacron',
	0x0101: 'amacron',
	0x0102: 'Abreve',
	0x0103: 'abreve',
	0x0104: 'Aogonek',
	0x0105: 'aogonek',
	0x0106: 'Cacute',
	0x0107: 'cacute',
	0x0108: 'Ccircumflex',
	0x0109: 'ccircumflex',
	0x010A: 'Cdotaccent',
	0x010B: 'cdotaccent',
	0x010C: 'Ccaron',
	0x010D: 'ccaron',
	0x010E: 'Dcaron',
	0x010F: 'dcaron',
	0x0110: 'Dcroat',
	0x0111: 'dcroat',
	0x0112: 'Emacron',
	0x0113: 'emacron',
	0x0114: 'Ebreve',
	0x0115: 'ebreve',
	0x0116: 'Edotaccent',
	0x0117: 'edotaccent',
	0x0118: 'Eogonek',
	0x0119: 'eogonek',
	0x011A: 'Ecaron',
	0x011B: 'ecaron',
	0x011C: 'Gcircumflex',
	0x011D: 'gcircumflex',
	0x011E: 'Gbreve',
	0x011F: 'gbreve',
	0x0120: 'Gdotaccent',
	0x0121: 'gdotaccent',
	0x0122: 'Gcommaaccent',
	0x0123: 'gcommaaccent',
	0x0124: 'Hcircumflex',
	0x0125: 'hcircumflex',
	0x0126: 'Hbar',
	0x0127: 'hbar',
	0x0128: 'Itilde',
	0x0129: 'itilde',
	0x012A: 'Imacron',
	0x012B: 'imacron',
	0x012C: 'Ibreve',
	0x012D: 'ibreve',
	0x012E: 'Iogonek',
	0x012F: 'iogonek',
	0x0130: 'Idotaccent',
	0x0131: 'dotlessi',
	0x0132: 'IJ',
	0x0133: 'ij',
	0x0134: 'Jcircumflex',
	0x0135: 'jcircumflex',
	0x0136: 'Kcommaaccent',
	0x0137: 'kcommaaccent',
	0x0138: 'kgreenlandic',
	0x0139: 'Lacute',
	0x013A: 'lacute',
	0x013B: 'Lcommaaccent',
	0x013C: 'lcommaaccent',
	0x013D: 'Lcaron',
	0x013E: 'lcaron',
	0x013F: 'Ldot',
	0x0140: 'ldot',
	0x0141: 'Lslash',
	0x0142: 'lslash',
	0x0143: 'Nacute',
	0x0144: 'nacute',
	0x0145: 'Ncommaaccent',
	0x0146: 'ncommaaccent',
	0x0147: 'Ncaron',
	0x0148: 'ncaron',
	0x0149: 'napostrophe',
	0x014A: 'Eng',
	0x014B: 'eng',
	0x014C: 'Omacron',
	0x014D: 'omacron',
	0x014E: 'Obreve',
	0x014F: 'obreve',
	0x0150: 'Ohungarumlaut',
	0x0151: 'ohungarumlaut',
	0x0152: 'OE',
	0x0153: 'oe',
	0x0154: 'Racute',
	0x0155: 'racute',
	0x0156: 'Rcommaaccent',
	0x0157: 'rcommaaccent',
	0x0158: 'Rcaron',
	0x0159: 'rcaron',
	0x015A: 'Sacute',
	0x015B: 'sacute',
	0x015C: 'Scircumflex',
	0x015D: 'scircumflex',
	0x015E: 'Scedilla',
	0x015F: 'scedilla',
	0x0160: 'Scaron',
	0x0161: 'scaron',
	0x0162: 'Tcommaaccent',
	0x0163: 'tcommaaccent',
	0x0164: 'Tcaron',
	0x0165: 'tcaron',
	0x0166: 'Tbar',
	0x0167: 'tbar',
	0x0168: 'Utilde',
	0x0169: 'utilde',
	0x016A: 'Umacron',
	0x016B: 'umacron',
	0x016C: 'Ubreve',
	0x016D: 'ubreve',
	0x016E: 'Uring',
	0x016F: 'uring',
	0x0170: 'Uhungarumlaut',
	0x0171: 'uhungarumlaut',
	0x0172: 'Uogonek',
	0x0173: 'uogonek',
	0x0174: 'Wcircumflex',
	0x0175: 'wcircumflex',
	0x0176: 'Ycircumflex',
	0x0177: 'ycircumflex',
	0x0178: 'Ydieresis',
	0x0179: 'Zacute',
	0x017A: 'zacute',
	0x017B: 'Zdotaccent',
	0x017C: 'zdotaccent',
	0x017D: 'Zcaron',
	0x017E: 'zcaron',
	0x017F: 'longs',
	0x0192: 'florin',
	0x01FA: 'Aringacute',
	0x01FB: 'aringacute',
	0x01FC: 'AEacute',
	0x01FD: 'aeacute',
	0x01FE: 'Oslashacute',
	0x01FF: 'oslashacute',
	0x02C6: 'circumflex',
	0x02C7: 'caron',
	0x02C9: 'macron',
	0x02D8: 'breve',
	0x02D9: 'dotaccent',
	0x02DA: 'ring',
	0x02DB: 'ogonek',
	0x02DC: 'tilde',
	0x02DD: 'hungarumlaut',
	0x0384: 'tonos',
	0x0385: 'dieresistonos',
	0x0386: 'Alphatonos',
	0x0387: 'anoteleia',
	0x0388: 'Epsilontonos',
	0x0389: 'Etatonos',
	0x038A: 'Iotatonos',
	0x038C: 'Omicrontonos',
	0x038E: 'Upsilontonos',
	0x038F: 'Omegatonos',
	0x0390: 'iotadieresistonos',
	0x0391: 'Alpha',
	0x0392: 'Beta',
	0x0393: 'Gamma',
	0x0394: 'Delta',
	0x0395: 'Epsilon',
	0x0396: 'Zeta',
	0x0397: 'Eta',
	0x0398: 'Theta',
	0x0399: 'Iota',
	0x039A: 'Kappa',
	0x039B: 'Lambda',
	0x039C: 'Mu',
	0x039D: 'Nu',
	0x039E: 'Xi',
	0x039F: 'Omicron',
	0x03A0: 'Pi',
	0x03A1: 'Rho',
	0x03A3: 'Sigma',
	0x03A4: 'Tau',
	0x03A5: 'Upsilon',
	0x03A6: 'Phi',
	0x03A7: 'Chi',
	0x03A8: 'Psi',
	0x03A9: 'Omega',
	0x03AA: 'Iotadieresis',
	0x03AB: 'Upsilondieresis',
	0x03AC: 'alphatonos',
	0x03AD: 'epsilontonos',
	0x03AE: 'etatonos',
	0x03AF: 'iotatonos',
	0x03B0: 'upsilondieresistonos',
	0x03B1: 'alpha',
	0x03B2: 'beta',
	0x03B3: 'gamma',
	0x03B4: 'delta',
	0x03B5: 'epsilon',
	0x03B6: 'zeta',
	0x03B7: 'eta',
	0x03B8: 'theta',
	0x03B9: 'iota',
	0x03BA: 'kappa',
	0x03BB: 'lambda',
	0x03BC: 'mu',
	0x03BD: 'nu',
	0x03BE: 'xi',
	0x03BF: 'omicron',
	0x03C0: 'pi',
	0x03C1: 'rho',
	0x03C2: 'sigma1',
	0x03C3: 'sigma',
	0x03C4: 'tau',
	0x03C5: 'upsilon',
	0x03C6: 'phi',
	0x03C7: 'chi',
	0x03C8: 'psi',
	0x03C9: 'omega',
	0x03CA: 'iotadieresis',
	0x03CB: 'upsilondieresis',
	0x03CC: 'omicrontonos',
	0x03CD: 'upsilontonos',
	0x03CE: 'omegatonos',
	0x0400: 'uni0400',
	0x0401: 'afii10023',
	0x0402: 'afii10051',
	0x0403: 'afii10052',
	0x0404: 'afii10053',
	0x0405: 'afii10054',
	0x0406: 'afii10055',
	0x0407: 'afii10056',
	0x0408: 'afii10057',
	0x0409: 'afii10058',
	0x040A: 'afii10059',
	0x040B: 'afii10060',
	0x040C: 'afii10061',
	0x040D: 'uni040D',
	0x040E: 'afii10062',
	0x040F: 'afii10145',
	0x0410: 'afii10017',
	0x0411: 'afii10018',
	0x0412: 'afii10019',
	0x0413: 'afii10020',
	0x0414: 'afii10021',
	0x0415: 'afii10022',
	0x0416: 'afii10024',
	0x0417: 'afii10025',
	0x0418: 'afii10026',
	0x0419: 'afii10027',
	0x041A: 'afii10028',
	0x041B: 'afii10029',
	0x041C: 'afii10030',
	0x041D: 'afii10031',
	0x041E: 'afii10032',
	0x041F: 'afii10033',
	0x0420: 'afii10034',
	0x0421: 'afii10035',
	0x0422: 'afii10036',
	0x0423: 'afii10037',
	0x0424: 'afii10038',
	0x0425: 'afii10039',
	0x0426: 'afii10040',
	0x0427: 'afii10041',
	0x0428: 'afii10042',
	0x0429: 'afii10043',
	0x042A: 'afii10044',
	0x042B: 'afii10045',
	0x042C: 'afii10046',
	0x042D: 'afii10047',
	0x042E: 'afii10048',
	0x042F: 'afii10049',
	0x0430: 'afii10065',
	0x0431: 'afii10066',
	0x0432: 'afii10067',
	0x0433: 'afii10068',
	0x0434: 'afii10069',
	0x0435: 'afii10070',
	0x0436: 'afii10072',
	0x0437: 'afii10073',
	0x0438: 'afii10074',
	0x0439: 'afii10075',
	0x043A: 'afii10076',
	0x043B: 'afii10077',
	0x043C: 'afii10078',
	0x043D: 'afii10079',
	0x043E: 'afii10080',
	0x043F: 'afii10081',
	0x0440: 'afii10082',
	0x0441: 'afii10083',
	0x0442: 'afii10084',
	0x0443: 'afii10085',
	0x0444: 'afii10086',
	0x0445: 'afii10087',
	0x0446: 'afii10088',
	0x0447: 'afii10089',
	0x0448: 'afii10090',
	0x0449: 'afii10091',
	0x044A: 'afii10092',
	0x044B: 'afii10093',
	0x044C: 'afii10094',
	0x044D: 'afii10095',
	0x044E: 'afii10096',
	0x044F: 'afii10097',
	0x0450: 'uni0450',
	0x0451: 'afii10071',
	0x0452: 'afii10099',
	0x0453: 'afii10100',
	0x0454: 'afii10101',
	0x0455: 'afii10102',
	0x0456: 'afii10103',
	0x0457: 'afii10104',
	0x0458: 'afii10105',
	0x0459: 'afii10106',
	0x045A: 'afii10107',
	0x045B: 'afii10108',
	0x045C: 'afii10109',
	0x045D: 'uni045D',
	0x045E: 'afii10110',
	0x045F: 'afii10193',
	0x0490: 'afii10050',
	0x0491: 'afii10098',
	0x1E80: 'Wgrave',
	0x1E81: 'wgrave',
	0x1E82: 'Wacute',
	0x1E83: 'wacute',
	0x1E84: 'Wdieresis',
	0x1E85: 'wdieresis',
	0x1EF2: 'Ygrave',
	0x1EF3: 'ygrave',
	0x2013: 'endash',
	0x2014: 'emdash',
	0x2015: 'afii00208',
	0x2017: 'underscoredbl',
	0x2018: 'quoteleft',
	0x2019: 'quoteright',
	0x201A: 'quotesinglbase',
	0x201B: 'quotereversed',
	0x201C: 'quotedblleft',
	0x201D: 'quotedblright',
	0x201E: 'quotedblbase',
	0x2020: 'dagger',
	0x2021: 'daggerdbl',
	0x2022: 'bullet',
	0x2026: 'ellipsis',
	0x2030: 'perthousand',
	0x2032: 'minute',
	0x2033: 'second',
	0x2039: 'guilsinglleft',
	0x203A: 'guilsinglright',
	0x203C: 'exclamdbl',
	0x203E: 'uni203E',
	0x2044: 'fraction',
	0x207F: 'nsuperior',
	0x20A3: 'franc',
	0x20A4: 'lira',
	0x20A7: 'peseta',
	0x20AC: 'Euro',
	0x2105: 'afii61248',
	0x2113: 'afii61289',
	0x2116: 'afii61352',
	0x2122: 'trademark',
	0x2126: 'Omega',
	0x212E: 'estimated',
	0x215B: 'oneeighth',
	0x215C: 'threeeighths',
	0x215D: 'fiveeighths',
	0x215E: 'seveneighths',
	0x2190: 'arrowleft',
	0x2191: 'arrowup',
	0x2192: 'arrowright',
	0x2193: 'arrowdown',
	0x2194: 'arrowboth',
	0x2195: 'arrowupdn',
	0x21A8: 'arrowupdnbse',
	0x2202: 'partialdiff',
	0x2206: 'Delta',
	0x220F: 'product',
	0x2211: 'summation',
	0x2212: 'minus',
	0x2215: 'fraction',
	0x2219: 'periodcentered',
	0x221A: 'radical',
	0x221E: 'infinity',
	0x221F: 'orthogonal',
	0x2229: 'intersection',
	0x222B: 'integral',
	0x2248: 'approxequal',
	0x2260: 'notequal',
	0x2261: 'equivalence',
	0x2264: 'lessequal',
	0x2265: 'greaterequal',
	0x2302: 'house',
	0x2310: 'revlogicalnot',
	0x2320: 'integraltp',
	0x2321: 'integralbt',
	0x2500: 'SF100000',
	0x2502: 'SF110000',
	0x250C: 'SF010000',
	0x2510: 'SF030000',
	0x2514: 'SF020000',
	0x2518: 'SF040000',
	0x251C: 'SF080000',
	0x2524: 'SF090000',
	0x252C: 'SF060000',
	0x2534: 'SF070000',
	0x253C: 'SF050000',
	0x2550: 'SF430000',
	0x2551: 'SF240000',
	0x2552: 'SF510000',
	0x2553: 'SF520000',
	0x2554: 'SF390000',
	0x2555: 'SF220000',
	0x2556: 'SF210000',
	0x2557: 'SF250000',
	0x2558: 'SF500000',
	0x2559: 'SF490000',
	0x255A: 'SF380000',
	0x255B: 'SF280000',
	0x255C: 'SF270000',
	0x255D: 'SF260000',
	0x255E: 'SF360000',
	0x255F: 'SF370000',
	0x2560: 'SF420000',
	0x2561: 'SF190000',
	0x2562: 'SF200000',
	0x2563: 'SF230000',
	0x2564: 'SF470000',
	0x2565: 'SF480000',
	0x2566: 'SF410000',
	0x2567: 'SF450000',
	0x2568: 'SF460000',
	0x2569: 'SF400000',
	0x256A: 'SF540000',
	0x256B: 'SF530000',
	0x256C: 'SF440000',
	0x2580: 'upblock',
	0x2584: 'dnblock',
	0x2588: 'block',
	0x258C: 'lfblock',
	0x2590: 'rtblock',
	0x2591: 'ltshade',
	0x2592: 'shade',
	0x2593: 'dkshade',
	0x25A0: 'filledbox',
	0x25A1: 'H22073',
	0x25AA: 'H18543',
	0x25AB: 'H18551',
	0x25AC: 'filledrect',
	0x25B2: 'triagup',
	0x25BA: 'triagrt',
	0x25BC: 'triagdn',
	0x25C4: 'triaglf',
	0x25CA: 'lozenge',
	0x25CB: 'circle',
	0x25CF: 'H18533',
	0x25D8: 'invbullet',
	0x25D9: 'invcircle',
	0x25E6: 'openbullet',
	0x263A: 'smileface',
	0x263B: 'invsmileface',
	0x263C: 'sun',
	0x2640: 'female',
	0x2642: 'male',
	0x2660: 'spade',
	0x2663: 'club',
	0x2665: 'heart',
	0x2666: 'diamond',
	0x266A: 'musicalnote',
	0x266B: 'musicalnotedbl',
	0xFB01: 'fi',
	0xFB02: 'fl',
}

def psName(cp):
	if type(cp) is not int:
		cp = ord(cp)
	if cp < 0 or cp >= 0x110000:
		return '.notdef'
	if cp in psNameTable:
		return psNameTable[cp]
	if cp < 0x10000:
		return 'uni%04X' % cp
	return 'u%05X' % cp

def psNames(s):
	try:
		return [psName(cp) for cp in unicode(s, 'utf8')]
	except:
		return [psName(cp) for cp in s]

class AsukiLine:
	def __init__(self, index, line):
		self.index = index
		fields = line.split('#', 1)
		self.comment = fields[1].strip() if len(fields) > 1 else None
		fields = re.split(r'\s+', fields[0].strip(), 1)
		self.outputPsName = fields[0]
		self.inputPsNames = psNames(fields[1])
		self.sortKey = (-len(self.inputPsNames), fields[1])
		rule = 'sub %s by %s;' % (' '.join(self.inputPsNames), self.outputPsName)
		self.subRule = rule if self.comment is None else '%s  # %s' % (rule, self.comment)
		rule = 'sub %s space by %s;' % (' '.join(self.inputPsNames), self.outputPsName)
		self.subRuleSpace = rule if self.comment is None else '%s  # %s' % (rule, self.comment)

def readAsukiSource(filename):
	asuki = {}
	index = 0
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			if len(line) > 0 and line[0] != '#':
				a = AsukiLine(index, line)
				if a.sortKey[0] not in asuki:
					asuki[a.sortKey[0]] = {}
				asuki[a.sortKey[0]][a.sortKey[1]] = a
				index += 1
	return asuki

def writeAsukiFeatures(filename, asuki):
	with open(filename, 'w') as f:
		f.write('feature liga {\n\n')
		for sk0 in sorted(asuki.keys()):
			f.write('  # Sequences of length %d (%d + space)\n' % (1-sk0, -sk0))
			for sk1 in sorted(asuki[sk0].keys()):
				f.write('  %s\n' % asuki[sk0][sk1].subRuleSpace)
			f.write('\n')
			f.write('  # Sequences of length %d\n' % -sk0)
			for sk1 in sorted(asuki[sk0].keys()):
				f.write('  %s\n' % asuki[sk0][sk1].subRule)
			f.write('\n')
		f.write('} liga;\n')

def readSFDGlyphNames(filename):
	glyphNames = []
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			if line.startswith('StartChar: '):
				line = line.split(' ', 1)[1]
				glyphNames.append(line)
	return glyphNames

def kijeExtensionTriples(glyphNames):
	for gn in glyphNames:
		ext = '%s.kijext' % gn
		end = '%s.kijend' % gn
		if ext in glyphNames and end in glyphNames:
			yield gn, ext, end

class ExtendableLine:
	def __init__(self, index, line):
		self.index = index
		fields = line.split('#', 1)
		self.comment = fields[1].strip() if len(fields) > 1 else None
		fields = re.split(r'\s+', fields[0].strip())
		self.base = fields[0] if len(fields) > 0 and fields[0][0] != '-' else None
		self.forward = fields[1] if len(fields) > 1 and fields[1][0] != '-' else None
		self.reverse = fields[2] if len(fields) > 2 and fields[2][0] != '-' else None
		self.both = fields[3] if len(fields) > 3 and fields[3][0] != '-' else None
		self.kijeReverse = fields[4] if len(fields) > 4 and fields[4][0] != '-' else None
		self.kijeBoth = fields[5] if len(fields) > 5 and fields[5][0] != '-' else None

	def wrap(self, text, additional=None):
		if text is not None:
			if self.comment is not None:
				if additional is not None:
					return '%s  # %s, %s' % (text, self.comment, additional)
				return '%s  # %s' % (text, self.comment)
			if additional is not None:
				return '%s  # %s' % (text, additional)
		return text

def readExtendableSource(filename):
	extendable = []
	index = 0
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			if len(line) > 0 and line[0] != '#':
				e = ExtendableLine(index, line)
				extendable.append(e)
				index += 1
	return extendable

def forwardExtendablePairs(extendable):
	for e in extendable:
		if e.base is not None and e.forward is not None:
			yield e.wrap(e.base), e.wrap(e.forward)
	for e in extendable:
		if e.reverse is not None and e.both is not None:
			yield e.wrap(e.reverse, 'reverse-extended'), e.wrap(e.both, 'reverse-extended')
	for e in extendable:
		if e.kijeReverse is not None and e.kijeBoth is not None:
			yield e.wrap(e.kijeReverse, 'reverse-extended'), e.wrap(e.kijeBoth, 'reverse-extended')

def reverseExtendablePairs(extendable):
	for e in extendable:
		if e.base is not None and e.reverse is not None:
			yield e.wrap(e.base), e.wrap(e.reverse)
	for e in extendable:
		if e.forward is not None and e.both is not None:
			yield e.wrap(e.forward, 'extended'), e.wrap(e.both, 'extended')

def kijeExtendablePairs(extendable):
	for e in extendable:
		if e.base is not None and e.kijeReverse is not None:
			yield e.wrap(e.base), e.wrap(e.kijeReverse)
	for e in extendable:
		if e.forward is not None and e.kijeBoth is not None:
			yield e.wrap(e.forward, 'extended'), e.wrap(e.kijeBoth, 'extended')

def writeExtendableFeatures(filename, glyphNames, extendable):
	with open(filename, 'w') as f:
		f.write('# all glyphs that can be included in a cartouche\n')
		f.write('@spCartoucheless = [%s];\n\n' % ' '.join(gn.rsplit('.', 1)[0] for gn in glyphNames if gn.endswith('.cartouche')))
		f.write('# corresponding glyphs with cartouche extension\n')
		f.write('@spCartouche = [%s];\n\n' % ' '.join(gn for gn in glyphNames if gn.endswith('.cartouche')));
		f.write('# all glyphs that can be included in a long glyph\n')
		f.write('@spExtensionless = [%s];\n\n' % ' '.join(gn.rsplit('.', 1)[0] for gn in glyphNames if gn.endswith('.extension')))
		f.write('# corresponding glyphs with long glyph extension\n')
		f.write('@spExtension = [%s];\n\n' % ' '.join(gn for gn in glyphNames if gn.endswith('.extension')))
		f.write('# sitelen pona ideographs that can be made long on the right side\n')
		f.write('@spExtendable = [\n%s];\n\n' % ''.join('  %s\n' % a for a, e in forwardExtendablePairs(extendable)))
		f.write('# corresponding glyphs made long on the right side\n')
		f.write('@spExtended = [\n%s];\n\n' % ''.join('  %s\n' % e for a, e in forwardExtendablePairs(extendable)))
		f.write('# sitelen pona ideographs that can be made long on the left side\n')
		f.write('@spReverseExtendable = [\n%s];\n\n' % ''.join('  %s\n' % a for a, e in reverseExtendablePairs(extendable)))
		f.write('# corresponding glyphs made long on the left side\n')
		f.write('@spReverseExtended = [\n%s];\n\n' % ''.join('  %s\n' % e for a, e in reverseExtendablePairs(extendable)))
		f.write('# reverse long glyph extension for kijetesantakalu\n')
		f.write('@spKijeExtensionless = [%s];\n' % ' '.join(gn for gn, ext, end in kijeExtensionTriples(glyphNames)))
		f.write('@spKijeExtension = [%s];\n' % ' '.join(ext for gn, ext, end in kijeExtensionTriples(glyphNames)))
		f.write('@spKijeExtensionEnd = [%s];\n' % ' '.join(end for gn, ext, end in kijeExtensionTriples(glyphNames)))
		f.write('@spKijeExtendable = [\n%s];\n' % ''.join('  %s\n' % a for a, e in kijeExtendablePairs(extendable)))
		f.write('@spKijeExtended = [\n%s];\n' % ''.join('  %s\n' % e for a, e in kijeExtendablePairs(extendable)))

class JoinerLine:
	def __init__(self, index, line):
		self.index = index
		fields = line.split('#', 1)
		self.comment = fields[1].strip() if len(fields) > 1 else None
		fields = re.split(r'\s+', fields[0].strip(), 1)
		self.outputPsName = fields[0]
		self.inputSource = fields[1]
		self.inputSourceItems = [fields[1]]
		self.inputSourceDelim = None
		self.inputSourceJoiner = None
		for delim, joiner in [('-','uni200D'),('+','uni200D'),('^','uF1995'),('*','uF1996')]:
			if delim in fields[1]:
				self.inputSourceItems = fields[1].split(delim)
				self.inputSourceDelim = delim
				self.inputSourceJoiner = joiner

	def subRule(self, nimi, includeComment=True):
		joiner = ' %s ' % self.inputSourceJoiner
		names = [i[1:] if i[0] == '\\' else nimi[i] for i in self.inputSourceItems]
		rule = 'sub %s by %s;' % (joiner.join(names), self.outputPsName)
		return rule if self.comment is None or not includeComment else '%s  # %s' % (rule, self.comment)

	def sortKey(self, nimi):
		return (
			(
				-len(self.inputSourceItems),
				self.inputSourceJoiner != 'uni200D',
				None if self.comment is None else '+' in self.comment
			),
			self.subRule(nimi, False)
		)

def readJoinerSource(filename, joiners=None, nimi=None):
	if joiners is None:
		joiners = {}
	if nimi is None:
		nimi = {}
	index = 0
	with open(filename, 'r') as f:
		for line in f:
			line = line.strip()
			if len(line) > 0 and line[0] != '#':
				j = JoinerLine(index, line)
				if j.inputSourceDelim is None:
					nimi[j.inputSource] = j.outputPsName
				elif j.inputSourceDelim != '+':
					sk = j.sortKey(nimi)
					if sk[0] not in joiners:
						joiners[sk[0]] = {}
					if sk[1] not in joiners[sk[0]]:
						joiners[sk[0]][sk[1]] = j
				index += 1
	return joiners, nimi

def writeJoinerFeatures(filename, joiners, nimi):
	with open(filename, 'w') as f:
		f.write('feature liga {\n\n')
		for sk0 in sorted(joiners.keys()):
			if sk0[2]:
				pass
			elif sk0[1]:
				f.write('  # Sequences of length %d, using stacking or scaling joiners\n' % -sk0[0])
			else:
				f.write('  # Sequences of length %d, using zero width joiners\n' % -sk0[0])
			for sk1 in sorted(joiners[sk0].keys()):
				f.write('  %s\n' % joiners[sk0][sk1].subRule(nimi))
			f.write('\n')
		f.write('} liga;\n')

def main():
	asuki = readAsukiSource('asuki.txt')
	writeAsukiFeatures('asuki.fea', asuki)
	glyphNames = readSFDGlyphNames('../FairfaxHD.sfd')
	extendable = readExtendableSource('extendable.txt')
	writeExtendableFeatures('extendable.fea', glyphNames, extendable)
	joiners, nimi = readJoinerSource('asuki.txt')
	joiners, nimi = readJoinerSource('joiners.txt', joiners, nimi)
	writeJoinerFeatures('joiners.fea', joiners, nimi)

if __name__ == '__main__':
	main()
