import {Component, OnInit} from '@angular/core';
import {UserService} from '../../services/user.service';
import {IUser} from '../../models/user.model';
import {ICreateGroup, IGroup} from '../../models/group.model';
import {GroupService} from '../../services/group.service';
import {FormArray, FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {groupNameValidator} from '../../services/validators/async.validator';
import {environment} from '../../../environments/environment';
import {SnackBarService} from '../../services/snackBar.service';
import {ActivatedRoute} from '@angular/router';

class GroupEditParams {
    id: string;
}

@Component({
    selector: 'app-group-edit',
    templateUrl: './group-edit.component.html',
    styleUrls: ['./group-edit.component.scss']
})
export class GroupEditComponent implements OnInit {
    user: IUser;
    activeUsers: IUser[] = [];
    groups: IGroup[];
    filteredGroup: IGroup;
    public createGroupForm: FormGroup;

    existingGroup = false;

    constructor(
        private userService: UserService,
        private groupService: GroupService,
        private snackBarService: SnackBarService,
        private formBuilder: FormBuilder,
        private route: ActivatedRoute
    ) {
    }

    ngOnInit(): void {
        this.createGroupForm = this.formBuilder.group({
            name: new FormControl('',
                {
                    validators: [Validators.required, Validators.minLength(3)],
                    asyncValidators: [groupNameValidator(this.groupService)]
                }),
            members: this.formBuilder.array([], {
                validators: [Validators.minLength(1)]
            }),
            newMember: this.formBuilder.control(null)
        });

        this.route.params.subscribe((params: GroupEditParams) => {
            this.groupService.getGroupList().then(result => {
                this.groups = result;
                if (params.id) {
                    const groupId = parseInt(params.id, 10);
                    this.existingGroup = true;

                    this.createGroupForm.controls.name.clearAsyncValidators();
                    this.filteredGroup = this.groups.find(group => group.id === groupId);
                    this.createGroupForm.patchValue(this.filteredGroup);
                    this.createGroupForm.controls.members = this.processMembers(this.filteredGroup.members);
                    this.createGroupForm.markAllAsTouched();
                }
            });
        });
        this.userService.getActiveUsers().then(result => {
            this.activeUsers = result;
        });
        this.userService.getProfile().then(result => {
            this.user = result;
        });
    }

    processMembers(members: IUser[]): FormArray {
        const groups: FormGroup[] = [];
        members.forEach(member => {
            groups.push(this.formBuilder.group(member));
        });
        return this.formBuilder.array(groups);
    }

    createOrUpdateGroup() {
        this.createGroupForm.markAllAsTouched();
        if (this.createGroupForm.valid) {
            const formValue = this.createGroupForm.value;
            delete formValue.newMember; // Only for adding new members to array

            let createOrUpdatePromise: Promise<any>;
            if (this.existingGroup) {
                formValue.id = this.filteredGroup.id;
                createOrUpdatePromise = this.groupService.updateGroup(formValue as IGroup);
            } else {
                createOrUpdatePromise = this.groupService.createGroup(formValue as ICreateGroup);
            }

            createOrUpdatePromise.then(result => {
                this.createGroupForm.reset();
                this.createGroupForm.patchValue(result);
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
