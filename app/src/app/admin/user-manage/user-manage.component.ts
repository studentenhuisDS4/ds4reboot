import {Component, OnInit, ViewChild} from '@angular/core';
import {GROUP, IGroup, IUser} from '../../models/user.model';
import {UserService} from '../../services/user.service';
import {MatPaginator, MatSort, MatTableDataSource} from '@angular/material';
import {AdminService} from '../../services/admin.service';
import {SnackBarService} from '../../services/snackBar.service';

@Component({
    selector: 'app-user-manage',
    templateUrl: './user-manage.component.html',
    styleUrls: ['./user-manage.component.scss']
})
export class UserManageComponent implements OnInit {
    user: IUser;
    displayedColumns: string[] = ['display_name', 'surname', 'is_superuser', 'has_thesau', 'balance', 'actions'];
    dataSource: MatTableDataSource<IUser>;
    @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;
    @ViewChild(MatSort, {static: true}) sort: MatSort;

    constructor(
        private userService: UserService,
        private adminService: AdminService,
        private snackBarService: SnackBarService
    ) {

    }

    ngOnInit() {
        this.userService.getProfile().then(result => {
            this.user = result;
        });
        this.adminService.getAdminUsers().then(result => {
            this.dataSource = new MatTableDataSource(result);
            this.dataSource.paginator = this.paginator;
            this.dataSource.sort = this.sort;
        });
    }

    findThesauGroup(groups: IGroup[]) {
        return groups.find(group => group.id === GROUP.THESAU);
    }

    applyFilter(filterValue: string) {
        this.dataSource.filter = filterValue.trim().toLowerCase();

        if (this.dataSource.paginator) {
            this.dataSource.paginator.firstPage();
        }
    }

    deleteUser(deleteUser: IUser) {
        if (deleteUser.id === this.user.id) {
            return;
        }
        if (confirm(`This will delete ${deleteUser.housemate.display_name}, ` +
            `reset their balance and add a transfer to eetlijst+HR. Every detail will be summarized in an email. Are you sure?`)) {
            this.adminService.deleteUser(deleteUser).then(output => {
                this.snackBarService.openSnackBar(
                    `${output.result.user.housemate.display_name} moved out, an email will be sent with the details.`,
                    'Confirm',
                    5000);

                const oldData = this.dataSource.data;
                const index = oldData.findIndex(u => u.id === deleteUser.id);
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
    }

    toggleActivationUser(toggleUser: IUser, active = false) {
        if (confirm(`This will ${active ? 'activate' : 'deactivate'} ${toggleUser.housemate.display_name}, ` +
            ` And allow them to use their account. Confirm?`)) {
            this.adminService.toggleUserActivation(toggleUser).then(output => {
                const newUser = output.result;

                this.updateDataSourceWithUser(newUser);

                this.snackBarService.openSnackBar(
                    `${newUser.housemate.display_name} ` +
                    `${newUser.is_active ? 'activated' : 'deactivated'} succesfully.`, 'Confirm', 3000);
            }, failure => {
                if (failure && failure.error && failure.error.message) {
                    this.snackBarService.openSnackBar(failure.error.message, 'Shit', 0);
                } else {
                    this.snackBarService.openSnackBar('Something went wrong: ' + failure.message, 'Shit', 0);
                }
            });
        }
    }

    toggleAdmin(adminUser: IUser) {
        this.adminService.toggleAdmin(adminUser).then(output => {
            this.snackBarService.openSnackBar(`${output.result.housemate.display_name} toggled admin.`, 'Confirm', 5000);
            this.updateDataSourceWithUser(output.result);
        });
    }

    toggleThesau(thesauUser: IUser) {
        this.adminService.toggleThesau(thesauUser).then(output => {
            this.snackBarService.openSnackBar(`${output.result.housemate.display_name} toggled thesau.`, 'Confirm', 5000);
            this.updateDataSourceWithUser(output.result);
        });
    }

    private updateDataSourceWithUser(newUser: IUser) {
        const oldData = this.dataSource.data;
        const index = oldData.findIndex(u => u.id === newUser.id);
        oldData[index] = newUser;
        this.dataSource.data = [...oldData];
    }

}
