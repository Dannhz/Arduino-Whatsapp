#define led1 2
#define led2 3
#define led3 4
#define buz 5
#define pinBotao 8
unsigned long horaPressionado = 0;
int vezesPressionado = 0;

void setup() { 
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(buz, OUTPUT);
  pinMode(pinBotao, INPUT_PULLUP);
  Serial.begin(9600);
}

bool botaoRet() { //Atribuir a função retenção ao botão do pino 8 - Baseado no código fornecido pelo canal Brincando com Ideias
   #define tempoDebounce 25 //(tempo para eliminar o efeito Bounce EM MILISEGUNDOS)
   bool estadoBotao; 
   static bool estadoBotaoAnt = true; //Por padrão inicializar com o valor True para não haver ativação inicial inesperada.
   bool estadoRet = true;
   static unsigned long delayBotao = 0;  
   
   if ((millis() - delayBotao) > tempoDebounce) { //Se o botão for pressionado por um tempo mais alto que 25ms...
       estadoBotao = digitalRead(pinBotao);   
       if ( estadoBotao && (estadoBotao != estadoBotaoAnt) ) { //Após soltar o botão...
          estadoRet = false;
       }
       delayBotao = millis();
       estadoBotaoAnt = estadoBotao;
   }
   return estadoRet;
}

String leStringSerial(){
  String conteudo = "";
  char caractere;
 
  // Enquanto receber algo pela serial
  while(Serial.available() > 0) {
    // Lê byte da serial
    caractere = Serial.read();
    // Ignora caractere de quebra de linha
    if (caractere != '\n'){
      // Concatena valores
      conteudo.concat(caractere);
    }
    // Aguarda buffer serial ler próximo caractere
    delay(10);
  }    
  Serial.print("Recebi: ");
  Serial.println(conteudo);
    
  return conteudo;
}

void loop() {
  if (!botaoRet()) {
    //Incrementa a quantidade de apertos que teve no botão e salva a ultima vez que foi pressionado.
    horaPressionado = millis();
    vezesPressionado += 1;
  }

  if((horaPressionado != 0) && (millis() >= horaPressionado + 750)){
    //Se o botão deixou de ser pressionado por 3/4 de segundo é enviada a mensagem e zera a contagem.
    String texto = "btnPressionado-" + String(vezesPressionado);
    horaPressionado = 0;
    vezesPressionado = 0;
    Serial.println(texto);  
  }

  if (Serial.available() > 0){
    // Lê toda string recebida
    String recebido = leStringSerial();

    if(recebido == "LED1:1")
      digitalWrite(led1, 1);
      
    else if(recebido == "LED2:1")
      digitalWrite(led2, 1);
    
    else if(recebido == "LED3:1")
      digitalWrite(led3, 1); 

    else if(recebido == "LED1:0")
      digitalWrite(led1, 0);
     
    else if(recebido == "LED2:0")
      digitalWrite(led2, 0);
    
    else if(recebido == "LED3:0")
      digitalWrite(led3, 0);       

    else if(recebido == "BUZZER:1")
      digitalWrite(buz, 1);

    else if(recebido == "BUZZER:0")
      digitalWrite(buz, 0);

    else if(recebido == "ALL:1"){
      digitalWrite(led1, 1);     
      digitalWrite(led2, 1);   
      digitalWrite(led3, 1);  
    }  
    else if(recebido == "ALL:0"){
      digitalWrite(led1, 0);     
      digitalWrite(led2, 0);   
      digitalWrite(led3, 0);  
    }  
  }
}
