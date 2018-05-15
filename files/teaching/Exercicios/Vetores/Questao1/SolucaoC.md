---
title: "Exercicios com Vetores - Soluções"
collection: classes
permalink: /teaching/Exercicios/Vetores/SolucaoC
---

Solução 1 da Questão 1:

```cpp
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
```

Solução 2 da Questão 1:

```cpp
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
```

Solução 3 da Questão 1:

```cpp
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
```