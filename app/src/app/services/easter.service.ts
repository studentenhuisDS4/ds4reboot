import {Injectable} from '@angular/core';

@Injectable({
    providedIn: 'root'
})
export class EasterEggService {
    myArray = [
        'Thanks!',
        'Awesome',
        'Noice',
        'Well... great.',
        'Ok.',
        'No!?',
        'Scheiβe',
        'Kutsjaarsch',
        'Miele, er is geen betere',
        'Yesh',
        'Yaaas',
        'Twaarsch',
        'Jawel \"huisgenoot\"',
        'Shit',
        'Okay',
        'I Am Groot.',
        'Well...?',
        'Sparta!',
        'KutSjaarsch nog an toe',
        'DS4!',
        'DSvier!',
        'Nais',
        'Ja, ik wil!',
        'SO AWESOME!',
        'Ja, ich brauch das',
        'Ja, ich darf mehr haben',
        'Ja.',
        'Gut.',
        'Confirm.',
        'Affirmative.',
        'Positief',
        'The jerries!',
        'Yankees!',
        'Aaaaaah!',
        'Cool.',
        'Vetklep!',
        'House bully!',
        'Dikzak!',
        'Grrrrr!',
        'Goed idee!',
        'Geweldig!',
        'Geweldig!!',
        'Trekkeeer!!!',
        'Trekker!',
        'Trekker?',
        'Plop de cork',
        'Thats sooo corky',
        'Fijn -_-',
        'Fijn :D',
        'Fijn =D!',
        'Plop',
        'Plopperdeplop',
        'House bully!',
        'Bier!',
        'Twee vrienden',
        'To... to... to...',
        'Tomatenplukkers!',
        'Rawr',
        'Rrrrr',
        'Brrrrr'
    ];

    easterEggo() {
        return this.myArray[Math.floor(Math.random() * this.myArray.length)];
    }
}
