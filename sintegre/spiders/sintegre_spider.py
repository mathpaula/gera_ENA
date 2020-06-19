#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 16:03:51 2020

@author: mazucanti
"""

from __future__ import absolute_import
import scrapy
import datetime as dt
from scrapy.loader import ItemLoader
from sintegre.items import SintegreItem




class Sintegre_Spider(scrapy.Spider):
    name = "sintegre_spider"
    
    
    def start_requests(self):                               
       urls = ['https://pops.ons.org.br/ons.pop.federation/?wa=wsignin1.0&wtrealm=https%3a%2f%2fsintegre.ons.org.br%2f_trust%2fdefault.aspx&wctx=https%3a%2f%2fsintegre.ons.org.br%2fsites%2f9%2f_layouts%2f15%2fAuthenticate.aspx%3fSource%3d%252Fsites%252F9%252F&wreply=https%3a%2f%2fsintegre.ons.org.br%2f_trust%2fdefault.aspx']
       
       for url in urls:
        #    yield scrapy.Request(url = url, callback = self.login)
            yield scrapy.Request(url = url, callback = self.usrnm)
            
    
    def usrnm(self, response):
        yield scrapy.FormRequest.from_response(response,
                                               formdata = {'username': 'vallim'},
                                               callback = self.pswrd)
    

    def pswrd(self, response):
        yield scrapy.FormRequest.from_response(response,
                                               formdata = { 'password': 'Skopos2020'},
                                               callback = self.debug_login)

    # def login(self, response):
        # yield scrapy.FormRequest.from_response(response,
        #                           formdata = {'username': 'vallim', 'password': 'Skopos2020'},
        #                           callback = self.debug_login)
     
        
    def debug_login(self, response):
        yield scrapy.FormRequest.from_response(response, 
                                               formdata = {'password': 'Skopos2020'},
                                               callback = self.after_login)
    
    
    def after_login(self, response):
        yield scrapy.FormRequest.from_response(response, 
                                               formdata = {'password': 'Skopos2020'},
                                               callback = self.parse_all)
        
        
    def parse_all(self, response):
        
        if response.status == 403 or response.status == 302:
            self.logger.error("Login failed")
            
        else:
            self.log("Login succesful")
            funcs = [self.acomph, self.carga_semanal, self.carga_mensal, self.ipdo]
            urls = ["https://sintegre.ons.org.br/sites/9/13/56//paginas/servicos/historico-de-produtos.aspx?produto=Acomph",
                    "https://sintegre.ons.org.br/sites/9/47//paginas/servicos/historico-de-produtos.aspx?produto=Carga%20por%20patamar%20-%20DECOMP",
                    "https://sintegre.ons.org.br/sites/9/47//paginas/servicos/historico-de-produtos.aspx?produto=Previs%C3%B5es%20de%20carga%20mensal%20e%20por%20patamar%20-%20NEWAVE",
                    "https://sintegre.ons.org.br/sites/7/39"]
            for i, url in enumerate(urls):
                yield scrapy.Request(url, funcs[i])
       
        
    def acomph(self, response):
        hoje = dt.date.today()
        dia = '0' + str(hoje.day) if hoje.day < 10 else str(hoje.day)
        mes = '0' + str(hoje.month) if hoje.month < 10 else str(hoje.month) 
        tupla_info = (dia, mes, hoje.year)
        url = "https://sintegre.ons.org.br/sites/9/13/56/_layouts/download.aspx?SourceUrl=/sites/9/13/56/Produtos/230/ACOMPH_%s.%s.%d.xls" % tupla_info
        loader = ItemLoader(item=SintegreItem())
        loader.add_value('file_urls', url)
        yield loader.load_item()
        
        
    def ipdo(self, response):
        hoje = dt.date.today() - dt.timedelta(days=1)
        for i in range(31):
            data = hoje - dt.timedelta(days=i)
            dia = '0' + str(data.day) if data.day < 10 else str(data.day)
            mes = '0' + str(data.month) if data.month < 10 else str(data.month) 
            tupla_info = (dia, mes, data.year)
            url = "https://sintegre.ons.org.br/sites/7/39/_layouts/download.aspx?SourceUrl=https://sintegre.ons.org.br/sites/7/39/Produtos/156/IPDO-%s-%s-%d.xlsm" % tupla_info
            loader = ItemLoader(item=SintegreItem())
            loader.add_value('file_urls', url)
            yield loader.load_item()

        
    
    def carga_semanal(self, response):
        data = dt.date.today()
        data += dt.timedelta(weeks=1)
        data -= dt.timedelta(days = (data.isoweekday()))
        data += dt.timedelta(days=5)
        mes = self.get_nome(data)
        urls = ["https://sintegre.ons.org.br/sites/9/47/_layouts/download.aspx?SourceUrl=/sites/9/47/Produtos/228/RV0_PMO_%s_carga_semanal.zip" % mes,
                "https://sintegre.ons.org.br/sites/9/47/_layouts/download.aspx?SourceUrl=/sites/9/47/Produtos/228/RV1_PMO_%s_carga_semanal.zip" % mes,
                "https://sintegre.ons.org.br/sites/9/47/_layouts/download.aspx?SourceUrl=/sites/9/47/Produtos/228/RV2_PMO_%s_carga_semanal.zip" % mes,
                "https://sintegre.ons.org.br/sites/9/47/_layouts/download.aspx?SourceUrl=/sites/9/47/Produtos/228/RV3_PMO_%s_carga_semanal.zip" % mes,
                "https://sintegre.ons.org.br/sites/9/47/_layouts/download.aspx?SourceUrl=/sites/9/47/Produtos/228/RV4_PMO_%s_carga_semanal.zip" % mes]
        loader = ItemLoader(item=SintegreItem())
        for url in urls:
            loader.add_value('file_urls', url)
            yield loader.load_item()
        
    
    def carga_mensal(self, response):
        data = dt.date.today() + dt.timedelta(weeks=4)
        mes = self.get_nome(data)
        url = "https://sintegre.ons.org.br/sites/9/47/_layouts/download.aspx?SourceUrl=/sites/9/47/Produtos/229/RV0_PMO_%s_carga_mensal.zip" % mes
        loader = ItemLoader(item=SintegreItem())
        loader.add_value('file_urls', url)
        yield loader.load_item()
    
    
    def get_nome(self, data):
        mes = data.month
        if mes == 1: return "Janeiro"
        elif mes == 2: return "Fevereiro"
        elif mes == 3: return "Março"
        elif mes == 4: return "Abril"
        elif mes == 5: return "Maio"
        elif mes == 6: return "Junho"
        elif mes == 7: return "Julho"
        elif mes == 8: return "Agosto"
        elif mes == 9: return "Setembro"
        elif mes == 10: return "Outubro"
        elif mes == 11: return "Novembro"
        elif mes == 12: return "Dezembro"
    
