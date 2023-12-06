//code for sending data serially to computer from microcontrolleruart port by DFTI module
#include <stm32f10x.h>
#include <stdio.h>
void  delay(int val){
	for(int i=0;i<=val;i++){
	SysTick->LOAD=72000;
	SysTick->VAL=0;
	SysTick->CTRL=0x05;
	while((SysTick->CTRL & 0x10000)==0){}
	SysTick->CTRL=0x0000;
	}
	
}
int main(){
	int adcval;
	float temp;
	char TEMP[16];
	//char array[15]={"Hello World"};
	RCC->CFGR|=0x00008000;    /*set the clk freq for adc eaual to 14Mhz by stting the prescaler value*/
	RCC->APB2ENR=0x0000420D;  /*clock enable for IOPA,IOPB,AFIO,ADC1,Usart1*/
	GPIOA->CRL=0x33330080;    /*PIN 4-7 config as output for lcd and pin 0 is adc channel 0*/
	GPIOA->CRH=0x000008B0; //Tx=pin 9,RX=Pin10
	GPIOA->ODR=(1<<10);    //PUll up active for PA10
	GPIOB->CRL=0x00000033;    /*RS And EN Pin selected as pin 0 and 1 of port B*/
	ADC1->SMPR2=0x00000038;   /*sampling rate is set to 239.5 samples by sampling register 2*/
	ADC1->SQR3=0x00000001;    /* channel 1 set for convertion , in the sequence register 3*/
	ADC1->CR2|=0x00000003;  /*Enable the ADC for the First time and set it in Continuous Mode*/
	USART1->BRR=625;//baudrate=115200
	USART1->CR1|=0x2008;         //UE TE RE enabled
	delay(1);
	ADC1->CR2|=0x00000001;/*turn on ADC for sevond time to actually turn it on and start conversion*/
	delay(1);
	ADC1->CR2|=0x00000004;/*calliberation bit set*/
	delay(1);
	while(1){
		while((ADC1->SR&(1<<1))==0);//wait until EOC flag is set
		adcval=ADC1->DR;
		temp=(float)((adcval*0.0008058));
		sprintf(TEMP,"%.2f",temp);
		int i=0;
		while(TEMP[i]!='\0'){
		USART1->DR=TEMP[i];
		while((USART1->SR &(1<<6))==0);//Wait until TC=1
			i++;
		}
		USART1->DR='\n';
		
		
	
	}
	
	
}
