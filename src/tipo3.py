#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from datetime import date, timedelta
from pathlib import Path


# In[2]:


def importa_vazoes():
    local = Path('../ex_csv/vazoes/vazões_para_tipo3.csv')
    vazoes = pd.read_csv(local, index_col=0)
    return vazoes


# In[3]:


def vazao_posto(posto):
    vazoes = importa_vazoes()
    return vazoes.loc[posto,:]


# In[4]:


def posto_37():
    #37 t)= 237(t) – 0,1 x [161(t) – 117(t) – 118 (t)] – 117 (t) – 118(t)
    p237 = vazao_posto(237)
    p161 = vazao_posto(161)
    p117 = vazao_posto(117)
    p118 = vazao_posto(118)
    vazao_posto_37 = p118
    vazao_posto_37 = p237 - 0.1 * (p161 - p117 - p118) - p117 - p118
    return vazao_posto_37


# In[5]:


def posto_38():
    #38(t) = 238(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t)  
    p238 = vazao_posto(238)
    p161 = vazao_posto(161)
    p117 = vazao_posto(117)
    p118 = vazao_posto(118)
    vazao_posto_38 = p117
    vazao_posto_38 = p238 - 0.1 * (p161 - p117 - p118) - p117 - p118
    return vazao_posto_38


# In[6]:


def posto_39():
    #39(t) = 239(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t) 
    p239 = vazao_posto(239)
    p161 = vazao_posto(161)
    p117 = vazao_posto(117)
    p118 = vazao_posto(118)
    vazao_posto_39 = p117
    vazao_posto_39 = p239 - 0.1 * (p161 - p117 - p118) - p117 - p118
    return vazao_posto_39


# In[7]:


def posto_40():
    #40(t) = 240(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t)
    p240 = vazao_posto(240)
    p161 = vazao_posto(161)
    p117 = vazao_posto(117)
    p118 = vazao_posto(118)
    vazao_posto_40 = p117
    vazao_posto_40 = p240 - 0.1 * (p161 - p117 - p118) - p117 - p118
    return vazao_posto_40


# In[8]:


def posto_42():
    #42(t) = 242(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t)
    p242 = vazao_posto(242)
    p161 = vazao_posto(161)
    p117 = vazao_posto(117)
    p118 = vazao_posto(118)
    vazao_posto_42 = p117
    vazao_posto_42 = p242 - 0.1 * (p161 - p117 - p118) - p117 - p118
    return vazao_posto_42


# In[9]:


def posto_43():
    #43(t) = 243(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t)
    p243 = vazao_posto(243)
    p161 = vazao_posto(161)
    p117 = vazao_posto(117)
    p118 = vazao_posto(118)
    vazao_posto_43 = p117
    vazao_posto_43 = p243 - 0.1 * (p161 - p117 - p118) - p117 - p118
    return vazao_posto_43


# In[10]:


def posto_45():
    #45(t) = 245(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t)
    p245 = vazao_posto(245)
    p161 = vazao_posto(161)
    p117 = vazao_posto(117)
    p118 = vazao_posto(118)
    vazao_posto_45 = p117
    vazao_posto_45 = p245 - 0.1 * (p161 - p117 - p118) - p117 - p118
    return vazao_posto_45


# In[11]:


def posto_46():
    #46(t) = 246(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t)  
    vazao_posto_46 = vazao_posto(246)
    p246 = vazao_posto(246)
    p161 = vazao_posto(161)
    p117 = vazao_posto(117)
    p118 = vazao_posto(118)
    vazao_posto_46 = p117
    vazao_posto_46 = p246 - 0.1 * (p161 - p117 - p118) - p117 - p118
    return vazao_posto_46


# In[12]:


def posto_66():
    #66(t) = 266(t) – 0,1 x [161(t) – 117(t) – 118(t)] – 117(t) – 118(t) 
    #66(t) = 266(t) -0,1x161(t) - 0,9x117(t) - 0,9x118(t) 
    p266 = vazao_posto(266)
    p161 = vazao_posto(161)
    p117 = vazao_posto(117)
    p118 = vazao_posto(118)
    vazao_posto_66 = p117
    vazao_posto_66 = p266 - 0.1 * p161 - 0.9 * p117 - 0.9 * p118
    return vazao_posto_66


# In[13]:


def posto_75():
    #75(t) = 76(t) + min[73(t) – 10 m³/s ;173,5 m³/s]
    vazao_posto_75 = vazao_posto(76)
    p73 = vazao_posto(73)
    p76 = vazao_posto(76)
    for i in range(30):
        vazao_posto_75.iloc[i] = p76.iloc[i] + min(p73.iloc[i] - 10, 173)
    return vazao_posto_75


# In[14]:


def posto_126():
    #Se 127(t) ≤ 430m³/s → 126(t) = máx[0; 127(t) - 90] Se 127(t) > 430m³/s → 126(t) = 340 m³/s
    vazao_posto_126 = vazao_posto(266)
    p127 = posto_127()
    for i in range(30):
        if((p127.iloc[i]) <= 430):
            vazao_posto_126.iloc[i] = max(0, p127.iloc[i] - 90)
        else:
            vazao_posto_126.iloc[i] = 340
    return vazao_posto_126


# In[15]:


