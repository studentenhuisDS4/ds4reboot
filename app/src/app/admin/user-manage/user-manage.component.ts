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

    deleteUser(user: IUser) {
        if (confirm(`This will delete ${user.housemate.display_name}, ` +
            `reset their balance and add a transfer to eetlijst+HR. Every detail will be summarized in an email. Are you sure?`)) {
            this.adminService.deleteUser(user).then(output => {
                this.snackBarService.openSnackBar(
                    `${output.result.user.housemate.display_name} moved out, an email will be sent with the details.`,
                    'Confirm',
                    5000);
            });
        }
    }

}
