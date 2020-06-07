import { Component, OnInit, ViewChild } from '@angular/core';
import { UserService } from '../../services/user.service';
import { IUser } from '../../models/user.model';
import { IGroup, ICreateGroup } from '../../models/group.model';
import { GroupService } from '../../services/group.service';
import { FormGroup, FormControl, Validators, FormBuilder, FormArray } from '@angular/forms';
import { groupNameValidator } from '../../services/validators/async.validator';
import { environment } from '../../../environments/environment';
import { SnackBarService } from '../../services/snackBar.service';
import { ActivatedRoute } from '@angular/router';

class GroupEditParams {
    id: number;
}

@Component({
    selector: 'app-group-edit',
    templateUrl: './group-edit.component.html',
    styleUrls: ['./group-edit.component.scss']
})
export class GroupEditComponent implements OnInit {
    user: IUser;
    groups: IGroup[];
    public createGroupForm: FormGroup;

    constructor(
        private userService: UserService,
        private groupService: GroupService,
        private snackBarService: SnackBarService,
        private formBuilder: FormBuilder,
        private route: ActivatedRoute
    ) { }

    ngOnInit(): void {
        this.createGroupForm = this.formBuilder.group({
            name: new FormControl('',
                {
                    validators: [Validators.required, Validators.minLength(4),],
                    asyncValidators: [groupNameValidator(this.groupService)]
                }),
            members: this.formBuilder.array([this.createItem()])
        });

        this.route.params.subscribe((params: GroupEditParams) => {
            this.groupService.getGroupList().then(result => {
                this.groups = result;
                if (params.id) {
                    let group = this.groups.find(group => group.id == params.id);
                    this.createGroupForm.patchValue(group);
                    this.createGroupForm.controls['members'] = this.processMembers(group.members);
                    this.createGroupForm.markAllAsTouched();
                }
            });
        });
        this.userService.getProfile().then(result => {
            this.user = result;
        });
    }

    processMembers(members: IUser[]): FormArray {
        const controls: FormControl[] = [];
        members.forEach(member => {
            controls.push(this.formBuilder.control(member));
        });
        const array = this.formBuilder.array(controls)
        console.log(array);
        return array;
    }

    createItem(): FormGroup {
        return this.formBuilder.group({
            username: ''
        });
    }

    createGroup() {
        this.createGroupForm.markAllAsTouched();

        const newGroup = this.createGroupForm.value as ICreateGroup;
        newGroup.members = [];
        if (this.createGroupForm.valid) {
            this.groupService.createGroup(newGroup).then(result => {
                this.createGroupForm.reset();

                if (environment.debug) {
                    console.log(result);
                }
            }, error => {
                if (error) {
                    console.error(error);
                }
                this.snackBarService.openSnackBar('Error occurred.', 'Ok.');
            });
        } else {
            this.snackBarService.openSnackBar('Correct the highlighted fields.', 'Ok.');
        }
    }

    public V(control: string) {
        return this.createGroupForm.get(control).value;
    }

    public E(control: string) {
        return this.createGroupForm.controls[control].errors;
    }

    public C(control: string) {
        return this.createGroupForm.controls[control];
    }

}
