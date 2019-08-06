import {Component, OnInit, ViewChild} from '@angular/core';
import {GROUP, IGroup, IUser} from '../../models/user.model';
import {UserService} from '../../services/user.service';
import {MatPaginator, MatSort, MatTableDataSource} from '@angular/material';

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

    constructor(private userService: UserService) {

    }

    ngOnInit() {
        this.userService.getProfile().then(result => {
            this.user = result;
        });
        this.userService.getActiveUsers().then(result => {
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

}