def posto_127():
    #127(t) = 129(t) – 298(t) – 203(t) + 304(t)
    vazao_posto_127 = vazao_posto(129) - posto_298() - vazao_posto(203) + posto_304()
    return vazao_posto_127


# In[16]:


def posto_131():
    #131(t) = min[316(t) ; 144 m³/s]
    vazao_posto_131 = posto_316()
    p316 = posto_316()
    for i in range(30):
        vazao_posto_131.iloc[i] = min(p316.iloc[i], 144)
    return vazao_posto_131


# In[17]:


def posto_132():
    #132 (t) = 202 (t) + mín [201 (t);25]
    vazao_posto_132 = vazao_posto(202)
    p201 = vazao_posto(201)
    p202 = vazao_posto(202)
    for i in range(30):
        vazao_posto_132.iloc[i] = p202.iloc[i] + min(p201.iloc[i], 25)
    return vazao_posto_132


# In[18]:


def posto_176():
    vazao_posto_176 = vazao_posto(172)
    return vazao_posto_176


# In[19]:


def posto_285():
    #285(t) = 0,985*287(t)
    vazao_posto_285 = 0.985 * vazao_posto(287)
    return vazao_posto_285


# In[20]:


def posto_292():
    #Se 288(t) ≤ 1600m³/s     →   292(t) = 0
    #Se 288(t) > 1600m³/s     →   
        #Se  288(t) ≤ (X+13900) m³/s    →    292(t) = 288(t) - X  m³/s   
        #Se 288(t) > (X+13900) m³/s → 292(t) = 13900  m³/s
    vazao_base = 0
    vazao_posto_292 = vazao_posto(288)
    p288 = vazao_posto(288)
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
        
        if(p288.iloc[i] <= vazao_base):
            vazao_posto_292.iloc[i] = 0
        else:
            if(p288.iloc[i] <= vazao_base + 13900): vazao_posto_292.iloc[i] = p288.iloc[i] - vazao_base
            else: vazao_posto_292.iloc[i] = 13900
    return vazao_posto_292


# In[21]:


def posto_298():
    #Se 125(t) ≤ 190m³/s → 298(t) = [125(t) x 119]/190 
    #Se 190 < 125(t) ≤  209 → 298(t) = 119 m³/s     
    #Se 209 < 125(t) ≤  250 → 298(t) = 125(t) - 90 m³/s
    #Se 125(t) > 250 → 298(t) = 160 m³/s 
    p125 = vazao_posto(125)
    vazao_posto_298 = vazao_posto(76)
    for i in range(30):
        if(p125.iloc[i] <= 190): vazao_posto_298.iloc[i] = (p125.iloc[i] * 119) / 190
        elif(p125.iloc[i] <= 209): vazao_posto_298.iloc[i] = 119
        elif(p125.iloc[i] <= 250): vazao_posto_298.iloc[i] = p125.iloc[i] - 90
        elif(p125.iloc[i] > 250): vazao_posto_298.iloc[i] = 160
    return vazao_posto_298


# In[22]:


def posto_299():
    #299(t) = 130(t) – 298(t) + 304(t)
    vazao_posto_299 = vazao_posto(130) - posto_298() + posto_304()
    return vazao_posto_299


# In[23]:


def posto_303():
    #303 (t) = 132 (t) + mín [316 (t)- 131(t);51]
    vazao_posto_303 = posto_132()
    p131 = posto_131()
    p132 = posto_132()
    p316 = posto_316()
    for i in range(30):
        vazao_posto_303.iloc[i] = p132.iloc[i] + min(p316.iloc[i] - p131.iloc[i], 51)
    return vazao_posto_303


# In[24]:


def posto_304():
    #304(t) = 315(t) - 316(t)
    vazao_posto_304 = posto_315() - posto_316()
    return vazao_posto_304


# In[25]:


def posto_306():
    #306 (t) = 303(t)+131(t)
    vazao_posto_306 = posto_303() + posto_131()
    return vazao_posto_306


# In[26]:


def posto_315():
    #315(t) = 203(t) – 201(t) + 317(t) + 298(t)
    vazao_posto_315 = vazao_posto(203) - vazao_posto(201) + posto_317() + posto_298()
    return vazao_posto_315


# In[27]:


def posto_316():
    #316(t) = min[315(t); 190 m³/s]
    vazao_posto_316 = posto_315()
    p315 = posto_315()
    for i in range(30):
        vazao_posto_316.iloc[i] = min(p315.iloc[i], 190)
    return vazao_posto_316


# In[28]:


def posto_317():
    #317(t) = max[ 0; (201(t) – 25 m³/s]
    vazao_posto_317 = vazao_posto(201)
    p201 = vazao_posto(201)
    for i in range(30):
        vazao_posto_317.iloc[i] = max(0, p201.iloc[i] - 25)
    return vazao_posto_317


# In[29]:


def posto_318():
    #318(t) = 116(t) + 117(t) + 118(t) + 0,1*[161(t) - 117(t) - 118(t)]
    p116 = vazao_posto(116)
    p117 = vazao_posto(117)
    p118 = vazao_posto(118)
    p161 = vazao_posto(161)
    vazao_posto_318 = p116
    vazao_posto_318 = p116 + p117 + p118 + 0.1 * (p161 - p117 - p118)
    return vazao_posto_318

