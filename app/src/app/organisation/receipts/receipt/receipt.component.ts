import {Component, OnInit} from '@angular/core';
import {IUser} from '../../../models/user.model';
import {FormControl, FormGroup} from '@angular/forms';
import {ReceiptService} from '../../../services/receipt.service';
import {UserService} from '../../../services/user.service';
import {SnackBarService} from '../../../services/snackBar.service';
import {ActivatedRoute} from '@angular/router';

@Component({
    selector: 'app-receipt',
    templateUrl: './receipt.component.html',
    styleUrls: ['./receipt.component.scss']
})
export class ReceiptComponent implements OnInit {
    loading = true;
    user: IUser;
    isThesau = true;
    receiptId: number;

    receiptForm = new FormGroup({
        receipt_title: new FormControl(null),
        receipt_description: new FormControl(null),
        receipt_cost: new FormControl(null),
        receipt_cost_split: new FormControl([]),
        attachment: new FormControl(null)
    });

    constructor(
        private receiptService: ReceiptService,
        private userService: UserService,
        private snackBar: SnackBarService,
        private route: ActivatedRoute
    ) {
    }

    ngOnInit(): void {
        this.receiptForm.disable();
        this.route.params.subscribe(params => {
            this.receiptId = params.id;
            this.userService.getProfile().then(response => {
                this.user = response;
                this.isThesau = !!this.userService.findThesauGroup(this.user.groups);
                this.receiptService.getReceipt(this.receiptId).then(output => {
                    console.log(output);
                    this.receiptForm.patchValue(output);
                    this.loading = false;
                }, error => {
                    if ('error' in error) {
                        this.snackBar.openSnackBar('Error: ' + error.error, 'Ok');
                    } else {
                        this.snackBar.openSnackBar('An unknown error happened. ' + error, 'Ok');
                    }
                });
            });
        });
    }

    public V(control: string) {
        return this.receiptForm.get(control).value;
    }
}
