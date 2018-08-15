#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from multiprocessing import Pool
import re
import psycopg2
import time

urls = [
    "https://www.rivalo.com/pt/apostas/futebol-clubes-internacionais-taca-dos-campeoes-internacionais/gcjabjdab/",
    "https://www.rivalo.com/pt/apostas/futebol-clubes-internacionais-supertaca-europeia/ggiadab/",
    "https://www.rivalo.com/pt/apostas/futebol-clubes-internacionais-copa-libertadores-fase-final/gdajdab/",
    "https://www.rivalo.com/pt/apostas/futebol-clubes-internacionais-copa-sul-americana/ggijdab/",
    "https://www.rivalo.com/pt/apostas/futebol-clubes-internacionais-concacaf-league/ggcbeedab/",
    "https://www.rivalo.com/pt/apostas/futebol-clubes-internacionais-amigaveis-de-clubes/gigdab/",
    "https://www.rivalo.com/pt/apostas/futebol-clubes-internacionais-apostas-em-partidas-da-temporada/ghhcaba/",
    "https://www.rivalo.com/pt/apostas/futebol-brasil-brasileirao-serie-a/giddab/",
    "https://www.rivalo.com/pt/apostas/futebol-brasil-brasileirao-serie-b/gbeejdab/",
    "https://www.rivalo.com/pt/apostas/futebol-brasil-copa-paulista-group-2/ggbafedab/",
    "https://www.rivalo.com/pt/apostas/futebol-brasil-brasileirao-serie-c/gchcbddab/",
    "https://www.rivalo.com/pt/apostas/futebol-brasil-brasileirao-serie-c-grupo-b/gchcbedab/",
    "https://www.rivalo.com/pt/apostas/futebol-brasil-campeonato-brasileiro-sub-20-grupo-f/gfcfjedab/",
    "https://www.rivalo.com/pt/apostas/futebol-brasil-brasileiro-serie-a-apostas-em-partidas-da-temporada/gbggjeba/",
    "https://www.rivalo.com/pt/apostas/futebol-brasil-brasileiro-u23/gbijdeba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-dos-campeoes-qualification/gibagba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-dos-campeoes-apostas-em-partidas-da-temporada/ggidgba/",
    "https://www.rivalo.com/pt/apostas/futebol-mexico-primeira-divisao-apertura/gcidab/",
    "https://www.rivalo.com/pt/apostas/futebol-mexico-liga-de-promocao-apertura/gbjbidab/",
    "https://www.rivalo.com/pt/apostas/futebol-inglaterra-primeira-liga/gbdab/",
    "https://www.rivalo.com/pt/apostas/futebol-inglaterra-championship/gcdab/",
    "https://www.rivalo.com/pt/apostas/futebol-inglaterra-league-one/gddab/",
    "https://www.rivalo.com/pt/apostas/futebol-inglaterra-league-two/giedab/",
    "https://www.rivalo.com/pt/apostas/futebol-inglaterra-national-league/ghcdab/",
    "https://www.rivalo.com/pt/apostas/futebol-inglaterra-taca-da-liga/gbhdab/",
    "https://www.rivalo.com/pt/apostas/futebol-russia-primeira-liga/gfddab/",
    "https://www.rivalo.com/pt/apostas/futebol-russia-liga-nacional-de-futebol/gbbbgdab/",
    "https://www.rivalo.com/pt/apostas/futebol-russia-pfl-centro/gcbcaidab/",
    "https://www.rivalo.com/pt/apostas/futebol-russia-pfl-oeste/gdbgcdab/",
    "https://www.rivalo.com/pt/apostas/futebol-russia-liga-junior/gbcgbadab/",
    "https://www.rivalo.com/pt/apostas/futebol-russia-premier-league-feminino/ggdfddab/",
    "https://www.rivalo.com/pt/apostas/futebol-alemanha-supertaca-da-ace-amja/ggefgdab/",
    "https://www.rivalo.com/pt/apostas/futebol-alemanha-3-liga/gideddab/",
    "https://www.rivalo.com/pt/apostas/futebol-alemanha-bundesliga-2-divisao/gebdab/",
    "https://www.rivalo.com/pt/apostas/futebol-alemanha-bundesliga/gecdab/",
    "https://www.rivalo.com/pt/apostas/futebol-alemanha-dfb-pokal/geddab/",
    "https://www.rivalo.com/pt/apostas/futebol-alemanha-bayern-especiais/gbeehaba/",
    "https://www.rivalo.com/pt/apostas/futebol-juniores-internacionais-taca-do-mundo-feminina-sub-20-grupo-c/gbdbahdab/",
    "https://www.rivalo.com/pt/apostas/futebol-juniores-internacionais-taca-do-mundo-feminina-sub-20-grupo-d/gbdbaidab/",
    "https://www.rivalo.com/pt/apostas/futebol-colombia-primera-a-clausura/gbjcdgdab/",
    "https://www.rivalo.com/pt/apostas/futebol-colombia-primeira-b-abertura/gfhhgjdab/",
    "https://www.rivalo.com/pt/apostas/futebol-australia-npl-new-south-wales/gdbdaadab/",
    "https://www.rivalo.com/pt/apostas/futebol-australia-primeira-divisao-da-liga-estatal-oeste/gdbejjdab/",
    "https://www.rivalo.com/pt/apostas/futebol-australia-primeira-liga-nacional-de-queensland/gdbciddab/",
    "https://www.rivalo.com/pt/apostas/futebol-australia-npl-tasmania/gdbfaidab/",
    "https://www.rivalo.com/pt/apostas/futebol-australia-primeira-liga-victoria/gbacbgdab/",
    "https://www.rivalo.com/pt/apostas/futebol-australia-liga-hyundai-a-apostas-em-partidas-da-temporada/gbciecba/",
    "https://www.rivalo.com/pt/apostas/futebol-dinamarca-superliga/gbcdab/",
    "https://www.rivalo.com/pt/apostas/futebol-dinamarca-1-divisao/gbddab/",
    "https://www.rivalo.com/pt/apostas/futebol-dinamarca-2-divisao-grupo-1/gefbgidab/",
    "https://www.rivalo.com/pt/apostas/futebol-dinamarca-2-divisao-grupo-2/gefbgjdab/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-europa-qualification/gibajba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-europa-apostas-em-partidas-da-temporada/ggidfba/",
    "https://www.rivalo.com/pt/apostas/futebol-peru-primeira-divisao-apertura/gdeeghdab/",
    "https://www.rivalo.com/pt/apostas/futebol-alemanha-amadores-liga-regional-bavaria/gcbcjjdab/",
    "https://www.rivalo.com/pt/apostas/futebol-alemanha-amadores-regionalliga-norte/geedab/",
    "https://www.rivalo.com/pt/apostas/futebol-alemanha-amadores-regionalliga-sudoeste/gcbdaadab/",
    "https://www.rivalo.com/pt/apostas/futebol-alemanha-amadores-regionalliga-nordeste/gcbdabdab/",
    "https://www.rivalo.com/pt/apostas/futebol-alemanha-amadores-liga-regional-oeste/gidgedab/",
    "https://www.rivalo.com/pt/apostas/futebol-suecia-allsvenskan/gcedab/",
    "https://www.rivalo.com/pt/apostas/futebol-suecia-superettan/gchdab/",
    "https://www.rivalo.com/pt/apostas/futebol-bolivia-liga-profissional-boliviana-encerramento/gbhbeadab/",
    "https://www.rivalo.com/pt/apostas/futebol-bolivia-liga-profesional-boliviano-clausura/gbaaaaaaabdhfa/",
    "https://www.rivalo.com/pt/apostas/futebol-venezuela-copa-venezuela/ghabbba/",
    "https://www.rivalo.com/pt/apostas/futebol-eua-united-soccer-league/gbfhgddab/",
    "https://www.rivalo.com/pt/apostas/futebol-eua-major-league-soccer/gbidab/",
    "https://www.rivalo.com/pt/apostas/futebol-franca-ligue-1/gedab/",
    "https://www.rivalo.com/pt/apostas/futebol-franca-ligue-2/gbjdab/",
    "https://www.rivalo.com/pt/apostas/futebol-franca-nacional/gjfadab/",
    "https://www.rivalo.com/pt/apostas/futebol-austria-bundesliga/gcjdab/",
    "https://www.rivalo.com/pt/apostas/futebol-austria-primeira-liga/gdadab/",
    "https://www.rivalo.com/pt/apostas/futebol-austria-bundesliga/gbjbbdba/",
    "https://www.rivalo.com/pt/apostas/futebol-espanha-supertaca-de-espanha/gcdafdab/",
    "https://www.rivalo.com/pt/apostas/futebol-espanha-la-liga/gdgdab/",
    "https://www.rivalo.com/pt/apostas/futebol-turquia-super-liga/ggcdab/",
    "https://www.rivalo.com/pt/apostas/futebol-turquia-tff-1-liga/gbabdab/",
    "https://www.rivalo.com/pt/apostas/futebol-italia-taca-de-italia/gdfdab/",
    "https://www.rivalo.com/pt/apostas/futebol-portugal-primeira-liga/gfcdab/",
    "https://www.rivalo.com/pt/apostas/futebol-portugal-segunda-liga/gciadab/",
    "https://www.rivalo.com/pt/apostas/futebol-suica-super-liga/gbagadab/",
    "https://www.rivalo.com/pt/apostas/futebol-suica-liga-challenge/gbagbdab/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-a-grupo-1/gbjahhba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-a-grupo-2/gbjahiba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-a-grupo-3/gbjahjba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-a-grupo-4/gbjaiaba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-resultados-finais-league-a/gbjahbba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-b-grupo-1/gbjaibba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-b-grupo-2/gbjaicba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-b-grupo-3/gbjaidba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-b-grupo-4/gbjaieba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-resultados-finais-league-b/gbjajdba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-c-grupo-1/gbjaifba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-c-grupo-2/gbjaigba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-c-grupo-3/gbjaihba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-c-grupo-4/gbjaiiba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-resultados-finais-league-c/gbjajeba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-d-grupo-1/gbjaijba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-d-grupo-2/gbjajaba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-d-grupo-3/gbjajbba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-liga-das-nacoes-da-uefa-d-grupo-4/gbjajcba/",
    "https://www.rivalo.com/pt/apostas/futebol-liga-das-nacoes-da-uefa-resultados-finais-league-d/gbjajfba/",
    "https://www.rivalo.com/pt/apostas/futebol-holanda-eredivisie/gdjdab/",
    "https://www.rivalo.com/pt/apostas/futebol-belgica-first-division-a/gdidab/",
    "https://www.rivalo.com/pt/apostas/futebol-belgica-primeira-divisao-b-primeira-etapa/gfedjfdab/",
    "https://www.rivalo.com/pt/apostas/futebol-noruega-eliteserien/gfdab/",
    "https://www.rivalo.com/pt/apostas/futebol-noruega-1-divisao/ggdab/",
    "https://www.rivalo.com/pt/apostas/futebol-escocia-premiership-da-escocia/gfedab/",
    "https://www.rivalo.com/pt/apostas/futebol-escocia-championship-da-escocia/gffdab/",
    "https://www.rivalo.com/pt/apostas/futebol-escocia-segunda-divisao/gfgdab/",
    "https://www.rivalo.com/pt/apostas/futebol-escocia-terceira-divisao/gfhdab/",
    "https://www.rivalo.com/pt/apostas/futebol-argentina-primeira-divisao-torneio-inicial/ggidab/",
    "https://www.rivalo.com/pt/apostas/futebol-croacia-1-hnl/geidab/",
    "https://www.rivalo.com/pt/apostas/futebol-finlandia-veikkausliiga/gdbdab/",
    "https://www.rivalo.com/pt/apostas/futebol-finlandia-ykkonen/gfchdab/",
    "https://www.rivalo.com/pt/apostas/futebol-finlandia-kakkonen-group-a/gbcaedab/",
    "https://www.rivalo.com/pt/apostas/futebol-rep-checa-primeira-liga-checa/gejdab/",
    "https://www.rivalo.com/pt/apostas/futebol-rep-checa-fnl/gieddab/",
    "https://www.rivalo.com/pt/apostas/futebol-eslovenia-liga-prva/gjedab/",
    "https://www.rivalo.com/pt/apostas/futebol-polonia-ekstraklasa/ggedab/",
    "https://www.rivalo.com/pt/apostas/futebol-polonia-i-liga/gbechdab/",
    "https://www.rivalo.com/pt/apostas/futebol-romenia-liga-i/gcbjdab/",
    "https://www.rivalo.com/pt/apostas/futebol-romenia-liga-2/gfeihidab/",
    "https://www.rivalo.com/pt/apostas/futebol-bulgaria-primeira-liga-prof/gcdcdab/",
    "https://www.rivalo.com/pt/apostas/futebol-eslovaquia-superliga/gjcdab/",
    "https://www.rivalo.com/pt/apostas/futebol-eslovaquia-2-liga/gbdhfdab/",
    "https://www.rivalo.com/pt/apostas/futebol-ucrania-primeira-liga/gdiedab/",
    "https://www.rivalo.com/pt/apostas/futebol-hungria-nb-i/gfadab/",
    "https://www.rivalo.com/pt/apostas/futebol-estonia-esilliga/giiejdab/",
    "https://www.rivalo.com/pt/apostas/futebol-islandia-primeira-divisao-da-islandia/gbacdab/",
    "https://www.rivalo.com/pt/apostas/futebol-islandia-segunda-divisao-da-islandia/gficdab/",
    "https://www.rivalo.com/pt/apostas/futebol-islandia-3-deild/gbdhbfdab/",
    "https://www.rivalo.com/pt/apostas/futebol-islandia-landsbankadeild-kvenna/ggcbddab/",
    "https://www.rivalo.com/pt/apostas/futebol-islandia-4-deild-group-a/ghhhaba/",
    "https://www.rivalo.com/pt/apostas/futebol-islandia-4-deild-group-c/ghhhjba/",
    "https://www.rivalo.com/pt/apostas/futebol-islandia-u19/gddagba/",
    "https://www.rivalo.com/pt/apostas/futebol-irlanda-do-norte-primeira-liga/giiddab/",
    "https://www.rivalo.com/pt/apostas/futebol-israel-league-cup-national-group-a/gfedfbdab/",
    "https://www.rivalo.com/pt/apostas/futebol-israel-league-cup-national-group-b/gfedfcdab/",
    "https://www.rivalo.com/pt/apostas/futebol-israel-league-cup-national-group-c/gfedfddab/",
    "https://www.rivalo.com/pt/apostas/futebol-israel-league-cup-national-group-d/gfedfedab/",
    "https://www.rivalo.com/pt/apostas/futebol-pais-de-gales-liga-premier-galesa/gjaedab/",
    "https://www.rivalo.com/pt/apostas/futebol-georgia-liga-nacional-2/gegbeadab/",
    "https://www.rivalo.com/pt/apostas/futebol-costa-rica-primera-division-campeonato-invierno/gehbddab/",
    "https://www.rivalo.com/pt/apostas/futebol-chile-primeira-divisao/gghciadab/",
    "https://www.rivalo.com/pt/apostas/futebol-chile-primera-b-torneo-transicion/ggbehgdab/",
    "https://www.rivalo.com/pt/apostas/futebol-equador-serie-a-segunda-etapa/gbdihdab/",
    "https://www.rivalo.com/pt/apostas/futebol-honduras-liga-nacional-abertura/gbhadedab/",
    "https://www.rivalo.com/pt/apostas/futebol-paraguai-primeira-divisao-encerramento/gbghfcdab/",
    "https://www.rivalo.com/pt/apostas/futebol-ruanda-taca-da-paz/geedhcdab/",
    "https://www.rivalo.com/pt/apostas/futebol-japao-j-league/gicdab/",
    "https://www.rivalo.com/pt/apostas/futebol-japao-j-league-2/gdadedab/",
    "https://www.rivalo.com/pt/apostas/futebol-china-super-liga-chinesa/ggfcdab/",
    "https://www.rivalo.com/pt/apostas/futebol-china-liga-chinesa/gdfiddab/",
    "https://www.rivalo.com/pt/apostas/futebol-indonesia-indonesia-soccer-championship/gebbddab/",
    "https://www.rivalo.com/pt/apostas/futebol-coreia-do-sul-classico-liga-k/gdciedab/",
    "https://www.rivalo.com/pt/apostas/futebol-coreia-do-sul-classico-liga-k-2/ggcdadab/",
    "https://www.rivalo.com/pt/apostas/futebol-irao-liga-pro/gdgcfdab/",
    "https://www.rivalo.com/pt/apostas/futebol-catar-liga-de-estrelas/geafbdab/",
    "https://www.rivalo.com/pt/apostas/futebol-argelia-liga-da-argelia/gdgfhdab/",
    "https://www.rivalo.com/pt/apostas/futebol-africa-do-sul-primeira-liga/gdidadab/",
    "https://www.rivalo.com/pt/apostas/futebol-africa-do-sul-mtn-8/gbbcdedab/",
    "https://www.rivalo.com/pt/apostas/futebol-egito-liga-principal/gdigbcdab/",
    "https://www.rivalo.com/pt/apostas/futebol-inglaterra-amadores-premier-league-2-division-1/gfeiejdab/",
    "https://www.rivalo.com/pt/apostas/futebol-inglaterra-amadores-liga-premier-divisao-2/gfeifadab/",
    "https://www.rivalo.com/pt/apostas/futebol-inglaterra-amadores-national-league-norte/gcdeidab/",
    "https://www.rivalo.com/pt/apostas/futebol-inglaterra-amadores-national-league-sul/gcdejdab/",
    "https://www.rivalo.com/pt/apostas/futebol-suecia-amadores-sub-19/ghdagadab/",
    "https://www.rivalo.com/pt/apostas/futebol-suecia-amateur-3-division-nordvastra-gotaland/gbbfbdab/",
    "https://www.rivalo.com/pt/apostas/futebol-suecia-amateur-3-division-vastra-svealand/gcbcjba/",
    "https://www.rivalo.com/pt/apostas/futebol-noruega-amador-u19-interkrets/ghijbdab/",
    "https://www.rivalo.com/pt/apostas/futebol-finnland-amateure-3-division-helsinki-uusimaa-1/giahhdab/",
    "https://www.rivalo.com/pt/apostas/futebol-finnland-amateure-3-division-helsinki-uusimaa-2/giahidab/",
    "https://www.rivalo.com/pt/apostas/futebol-finnland-amateure-3-division-helsinki-uusimaa-3/giahjdab/",
    "https://www.rivalo.com/pt/apostas/basquetebol/gcbab/l/",
    "https://www.rivalo.com/pt/apostas/basquetebol-estados-unidos-america-wnba/gfjbdab/",
    "https://www.rivalo.com/pt/apostas/basquetebol-alemanha-apostas-em-partidas-da-temporada/ghgjgba/",
    "https://www.rivalo.com/pt/apostas/basquetebol-internacional-campeonato-europeu-sub-18-div-a-feminino-playoffs/ggdjgdab/",
    "https://www.rivalo.com/pt/apostas/basquetebol-internacional-campeonato-europeu-sub-18-div-a-feminino-qualificacao-para-jogos-de-posicao/gcjefidab/",
    "https://www.rivalo.com/pt/apostas/basquetebol-brasil-paulista-league/gbbjhgba/",
    "https://www.rivalo.com/pt/apostas/basquetebol-ilhas-filipinas-mpbl/ggidcddab/",
    "https://www.rivalo.com/pt/apostas/basquetebol-puerto-rico-superior-nacional/gfgifba/",
    "https://www.rivalo.com/pt/apostas/basquetebol-uruguai-el-metro/gbjeghba/",
    "https://www.rivalo.com/pt/apostas/tenis/gfbab/h/",
    "https://www.rivalo.com/pt/apostas/tenis/gfbab/l/",
    "https://www.rivalo.com/pt/apostas/tenis-atp-atp-toronto-canada-men-singles/ggfiicdab/",
    "https://www.rivalo.com/pt/apostas/tenis-atp-atp-toronto-canada-men-double/ggfiiddab/",
    "https://www.rivalo.com/pt/apostas/tenis-atp-grand-slam/gdhghba/",
    "https://www.rivalo.com/pt/apostas/tenis-atp-atp-torneio-vencedor-final/gbbfhbba/",
    "https://www.rivalo.com/pt/apostas/tenis-wta-wta-montreal-canada-women-singles/gggbejdab/",
    "https://www.rivalo.com/pt/apostas/tenis-wta-wta-montreal-canada-women-double/gggbfadab/",
    "https://www.rivalo.com/pt/apostas/tenis-wta-grand-slam/gcgdbba/",
    "https://www.rivalo.com/pt/apostas/tenis-encontro-atp-challenger-aptos-usa-men-singles/ghaejbdab/",
    "https://www.rivalo.com/pt/apostas/tenis-encontro-atp-challenger-aptos-usa-men-double/ghaejcdab/",
    "https://www.rivalo.com/pt/apostas/tenis-encontro-atp-challenger-portoroz-slovenia-men-singles/ghaejedab/",
    "https://www.rivalo.com/pt/apostas/tenis-encontro-atp-challenger-portoroz-slovenia-men-double/ghaejfdab/",
    "https://www.rivalo.com/pt/apostas/tenis-encontro-atp-challenger-pullach-germany-men-singles/ghaejhdab/",
    "https://www.rivalo.com/pt/apostas/tenis-encontro-atp-challenger-pullach-germany-men-double/ghaejidab/",
    "https://www.rivalo.com/pt/apostas/tenis-encontro-atp-challenger-jinan-china-men-singles/ghaeihdab/",
    "https://www.rivalo.com/pt/apostas/hoquei-russia-khl/gghddab/",
    "https://www.rivalo.com/pt/apostas/hoquei-internacional-amigaveis-de-clubes/gbeifdab/",
    "https://www.rivalo.com/pt/apostas/hoquei-internacional-liga-dos-campeoes-de-hoquei-grupo-a/gecafidab/",
    "https://www.rivalo.com/pt/apostas/hoquei-internacional-liga-dos-campeoes-de-hoquei-grupo-b/gecafjdab/",
    "https://www.rivalo.com/pt/apostas/hoquei-internacional-liga-dos-campeoes-de-hoquei-grupo-c/gecagadab/",
    "https://www.rivalo.com/pt/apostas/hoquei-internacional-liga-dos-campeoes-de-hoquei-grupo-d/gecagbdab/",
    "https://www.rivalo.com/pt/apostas/hoquei-internacional-liga-dos-campeoes-de-hoquei-grupo-e/gecagcdab/",
    "https://www.rivalo.com/pt/apostas/hoquei-internacional-liga-dos-campeoes-de-hoquei-grupo-h/gecagfdab/",
    "https://www.rivalo.com/pt/apostas/hoquei-internacional-presidents-cup/gcjcghdab/",
    "https://www.rivalo.com/pt/apostas/hoquei-internacional-apostas-em-partidas-da-temporada/gbcfigba/",
    "https://www.rivalo.com/pt/apostas/hoquei-internacional-amigaveis-de-clubes-modziez/gbegdeba/",
    "https://www.rivalo.com/pt/apostas/hoquei-suecia-shl/gbbfdab/",
    "https://www.rivalo.com/pt/apostas/andebol-internacional-u18-world-championship-damen/gbdehidab/",
    "https://www.rivalo.com/pt/apostas/andebol-internacional-campeonato-europeu-grupo-a/ghbaebdab/",
    "https://www.rivalo.com/pt/apostas/andebol-internacional-campeonato-europeu-grupo-b/ghbaiddab/",
    "https://www.rivalo.com/pt/apostas/andebol-internacional-campeonato-europeu-sub-18-grupo-c/ghbaeddab/",
    "https://www.rivalo.com/pt/apostas/andebol-internacional-campeonato-europeu-grupo-d/ghbaefdab/",
    "https://www.rivalo.com/pt/apostas/andebol-internacional-campeonato-europeu-2018-feminino/gbbjddba/",
    "https://www.rivalo.com/pt/apostas/andebol-internacional-apostas-em-partidas-da-temporada/gecedba/",
    "https://www.rivalo.com/pt/apostas/andebol-internacional-campeonato-do-mundo-2019-masculinos/ghcefba/",
    "https://www.rivalo.com/pt/apostas/andebol-brasil-super-paulista/gbihhdba/",
    "https://www.rivalo.com/pt/apostas/beisebol-estados-unidos-america-mlb/gcfdab/",
    "https://www.rivalo.com/pt/apostas/beisebol-mexico-liga-mexicana/gfhgfdab/",
    "https://www.rivalo.com/pt/apostas/futsal-brasil-taca-brazil/gbjgifba/",
    "https://www.rivalo.com/pt/apostas/futebol-americano-estados-unidos-america-nfl/gehdab/",
    "https://www.rivalo.com/pt/apostas/futebol-americano-estados-unidos-america-nfl-pre-epoca/ggdeedab/",
    "https://www.rivalo.com/pt/apostas/futebol-americano-canada-cfl/ggcbdab/",
    "https://www.rivalo.com/pt/apostas/badmington/gdbbab/l/",
    "https://www.rivalo.com/pt/apostas/badmington-internacional-open-do-vietname-wt/ghcjfidab/",
    "https://www.rivalo.com/pt/apostas/badmington-internacional-open-do-vietname-wt-pares/ghcjfjdab/",
    "https://www.rivalo.com/pt/apostas/cricket-australia-apostas-em-partidas-da-temporada/gbhefiba/",
    "https://www.rivalo.com/pt/apostas/cricket-inglaterra-natwest-t20-blast-north-group/ggahgidab/",
    "https://www.rivalo.com/pt/apostas/cricket-inglaterra-natwest-t20-blast-south-group/ggahhadab/",
    "https://www.rivalo.com/pt/apostas/cricket-inglaterra-cricket-super-league-feminino/gfecghdab/",
    "https://www.rivalo.com/pt/apostas/cricket-indias-ocidentais-premier-league-das-caraibas/gcjaeddab/",
    "https://www.rivalo.com/pt/apostas/cricket-internacional-icc-taca-do-mundo/gbjgdiba/",
    "https://www.rivalo.com/pt/apostas/cricket-india-liga-premier-tamil-nadu-play-offs/ggcefcdab/",
]

