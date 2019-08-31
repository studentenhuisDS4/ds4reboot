import {NgControl} from '@angular/forms';
import {Directive, Input} from '@angular/core';

@Directive({selector: '[appDisableControl]'})
export class DisableControlDirective {

    constructor(private ngControl: NgControl) {
    }

    @Input() set appDisableControl(condition: boolean) {
        const action = condition ? 'disable' : 'enable';
        this.ngControl.control[action]();
    }
}
