import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {ServiceWorkerModule} from '@angular/service-worker';
import {environment} from '../environments/environment';
import {HttpClientModule} from '@angular/common/http';
import {MaterialModule} from './material/material.module';
import {DinnerListComponent} from './dinner-list/dinner-list.component';
import {TurfListComponent} from './turf-list/turf-list.component';
import {AdminComponent} from './admin/admin.component';
import {ContactComponent} from './contact/contact.component';
import {OrganizationComponent} from './organization/organization.component';
import {ProfileComponent} from './profile/profile.component';
import {NewsComponent} from './news/news.component';
import {HomeComponent} from './home/home.component';
import {FlexLayoutModule} from '@angular/flex-layout';
import {FormsModule} from '@angular/forms';
import {LayoutComponent} from './layout/layout.component';
import {HeaderComponent} from './navigation/header/header.component';
import {SidenavListComponent} from './navigation/sidenav-list/sidenav-list.component';
import {LoginComponent} from './login/login.component';


@NgModule({
    declarations: [
        AppComponent,
        DinnerListComponent,
        TurfListComponent,
        AdminComponent,
        ContactComponent,
        OrganizationComponent,
        ProfileComponent,
        NewsComponent,
        HomeComponent,
        LayoutComponent,
        HeaderComponent,
        SidenavListComponent,
        LoginComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        BrowserAnimationsModule,

        // REST HTTP consumer
        HttpClientModule,
        // Design & styling
        MaterialModule,
        FlexLayoutModule,
        // PWA
        ServiceWorkerModule.register('ngsw-worker.js', {enabled: environment.production}),
        FormsModule
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule {
}
