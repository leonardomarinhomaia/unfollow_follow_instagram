#!/usr/bin/env python
# coding: utf-8

# #
# TODOS IMPORTS NECESSÁRIOS

# In[1]:


import sys
import time
import smtplib
import email.message
from random import randint, choice
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium import webdriver


# #
# PAUSAS

# In[2]:


def tempo_l_unfollow():
    return time.sleep(randint(84, 92))


def tempo_longo():
    return time.sleep(randint(42, 50))


def tempo_curto():
    return time.sleep(randint(4, 6))


# #
# ENVIO DE EMAILS

# In[3]:


def email_sucesso():
    corpo_email = f"""PROGRAMA FINALIZADO COM SUCESSO
    <p>O programa de automação do instagram {nome_programa} foi iniciado em {data_hora_inicio} e finalizado com SUCESSO em {data_hora_fim}</p>
    <p>Favorecido: {favorecido}</p>
    <p>Local alvo: {local}</p>
    <p>Total de perfis que deixou de seguir: {num_unfollow}</p>
    <p>Total de perfis seguidos: {num_follow}</p>"""
    msg = email.message.Message()
    msg['Subject'] = f"SUCESSO {nome_programa}"
    msg['From'] = '******** EMAIL ORIGEM ********'
    msg['To'] = '******** EMAIL DESTINO ********'
    password = '******** SENHAS DE APP DO GMAIL ORIGEM ********'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))


def email_erro():
    corpo_email = f"""PROGRAMA FINALIZADO COM ERRO
    <p>O programa de automação do instagram {nome_programa} foi iniciado em {data_hora_inicio} e finalizado com ERRO em {data_hora_erro}</p>
    <p>Favorecido: {favorecido}</p>
    <p>Local alvo: {local}</p>
    <p>Total de perfis que deixou de seguir até o erro: {num_unfollow}</p>
    <p>Total de perfis seguidos até o erro: {num_follow}</p>"""
    msg = email.message.Message()
    msg['Subject'] = f"ERRO {nome_programa}"
    msg['From'] = '******** EMAIL ORIGEM ********'
    msg['To'] = '******** EMAIL DESTINO ********'
    password = '******** SENHAS DE APP DO GMAIL ORIGEM ********'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))


# #
# DEIXAR DE SEGUIR

# In[4]:


