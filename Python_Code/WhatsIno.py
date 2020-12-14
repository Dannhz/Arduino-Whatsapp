from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import serial
import time
#------------------------VARIÁVEIS GLOBAIS-------------------------------------

    #identificação de elementos da página (Para eventuais atualizações)
elemFotoPerfil = '//*[@id="side"]/header/div[1]/div/img'
elemCaixaMsg = '//*[@id="main"]/footer/div[1]/div[2]/div'
elemMensagens = '//*[@id="main"]/div[3]/div/div/div[3]/div'
elemBtnPesquisa = '//*[@id="side"]/header/div[2]/div/span/div[2]/div/span'
elemTxtContatos = '//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[1]/div/label/div/div[2]'
elemContatos = '//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div[1]/div/div/div[*]/div/div/div[2]/div[1]/div/span' 

#-------------------------------------------------------------------------------

try:
    ser = serial.Serial('COM4', 9600, timeout=0.1) #Estabelece conexão com o arduino
except Exception as e:
    print(e)
    print("Houve uma falha na conexão com o arduino")
    
driver = webdriver.Chrome() #Instancia o Webdriver e inicializa o web.whatsapp
driver.get("https://web.whatsapp.com")

contato = "WhatsIno" #nome do grupo/contato que o sistema irá interagir.

def main(): #Inicialização do Sistema   
    while(1): #Entra num loop que se encerra após identificar o elemento da foto de perfil
        time.sleep(1)
        try:
            fotoPerfil = driver.find_element_by_xpath(elemFotoPerfil)
        except:
            print("Por favor, efetue a leitura do QR através do WhatsApp. Caso queira sair, digite ctrl+c ou feche o prompt de comando.")
            continue
        break

    print("Leitura efetuada...")

    searchCtt(contato)

    while(1):      
        wRead() 
        aRead()

def searchCtt(destino): #Busca o contato do Whatsapp.
    while(1): #ETAPA 1 - Botão Contatos
        try:
            time.sleep(.3)
            conversas = driver.find_element_by_xpath(elemBtnPesquisa)
            conversas.click()
            break
        except Exception as e:
            print("ERRO NA BUSCA DE CONTATOS...")
            print(e)
            continue

    while(1): #ETAPA 2 - Inserção do nome do contato
        try:
            time.sleep(.3)
            buscaContato = driver.find_element_by_xpath(elemTxtContatos)
            buscaContato.send_keys(destino)
            print("Nome inserido no campo de busca...")
            break
        except Exception as e :
            print("ERRO NA INSERÇÃO DO NOME...")
            print(e)
            continue

    while(1): #ETAPA 3 - Seleção do contato 
        try:
            time.sleep(.3)
            contatos = driver.find_elements_by_xpath(elemContatos)
            
            for contato in contatos:
                if contato.text == destino:
                    time.sleep(.3)
                    contato.click()
                    time.sleep(.3)
                    if wReturn("App inicializado"):
                        break
            break

        except Exception as e:
            print("ERRO NA SELEÇÃO DO CONTATO...")
            print(e)
            break

def wRead(): #Faz a leitura do chat do WhatsApp
    try:
        todasMsgs = driver.find_elements_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div') #Armazena todas as mensagens enviadas/recebidas visíveis
        ultimaMsg = len(todasMsgs) #Coleta a quantidade de mensagens armazenadas
        classe = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div[{}]'.format(ultimaMsg)).get_attribute("class") #Armazena a classe da ultima msg
    except:
        return

    if 'message-in' in classe: # (message-out = Mensagem enviada // message-in = Mensagem recebida)
        textoChat = driver.find_element_by_xpath('//div[{}]/div/div/div/div[last()-1]/div/span[1]/span'.format(ultimaMsg)).text
        #                                                               div[1] - Nome do contato
        #                                                               div[2] - Texto da msg
        #                                                               div[3] - horário da msg
        #nem sempre o elemento da mensagem possui 3 divs, pois caso um contato envie 2 ou mais mensagens consecutivas, a div de seu nome é desconsiderada.

        if(textoChat.lower() == 'acender led1'):
            aWrite("LED1:1")
            wReturn("*Led 1 aceso.*")
            
        elif(textoChat.lower() == 'acender led2'):
            aWrite("LED2:1")
            wReturn("*Led 2 aceso.*")

        elif(textoChat.lower() == 'acender led3'):
            aWrite("LED3:1")
            wReturn("*Led 3 aceso.*")
            
        elif(textoChat.lower() == 'apagar led1'):
            aWrite("LED1:0")
            wReturn("*Led 1 apagado.*")
        
        elif(textoChat.lower() == 'apagar led2'):
            aWrite("LED2:0")
            wReturn("*Led 2 apagado.*")
            
        elif(textoChat.lower() == 'apagar led3'):
            aWrite("LED3:0")
            wReturn("*Led 3 apagado.*")            
            
        elif(textoChat.lower() == 'acender todos'):
            aWrite("ALL:1")
            wReturn("*Todos os leds foram acesos.*")
            
        elif(textoChat.lower() == 'apagar todos'):
            aWrite("ALL:0")
            wReturn("*Todos os leds foram apagados.*")
            
        else:
            wReturn("*Não entendi o que você quis dizer.*")
            
def wReturn(mensagem): #Retorna uma mensagem no WhatsApp
    while(1):
        try:
            caixaMsg = driver.find_element_by_xpath(elemCaixaMsg)
            caixaMsg.click()
            for line in mensagem.split('\n'):
                ActionChains(driver).send_keys(line).perform()
                ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            ActionChains(driver).send_keys(Keys.RETURN).perform()
            break
        except:
            print("Erro")
            continue

def aRead(): #Efetua a leitura constante do Serial do Arduino
    msg = ser.readline().rstrip().decode("utf-8")
  
    if(msg != ''):
        msgFrag = msg.split("-")
        if(msgFrag[0] == 'btnPressionado'):
            wReturn("Botão pressionado{}".format(" {} vezes!".format(msgFrag[1]) if int(msgFrag[1]) > 1 else "!"))
   
def aWrite(msg): #Encaminha uma mensagem ao Arduino através do Serial
    try:
        ser.write(msg.encode())
        return True
    except Exception as e:
        print(e)
        return False
     
if(__name__ == "__main__"):
    main()