import {Injectable} from '@angular/core';
import { MatIconRegistry } from '@angular/material/icon';
import {DomSanitizer} from '@angular/platform-browser';

@Injectable({
    providedIn: 'root'
})
export class IconService {

    constructor(
        private matIconRegistry: MatIconRegistry,
        private domSanitizer: DomSanitizer,
    ) {
    }

    init() {
        this.matIconRegistry.addSvgIcon(
            `cooking_hat`,
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/iconset/hat.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'remove_cooking_hat',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/iconset/hat_crossout.svg')
        );
        this.matIconRegistry.addSvgIcon(
            'cooking_hat_outline',
            this.domSanitizer.bypassSecurityTrustResourceUrl('../assets/iconset/hat_outline.svg')
        );
    }
}