def unfollow():
    navegador.get(favorecido)
    try:
        navegador.maximize_window()
    except:
        pass
    tempo_curto()
    
    # ABRE UMA SEGUNDA GUIA NO EDGE / O OBJETIVO DE TER UMA SEGUNDA GUIA ABERTA É EVITAR ERROS DE GUIAS INATIVAS
    navegador.execute_script("window.open('https://www.google.com/','_blank');")
    tempo_curto()
    guia_instagram = navegador.window_handles[0]
    guia_outra = navegador.window_handles[1]
    navegador.switch_to.window(guia_instagram)
    tempo_curto()

    # COPIA E TRATA O NÚMERO DE PERFIS QUE O PERFIL FAVORECIDO ESTÁ SEGUINDO
    num_following = navegador.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[3]/a/span').text
    num_following = num_following.replace('.', '')

    # SE ESTÁ SEGUINDO MAIS DE 1500 PERFIS VAI EXECUTAR 100% "unfollow"
    if int(num_following) > 1500:
        tempo_tentando = 50
        tentativas_descer = 0
        navegador.get(f'{favorecido}following/')

        # IDENTIFICA E PASSA A AGIR NO POP UP "seguindo"
        tempo_longo()
        pop_up_window = WebDriverWait(navegador, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, '_aano')))
        tempo_curto()
        
        # PRA NÃO CORRER O RISCO DE DAR ERRO DE GUIA INATIVA, VAI PRA OUTRA GUIA, DÁ UM F5 E DEPOIS VOLTA PARA O INSTAGRAM
        navegador.switch_to.window(guia_outra)
        navegador.refresh()
        tempo_curto()
        navegador.switch_to.window(guia_instagram)
        
        # NO POP UP SEGUINDO EXISTE UM ÍNDICE NOS PERFIS, E O 1º QUE ENXERGAMOS É O 1, O 2º É O 2 E ASSIM POR DIANTE
        # SE QUER CLICAR NO PERFIL 700 (EXEMPLO), DEVE-SE DESCER A BARRA DE ROLAGEM ALÉM DO PERFIL 700 PARA "CARREGÁ-LO"
        perfil = 4
        descer = randint(901, 949)
        for l in range(1, descer):

            # DESCE O MOUSE DE 1 EM 1 PERFIL / SE DER ERRO E TIVER QUE TROCAR XPATH AQUI DEVE-SE FAZER O MESMO NA LINHA 96
            try:
                seguindo = WebDriverWait(navegador, tempo_tentando).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div/div[{perfil}]/div/div/div/div[3]/div/button')))                                                                                                                  
                ActionChains(navegador).move_to_element(seguindo).perform()
                perfil += 1
                time.sleep(1)
            
            # ENTRA AQUI SE FICAR MAIS DE 50 SEGUNDOS NO "try" ACIMA OU SE DER ERRO DE XPATH OU OUTROS ERROS NO "try" ACIMA
            except TimeoutException:
                navegador.switch_to.window(guia_outra)
                navegador.refresh()
                tempo_curto()
                navegador.switch_to.window(guia_instagram)
                tentativas_descer += 1
                print(f'{tentativas_descer}x - Tempo limite excedido ao descer a barra para carregar no total {descer} perfis')
                print('Trocando guias e atualizando para voltar a funcionar')
            
            # SE ENTRAR 6 VEZES EM "TimeoutException" DAÍ ENCERRA O PROGRAMA COM ERRO
            finally:
                if tentativas_descer == 6:
                    sys.exit()
        tempo_curto()
        
        # PRA NÃO CORRER O RISCO DE DAR ERRO DE GUIA INATIVA, VAI PRA OUTRA GUIA, DÁ UM F5 E DEPOIS VOLTA PARA O INSTAGRAM
        navegador.switch_to.window(guia_outra)
        navegador.refresh()
        tempo_curto()
        navegador.switch_to.window(guia_instagram)
        
        # DEIXAR DE SEGUIR
        # O PERFIL INICIAL É ALÉM DE 650 PQ ENTRE OS PRIMEIROS 650 PERFIS ESTÃO AQUELES DE "CONHECIDOS" E/OU MAIS ENGAJADOS
        p_start = randint(651, 699)
        p_unfollow = 0
        tentativas_seguindo = 0
        tentativas_deixar_seguir = 0
        global num_unfollow
        while num_unfollow < unfollow_daily:

            # PRA NÃO CORRER O RISCO DE DAR ERRO DE GUIA INATIVA, VAI PRA OUTRA GUIA, DÁ UM F5 E DEPOIS VOLTA PARA O INSTA
            navegador.switch_to.window(guia_outra)
            navegador.refresh()
            tempo_curto()
            navegador.switch_to.window(guia_instagram)
            if num_unfollow == 0:
                p_unfollow += p_start
            else:
                step = randint(1, 3)
                p_unfollow += step           
            tempo_curto()
            
            # CLICA EM "seguindo"
            try:
                clicar_seguindo = WebDriverWait(navegador, tempo_tentando).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[4]/div[1]/div/div[{p_unfollow}]/div/div/div/div[3]/div/button')))
                ActionChains(navegador).move_to_element(clicar_seguindo).perform()
                clicar_seguindo.click()
                tempo_curto()
            
            # ENTRA AQUI SE FICAR MAIS DE 50 SEGUNDOS NO "try" ACIMA OU SE DER ERRO DE XPATH OU OUTROS ERROS NO "try" ACIMA
            except TimeoutException:
                navegador.switch_to.window(guia_outra)
                navegador.refresh()
                tempo_curto()
                navegador.switch_to.window(guia_instagram)
                tentativas_seguindo +=1
                print(f'{tentativas_seguindo}x - Tempo limite excedido ao clicar em seguindo')
                print('Trocando guias e atualizando para voltar a funcionar')
                
            # SE ENTRAR 6 VEZES EM "TimeoutException" DAÍ ENCERRA O PROGRAMA COM ERRO
            finally:
                if tentativas_seguindo == 6:
                    sys.exit()
            
            # CLICA EM DEIXAR DE SEGUIR
            try:
                deixar_seguir = WebDriverWait(navegador, tempo_tentando).until(EC.element_to_be_clickable((By.CLASS_NAME, '_a9-_')))            
                ActionChains(navegador).move_to_element(deixar_seguir).perform()
                deixar_seguir.click()
                num_unfollow += 1
                print(f'Unfollow {num_unfollow}: OK')
            
            # ENTRA AQUI SE FICAR MAIS DE 50 SEGUNDOS NO "try" ACIMA OU SE DER ERRO DE XPATH OU OUTROS ERROS NO "try" ACIMA
            except TimeoutException:
                navegador.switch_to.window(guia_outra)
                navegador.refresh()
                tempo_curto()
                navegador.switch_to.window(guia_instagram)
                tentativas_deixar_seguir +=1
                print(f'{tentativas_deixar_seguir}x - Tempo limite excedido ao clicar em deixar de seguir')
                print('Trocando guias e atualizando para voltar a funcionar')
                
            # SE ENTRAR 6 VEZES EM "TimeoutException" DAÍ ENCERRA O PROGRAMA COM ERRO
            finally:
                if tentativas_deixar_seguir == 6:
                    sys.exit()
            tempo_l_unfollow()

    # SE ESTÁ SEGUINDO MENOS DE 1500 PERFIS DAÍ NÃO EXECUTA TODO "unfollow" E SEGUE ADIANTE
    else:
        print(f'\n\nOBSERVAÇÃO: {favorecido} está seguindo menos de 1500 perfis e então não executará UNFOLLOW')
    tempo_curto()


