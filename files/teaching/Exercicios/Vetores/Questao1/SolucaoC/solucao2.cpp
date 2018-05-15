/*
 * Solução 2 da Questão 1
 */ 
#include <iostream>

using namespace std;

int main() {
  int n;           /* comprimento da sequencia de entrada                    */

  cout << "Digite o numero de elementos da sequencia: ";
  cin >> n;

  int conta[n];    /* contador de repeticoes de cada numero da sequencia     */
  float seq[n];    /* sequencia de entrada sem repeticoes                    */
  int comp = 0;    /* comprimento do vetor conta                             */
  int i = 0;       /* contador de número de entradas fornecidas pelo usuário */
  int j = 0;

  cout << "Digite uma sequencia de " << n << " números reais: " << endl;
  while(i < n) {
    cin >> seq[comp];

    /* procura esse numero no vetor seq a partir do inicio */
    j = 0;
    while(seq[j] != seq[comp]){ 
      /* não faço nada, apenas conto */
      j = j + 1;
    }

    if (j == comp) {
      /* se o numero nunca tinha aparecido */
      conta[comp] = 1;
      comp = comp + 1;
    }
    else {
      /* se já apareceu, incrementa o número de vezes que esse número apareceu */
      conta[j] = conta[j] + 1;
    }

    i = i + 1;
  }

  /* imprime o resultado */
  j = 0;
  while(j < comp){
    cout << "O numero " << seq[j] << " aparece " << conta[j] << " vezes na sequência." << endl;
    j = j + 1;
  }
  return 0;
}