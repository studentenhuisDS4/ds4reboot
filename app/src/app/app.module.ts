import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatButtonModule, MatCardModule, MatFormFieldModule, MatInputModule, MatTableModule} from '@angular/material';
import {ServiceWorkerModule} from '@angular/service-worker';
import {environment} from '../environments/environment';
import {DinnerListComponent} from './dinner-list/dinner-list.component';
import {TurfListComponent} from './turf-list/turf-list.component';
import {AdminComponent} from './admin/admin.component';
import {ContactComponent} from './contact/contact.component';
import {OrganizationComponent} from './organization/organization.component';
import {ProfileComponent} from './profile/profile.component';
import {NewsComponent} from './news/news.component';
import {HttpClientModule} from '@angular/common/http';
import { HomeComponent } from './home/home.component';

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
        HomeComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        BrowserAnimationsModule,

        // REST HTTP consumer
        HttpClientModule,

        // Material
        MatTableModule,
        MatCardModule,
        MatInputModule,
        MatFormFieldModule,
        MatButtonModule,

        // PWA
        ServiceWorkerModule.register('ngsw-worker.js', {enabled: environment.production})
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule {
}
