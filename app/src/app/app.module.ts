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
import {UserCreateComponent} from './admin/user-create/user-create.component';
import {UserEditComponent} from './admin/user-edit/user-edit.component';
import {UserManageComponent} from './admin/user-manage/user-manage.component';
import {ContactComponent} from './contact/contact.component';
import {OrganisationComponent} from './organisation/organisation.component';
import {ProfileComponent} from './profile/profile.component';
import {ProfileEditComponent} from './profile/profile-edit/profile-edit.component';
import {NewsComponent} from './news/news.component';
import {HomeComponent} from './home/home.component';
import {FlexLayoutModule} from '@angular/flex-layout';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {LayoutComponent} from './layout/layout.component';
import {HeaderComponent} from './navigation/header/header.component';
import {SidenavListComponent} from './navigation/sidenav-list/sidenav-list.component';
import {LoginComponent} from './login/login.component';
import {AutoFocusDirective} from './directives/auto-focus.directive';
import {AuthGuardService} from './services/guards/auth-guard.service';
import {AdminGuardService} from './services/guards/admin-guard.service';
import {TokenInterceptor} from './services/interceptors/token.interceptor';
import {BottomNavComponent} from './navigation/bottom-nav/bottom-nav.component';
import {CalendarModule, DateAdapter} from 'angular-calendar';
import {adapterFactory} from 'angular-calendar/date-adapters/date-fns';
import {ThesauComponent} from './thesau/thesau.component';
import {ThesauGuardService} from './services/guards/thesau-guard.service';
import {ManageReceiptsComponent} from './thesau/manage-receipts/manage-receipts.component';
import {ReceiptsComponent} from './organisation/receipts/receipts.component';
import {UploadReceiptComponent} from './organisation/receipts/upload-receipt/upload-receipt.component';
import {SignupComponent} from './login/signup/signup.component';
import {TurfLogComponent} from './turf-list/turf-log/turf-log.component';
import {BoeteComponent} from './turf-list/boete/boete.component';
import {TurfComponent} from './turf-list/turf-component/turf.component';


@NgModule({
    declarations: [
        AppComponent,
        DinnerListComponent,
        TurfListComponent,
        AdminComponent,
        UserManageComponent,
        UserEditComponent,
        UserCreateComponent,
        ContactComponent,
        OrganisationComponent,
        ReceiptsComponent,
        UploadReceiptComponent,
        ThesauComponent,
        ManageReceiptsComponent,
        ProfileComponent,
        ProfileEditComponent,
        NewsComponent,
        HomeComponent,
        LayoutComponent,
        HeaderComponent,
        SidenavListComponent,
        LoginComponent,
        SignupComponent,
        AutoFocusDirective,
        BottomNavComponent,
        TurfLogComponent,
        BoeteComponent,
        TurfComponent,
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
        }),
    ],
    providers: [AuthGuardService, AdminGuardService, ThesauGuardService, {
        provide: HTTP_INTERCEPTORS,
        useClass: TokenInterceptor,
        multi: true
    }],
    bootstrap: [AppComponent]
})
export class AppModule {
}
