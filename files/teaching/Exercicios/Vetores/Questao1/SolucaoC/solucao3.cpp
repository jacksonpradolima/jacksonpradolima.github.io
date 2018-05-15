/*
 * Solução 3 da Questão 1
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

  /*Ordena os valores*/
  while(i < n){
    float aux; /*Variável auxiliar*/
    j = 0;
    while(j < n-1){
      if (seq[j] > seq[j+1] ){
          aux = seq[j];
          seq[j] = seq[j+1];
          seq[j+1] = aux;
      }
      j = j + 1;
    }
    i = i + 1;
  }
  
  i = 0;
  j = 1;
  int cont = 1;

  /*Conta quantas vezes aparece*/
  while(i < n)
  {
    while (seq[i] == seq[j]){
      cont = cont + 1;
      j = j + 1;
    }

    cout << seq[i] << " ocorre " << cont << " vezes" << endl;

    i = j;
    cont = 0;
  }
  return 0;
}