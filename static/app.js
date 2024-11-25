'use strict;'
document.querySelector('#filtercategories').addEventListener('change', filter_categories)
// quando c'è un cambiamento chiamo la funzione filter_categories 

function filter_categories() {
    // prendo filter_categories(select)
    const filterCategorie = document.querySelector("#filtercategories")
    //prendo la categoria che mi interessa in stringa
    const filter =  filterCategorie.value.toString()

    // prendo tutti i corsi che sono presenti nel
    const listaCorsi = document.querySelectorAll('.ifcorso')
    // per ogni riga prendo la categoria 
    listaCorsi.forEach((corso) => {
        // 2 for: 1 seleziona tutte le righe (i corsi); 2 seleziona tutte le categorie(potevo fare con include e un solo for ma avrei avuto problemi con i nomi dei corsi che si chiamano come le categorie)
        let flag = false ;
        // seleziono tutte le categorie
        let categorie = corso.querySelectorAll('.corso_categoria')
        for (let categoria of categorie ) {
            //console.log(categoria.textContent)
            // mostro tutti corsi quando il filtro non ha valore, mostro solo i corsi filtrati se il filtro ha valore per ogni categoria
            if(categoria.textContent == filter || filter == '')  {
                flag = true
            }

        }
        // console.log(categori.textContent)

        if ( flag == true ) {
            corso.style.display = '' ;
        } 
        else {
            corso.style.display = 'none'
        }

    });
}




