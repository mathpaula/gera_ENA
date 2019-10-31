#!/usr/bin/env python
# coding: utf-8

# In[153]:


import pandas as pd
import numpy as np
from datetime import date, timedelta
from pathlib import Path


# In[154]:


def importa_acomph():
    acomph = pd.read_csv('../../ex_csv/acomph.csv', index_col=0)
    return acomph


# In[156]:


def vazao_posto(posto):
    acomph = importa_acomph()
    return acomph.loc[posto,:]


# In[157]:


def posto_37():
    #37 t)= 237(t) – 0,1 x [161(t) – 117(t) – 118 (t)] – 117 (t) – 118(t)
    vazao_posto_37 = vazao_posto(237) - 0.1 * (vazao_posto(161) - vazao_posto(117) - vazao_posto(118)) - vazao_posto(117) - vazao_posto(118)
    return vazao_posto_37


# In[158]:


def posto_38():
    #38(t) = 238(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t)  
    vazao_posto_38 = vazao_posto(238) - 0.1 * (vazao_posto(161) - vazao_posto(117) - vazao_posto(118)) - vazao_posto(117) - vazao_posto(118)
    return vazao_posto_38


# In[159]:


def posto_39():
    #39(t) = 239(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t) 
    vazao_posto_39 = vazao_posto(239) - 0.1 * (vazao_posto(161) - vazao_posto(117) - vazao_posto(118)) - vazao_posto(117) - vazao_posto(118)
    return vazao_posto_39


# In[160]:


def posto_40():
    #40(t) = 240(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t)
    vazao_posto_40 = vazao_posto(240) - 0.1 * (vazao_posto(161) - vazao_posto(117) - vazao_posto(118)) - vazao_posto(117) - vazao_posto(118)
    return vazao_posto_40


# In[161]:


def posto_42():
    #42(t) = 242(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t)
    vazao_posto_42 = vazao_posto(242) - 0.1 * (vazao_posto(161) - vazao_posto(117) - vazao_posto(118)) - vazao_posto(117) - vazao_posto(118)
    return vazao_posto_42


# In[162]:


def posto_43():
    #43(t) = 243(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t)
    vazao_posto_43 = vazao_posto(243) - 0.1 * (vazao_posto(161) - vazao_posto(117) - vazao_posto(118)) - vazao_posto(117) - vazao_posto(118)
    return vazao_posto_43


# In[163]:


def posto_45():
    #45(t) = 245(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t)
    vazao_posto_45 = vazao_posto(245) - 0.1 * (vazao_posto(161) - vazao_posto(117) - vazao_posto(118)) - vazao_posto(117) - vazao_posto(118)
    return vazao_posto_45


# In[164]:


def posto_46():
    #46(t) = 246(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t)   
    vazao_posto_46 = vazao_posto(246) - 0.1 * (vazao_posto(161) - vazao_posto(117) - vazao_posto(118)) - vazao_posto(117) - vazao_posto(118)
    return vazao_posto_46


# In[165]:


def posto_66():
    #66(t) = 266(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t) 
    #66(t) = 266(t) -0,1x161(t) - 0,9x117(t) - 0,9x118(t) 
    vazao_posto_66 = vazao_posto(266) - 0.1 * vazao_posto(161) - 0.9 * vazao_posto(117) - 0.9 * vazao_posto(118)
    return vazao_posto_66


# In[166]:


def posto_75():
    #75(t) = 76(t) + min[73(t) – 10 m³/s ;173,5 m³/s]
    vazao_posto_75 = vazao_posto(76)
    for i in range(30):
        vazao_posto_75.iloc[i] = vazao_posto(76).iloc[i] + min(vazao_posto(73).iloc[i] - 10, 173)
    return vazao_posto_75


# In[167]:


def posto_126():
    #Se 127(t) ≤ 430m³/s → 126(t) = máx[0; 127(t) - 90] Se 127(t) > 430m³/s → 126(t) = 340 m³/s
    vazao_posto_126 = vazao_posto(266)
    for i in range(30):
        if(posto_127().iloc[i] <= 430):
            vazao_posto_126.iloc[i] = max(0, posto_127().iloc[i] - 90)
        else:
            vazao_posto_126.iloc[i] = 340
    return vazao_posto_126


# In[168]:


def posto_127():
    #127(t) = 129(t) – 298(t) – 203(t) + 304(t)
    vazao_posto_127 = vazao_posto(129) - vazao_posto(298) - vazao_posto(203) + vazao_posto(304)
    return vazao_posto_127


# In[169]:


def posto_131():
    #131(t) = min[316(t) ; 144 m³/s]
    vazao_posto_131 = posto_316()
    for i in range(30):
        vazao_posto_131.iloc[i] = min(posto_316().iloc[i], 144)
    return vazao_posto_131


# In[170]:


def posto_132():
    #132 (t) = 202 (t) + mín [201 (t);25]
    for i in range(30):
        vazao_posto_132.iloc[i] = vazao_posto(202).iloc[i] + min(vazao_posto(201).iloc[i], 25)
    return vazao_posto_132


