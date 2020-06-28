import {Component, OnInit} from '@angular/core';
import {UserService} from '../../services/user.service';
import {IUser} from '../../models/user.model';
import {ICreateGroup, IGroup} from '../../models/group.model';
import {GroupService} from '../../services/group.service';
import {FormArray, FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {groupNameValidator} from '../../services/validators/async.validator';
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
    createOrEditGroup: IGroup;
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
            members: this.formBuilder.array([]),
            newMember: this.formBuilder.control(null)
        });

        this.route.params.subscribe((params: GroupEditParams) => {
            this.groupService.getGroupList().then(result => {
                this.groups = result;
                if (params.id) {
                    const groupId = parseInt(params.id, 10);
                    this.createGroupForm.controls.name.clearAsyncValidators();
                    this.createGroupForm.controls.newMember
                        .valueChanges
                        .subscribe((changedMember: IUser) => this.addMemberToFormArray(changedMember));

                    this.createOrEditGroup = this.groups.find(group => group.id === groupId);
                    this.seedFormWithGroup();
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

    createOrUpdateGroup() {
        this.createGroupForm.markAllAsTouched();
        if (this.createGroupForm.valid) {
            const formValue = this.createGroupForm.getRawValue();
            delete formValue.newMember; // Only for adding new members to array

            let createOrUpdatePromise: Promise<any>;
            if (this.existingGroup) {
                formValue.id = this.createOrEditGroup.id;
                createOrUpdatePromise = this.groupService.updateGroup(formValue as IGroup);
            } else {
                createOrUpdatePromise = this.groupService.createGroup(formValue as ICreateGroup);
            }

            createOrUpdatePromise.then(result => {
                this.createGroupForm.reset();
                this.createOrEditGroup = result;
                this.seedFormWithGroup();
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

    processMembers(members: IUser[]): FormArray {
        const groups: FormControl[] = [];
        members.forEach(member => {
            groups.push(this.formBuilder.control(member));
        });
        return this.formBuilder.array(groups, {
            validators: [Validators.minLength(1)]
        });
    }

    addMemberToFormArray(member: IUser) {
        const memberFormArray = this.createGroupForm.controls.members as FormArray;
        const existingMember = memberFormArray.controls.find(control => control?.value?.id === member?.id);
        if (!existingMember) {
            memberFormArray.controls.push(this.formBuilder.control(member));
        }
        this.createGroupForm.controls.newMember.reset(null, {
            emitEvent: false
        });
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

    public compareTwoMembers(input: IUser, output: IUser) {
        if (input?.id && output?.id) {
            return input.id === output.id;
        } else {
            return null;
        }
    }

    deleteGroupMemberControl(i: number) {
        const memberFormArray = this.createGroupForm.controls.members as FormArray;
        memberFormArray.removeAt(i);
        this.createGroupForm.controls.members.markAllAsTouched();
    }

    addAllActiveMembers() {
        this.activeUsers.forEach(user => {
            this.addMemberToFormArray(user);
        });
    }

    private seedFormWithGroup() {
        this.existingGroup = true;
        this.createGroupForm.reset();
        this.createGroupForm.patchValue(this.createOrEditGroup);
        this.createGroupForm.controls.members = this.formBuilder.array([]);
        this.createGroupForm.controls.members = this.processMembers(this.createOrEditGroup.members);
        this.createGroupForm.markAllAsTouched();
    }
}