# #
# SEGUIR

# In[5]:


def follow():
    navegador.get(local)
    tempo_longo()
    guia_instagram = navegador.window_handles[0]
    guia_outra = navegador.window_handles[1]
    
    # PRA NÃO CORRER O RISCO DE DAR ERRO DE GUIA INATIVA, VAI PRA OUTRA GUIA, DÁ UM F5 E DEPOIS VOLTA PARA O INSTAGRAM
    navegador.switch_to.window(guia_outra)
    navegador.refresh()
    tempo_curto()
    navegador.switch_to.window(guia_instagram)
        
    # CLICA NO PRIMEIRO POST
    navegador.find_element(By.CLASS_NAME, '_aagu').click()
    
    # LAÇO A SER REPETIDO O NÚMERO DE VEZES IGUAL AO DA QUANTIDADE DE PERFIS QUE VAI SEGUIR
    tentativas_passar = 0
    tentativas_passar_destravar = 5
    tempo_tentando = 60
    global num_follow
    while num_follow != follow_daily:
        tempo_longo()

        # SE NÃO SEGUIA O PERFIL, DAÍ CLICA EM SEGUIR
        try:
            navegador.find_element(By.CLASS_NAME, '_aacw').click()
            num_follow += 1
            print(f'Follow {num_follow}: OK')

        # SE JÁ SEGUIA O PERFIL DARÁ ERRO NO "try" ACIMA E DAÍ SEGUE ADIANTE
        except:
            pass

        # VAI PRA OUTRA GUIA, DÁ UM F5 E DEPOIS VOLTA PARA O INSTAGRAM
        navegador.switch_to.window(guia_outra)
        navegador.refresh()
        tempo_curto()
        navegador.switch_to.window(guia_instagram)
        tempo_longo()
        
        # PASSA PARA O(S) PRÓXIMO(S) POST(S) NAQUELA LOCALIZAÇÃO / VAI PULAR ENTRE 1 E 3 POSTS
        # TEM QUE SER COM "move_to_element" PQ ALGUMAS VEZES DÁ ERRO SE COLOCAR DIRETO PRA CLICAR NO ELEMENTO
        proximo_post = randint(1, 3)
        for l in range(1, proximo_post + 1):
            try:
                passar = WebDriverWait(navegador, tempo_tentando).until(EC.element_to_be_clickable((By.CLASS_NAME, '_aaqg')))                                                                                                         
                ActionChains(navegador).move_to_element(passar).perform()
                passar.click()
            
            # ENTRA AQUI SE FICAR MAIS DE 60 SEGUNDOS NO "try" ACIMA (NÃO CONSEGUIR CLICAR EM SEGUINDO)
            # VAI ENTRAR AQUI TAMBÉM DE DER ERRO DE CLASS_NAME OU OUTROS ERROS NO "try" ACIMA
            except TimeoutException:
                tentativas_passar +=1
                print(f'{tentativas_passar}x - Tempo limite excedido ao clicar em passar para o próximo post')
            
            finally:    
                
                # SE ENTRAR 3 VEZES EM "TimeoutException" DAÍ VAI PRA OUTRA GUIA, DÁ UM F5 E DEPOIS VOLTA PARA O INSTAGRAM
                # ISSO "DESTRAVA" O EDGE E O PROGRAMA VOLTA A FUNCIONAR
                if tentativas_passar == tentativas_passar_destravar:
                    navegador.switch_to.window(guia_outra)
                    navegador.refresh()
                    tempo_curto()
                    navegador.switch_to.window(guia_instagram)
                    tentativas_passar_destravar += 5
                    print('Trocando guias e atualizando para voltar a funcionar')
    
                # SE ENTRAR 251 VEZES EM "TimeoutException" (50 VEZES NO "if" ACIMA) DAÍ ENCERRA O PROGRAMA COM ERRO
                # DAÍ PODE SER PROBLEMA DE CONEXÃO COM A INTERNET, ERRO DE XPATH OU OUTROS ERROS
                if tentativas_passar == 251:
                    sys.exit()
    tempo_curto()
    navegador.quit()