# In[171]:


def posto_176():
    vazao_posto_176 = vazao_posto(172)
    return


# In[172]:


def posto_285():
    #285(t) = 0,985*287(t)
    vazao_posto_285 = 0.985 * vazao_posto(287)
    return vazao_posto_285


# In[173]:


def posto_292():
    #Se 288(t) ≤ 1600m³/s     →   292(t) = 0
    #Se 288(t) > 1600m³/s     →   
        #Se  288(t) ≤ (X+13900) m³/s    →    292(t) = 288(t) - X  m³/s   
        #Se 288(t) > (X+13900) m³/s → 292(t) = 13900  m³/s
    vazao_base = 0
    vazao_posto_292 = vazao_posto(288)
    for i in range(30):
        mes = (date.today()-timedelta(days = 30-i)).month
        if (mes == 1): vazao_base = 1100
        elif (mes == 2): vazao_base = 1600
        elif (mes == 3): vazao_base = 4000
        elif (mes == 4): vazao_base = 8000
        elif (mes == 5): vazao_base = 4000
        elif (mes == 6): vazao_base = 2000
        elif (mes == 7): vazao_base = 1200
        elif (mes == 8): vazao_base = 900
        elif (mes == 9): vazao_base = 750
        elif (mes == 10): vazao_base = 700
        elif (mes == 11): vazao_base = 800
        elif (mes == 12): vazao_base = 900
        
        if(vazao_posto(288).iloc[i] <= vazao_base):
            vazao_posto_292.iloc[i] = 0
        else:
            if(vazao_posto(288) <= vazao_base + 13900): vazao_posto_292.iloc[i] = vazao_posto(288).iloc[i] - vazao_base
            else: vazao_posto_292.iloc[i] = 13900
    return vazao_posto_292


# In[174]:


def posto_298():
    #Se 125(t) ≤ 190m³/s → 298(t) = [125(t) x 119]/190 
    #Se 190 < 125(t) ≤  209 → 298(t) = 119 m³/s     
    #Se 209 < 125(t) ≤  250 → 298(t) = 125(t) - 90 m³/s
    #Se 125(t) > 250 → 298(t) = 160 m³/s 
    vazao_posto_298 = vazao_posto(125)
    for i in range(30):
        if(vazao_posto(125).iloc[i] <= 190): vazao_posto_298.iloc[i] = (vazao_posto(125).iloc[i] * 119) / 190
        elif(vazao_posto(125).iloc[i] <= 209): vazao_posto_298.iloc[i] = 119
        elif(vazao_posto(125).iloc[i] <= 250): vazao_posto_298.iloc[i] = vazao_posto(125).iloc[i] - 90
        elif(vazao_posto(125).iloc[i] > 250): vazao_posto_298.iloc[i] = 160
    return vazao_posto_298


# In[175]:


def posto_299():
    #299(t) = 130(t) – 298(t) + 304(t)
    vazao_posto_299 = vazao_posto(130) - posto_298() + posto_304()
    return vazao_posto_299


# In[176]:


def posto_303():
    #303 (t) = 132 (t) + mín [316 (t)- 131(t);51]
    vazao_posto_303 = posto_132()
    for i in range(30):
        vazao_posto_303.iloc[i] = posto_132().iloc[i] + min(posto_316().iloc[i] - posto_131.iloc[i], 51)
    return vazao_posto_303


# In[177]:


def posto_304():
    #304(t) = 315(t) - 316(t)
    vazao_posto_304 = posto_315() - posto_316()
    return vazao_posto_304


# In[178]:


def posto_306():
    #306 (t) = 303(t)+131(t)
    vazao_posto_306 = posto_303() + posto_131()
    return vazao_posto_306


# In[179]:


def posto_315():
    #315(t) = 203(t) – 201(t) + 317(t) + 298(t)
    vazao_posto_315 = vazao_posto(203) - vazao_posto(201) + posto_317() + posto_298()
    return vazao_posto_315


# In[180]:


def posto_316():
    #316(t) = min[315(t); 190 m³/s]
    vazao_posto_316 = posto_315()
    for i in range(30):
        vazao_posto_316.iloc[i] = min(posto_315.iloc[i], 190)
    return vazao_posto_316


# In[181]:


def posto_317():
    #317(t) = max[ 0; (201(t) – 25 m³/s]
    vazao_posto_317 = vazao_posto(201)
    for i in range(30):
        vazao_posto_317 = max(0, vazao_posto(201) - 25)
    return vazao_posto_317


# In[182]:


def posto_318():
    #318(t) = 116(t) + 117(t) + 118(t) + 0,1*[161(t) - 117(t) - 118(t)]
    vazao_posto_318 = vazao_posto(116) + vazao_posto(117) + vazao_posto(118) + 0.1 * (vazao_posto(161) - vazao_posto(117) - vazao_posto(118))
    return vazao_posto_318


# In[ ]:




