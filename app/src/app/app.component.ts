import {Component} from '@angular/core';
import {IconService} from './services/icon.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent {
    title = 'DS4';

    constructor(
        private iconService: IconService) {
        this.iconService.init();
    }
}
