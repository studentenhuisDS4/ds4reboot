import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {
    MatAutocompleteModule,
    MatBadgeModule,
    MatButtonModule,
    MatButtonToggleModule,
    MatCardModule,
    MatChipsModule,
    MatExpansionModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatListModule,
    MatMenuModule,
    MatPaginatorModule,
    MatProgressSpinnerModule,
    MatSidenavModule,
    MatSlideToggleModule,
    MatSnackBarModule, MatSortModule,
    MatTableModule,
    MatTabsModule,
    MatToolbarModule,
    MatTooltipModule
} from '@angular/material';

@NgModule({
    declarations: [],
    imports: [
        CommonModule
    ],
    exports: [
        MatTableModule,
        MatPaginatorModule,
        MatSortModule,
        MatCardModule,
        MatInputModule,
        MatTooltipModule,
        MatFormFieldModule,
        MatButtonModule,
        MatButtonToggleModule,
        MatSlideToggleModule,
        MatTabsModule,
        MatSidenavModule,
        MatToolbarModule,
        MatIconModule,
        MatListModule,
        MatExpansionModule,
        MatMenuModule,
        MatProgressSpinnerModule,
        MatBadgeModule,
        MatSnackBarModule,
        MatChipsModule,
        MatAutocompleteModule,
    ]
})
export class MaterialModule {
}
