import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {ProfileComponent} from './profile/profile.component';
import {AdminComponent} from './admin/admin.component';
import {TurfListComponent} from './turf-list/turf-list.component';
import {DinnerListComponent} from './dinner-list/dinner-list.component';
import {OrganizationComponent} from './organization/organization.component';
import {ContactComponent} from './contact/contact.component';
import {NewsComponent} from './news/news.component';
import {HomeComponent} from './home/home.component';
import {LoginComponent} from './login/login.component';
import {
    AuthGuardService as AuthGuard
} from './services/auth-guard.service';
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
        canActivate: [AuthGuard]
    }, {
        path: 'admin',
        component: AdminComponent,
        canActivate: [AuthGuard]
        //    TODO: implement RoleGuard
        //     data: {
        //       expectedRole: 'admin'
        //     }
    }, {
        path: 'turf',
        component: TurfListComponent,
        canActivate: [AuthGuard]
    }, {
        path: 'dinner',
        component: DinnerListComponent,
        canActivate: [AuthGuard]
    }, {
        path: 'organization',
        component: OrganizationComponent,
        canActivate: [AuthGuard]
    }, {
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
