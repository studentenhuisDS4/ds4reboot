import {Component, OnInit} from '@angular/core';
import {IAttachments} from '../../../models/attachments.model';
import {IReceipt, IReceiptCost} from '../../../models/receipt.model';
import {ReceiptService} from '../../../services/receipt.service';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {UserService} from '../../../services/user.service';
import {IUser} from '../../../models/user.model';
import {ThesauService} from '../../../services/thesau.service';
import {SnackBarService} from '../../../services/snackBar.service';

export enum SHARE {
    ALL = 'share_all',
    CUSTOM = 'specific',
    HOUSE = 'house'
}

interface IReceiptCostUser extends IReceiptCost {
    user?: IUser;
}

@Component({
    selector: 'app-upload-receipt',
    templateUrl: './edit-receipt.component.html',
    styleUrls: ['./edit-receipt.component.scss']
})
export class EditReceiptComponent implements OnInit {
    readonly maxAttachmentSize = 50 * 2 ** 20;

    SHARE = SHARE;

    loadingUsers = true;
    user: IUser;
    isThesau = true;
    allUsers: IUser[];
    billableUsers: IUser[];
    billedUsers: IReceiptCostUser[] = [];

    editReceiptForm = new FormGroup({
        show_old_housemates: new FormControl(false),
        receipt_title: new FormControl('',
            {
                validators: [Validators.maxLength(100), Validators.required],
            }),
        receipt_description: new FormControl('',
            {
                validators: [Validators.maxLength(300)],
            }),
        receipt_cost: new FormControl(0,
            {
                validators: [Validators.required],
            },
        ),
        charged_user: new FormControl(null),
        reimbursed_user: new FormControl(null, {
            validators: [Validators.required]
        }),
        share_cost_method: new FormControl({value: 'share_all', disabled: true}),
        attachment: new FormControl({disabled: true})
    });

    constructor(
        private receiptService: ReceiptService,
        private userService: UserService,
        private thesauService: ThesauService,
        private snackBar: SnackBarService) {
    }

    ngOnInit() {
        this.editReceiptForm.disable();

        const showOldHousemates = this.C('show_old_housemates');
        this.userService.getProfile().then(response => {
            this.user = response;
            this.isThesau = !!this.userService.findThesauGroup(this.user.groups);
            this.editReceiptForm.disable();
            this.loadingUsers = false;
        });
    }

    updateUserDropdown(change: boolean) {
        if (this.isThesau) {
            this.loadingUsers = true;
            this.thesauService.getAllUsers(change).then(output => {
                this.allUsers = output;
                this.loadingUsers = false;
            });
        }
    }

    addBillableUsers(popup = false) {
        if (this.billableUsers || !this.loadingUsers) {
            let addedUserCount = 0;
            this.billableUsers.forEach(user => {
                if (!this.billedUsers.find(bu => bu.affected_user_id === user.id)) {
                    this.billedUsers.push({
                        user,
                        affected_user_id: user.id,
                        cost_user: 0.00
                    });
                    addedUserCount++;
                }
            });
            if (popup) {
                if (addedUserCount) {
                    this.snackBar.openSnackBar('Added ' + addedUserCount.toString() + ' users to receipt', 'Thx');
                } else {
                    this.snackBar.openSnackBar('No missing users', 'Nice');
                }
            }
        } else if (popup) {
            this.snackBar.openSnackBar('It seems users are still loading, report bug if incorrect.', 'Okay.');
        }
    }

    splitCost(popup = true) {
        const cost = this.V('receipt_cost');
        if (cost && this.billedUsers && this.billedUsers.length) {
            const split = this.V('receipt_cost') / this.billedUsers.length;
            this.billedUsers.forEach(bu => bu.cost_user = split);
            this.snackBar.openSnackBar(
                'Split ' + this.V('receipt_cost').toString(), 'Thx');
        } else if (popup) {
            if (!cost) {
                this.snackBar.openSnackBar('No cost set.', 'Whoops');
            } else {
                this.snackBar.openSnackBar('No users added.', 'Whoops');
            }
        }
    }

    emptyBilledUsers() {
        this.billedUsers = [];
    }

    deleteBilledUser(index) {
        this.billedUsers.splice(index, 1);
    }

    addBillableUser(user: IUser) {
        if (user) {
            this.billedUsers.push({
                user,
                affected_user_id: user.id,
                cost_user: 0.00
            });
        }
    }

    processForm() {
        const formData = this.editReceiptForm.value;
        const costMethod = formData.share_cost_method as SHARE;
        const reimbursedUser = formData.reimbursed_user;
        const removeKeys = ['reimbursed_user', 'share_cost_method', 'show_old_housemates', 'attachment', 'charged_user'];
        removeKeys.forEach(key => {
            if (key in formData) {
                delete formData[key];
            }
        });

        const newReceipt: IReceipt = formData;
        newReceipt.receipt_costs_split = [];
        newReceipt.receipt_costs_split.push({
            cost_user: -formData.receipt_cost,
            affected_user_id: reimbursedUser ? reimbursedUser.id : this.user.id
        });
        if (costMethod === SHARE.ALL) {
            this.emptyBilledUsers();
            this.addBillableUsers(false);
            this.splitCost(false);
        } else if (costMethod === SHARE.HOUSE) {
            this.billedUsers = [{
                affected_user_id: 2,
                cost_user: formData.receipt_cost,
            }];
            this.splitCost(false);
        } else {
            this.billedUsers = [{
                affected_user_id: 2,
                cost_user: formData.receipt_cost,
            }];
            this.splitCost(false);
        }

        this.billedUsers.forEach(receiptCost => {
            newReceipt.receipt_costs_split.push({
                cost_user: receiptCost.cost_user,
                affected_user_id: receiptCost.affected_user_id
            });
        });
        if (!newReceipt.receipt_description) {
            newReceipt.receipt_description = '';
        }
        return newReceipt;
    }

    submitReceipt() {
        this.C('charged_user').disable();
        if (this.editReceiptForm.valid) {
            const receipt = this.processForm();
            const attachments = this.V('attachment')._files;
            const upload: IAttachments<IReceipt> = {
                attachments,
                json_object: receipt,
            };
            this.receiptService.uploadReceipt(upload).then(
                data => {
                    this.editReceiptForm.reset();
                    this.snackBar.openSnackBar('Receipt uploaded successfully!', 'Nice');
                },
                error => {
                    if ('error' in error && 'message' in error.error) {
                        this.snackBar.openSnackBar('Error from server: ' + error.error.message, 'Aight');
                    } else if ('error' in error) {
                        this.snackBar.openSnackBar('Unknown error: ' + error.error, 'Okay');
                    } else {
                        this.snackBar.openSnackBar('Unknown error: ' + error, 'Okay');
                        console.log(error);
                    }
                }
            );
        } else {
            this.editReceiptForm.markAllAsTouched();
        }
        this.C('charged_user').enable();
    }

    public V(control: string) {
        return this.editReceiptForm.get(control).value;
    }

    public E(control: string) {
        return this.editReceiptForm.controls[control].errors;
    }

    public C(control: string) {
        return this.editReceiptForm.controls[control];
    }

}