main_url = "https://www.rivalo.com/pt/apostas/"


def instance_browser():
    chrome_options = Options()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("no-sandbox")
    return webdriver.Chrome(executable_path='/root/bet-crawlers/chromedriver', chrome_options=chrome_options)
    # return webdriver.Chrome(chrome_options=chrome_options)


def main_page(browser, main_url):
    print('getting...', main_url)
    browser.get(main_url)


def split_list(old_list):
    new_list = []
    new_list.append(old_list[:len(old_list)//2])
    new_list.append(old_list[len(old_list)//2:])
    return new_list


def write_file(name, data):
    with open(name + ".json", 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def is_hour(item):
    pattern = re.compile("\d{2}:\d{2}")
    if pattern.match(item):
        return True
    else:
        return False


mercado_list = [
    "Dupla possibilidade",
    "Empate não tem aposta",
    "Handicap (0:1)",
    "Handicap (0:2)",
    "Handicap (1:0)",
    "Aposta Acima/Abaixo (2,5)",
    "Aposta Acima/Abaixo (0,5)",
    "Aposta Acima/Abaixo (1,5)",
    "Aposta Acima/Abaixo (3,5)",
    "Aposta Acima/Abaixo (4,5)",
    "Os dois times marcam?",
    "Quem é o próximo a marcar?",
    "Quem ganha o 1. tempo?",
    "Quem ganha o 2. tempo?",
    "Par/ Impar",
    # "Acima/Abaixo de gols (para cada time)",
    "Acima/ Abaixo Faltas",
    # "Acima/Abaixo escanteios",
    "Qual time vai conseguir a maioria dos escanteios?",
    # "Acima/Abaixo escanteios 1 tempo",
    # "Acima/Abaixo escanteios 2 tempo",
    "1. tempo Aposta Acima/Abaixo",
    "2. tempo Aposta Acima/Abaixo",
    "Acima/ Abaixo cartões tempo total",
    "Acima/ Abaixo cartões primeiro tempo",
    "Dupla Possibilidade primeiro tempo",
    "Empate não tem aposta primeiro tempo",
    "Acima/Abaixo gols segundo tempo",
    "Acima/Abaixo cartões segundo tempo",
    "Dupla Possibilidade segundo tempo",
    "Empate não tem aposta segundo tempo",
    "Acima/Abaixo pontos",
    "Quem vencerá o 1.tempo?",
    "Acima/Abaixo sets na partida",
    "Acima/Abaixo games na partida",
    "HC 1,5:0 games na partida",
    # "Acima/Abaixo games na partida",
    # "Acima/Abaixo Games Ganhos (Para cada jogador)",
    "Quem vai ganhar o set 1?",
    "Quem vai ganhar o set 2?",
    # "2-way ( incluindo a prorrogação/pênaltis)",
    "Quem ganha o período Num. 1?",
    "Período Num. 1 Acima/Abaixo da aposta",
    "Empate não tem aposta",
    "Acima/Abaixo de gols(para cada time)",
    "Quem ganha o período Num. 1?",
    # "Período Num. 1 Acima/Abaixo da aposta(todos dessa categoria)",
    "Dupla possibilidade",
    "Handicap",
    "Aposta Acima/Abaixo",
    "Quem ganha o tempo Num. 1",
    # "Aposta acima/abaixo pontos na partida(quando tiver mercado aberto)",
    # "Aposta acima/abaixo pontos no set(quando tiver mercado aberto)",
    "Quem vai ganhar o set Num. 1?",
]


def running_crawler(league_url, current_item, total_items):
    rivalo = []
    camp_name = str(current_item)
    con = psycopg2.connect(host='0.0.0.0', database='bet-crawlers',
                           user='postgres', password='betcrawlers@321', port='1234')
    cur = con.cursor()

    try:
        browser = instance_browser()
        browser.set_page_load_timeout(60)
        main_page(browser, main_url)

        print("Running item: " + str(current_item + 1) + " of " + str(total_items))

        print("Getting...", league_url)
        browser.get(league_url)

        league_infos = browser.find_element_by_css_selector(
            ".t_head .fs_16").text.split('-')
        if len(league_infos) <= 1:
            raise Exception('Not infos founds in ' + league_url)

        esp_name = league_infos[0]
        league_name = league_infos[1]
        camp_name = league_infos[2]
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("")
        # print(esp_name, league_name, camp_name)

        matches_list = []
        match_rows = browser.find_elements_by_css_selector(
            ".jq-compound-event-block .e_active .jq-event-row-cont , .jq-compound-event-block .e_active .t_space"
        )

        if len(match_rows) == 0:
            raise Exception('Not matches founds in ' + league_url)

        current_date = None

        for idx, match in enumerate(match_rows):
            evento = {}
            match_idx = idx
            current_hour = None
            event_name = None
            home = None
            visitant = None
            home_odd = None
            draw_odd = None
            visitant_odd = None
            debug = None

            categoria_nome = None
            mercado_nome = None
            poss_nome = None
            poss_valor = None

            match_class = match.get_attribute("class")
            m = re.match("(t_space)", match_class)
            if m:
                current_date = re.search(
                    "\s(\d{2}\.\d{2})\.", match.text.strip()).group(1)
                continue

            match_data_list = match.text.strip().splitlines()
            match_len = len(match_data_list)

            if match_len < 6:
                print("Drop match" + str(idx + 1), league_url)
                continue

            current_hour = match_data_list[0]
            home = match_data_list[1]
            visitant = match_data_list[2]

            if match_data_list[5].strip() == 'LIVE':
                home_odd = float(match_data_list[3].replace(",", "."))
                visitant_odd = float(match_data_list[4].replace(",", "."))
            else:
                home_odd = float(match_data_list[3].replace(",", "."))
                draw_odd = float(match_data_list[4].replace(",", "."))
                visitant_odd = float(match_data_list[5].replace(",", "."))

            event_name = home + ' - ' + visitant

            print('Event: ', event_name)
            print('Casa: ', home)
            print('Visitante: ', visitant)

            print('Casa odd: ', home_odd)
            print('Empate odd: ', draw_odd)
            print('Visitante odd:', visitant_odd)

            print('Data :', current_date)
            print('Hora :', current_hour)

            evento["esporte_nome"] = esp_name
            evento["liga_nome"] = league_name
            evento["campeonato_nome"] = camp_name
            evento["camp_url"] = league_url

            evento["data"] = current_date
            evento["hora"] = current_hour

            evento["nome"] = event_name
            evento["casa"] = home
            evento["visitante"] = visitant

            evento["casa_odd"] = home_odd
            evento["empate_odd"] = draw_odd
            evento["visitante_odd"] = visitant_odd

            sql = "select id, evento_nome from rivalo_eventos where evento_nome = %s"
            cur.execute(sql, [event_name])
            old_event = cur.fetchone()
            if old_event:
                print("Delete event...")
                sql = "delete from rivalo_mercados where evento_nome = %s"
                cur.execute(sql, [event_name])
                con.commit()
                sql = "delete from rivalo_eventos where evento_nome = %s"
                cur.execute(sql, [event_name])
                con.commit()

            print("Saving event")
            sql = "insert into rivalo_eventos values (default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, default) RETURNING id"
            cur.execute(sql, (esp_name, league_name, camp_name,
                              league_url, current_date, current_hour, event_name,
                              home, visitant, evento["casa_odd"], evento["empate_odd"], evento["visitante_odd"]))
            con.commit()
            evento_id = cur.fetchone()[0]
            print(evento_id)

            load_scout = None
            try:
                load_scout = match.find_element_by_css_selector(
                    ".t_more"
                )
            except:
                print("This match dont have scouts")
                continue
            load_scout.click()
            time.sleep(2)

            categorias = match.find_elements_by_css_selector(".t_more_head")

            if idx == 1:
                categorias = match.find_elements_by_css_selector(".t_more_head")[
                    1:]
                for cat in categorias:
                    cat.click()
                    time.sleep(1)

            mercados = match.find_elements_by_css_selector(
                ".border_ccc div.t_more_row")
            scouts = []
            for me in mercados:
                data = {}
                mercado = {}
                have_mercado = 0
                mercado_data = me.text.strip().splitlines()
                poss_list = mercado_data[1:]
                if len(poss_list) == 0:
                    continue
                for m in mercado_list:
                    mercado_pattern = "Acima/Abaixo games na partida ("

                    if m == mercado_data[0]:
                        have_mercado = 1
                        mercado["mercado_nome"] = mercado_data[0]
                        if len(poss_list) == 6:
                            mercado["poss_nome_1"] = poss_list[0] + \
                                " " + poss_list[1]
                            mercado["poss_valor_1"] = float(
                                poss_list[1].replace(",", "."))
                            mercado["poss_nome_2"] = poss_list[2] + \
                                " " + poss_list[3]
                            mercado["poss_valor_2"] = float(
                                poss_list[3].replace(",", "."))
                            mercado["poss_nome_3"] = poss_list[4] + \
                                " " + poss_list[5]
                            mercado["poss_valor_3"] = float(
                                poss_list[5].replace(",", "."))
                        else:
                            mercado["poss_nome_1"] = poss_list[0] + \
                                " " + poss_list[1]
                            mercado["poss_valor_1"] = float(
                                poss_list[1].replace(",", "."))
                            mercado["poss_nome_2"] = poss_list[2] + \
                                " " + poss_list[3]
                            mercado["poss_valor_2"] = float(
                                poss_list[3].replace(",", "."))

                            mercado["poss_nome_3"] = None
                            mercado["poss_valor_3"] = None

                        mercado_nome = mercado["mercado_nome"]
                        poss_nome_1 = mercado["poss_nome_1"]
                        poss_valor_1 = mercado["poss_valor_1"]
                        poss_nome_2 = mercado["poss_nome_2"]
                        poss_valor_2 = mercado["poss_valor_2"]
                        poss_nome_3 = mercado["poss_nome_3"]
                        poss_valor_3 = mercado["poss_valor_3"]

                        casa_odd = None
                        empate_odd = None
                        visitante_odd = None

                        if mercado_data[0] == "Dupla possibilidade":
                            casa_odd = evento["casa_odd"]
                            empate_odd = evento["empate_odd"]
                            visitante_odd = evento["visitante_odd"]

                        sql = "insert into rivalo_mercados values (default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, default)"
                        cur.execute(sql, (evento_id, mercado_nome, casa_odd, empate_odd, visitante_odd,
                                          evento["nome"], evento["esporte_nome"], poss_nome_1, poss_valor_1,
                                          poss_nome_2, poss_valor_2,
                                          poss_nome_3, poss_valor_3))
                        con.commit()
                        break

                data["evento"] = evento
                data["mercado"] = mercado
                if have_mercado == 1:
                    print(data)
                    rivalo.append(data)

            load_scout.click()
            time.sleep(1)

        time.sleep(1)
    except Exception as e:
        print(e)
        print("crawler broken: ", league_url)
    finally:
        print("DONE")
        con.close()
        browser.close()


if __name__ == '__main__':
    while True:
        print("Start")
        start_time = time.time()
        pool = Pool(processes=12)
        # urls = [
            # "https://www.rivalo.com/pt/apostas/futebol-brasil-brasileirao-serie-a/giddab/",
            # "https://www.rivalo.com/pt/apostas/futebol-brasil-taca-paulista/gbhjhddab/",
            # "https://www.rivalo.com/pt/apostas/futebol-clubes-internacionais-copa-libertadores-fase-final/gdajdab/",
            # "https://www.rivalo.com/pt/apostas/futebol-clubes-internacionais-taca-dos-campeoes-internacionais/gcjabjdab/",
            # "https://www.rivalo.com/pt/apostas/futebol-clubes-internacionais-supertaca-europeia/ggiadab/",
            # "https://www.rivalo.com/pt/apostas/hoquei-internacional-liga-dos-campeoes-de-hoquei-grupo-h/gecagfdab/",
            # "https://www.rivalo.com/pt/apostas/hoquei-internacional-presidents-cup/gcjcghdab/",
            # "https://www.rivalo.com/pt/apostas/cricket-inglaterra-cricket-super-league-feminino/gfecghdab/",
            # "https://www.rivalo.com/pt/apostas/cricket-indias-ocidentais-premier-league-das-caraibas/gcjaeddab/",
            # "https://www.rivalo.com/pt/apostas/futebol-clubes-internacionais-amigaveis-de-clubes/gigdab/",
            # "https://www.rivalo.com/pt/apostas/futebol-inglaterra-taca-da-liga/gbhdab/",
            # "https://www.rivalo.com/pt/apostas/futebol-russia-liga-junior/gbcgbadab/",
            # "https://www.rivalo.com/pt/apostas/futebol-hungria-nb-i/gfadab/",
            # "https://www.rivalo.com/pt/apostas/futebol-juniores-internacionais-taca-do-mundo-feminina-sub-20-grupo-c/gbdbahdab/",
        # ]
        pool_list = []
        urls_len = len(urls)
        for idx, item in enumerate(urls):
            pool.apply_async(running_crawler, (item, idx, urls_len))
        pool.close()
        pool.join()
        write_file("time", "loop time: " + "--- %s seconds ---" %
                   (time.time() - start_time))
        print("--- %s seconds ---" % (time.time() - start_time))
        print("Finish loop")
        time.sleep(1)


# 60099, samuelcarvalho, JFppOslQ

# 146.252.88.44
# 146.252.88.59
# 146.252.88.61
# 146.252.88.72
# 146.252.88.85
# 146.252.88.91
# 146.252.88.92
# 146.252.88.108
# 146.252.88.110
# 146.252.88.113
# 146.252.88.134
# 146.252.88.147
# 146.252.88.148
# 146.252.88.153
# 146.252.88.157
# 146.252.88.170
# 146.252.88.182
# 146.252.88.184
# 146.252.88.209
# 146.252.88.211
# 146.252.88.227
# 146.252.88.239
# 146.252.88.242
# 146.252.88.243
# 146.252.88.250
