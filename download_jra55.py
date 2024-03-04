#!/usr/bin/env python

"""
Python script to download selected data files from rda.ucar.edu.
Number of files selected: 237
Data volume: 157.19G
RDA dataset: ds628.0
Request index: 686214

After you save the file, don't forget to make it executable
  i.e. - "chmod 755 <name_of_script>"

Contact rdahelp@ucar.edu (RDA help desk) for further assistance.
"""

import sys, os
from urllib.request import build_opener

opener = build_opener()
dspath = 'https://request.rda.ucar.edu/dsrqst/LEE686214/'
filelist = [
  'fcst_phy2m.061_tprat.reg_tl319.1958010100_1958033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1958040100_1958063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1958070100_1958093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1958100100_1958123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1959010100_1959033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1959040100_1959063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1959070100_1959093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1959100100_1959123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1960010100_1960033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1960040100_1960063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1960070100_1960093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1960100100_1960123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1961010100_1961033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1961040100_1961063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1961070100_1961093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1961100100_1961123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1962010100_1962033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1962040100_1962063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1962070100_1962093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1962100100_1962123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1963010100_1963033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1963040100_1963063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1963070100_1963093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1963100100_1963123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1964010100_1964033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1964040100_1964063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1964070100_1964093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1964100100_1964123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1965010100_1965033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1965040100_1965063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1965070100_1965093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1965100100_1965123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1966010100_1966033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1966040100_1966063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1966070100_1966093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1966100100_1966123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1967010100_1967033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1967040100_1967063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1967070100_1967093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1967100100_1967123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1968010100_1968033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1968040100_1968063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1968070100_1968093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1968100100_1968123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1969010100_1969033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1969040100_1969063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1969070100_1969093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1969100100_1969123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1970010100_1970033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1970040100_1970063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1970070100_1970093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1970100100_1970123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1971010100_1971033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1971040100_1971063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1971070100_1971093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1971100100_1971123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1972010100_1972033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1972040100_1972063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1972070100_1972093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1972100100_1972123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1973010100_1973033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1973040100_1973063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1973070100_1973093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1973100100_1973123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1974010100_1974033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1974040100_1974063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1974070100_1974093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1974100100_1974123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1975010100_1975033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1975040100_1975063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1975070100_1975093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1975100100_1975123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1976010100_1976033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1976040100_1976063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1976070100_1976093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1976100100_1976123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1977010100_1977033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1977040100_1977063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1977070100_1977093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1977100100_1977123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1978010100_1978033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1978040100_1978063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1978070100_1978093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1978100100_1978123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1979010100_1979033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1979040100_1979063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1979070100_1979093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1979100100_1979123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1980010100_1980033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1980040100_1980063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1980070100_1980093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1980100100_1980123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1981010100_1981033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1981040100_1981063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1981070100_1981093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1981100100_1981123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1982010100_1982033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1982040100_1982063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1982070100_1982093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1982100100_1982123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1983010100_1983033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1983040100_1983063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1983070100_1983093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1983100100_1983123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1984010100_1984033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1984040100_1984063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1984070100_1984093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1984100100_1984123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1985010100_1985033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1985040100_1985063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1985070100_1985093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1985100100_1985123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1986010100_1986033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1986040100_1986063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1986070100_1986093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1986100100_1986123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1987010100_1987033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1987040100_1987063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1987070100_1987093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1987100100_1987123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1988010100_1988033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1988040100_1988063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1988070100_1988093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1988100100_1988123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1989010100_1989033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1989040100_1989063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1989070100_1989093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1989100100_1989123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1990010100_1990033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1990040100_1990063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1990070100_1990093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1990100100_1990123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1991010100_1991033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1991040100_1991063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1991070100_1991093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1991100100_1991123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1992010100_1992033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1992040100_1992063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1992070100_1992093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1992100100_1992123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1993010100_1993033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1993040100_1993063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1993070100_1993093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1993100100_1993123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1994010100_1994033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1994040100_1994063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1994070100_1994093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1994100100_1994123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1995010100_1995033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1995040100_1995063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1995070100_1995093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1995100100_1995123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1996010100_1996033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1996040100_1996063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1996070100_1996093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1996100100_1996123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1997010100_1997033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1997040100_1997063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1997070100_1997093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1997100100_1997123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1998010100_1998033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1998040100_1998063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1998070100_1998093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1998100100_1998123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1999010100_1999033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1999040100_1999063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1999070100_1999093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.1999100100_1999123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2000010100_2000033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2000040100_2000063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2000070100_2000093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2000100100_2000123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2001010100_2001033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2001040100_2001063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2001070100_2001093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2001100100_2001123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2002010100_2002033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2002040100_2002063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2002070100_2002093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2002100100_2002123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2003010100_2003033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2003040100_2003063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2003070100_2003093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2003100100_2003123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2004010100_2004033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2004040100_2004063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2004070100_2004093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2004100100_2004123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2005010100_2005033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2005040100_2005063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2005070100_2005093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2005100100_2005123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2006010100_2006033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2006040100_2006063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2006070100_2006093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2006100100_2006123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2007010100_2007033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2007040100_2007063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2007070100_2007093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2007100100_2007123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2008010100_2008033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2008040100_2008063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2008070100_2008093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2008100100_2008123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2009010100_2009033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2009040100_2009063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2009070100_2009093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2009100100_2009123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2010010100_2010033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2010040100_2010063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2010070100_2010093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2010100100_2010123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2011010100_2011033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2011040100_2011063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2011070100_2011093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2011100100_2011123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2012010100_2012033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2012040100_2012063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2012070100_2012093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2012100100_2012123121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2013010100_2013033121.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2013040100_2013063021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2013070100_2013093021.lee686214.nc',
  'fcst_phy2m.061_tprat.reg_tl319.2013100100_2013123121.lee686214.nc', 
  'TarFiles/fcst_phy2m.061_tprat.reg_tl319.2014010100_2014013121-319.2014090100_2014093021.lee686214.nc.tar',
  'TarFiles/fcst_phy2m.061_tprat.reg_tl319.2016110100_2016113021-319.2017070100_2017073121.lee686214.nc.tar',
  'TarFiles/fcst_phy2m.061_tprat.reg_tl319.2014100100_2014103121-319.2015060100_2015063021.lee686214.nc.tar',
  'TarFiles/fcst_phy2m.061_tprat.reg_tl319.2017080100_2017083121-319.2018040100_2018043021.lee686214.nc.tar',
  'TarFiles/fcst_phy2m.061_tprat.reg_tl319.2015070100_2015073121-319.2016030100_2016033121.lee686214.nc.tar',
  'TarFiles/fcst_phy2m.061_tprat.reg_tl319.2018050100_2018053121-319.2019010100_2019013121.lee686214.nc.tar',
  'TarFiles/fcst_phy2m.061_tprat.reg_tl319.2016040100_2016043021-319.2016100100_2016103121.lee686214.nc.tar',
  'TarFiles/fcst_phy2m.061_tprat.reg_tl319.2019020100_2019022821-319.2019100100_2019103121.lee686214.nc.tar',
  'TarFiles/fcst_phy2m.061_tprat.reg_tl319.2019110100_2019113021-319.2020070100_2020073121.lee686214.nc.tar',
  'TarFiles/fcst_phy2m.061_tprat.reg_tl319.2020080100_2020083121-319.2021040100_2021043021.lee686214.nc.tar',
  'TarFiles/fcst_phy2m.061_tprat.reg_tl319.2021050100_2021053121-319.2022010100_2022013121.lee686214.nc.tar',
  'TarFiles/fcst_phy2m.061_tprat.reg_tl319.2022020100_2022022821-319.2022100100_2022103121.lee686214.nc.tar',
  'TarFiles/fcst_phy2m.061_tprat.reg_tl319.2022110100_2022113021-319.2023080100_2023083121.lee686214.nc.tar'
] 

for file in filelist:
   filename = dspath + file
   ofile = os.path.basename(filename)
   sys.stdout.write("downloading " + ofile + " ... ")
   sys.stdout.flush()
   infile = opener.open(filename)
   outfile = open(ofile, "wb")
   outfile.write(infile.read())
   outfile.close()
   sys.stdout.write("done\n")