# #
# CONFIGURAÇÃO, ATUALIZAÇÃO E PROFILE DO NAVEGADOR EDGE
# <br>
# VARIÁVEIS DO ESCOPO PRINCIPAL

# In[6]:


servico = EdgeChromiumDriverManager().install()
options = webdriver.EdgeOptions()
options.add_argument(r'user-data-dir=C:\******** CAMINHO PROFILE EDGE COM PERFIL FAVORECIDO LOGADO INSTAGRAM ********')
navegador = webdriver.Edge(options=options)
num_follow = 0
num_unfollow = 0
extra = randint(3, 7)
follow_daily = randint(90, 95)
unfollow_daily = follow_daily + extra
nome_programa = 'unfollow_follow_insta_1.0'
favorecido = '******** URL PERFIL FAVORECIDO ********'


# #
# EXECUÇÃO DO PROGRAMA

# In[7]:


try:
    data_hora_inicio = time.ctime()
    print(f'\n\n******\n\nPrograma {nome_programa} iniciado em {data_hora_inicio}\n\nFavorecido: {favorecido}\n\nPerfis que vai deixar de seguir: {unfollow_daily}\n\nPerfis que vai seguir: {follow_daily}\n')

    # INPUT PARA INFORMAR O LOCAL ALVO DO PROGRAMA
    local = input('******\n\n* Não inserir aspas\n* Deve iniciar com https\n* Deve conter explore/locations\nINFORME O LINK DO LOCAL ALVO:\n').lower()
    while not local.startswith('http') or not 'explore/locations' in local or '"' in local or "'" in local:
        local = input('******\n\n* Não inserir aspas\n* Deve iniciar com https\n* Deve conter explore/locations\nINFORME O LINK DO LOCAL ALVO:\n').lower()
    unfollow()
    follow()
    data_hora_fim = time.ctime()
    email_sucesso()
    print(f'\n******\n\nPrograma {nome_programa} finalizado com SUCESSO em {data_hora_fim}\n\nTotal de perfis que deixou de seguir: {num_unfollow}\n\nTotal de perfis seguidos: {num_follow}\n\n')

except:
    data_hora_erro = time.ctime()
    email_erro()
    print(f'\n******\n\nPrograma {nome_programa} finalizado com ERRO em {data_hora_erro}\n\nTotal de perfis que deixou de seguir até o erro: {num_unfollow}\n\nTotal de perfis seguidos até o erro: {num_follow}\n\n')
    sys.exit()


# In[ ]:




