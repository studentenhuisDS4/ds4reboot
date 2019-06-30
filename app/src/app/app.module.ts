import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {ServiceWorkerModule} from '@angular/service-worker';
import {environment} from '../environments/environment';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import {MaterialModule} from './material.module';
import {DinnerListComponent} from './dinner-list/dinner-list.component';
import {TurfListComponent} from './turf-list/turf-list.component';
import {AdminComponent} from './admin/admin.component';
import {ContactComponent} from './contact/contact.component';
import {OrganizationComponent} from './organization/organization.component';
import {ProfileComponent} from './profile/profile.component';
import {NewsComponent} from './news/news.component';
import {HomeComponent} from './home/home.component';
import {FlexLayoutModule} from '@angular/flex-layout';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {LayoutComponent} from './layout/layout.component';
import {HeaderComponent} from './navigation/header/header.component';
import {SidenavListComponent} from './navigation/sidenav-list/sidenav-list.component';
import {LoginComponent} from './login/login.component';
import {AutoFocusDirective} from './directives/auto-focus.directive';
import {AuthGuardService as AuthGuard} from './services/auth-guard.service';
import {TokenInterceptor} from './services/interceptors/token.interceptor';
import {BottomNavComponent} from './navigation/bottom-nav/bottom-nav.component';
import {CalendarModule, DateAdapter} from 'angular-calendar';
import {adapterFactory} from 'angular-calendar/date-adapters/date-fns';


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
        LoginComponent,
        AutoFocusDirective,
        BottomNavComponent
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
        FormsModule,
        ReactiveFormsModule,
        // Angular Calendar
        CalendarModule.forRoot({
            provide: DateAdapter,
            useFactory: adapterFactory
        })
    ],
    providers: [AuthGuard, {
        provide: HTTP_INTERCEPTORS,
        useClass: TokenInterceptor,
        multi: true
    }],
    bootstrap: [AppComponent]
})
export class AppModule {
}
