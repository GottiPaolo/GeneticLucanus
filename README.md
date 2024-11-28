# Davide Simulation
Facciamo una piccola e buffa simulazione per ridere con davide.

L'idea generale è creare un sistema molto stupido dove ci sono tre entità:
- Lucani
- Piante (o qualsiasi cosa di cui si cibi un lucano)
- Bambini pestiferi (o qualsiasi predatore che mi viene in mente di un lucano)

## Lucani
I lucani sono insetti con i seguenti attributi:
- Vettore x,y di poizione
- Vettore x,y di orientamento
- raggio di campo visivo, magari limitato ad una certa ampiezza rispetto alla posizione, o magari infinito in lunghezza ma limitato in ampiezza
- Stamina: energia a disposizione del Lucano
- Genere: in base a quanto voglio complicarmi la vita ma devo introdurre tutta la dinamica di accopiamento

Ed avranno le seugenti funzioni
- muovi: aumenta la posizione di orientamento. Il modulo dipende dalla velocità che sarà customizzabile ma consumerà stamina. A stamina 0 il lucano muore
- Ruota orientamento (da un lato o dall'altro) devo capire come configurare bene il fatto che deve essere continuo ma evitando velocità costante, farò un po' di test
- Riproduci (?) non so se voglio inserire anche questo ma sarebbe divertente

Il cervello del lucano deve avere i seguenti input:
- pos.x
- pos.y
- dir.x
- dir.y
- d.x da cibo
- d.y da cibo
- cibo si no
- d.x da bambino
- d.y da bambino
- bambino si no
- stamina

ed i seguenti output
- ruota -> numero (-1,1) che indica di quanto ruotare da un lato, non costa stamina
- muovi -> numero (0,1) che indica quanto velocemente muoversi verso la posizione in cui guarda (costa stamina proporzionatamente)


## Piante
In realtà saranno solo pallini verdi di cui si cibano i lucani, che spuntano con probabilità da definire. Renderei la probabilità funzione della temperatura 

## Bambini pestiferi
Se entrano in contatto con un lucano lo uccidono

