/*
 * Solução 1 da Questão 1
 */ 
#include <iostream>

using namespace std;

int main() {
  int n; /* numero de elementos da sequencia  */

  cout << "Digite o numero de elementos da sequencia: ";
  cin >> n;
  cout << "Digite uma sequencia de " << n << " números reais: " << endl;

  float seq[n]; /*Novo vetor de tamanho n*/
  int i = 0;

  /*Lê os valores*/
  while(i < n){
    cin >> seq[i];
    i = i + 1;
  }

  i = 0; /*Reinicia o valor de i para reutilizar ela no novo laço*/
  int j = 0; /*Outra variável para auxiliar a percorrer o mesmo vetor em outros índices*/
  int vezes = 0; /*Número de vezes que cada número aparece no vetor*/

  /* conta o numero de vezes que seq[i] aparece no vetor a partir da posição i */
  while(i < n){
    vezes = 1;
    j = i + 1;

    while (j < n)
      if (seq[j] != seq[i]){
		j = j + 1;    
	  } else {
        vezes = vezes +1;
		/* quando repete, remove */
        n = n - 1;
        seq[j] = seq[n];
      }     
    cout << seq[i] << " ocorre " << vezes << " vezes" << endl;
  	i = i + 1;
  }

  return 0;
}