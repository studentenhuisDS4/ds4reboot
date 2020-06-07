import { Component, OnInit, ViewChild } from '@angular/core';
import { IUser } from '../../models/user.model';
import { GROUP, IGroup } from '../../models/group.model';
import { UserService } from '../../services/user.service';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { GroupService } from '../../services/group.service';
import { ActivatedRoute } from '@angular/router';

@Component({
    selector: 'app-group-manage',
    templateUrl: './group-manage.component.html',
    styleUrls: ['./group-manage.component.scss']
})
export class GroupManageComponent implements OnInit {
    user: IUser;
    groups: IGroup[];
    displayedColumns: string[] = ['name', 'members', 'actions']; // 'members'
    dataSource: MatTableDataSource<IGroup>;
    @ViewChild(MatPaginator, { static: true }) paginator: MatPaginator;
    @ViewChild(MatSort, { static: true }) sort: MatSort;

    constructor(
        private userService: UserService,
        private groupService: GroupService
    ) { }

    ngOnInit(): void {
        this.userService.getProfile().then(result => {
            this.user = result;
        });
        this.groupService.getGroupList().then(result => {
            this.groups = result;
            this.dataSource = new MatTableDataSource(this.groups);
            this.dataSource.paginator = this.paginator;
            this.dataSource.sort = this.sort;
        });
    }

    applyFilter(filterValue: string) {
        this.dataSource.filter = filterValue.trim().toLowerCase();

        if (this.dataSource.paginator) {
            this.dataSource.paginator.firstPage();
        }
    }

}
