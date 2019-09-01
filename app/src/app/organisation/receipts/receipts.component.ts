import {Component, OnInit, ViewChild} from '@angular/core';
import {IReceipt} from '../../models/receipt.model';
import {IUser} from '../../models/user.model';
import {MatPaginator, MatSort, MatTableDataSource} from '@angular/material';
import {UserService} from '../../services/user.service';
import {AdminService} from '../../services/admin.service';
import {SnackBarService} from '../../services/snackBar.service';
import {ReceiptService} from '../../services/receipt.service';

@Component({
    selector: 'app-receipt',
    templateUrl: './receipts.component.html',
    styleUrls: ['./receipts.component.scss']
})
export class ReceiptsComponent implements OnInit {
    user: IUser;
    isThesau: boolean;
    displayedColumns: string[] =
        ['receipt_cost', 'receipt_title', 'receipt_description', 'upload_user', 'upload_time',
            'accepted', 'accepted_user', 'accepted_time', 'actions'];
    dataSource: MatTableDataSource<IReceipt>;
    @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;
    @ViewChild(MatSort, {static: true}) sort: MatSort;

    constructor(
        private userService: UserService,
        private adminService: AdminService,
        private snackBarService: SnackBarService,
        private receiptService: ReceiptService,
    ) {

    }

    ngOnInit() {
        this.userService.getProfile().then(result => {
            this.user = result;
            this.isThesau = !!this.userService.findThesauGroup(this.user.groups);

            this.receiptService.getReceipts(this.isThesau ? null : this.user).then(response => {
                this.dataSource = new MatTableDataSource(response);
                this.dataSource.paginator = this.paginator;
                this.dataSource.sort = this.sort;
            });
        });

    }

    applyFilter(filterValue: string) {
        this.dataSource.filter = filterValue.trim().toLowerCase();

        if (this.dataSource.paginator) {
            this.dataSource.paginator.firstPage();
        }
    }

    deleteReceipt(deleteReceipt: IReceipt) {
        if (deleteReceipt.id === this.user.id) {
            return;
        }
        this.receiptService.deleteReceipt(deleteReceipt).then(output => {
            this.snackBarService.openSnackBar(
                `Receipt removed.`,
                'Confirm',
                2500);

            const oldData = this.dataSource.data;
            const index = oldData.findIndex(r => r.id === deleteReceipt.id);
            oldData.splice(index, 1);
            this.dataSource.data = oldData;
        }, failure => {
            if (failure && failure.error && failure.error.message) {
                this.snackBarService.openSnackBar(failure.error.message, 'Shit', 0);
            } else {
                this.snackBarService.openSnackBar('Something went wrong: ' + failure.message, 'Shit', 0);
            }
        });
    }

    acceptReceipt(receipt: IReceipt) {
        this.receiptService.acceptReceipt(receipt).then(result => {
            receipt.accepted = true;
            receipt.accepted_user = this.user;
            this.snackBarService.openSnackBar('The receipt has been accepted.', 'Confirm');
        }, error => {
            this.snackBarService.openSnackBar('An error occurred, does the receipt still exist?', 'Hmm');
        });
    }

    unacceptReceipt(receipt: IReceipt) {
        this.receiptService.unacceptReceipt(receipt).then(result => {
            receipt.accepted = false;
            receipt.accepted_user = null;
            this.snackBarService.openSnackBar('The receipt is now a draft.', 'Confirm');
        }, error => {
            this.snackBarService.openSnackBar('An error occurred, does the receipt still exist?', 'Hmm');
        });
    }
}
