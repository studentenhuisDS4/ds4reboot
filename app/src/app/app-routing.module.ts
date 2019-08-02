import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {ProfileComponent} from './profile/profile.component';
import {AdminComponent} from './admin/admin.component';
import {TurfListComponent} from './turf-list/turf-list.component';
import {DinnerListComponent} from './dinner-list/dinner-list.component';
import {OrganisationComponent} from './organisation/organisation.component';
import {ContactComponent} from './contact/contact.component';
import {NewsComponent} from './news/news.component';
import {HomeComponent} from './home/home.component';
import {LoginComponent} from './login/login.component';
import {AuthGuardService as AuthGuard} from './services/auth-guard.service';
import {AdminGuardService as AdminGuard} from './services/admin-guard.service';
import {ThesauGuardService} from './services/thesau-guard.service';
import {ProfileEditComponent} from './profile/profile-edit/profile-edit.component';
import {UserManageComponent} from './admin/user-manage/user-manage.component';
import {UserCreateComponent} from './admin/user-create/user-create.component';
import {ThesauComponent} from './thesau/thesau.component';
import {ManageReceiptsComponent} from './thesau/manage-receipts/manage-receipts.component';
import {UploadReceiptComponent} from './organisation/receipts/upload-receipt/upload-receipt.component';
import {ReceiptsComponent} from './organisation/receipts/receipts.component';
// import {
//     RoleGuardService as RoleGuard
// } from './services/role-guard.service';
// {
//     path: '',
//         component:
// }

const routes: Routes = [
    {path: '', redirectTo: 'home', pathMatch: 'full'},
    {
        path: 'login',
        component: LoginComponent
    },

    {
        path: 'profile',
        component: ProfileComponent,
        canActivate: [AuthGuard],
    }, {
        path: 'profile-edit',
        component: ProfileEditComponent,
        canActivate: [AuthGuard],
    },

    {
        path: 'admin',
        component: AdminComponent,
        canActivate: [AuthGuard, AdminGuard],
    }, {
        path: 'admin/user-manage',
        component: UserManageComponent,
        canActivate: [AuthGuard, AdminGuard],
    }, {
        path: 'admin/user-create',
        component: UserCreateComponent,
        canActivate: [AuthGuard, AdminGuard],
    },

    {
        path: 'turf',
        component: TurfListComponent,
        canActivate: [AuthGuard]
    }, {
        path: 'dinner',
        component: DinnerListComponent,
        canActivate: [AuthGuard]
    },

    {
        path: 'organisation',
        component: OrganisationComponent,
        canActivate: [AuthGuard]
    }, {
        path: 'organisation/receipts',
        component: ReceiptsComponent,
        canActivate: [AuthGuard]
    }, {
        path: 'organisation/receipts/upload-receipt',
        component: UploadReceiptComponent,
        canActivate: [AuthGuard]
    },

    {
        path: 'thesau',
        component: ThesauComponent,
        canActivate: [AuthGuard, ThesauGuardService]
    }, {
        path: 'manage-receipts',
        component: ManageReceiptsComponent,
        canActivate: [AuthGuard, ThesauGuardService]
    },

    {
        path: 'contact',
        component: ContactComponent
    }, {
        path: 'news',   // This will probably be the injected into the home page.
        component: NewsComponent,
        canActivate: [AuthGuard]
    }, {
        path: 'home',
        component: HomeComponent,
        canActivate: [AuthGuard]
    },
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
