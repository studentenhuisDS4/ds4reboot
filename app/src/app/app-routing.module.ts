import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {ProfileComponent} from './profile/profile.component';
import {AdminComponent} from './admin/admin.component';
import {TurfListComponent} from './turf-list/turf-list.component';
import {DinnerListComponent} from './dinner-list/dinner-list.component';
import {OrganizationComponent} from './organization/organization.component';
import {ContactComponent} from './contact/contact.component';
import {NewsComponent} from './news/news.component';

// {
//     path: '',
//         component:
// }

const routes: Routes = [{path: '', redirectTo: 'contacts', pathMatch: 'full'},
    {
        path: 'profile',
        component: ProfileComponent
    }, {
        path: 'admin',
        component: AdminComponent
    }, {
        path: 'turf-list',
        component: TurfListComponent
    }, {
        path: 'dinner-list',
        component: DinnerListComponent
    }, {
        path: 'organization',
        component: OrganizationComponent
    }, {
        path: 'contact',
        component: ContactComponent
    }, {
        path: 'news',   // This will probably be the home page.
        component: NewsComponent
    },
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
